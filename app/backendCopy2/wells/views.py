"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from urllib.parse import quote
import logging
import json
import requests

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSException, GEOSGeometry
from django.contrib.gis.gdal import GDALException
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.http import (
    FileResponse, Http404, HttpResponse, HttpResponseNotFound,
    HttpResponseRedirect, JsonResponse, StreamingHttpResponse
)
from django.shortcuts import get_object_or_404
from django.db import connection

from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from minio import Minio

from gwells.documents import MinioClient
from gwells.roles import WELLS_VIEWER_ROLE, WELLS_EDIT_ROLE
from gwells.pagination import APILimitOffsetPagination
from gwells.settings.base import get_env_variable
from gwells.open_api import (
    get_geojson_schema, get_model_feature_schema, GEO_JSON_302_MESSAGE, GEO_JSON_PARAMS)
from gwells.management.commands.export_databc import (
    GeoJSONIterator,
    LITHOLOGY_CHUNK_SIZE,
    LITHOLOGY_SQL,
    WELL_CHUNK_SIZE,
    PUMPING_TEST_AQUIFER_PARAMETER_CHUNK_SIZE,
    PUMPING_TEST_AQUIFER_PARAMETER_SQL,
    WELLS_SQL_V1,
)

from submissions.serializers import WellSubmissionListSerializer
from submissions.models import WellActivityCode

from wells.filters import (
    BoundingBoxFilterBackend,
    GeometryFilterBackend,
    RadiusFilterBackend,
    WellListFilterBackend,
    WellListOrderingFilter,
)
from wells.models import (
    ActivitySubmission,
    Casing,
    IntendedWaterUseCode,
    LicencedStatusCode,
    LithologyColourCode,
    LithologyDescription,
    LithologyDescriptionCode,
    LithologyHardnessCode,
    LithologyMaterialCode,
    Well,
    WellAttachment,
    WellClassCode,
    WellYieldUnitCode,
    WellStatusCode,
)

from wells.change_history import get_well_history
from wells.renderers import WellListCSVRenderer, WellListExcelRenderer
from wells.serializers import (
    WellExportAdminSerializerV1,
    WellExportSerializerV1,
    WellListAdminSerializerV1,
    WellListSerializerV1,
    WellTagSearchSerializer,
    WellDetailSerializer,
    WellDetailAdminSerializer,
    WellLocationSerializerV1,
    WellDrawdownSerializer,
    WellLithologySerializer,
)
from wells.permissions import WellsEditPermissions, WellsEditOrReadOnly
from wells.constants import MAX_EXPORT_COUNT, MAX_LOCATION_COUNT, WELL_TAGS

logger = logging.getLogger(__name__)


class WellDetail(RetrieveAPIView):
    """
    Return well detail.
    get:
    Returns information about a well given the well_tag_number. Unpublished wells are filtered if user is not authenticated.
    """
    serializer_class = WellDetailSerializer

    lookup_field = 'well_tag_number'

    def get_queryset(self):
        """ Excludes Unpublished wells for users without edit permissions """
        if self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = Well.objects.all()
        else:
            qs = Well.objects.all().exclude(well_publication_status='Unpublished')

        return qs


class WellStaffEditDetail(RetrieveAPIView):
    """
    Return well detail for use in a staff edit
    """
    serializer_class = WellDetailAdminSerializer
    queryset = Well.objects.all()
    lookup_field = 'well_tag_number'
    permission_classes = (WellsEditPermissions,)


class ListExtracts(APIView):
    """
    List well extracts

    get:
    list well extracts
    """
    @swagger_auto_schema(auto_schema=None)
    def get(self, request, **kwargs):
        host = get_env_variable('S3_HOST')
        use_secure = int(get_env_variable('S3_USE_SECURE', 1))
        minioClient = Minio(host,
                            access_key=get_env_variable(
                                'S3_PUBLIC_ACCESS_KEY'),
                            secret_key=get_env_variable(
                                'S3_PUBLIC_SECRET_KEY'),
                            secure=use_secure)
        objects = minioClient.list_objects(
            get_env_variable('S3_WELL_EXPORT_BUCKET'), 'export/v2/')
        urls = list(
            map(
                lambda document: {
                    'url': 'https://{}/{}/{}'.format(host,
                                                     quote(
                                                         document.bucket_name),
                                                     quote(document.object_name)),
                    'name': document.object_name,
                    'size': document.size,
                    'last_modified': document.last_modified,
                    'description': self.create_description(document.object_name)
                }, objects)
        )
        return Response(urls)

    def create_description(self, name):
        extension = name[name.rfind('.')+1:]
        if extension == 'zip':
            return 'ZIP, CSV'
        elif extension == 'xlsx':
            return 'XLSX'
        else:
            return None


LIST_FILES_OK = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'public': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )),
        'private': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ))
    })


class ListFiles(APIView):
    """
    List documents associated with a well (e.g. well construction report)

    get:
    List uploaded files associated with the well identified in the URI.
    """

    @swagger_auto_schema(responses={200: openapi.Response('OK', LIST_FILES_OK)})
    def get(self, request, tag, **kwargs):
        well = get_object_or_404(Well, pk=tag)

        if well.well_publication_status\
                .well_publication_status_code == 'Unpublished':
            if not self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
                return HttpResponseNotFound()

        user_is_staff = self.request.user.groups.filter(
            name=WELLS_VIEWER_ROLE).exists()

        client = MinioClient(
            request=request, disable_private=(not user_is_staff))

        documents = client.get_documents(
            int(tag), resource="well", include_private=user_is_staff)

        return Response(documents)

class FileSumView(APIView):
    """
    Handler for Updating File counts for a well. Bridge method to keep database records for files stored in S3 buckets.
    Primarily used for Advanced Search function 'Wells containing File of type n'

    get:
    Increments or decrements the count for files stored of a given type.
    """
    
    def get(self, request, tag, **kwargs):
        # Verify user has permissions to edit wells
        if not self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            return HttpResponse(status=403)
        increment = self.request.query_params.get('inc')
        document_type = self.request.query_params.get('documentType')
        
        # Verify we have correct query params, and the document type is valid
        if self.request.query_params.get('documentType') == None \
            or increment == None \
            or not any(item['value'] == document_type for item in WELL_TAGS):
            return HttpResponse(status=400)
        
        attachment = document_type.replace(' ', "_").lower()
        try:
            # Create entry to WellAttachment in event it does not already have one
            if not WellAttachment.objects.filter(well_tag_number=tag).exists():
                well = Well.objects.get(well_tag_number=tag)
                WellAttachment.objects.create(well_tag_number=well)
                
            if increment == "true":
                well_attach = WellAttachment.objects.get(well_tag_number=tag)
                setattr(well_attach, attachment, getattr(well_attach, attachment) + 1)
                well_attach.save()
                return HttpResponse("Count updated successfully", status=200)
            elif increment == "false":
                well_attach = WellAttachment.objects.get(well_tag_number=tag)
                if getattr(well_attach, attachment) > 0:
                    setattr(well_attach, attachment, getattr(well_attach, attachment) - 1)
                    well_attach.save()
                    return HttpResponse("File count decreased", status=200)
                else:
                    return HttpResponse("Cannot have negative number of files", status=400)
            else:
                return HttpResponse("Invalid value for qs: increment", status=400)
                
        except Exception as e:
            print(e)
            return HttpResponse(400)

class WellListAPIViewV1(ListAPIView):
    """List and create wells

    get:
    Returns a list of wells.
    """

    permission_classes = (WellsEditOrReadOnly,)
    model = Well
    pagination_class = APILimitOffsetPagination

    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, WellListOrderingFilter, GeometryFilterBackend)
    ordering = ('well_tag_number',)
    search_fields = ('well_tag_number', 'identification_plate_number',
                     'street_address', 'city', 'owner_full_name')
    default_limit = 10

    def get_serializer_class(self):
        """Returns a different serializer class for admin users."""
        serializer_class = WellListSerializerV1
        if (self.request.user and self.request.user.is_authenticated and
                self.request.user.groups.filter(name=WELLS_VIEWER_ROLE).exists()):
            serializer_class = WellListAdminSerializerV1

        return serializer_class

    def get_queryset(self):
        """ Excludes Unpublished wells for users without edit permissions """
        if self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = Well.objects.all()
        else:
            qs = Well.objects.all().exclude(well_publication_status='Unpublished')

        qs = qs \
            .select_related(
                "bcgs_id",
            ).prefetch_related(
                "water_quality_characteristics",
                "drilling_methods",
                "development_methods"
            )

        return qs


class WellTagSearchAPIView(ListAPIView):
    """
    get:
    Search for wells by tag or owner.
    """

    permission_classes = (WellsEditOrReadOnly,)
    model = Well
    pagination_class = None
    serializer_class = WellTagSearchSerializer
    lookup_field = 'well_tag_number'

    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('well_tag_number',)
    search_fields = (
        'well_tag_number',
        'owner_full_name',
    )

    def get_queryset(self):
        """ Excludes Unpublished wells for users without edit permissions """
        if self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = Well.objects.all()
        else:
            qs = Well.objects.all().exclude(well_publication_status='Unpublished')

        return qs

    def get(self, request, **kwargs):
        data = self.get_queryset().values('well_tag_number', 'owner_full_name').order_by('well_tag_number')
        return Response(data)


class WellSubmissionsListAPIView(ListAPIView):
    """ lists submissions for a well
        See also:  submissions.SubmissionListAPIView (list all submission records)

        get:
        Returns submission records for a given well.
    """

    permission_classes = (WellsEditPermissions,)
    serializer_class = WellSubmissionListSerializer

    def get_queryset(self):
        well = self.kwargs.get('well_id')
        records = ActivitySubmission.objects.filter(well=well).select_related(
            'well_activity_type').order_by('create_date')
        return sorted(records, key=lambda record:
                      (record.well_activity_type.code != WellActivityCode.types.legacy().code,
                          record.well_activity_type.code != WellActivityCode.types.construction().code,
                          record.create_date), reverse=True)


class WellLocationListAPIViewV1(ListAPIView):
    """ Returns well locations for a given search.

        get:
        Returns a list of wells with locations only.
    """
    permission_classes = (WellsEditOrReadOnly,)
    model = Well
    serializer_class = WellLocationSerializerV1

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, WellListOrderingFilter)
    ordering = ('well_tag_number',)
    pagination_class = None

    search_fields = ('well_tag_number', 'identification_plate_number',
                     'street_address', 'city', 'owner_full_name')

    def get_queryset(self):
        """ Excludes Unpublished wells for users without edit permissions """
        if self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = Well.objects.all()
        else:
            qs = Well.objects.all().exclude(well_publication_status='Unpublished')

        return qs

    def get(self, request, **kwargs):
        """
        Cancels request if too many wells are found.
        
        get:
        Returns compact set of well information data for populating the maps.
        """

        qs = self.get_queryset()
        locations = self.filter_queryset(qs)
        count = locations.count()
        # return an empty response if there are too many wells to display
        if count > MAX_LOCATION_COUNT:
            raise PermissionDenied('Too many wells to display on map. '
                                   'Please zoom in or change your search criteria.')

        if count == 0:
            raise NotFound("No well records could be found.")

        return super().get(request)


class WellExportListAPIViewV1(ListAPIView):
    """Returns CSV or Excel data for wells.
    """
    permission_classes = (WellsEditOrReadOnly,)
    model = Well

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering = ('well_tag_number',)
    pagination_class = None

    search_fields = ('well_tag_number', 'identification_plate_number',
                     'street_address', 'city', 'owner_full_name')
    renderer_classes = (WellListCSVRenderer, WellListExcelRenderer)

    SELECT_RELATED_OPTIONS = [
        'well_class',
        'well_subclass',
        'well_status',
        'licenced_status',
        'land_district',
        'company_of_person_responsible',
        'ground_elevation_method',
        'surface_seal_material',
        'surface_seal_method',
        'liner_material',
        'screen_intake_method',
        'screen_type',
        'screen_material',
        'screen_opening',
        'screen_bottom',
        'well_yield_unit',
        'observation_well_status',
        'coordinate_acquisition_code',
        'bcgs_id',
        'decommission_method',
        'aquifer',
        'aquifer_lithology',
        'yield_estimation_method',
        'well_disinfected_status',
    ]
    PREFETCH_RELATED_OPTIONS = [
        'development_methods',
        'drilling_methods',
        'water_quality_characteristics',
    ]

    def get_fields(self):
        raw_fields = self.request.query_params.get('fields')
        return raw_fields.split(',') if raw_fields else None

    def get_queryset(self):
        """Excludes unpublished wells for users without edit permissions.
        """
        if self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = Well.objects.all()
        else:
            qs = Well.objects.all().exclude(well_publication_status='Unpublished')

        included_fields = self.get_fields()

        if included_fields:
            select_relateds = [
                relation for relation in self.SELECT_RELATED_OPTIONS
                if relation in included_fields
            ]
            prefetches = [
                relation for relation in self.PREFETCH_RELATED_OPTIONS
                if relation in included_fields
            ]

            if select_relateds:
                qs = qs.select_related(*select_relateds)
            if prefetches:
                qs = qs.prefetch_related(*prefetches)
        elif included_fields is None:
            # If no fields are passed, then include everything
            qs = qs.select_related(*self.SELECT_RELATED_OPTIONS)
            qs = qs.prefetch_related(*self.PREFETCH_RELATED_OPTIONS)

        return qs

    def get_serializer_class(self):
        """Returns a different serializer class for admin users."""
        serializer_class = WellExportSerializerV1
        if (self.request.user and self.request.user.is_authenticated and
                self.request.user.groups.filter(name=WELLS_VIEWER_ROLE).exists()):
            serializer_class = WellExportAdminSerializerV1

        return serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()

        fields = self.get_fields()
        if fields:
            context['fields'] = fields

        return context

    def get_renderer_context(self):
        context = super().get_renderer_context()

        fields = self.get_fields()
        if fields:
            context['header'] = fields

        return context

    def batch_iterator(self, queryset, count, batch_size=200):
        """Batch a queryset into chunks of batch_size, and serialize the results

        Allows iterative processing while taking advantage of prefetching many
        to many relations.
        """
        for offset in range(0, count, batch_size):
            end = min(offset + batch_size, count)
            batch = queryset[offset:end]

            serializer = self.get_serializer(batch, many=True)
            for item in serializer.data:
                yield item

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        # return an empty response if there are too many wells to display
        if count > MAX_EXPORT_COUNT:
            raise PermissionDenied(
                'Too many wells to export. Please change your search criteria.'
            )
        elif count == 0:
            raise NotFound('No well records could be found.')

        renderer = request.accepted_renderer
        if renderer.format == 'xlsx':
            response_class = FileResponse
        else:
            response_class = StreamingHttpResponse

        context = self.get_renderer_context()
        data_iterator = self.batch_iterator(queryset, count)
        render_result = renderer.render(data_iterator, renderer_context=context)

        response = response_class(render_result, content_type=renderer.media_type)
        response['Content-Disposition'] = 'attachment; filename="search-results.{ext}"'.format(ext=renderer.format)

        return response


class PreSignedDocumentKey(APIView):
    """
    Get a pre-signed document key to upload into an S3 compatible document store.

    post:
    Obtain a URL that is pre-signed to allow client-side uploads.
    """

    queryset = Well.objects.all()
    permission_classes = (WellsEditPermissions,)

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, tag, **kwargs):
        well = get_object_or_404(self.queryset, pk=tag)
        client = MinioClient(
            request=request, disable_private=False)

        object_name = request.GET.get("filename")
        filename = client.format_object_name(
            object_name, int(well.well_tag_number), "well")
        bucket_name = get_env_variable("S3_ROOT_BUCKET")

        is_private = False
        if request.GET.get("private") == "true":
            is_private = True
            bucket_name = get_env_variable("S3_PRIVATE_ROOT_BUCKET")

        # TODO: This should probably be "S3_WELL_BUCKET" but that will require a file migration
        url = client.get_presigned_put_url(
            filename, bucket_name=bucket_name, private=is_private)

        return JsonResponse({"object_name": object_name, "url": url})


class DeleteWellDocument(APIView):
    """
    Delete a document from a S3 compatible store.

    delete:
    Remove the specified object from the S3 store.
    """

    queryset = Well.objects.all()
    permission_classes = (WellsEditPermissions,)

    @swagger_auto_schema(auto_schema=None)
    def delete(self, request, tag, **kwargs):
        well = get_object_or_404(self.queryset, pk=tag)
        client = MinioClient(
            request=request, disable_private=False)

        is_private = False
        bucket_name = get_env_variable("S3_ROOT_BUCKET")

        if request.GET.get("private") == "true":
            is_private = True
            bucket_name = get_env_variable("S3_PRIVATE_ROOT_BUCKET")

        object_name = client.get_bucket_folder(
            int(well.well_tag_number), "well") + "/" + request.GET.get("filename")

        # TODO: This should probably be "S3_WELL_BUCKET" but that will require a file migration
        client.delete_document(
            object_name, bucket_name=bucket_name, private=is_private)

        return HttpResponse(status=204)


class WellHistory(APIView):
    """
    get:
    Returns a history of changes to a Well model record.
    """
    permission_classes = (WellsEditPermissions,)
    queryset = Well.objects.all()

    def get(self, request, well_id, **kwargs):
        """
        get:
        Retrieves version history for the specified Well record and creates a list of diffs for each revision.
        """
        try:
            well = Well.objects.get(well_tag_number=well_id)
        except Well.DoesNotExist:
            raise Http404("Well not found")

        return Response(get_well_history(well))


WELL_PROPERTIES = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title='GeoJSON Feature properties.',
    description='See: https://tools.ietf.org/html/rfc7946#section-3.2',
    properties={
        'well_tag_number': get_model_feature_schema(Well, 'well_tag_number'),
        'identification_plate_number': get_model_feature_schema(Well, 'identification_plate_number'),
        'well_status': get_model_feature_schema(WellStatusCode, 'description'),
        'licence_status': get_model_feature_schema(LicencedStatusCode, 'description'),
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            max_length=255,
            title='Detail',
            description=('Link to well summary report within the Groundwater Wells and Aquifer (GWELLS)'
                         ' application. The well summary provides the overall desription and history of the'
                         ' well.')),
        'artesian_flow': get_model_feature_schema(Well, 'artesian_flow'),
        'artesian_flow_units': openapi.Schema(
            type=openapi.TYPE_STRING,
            max_length=255,
            title='Artesian Flow',
            description='Unit of measure for artesian flow'),
        'artesian_pressure': get_model_feature_schema(Well, 'artesian_pressure'),
        'well_class': get_model_feature_schema(WellClassCode, 'description'),
        'intended_water_use': get_model_feature_schema(IntendedWaterUseCode, 'description'),
        'street_address': get_model_feature_schema(Well, 'street_address'),
        'finished_well_depth': get_model_feature_schema(Well, 'finished_well_depth'),
        'diameter': get_model_feature_schema(Casing, 'diameter'),
        'static_water_level': get_model_feature_schema(Well, 'static_water_level'),
        'bedrock_depth': get_model_feature_schema(Well, 'bedrock_depth'),
        'yield': get_model_feature_schema(Well, 'well_yield'),
        'yield_unit': get_model_feature_schema(WellYieldUnitCode, 'description'),
        'aquifer_id': get_model_feature_schema(Well, 'aquifer'),
        'observation_well_number': get_model_feature_schema(Well, 'observation_well_number'),
        'observation_well_status': get_model_feature_schema(Well, 'observation_well_status')
    })


@swagger_auto_schema(
    method="GET",
    auto_schema=None
)
@api_view(['GET'])
def well_geojson(request, **kwargs):
    realtime = request.GET.get('realtime') in ('True', 'true')
    if realtime:
        sw_long = request.query_params.get('sw_long')
        sw_lat = request.query_params.get('sw_lat')
        ne_long = request.query_params.get('ne_long')
        ne_lat = request.query_params.get('ne_lat')
        bounds = None
        bounds_sql = ''

        if sw_long and sw_lat and ne_long and ne_lat:
            bounds_sql = 'and well.geom @ ST_MakeEnvelope(%s, %s, %s, %s, 4326)'
            bounds = (sw_long, sw_lat, ne_long, ne_lat)

        iterator = GeoJSONIterator(
            WELLS_SQL_V1.format(bounds=bounds_sql), WELL_CHUNK_SIZE, connection.cursor(), bounds)
        response = StreamingHttpResponse((item for item in iterator),
                                         content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="well.json"'
        return response
    else:
        # Generating spatial data realtime is much too slow,
        # so we have to redirect to a pre-generated instance.
        url = 'https://{}/{}/{}'.format(
            get_env_variable('S3_HOST'),
            get_env_variable('S3_WELL_EXPORT_BUCKET'),
            'api/v1/gis/wells.json')
        return HttpResponseRedirect(url)


LITHOLOGY_PROPERTIES = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title='GeoJSON Feature properties.',
    description='See: https://tools.ietf.org/html/rfc7946#section-3.2',
    properties={
        'well_tag_number': get_model_feature_schema(Well, 'well_tag_number'),
        'identification_plate_number': get_model_feature_schema(Well, 'identification_plate_number'),
        'well_status': get_model_feature_schema(WellStatusCode, 'description'),
        'licence_status': get_model_feature_schema(LicencedStatusCode, 'description'),
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            max_length=255,
            title='Detail',
            description=('Link to well summary report within the Groundwater Wells and Aquifer (GWELLS)'
                         ' application. The well summary provides the overall desription and history of the'
                         ' well.')),
        'from': get_model_feature_schema(LithologyDescription, 'start'),
        'to': get_model_feature_schema(LithologyDescription, 'end'),
        'colour': get_model_feature_schema(LithologyColourCode, 'description'),
        'description': get_model_feature_schema(LithologyDescriptionCode, 'description'),
        'material': get_model_feature_schema(LithologyMaterialCode, 'description'),
        'observation': get_model_feature_schema(LithologyDescription, 'lithology_observation'),
        'hardness': get_model_feature_schema(LithologyHardnessCode, 'description'),
        'well_class': get_model_feature_schema(WellClassCode, 'description'),
        'intended_water_use': get_model_feature_schema(IntendedWaterUseCode, 'description'),
        'street_address': get_model_feature_schema(Well, 'street_address'),
        'finished_well_depth': get_model_feature_schema(Well, 'finished_well_depth'),
        'diameter': get_model_feature_schema(Casing, 'diameter'),
        'static_water_level': get_model_feature_schema(Well, 'static_water_level'),
        'bedrock_depth': get_model_feature_schema(Well, 'bedrock_depth'),
        'yield': get_model_feature_schema(Well, 'well_yield'),
        'yield_unit': get_model_feature_schema(WellYieldUnitCode, 'description'),
        'aquifer_id': get_model_feature_schema(Well, 'aquifer'),
        'raw_data': get_model_feature_schema(LithologyDescription, 'lithology_raw_data')
    })


@swagger_auto_schema(
    method="GET",
    auto_schema=None
)
@api_view(['GET'])
def lithology_geojson(request, **kwargs):
    realtime = request.GET.get('realtime') in ('True', 'true')
    if realtime:
        sw_long = request.query_params.get('sw_long')
        sw_lat = request.query_params.get('sw_lat')
        ne_long = request.query_params.get('ne_long')
        ne_lat = request.query_params.get('ne_lat')
        bounds = None
        bounds_sql = ''

        if sw_long and sw_lat and ne_long and ne_lat:
            bounds_sql = 'and well.geom @ ST_MakeEnvelope(%s, %s, %s, %s, 4326)'
            bounds = (sw_long, sw_lat, ne_long, ne_lat)

        iterator = GeoJSONIterator(
            LITHOLOGY_SQL.format(bounds=bounds_sql), LITHOLOGY_CHUNK_SIZE, connection.cursor(), bounds)
        response = StreamingHttpResponse((item for item in iterator),
                                         content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="lithology.json"'
        return response
    else:
        # Generating spatial data realtime is much too slow,
        # so we have to redirect to a pre-generated instance.
        url = 'https://{}/{}/{}'.format(
            get_env_variable('S3_HOST'),
            get_env_variable('S3_WELL_EXPORT_BUCKET'),
            'api/v1/gis/lithology.json')
        return HttpResponseRedirect(url)

@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
def well_licensing(request, **kwargs):
    tag = request.GET.get('well_tag_number')
    try:
        if tag and tag.isnumeric():
            well = Well.objects.get(well_tag_number=tag)
            raw_query = """
                SELECT DISTINCT 
                aw.licence_number 
                FROM well_licences wl 
                LEFT JOIN aquifers_waterrightslicence aw 
                ON aw.wrl_sysid = wl.waterrightslicence_id
                WHERE well_id = %s
            """

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [tag])
                result = cursor.fetchall()
                flattened_result = [value for row in result for value in row]
                data = {
                    'status': well.licenced_status.description,
                    'number': flattened_result,
                    'date': ''
                }
            return JsonResponse(data)
    except Exception:
        return HttpResponse(status=500)
    return HttpResponse(status=400)

    


# Deprecated. Use WellSubsurface instead
class WellScreens(ListAPIView):
    """
    Returns well screen info for a range of wells

    get:
    Returns a compact list of wells including screen_set fields
    """


    model = Well
    serializer_class = WellDrawdownSerializer
    filter_backends = (GeometryFilterBackend, RadiusFilterBackend)

    def get_queryset(self):
        qs = Well.objects.all() \
            .select_related('intended_water_use', 'aquifer', 'aquifer__subtype') \
            .prefetch_related('screen_set')


        if not self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = qs.exclude(well_publication_status='Unpublished')

        # check if a point was supplied (note: actual filtering will be by
        # the filter_backends classes).  If so, add distances from the point.
        point = self.request.query_params.get('point', None)
        srid = self.request.query_params.get('srid', 4326)
        radius = self.request.query_params.get('radius', None)
        if point and radius:
            try:
                shape = GEOSGeometry(point, srid=int(srid))
                radius = float(radius)
                assert shape.geom_type == 'Point'
            except (ValueError, AssertionError, GDALException, GEOSException):
                raise ValidationError({
                    'point': 'Invalid point geometry. Use geojson geometry or WKT. Example: {"type": "Point", "coordinates": [-123,49]}'
                })
            else:
                qs = qs.annotate(
                    distance=Cast(Distance('geom', shape), output_field=FloatField())
                ).order_by('distance')

        # can also supply a comma separated list of wells
        wells = self.request.query_params.get('wells', None)
        if wells:
            wells = wells.split(',')

            for w in wells:
                if not w.isnumeric():
                    raise ValidationError(detail='Invalid well')

            wells = map(int, wells)

            qs = qs.filter(well_tag_number__in=wells)

        return qs


class WellLithology(ListAPIView):
    """
    Returns the lithologydescription_set information for a range of wells.
    
    get:
    Returns list of wells with lat/long and lithologydescription_set information.
    """    

    model = Well
    serializer_class = WellLithologySerializer
    filter_backends = (GeometryFilterBackend,)

    def get_queryset(self):
        qs = Well.objects.all()

        if not self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = qs.exclude(well_publication_status='Unpublished')

        # allow comma separated list of wells by well tag number
        wells = self.request.query_params.get('wells', None)
        if wells:
            wells = wells.split(',')

            for w in wells:
                if not w.isnumeric():
                    raise ValidationError(detail='Invalid well')

            wells = map(int, wells)

            qs = qs.filter(well_tag_number__in=wells)

        return qs
class AddressGeocoder(APIView):
    """
    Address Autocomplete Request handler
    
    get:
    Takes Partial Address Values and returns list of possible auto complete values
    """
    def get(self, request,**kwargs):
        GEOCODER_ADDRESS_URL = get_env_variable('GEOCODER_ADDRESS_API_BASE') + self.request.query_params.get('searchTag')
        response = requests.get(GEOCODER_ADDRESS_URL)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Create a Django JsonResponse object and return it
            return JsonResponse(data)
        else:
        # If the request was not successful, return an appropriate HTTP response
            return JsonResponse({'error': f"Error: {response.status_code} - {response.text}"}, status=500)

@api_view(['GET'])
def aquifer_pump_params(request, **kwargs):
    realtime = request.GET.get('realtime') in ('True', 'true')
    if realtime:
        sw_long = request.query_params.get('sw_long')
        sw_lat = request.query_params.get('sw_lat')
        ne_long = request.query_params.get('ne_long')
        ne_lat = request.query_params.get('ne_lat')
        bounds = None
        bounds_sql = ''

        if sw_long and sw_lat and ne_long and ne_lat:
            bounds_sql = 'and well.geom @ ST_MakeEnvelope(%s, %s, %s, %s, 4326)'
            bounds = (sw_long, sw_lat, ne_long, ne_lat)

        iterator = GeoJSONIterator(
                        PUMPING_TEST_AQUIFER_PARAMETER_SQL.format(bounds=bounds_sql), PUMPING_TEST_AQUIFER_PARAMETER_CHUNK_SIZE,
                        connection.cursor(),
                        bounds)
        response = StreamingHttpResponse((item for item in iterator),
                                         content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="pumpingTestAquiferParameters.json"'
        return response
    else:
        # Generating spatial data realtime is much too slow,
        # so we have to redirect to a pre-generated instance.
        url = 'https://{}/{}/{}'.format(
            get_env_variable('S3_HOST'),
            get_env_variable('S3_WELL_EXPORT_BUCKET'),
            'api/v2/gis/pumpingTestAquiferParameters.json')
        return HttpResponseRedirect(url)
