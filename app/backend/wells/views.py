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
from datetime import datetime
import logging
import sys

from django.db.models import Prefetch
from django.http import (
    Http404, HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound, StreamingHttpResponse)
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django_filters import rest_framework as restfilters
from django.db.models import Q
from django_filters import rest_framework as restfilters
from django.db import connection

from functools import reduce
import operator

from django.db.models import Q

from rest_framework import filters, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from minio import Minio

from gwells import settings
from gwells.change_history import generate_history_diff
from gwells.documents import MinioClient
from gwells.models import Survey
from gwells.roles import WELLS_VIEWER_ROLE, WELLS_EDIT_ROLE
from gwells.pagination import APILimitOffsetPagination
from gwells.settings.base import get_env_variable
from gwells.db_comments import get_column_description
from gwells.open_api import (
    get_geojson_schema, get_model_feature_schema, GEO_JSON_302_MESSAGE, GEO_JSON_PARAMS)
from gwells.management.commands.export_databc import (WELLS_SQL, LITHOLOGY_SQL, GeoJSONIterator,
                                                      LITHOLOGY_CHUNK_SIZE, WELL_CHUNK_SIZE,
                                                      MAX_LITHOLOGY_SQL, MAX_WELLS_SQL)

from submissions.serializers import WellSubmissionListSerializer
from submissions.models import WellActivityCode

from wells.filters import BoundingBoxFilterBackend, WellListFilterBackend
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
    WellClassCode,
    WellYieldUnitCode,
    WellStatusCode)
from wells.serializers import (
    WellListAdminSerializer,
    WellListSerializer,
    WellTagSearchSerializer,
    WellDetailSerializer,
    WellDetailAdminSerializer,
    WellLocationSerializer)
from wells.permissions import WellsEditPermissions, WellsEditOrReadOnly


logger = logging.getLogger(__name__)


class WellSearchFilter(restfilters.FilterSet):
    well_tag_number = restfilters.CharFilter()
    identification_plate_number = restfilters.CharFilter()
    owner_full_name = restfilters.CharFilter(lookup_expr='icontains')
    street_address = restfilters.CharFilter(lookup_expr='icontains')
    legal_plan = restfilters.CharFilter()
    legal_lot = restfilters.CharFilter()


class WellLocationFilter(WellSearchFilter, restfilters.FilterSet):
    ne_lat = restfilters.NumberFilter(field_name='latitude', lookup_expr='lte')
    ne_long = restfilters.NumberFilter(
        field_name='longitude', lookup_expr='lte')
    sw_lat = restfilters.NumberFilter(field_name='latitude', lookup_expr='gte')
    sw_long = restfilters.NumberFilter(
        field_name='longitude', lookup_expr='gte')


class WellDetailView(DetailView):
    model = Well
    context_object_name = 'well'
    template_name = 'wells/well_detail.html'

    def get_context_data(self, **kwargs):
        """
        Return the context for the well details page.
        """

        context = super(WellDetailView, self).get_context_data(**kwargs)
        surveys = Survey.objects.order_by('create_date')
        context['surveys'] = surveys
        context['page'] = 'w'

        return context


class WellDetail(RetrieveAPIView):
    """
    Return well detail.
    This view is open to all, and has no permissions.
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

    get: list well extracts
    """
    @swagger_auto_schema(auto_schema=None)
    def get(self, request):
        host = get_env_variable('S3_HOST')
        use_secure = int(get_env_variable('S3_USE_SECURE', 1))
        minioClient = Minio(host,
                            access_key=get_env_variable(
                                'S3_PUBLIC_ACCESS_KEY'),
                            secret_key=get_env_variable(
                                'S3_PUBLIC_SECRET_KEY'),
                            secure=use_secure)
        objects = minioClient.list_objects(
            get_env_variable('S3_WELL_EXPORT_BUCKET'), 'export/')
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

    get: list files found for the well identified in the uri
    """

    @swagger_auto_schema(responses={200: openapi.Response('OK', LIST_FILES_OK)})
    def get(self, request, tag):

        if Well.objects.get(pk=tag).well_publication_status\
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


class WellListAPIView(ListAPIView):
    """List and create wells

    get: returns a list of wells
    """

    permission_classes = (WellsEditOrReadOnly,)
    model = Well
    pagination_class = APILimitOffsetPagination

    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering = ('well_tag_number',)
    search_fields = ('well_tag_number', 'identification_plate_number',
                     'street_address', 'city', 'owner_full_name')

    def get_serializer_class(self):
        """Returns a different serializer class for admin users."""
        serializer_class = WellListSerializer
        if (self.request.user and self.request.user.is_authenticated and
                self.request.user.groups.filter(name=WELLS_VIEWER_ROLE).exists()):
            serializer_class = WellListAdminSerializer

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
            ) \
            .order_by("well_tag_number")

        return qs


class WellTagSearchAPIView(ListAPIView):
    """ seach for wells by tag or owner """

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

    def get(self, request):
        data = self.get_queryset().values('well_tag_number', 'owner_full_name').order_by('well_tag_number')
        return Response(data)


class WellSubmissionsListAPIView(ListAPIView):
    """ lists submissions for a well
        See also:  submissions.SubmissionListAPIView (list all submission records)
        get: returns submission records for a given well
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


class WellLocationListAPIView(ListAPIView):
    """ returns well locations for a given search

        get: returns a list of wells with locations only
    """

    permission_classes = (WellsEditOrReadOnly,)
    model = Well
    serializer_class = WellLocationSerializer

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering = ('well_tag_number',)
    filterset_class = WellLocationFilter
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

    def get(self, request):
        """ cancels request if too many wells are found"""

        qs = self.get_queryset()
        locations = self.filter_queryset(qs)
        count = locations.count()
        # return an empty response if there are too many wells to display
        if count > 2000:
            raise PermissionDenied('Too many wells to display on map. '
                                   'Please zoom in or change your search criteria.')

        if count is 0:
            raise NotFound("No well records could be found.")

        return super().get(request)


class PreSignedDocumentKey(APIView):
    """
    Get a pre-signed document key to upload into an S3 compatible document store

    post: obtain a URL that is pre-signed to allow client-side uploads
    """

    queryset = Well.objects.all()
    permission_classes = (WellsEditPermissions,)

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, tag):
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
    Delete a document from a S3 compatible store

    delete: remove the specified object from the S3 store
    """

    queryset = Well.objects.all()
    permission_classes = (WellsEditPermissions,)

    @swagger_auto_schema(auto_schema=None)
    def delete(self, request, tag):
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
    get: returns a history of changes to a Well model record
    """
    permission_classes = (WellsEditPermissions,)
    queryset = Well.objects.all()
    swagger_schema = None

    def get(self, request, well_id):
        """
        Retrieves version history for the specified Well record and creates a list of diffs
        for each revision.
        """

        try:
            well = Well.objects.get(well_tag_number=well_id)
        except Well.DoesNotExist:
            raise Http404("Well not found")

        # query records in history for this model.
        well_history = [obj for obj in well.history.all().order_by(
            '-revision__date_created')]

        well_history_diff = generate_history_diff(
            well_history, 'well ' + well_id)

        history_diff = sorted(
            well_history_diff, key=lambda x: x['date'], reverse=True)

        return Response(history_diff)


WELL_PROPERTIES = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title='GeoJSON Feature properties.',
    description='See: https://tools.ietf.org/html/rfc7946#section-3.2',
    properties={
        'well_tag_number': get_model_feature_schema(Well, 'well_tag_number'),
        'identification_plate_number': get_model_feature_schema(Well, 'identification_plate_number'),
        'well_status': get_model_feature_schema(WellStatusCode, 'description'),
        'licenced_status': get_model_feature_schema(LicencedStatusCode, 'description'),
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            max_length=255,
            title='Detail',
            description='Well summary.'),
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
        'aquifer_id': get_model_feature_schema(Well, 'aquifer')
    })


@swagger_auto_schema(
    operation_description=('Get GeoJSON (see https://tools.ietf.org/html/rfc7946) dump of wells.'),
    method='get',
    manual_parameters=GEO_JSON_PARAMS,
    responses={
        302: openapi.Response(GEO_JSON_302_MESSAGE),
        200: openapi.Response(
            'GeoJSON data for well.',
            get_geojson_schema(WELL_PROPERTIES, 'Point'))
    }
)
@api_view(['GET'])
def well_geojson(request):
    realtime = request.GET.get('realtime') in ('True', 'true')
    if realtime:
        sw_long = request.query_params.get('sw_long')
        sw_lat = request.query_params.get('sw_lat')
        ne_long = request.query_params.get('ne_long')
        ne_lat = request.query_params.get('ne_lat')
        bounds = None
        bounds_sql = ''

        if sw_long and sw_lat and ne_long and ne_lat:
            bounds_sql = 'and geom @ ST_MakeEnvelope(%s, %s, %s, %s, 4326)'
            bounds = (sw_long, sw_lat, ne_long, ne_lat)

        iterator = GeoJSONIterator(
            WELLS_SQL.format(bounds=bounds_sql), WELL_CHUNK_SIZE, connection.cursor(), MAX_WELLS_SQL, bounds)
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
        'licenced_status': get_model_feature_schema(LicencedStatusCode, 'description'),
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            max_length=255,
            title='Detail',
            description='Well summary.'),
        'from': get_model_feature_schema(LithologyDescription, 'lithology_from'),
        'to': get_model_feature_schema(LithologyDescription, 'lithology_to'),
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
        'aquifer': get_model_feature_schema(Well, 'aquifer')
    })


@swagger_auto_schema(
    operation_description=('Get GeoJSON (see https://tools.ietf.org/html/rfc7946) dump of well '
                           'lithology.'),
    method='get',
    manual_parameters=GEO_JSON_PARAMS,
    responses={
        302: openapi.Response(GEO_JSON_302_MESSAGE),
        200: openapi.Response(
            'GeoJSON data for well lithology.',
            get_geojson_schema(LITHOLOGY_PROPERTIES, 'Point'))
    }
)
@api_view(['GET'])
def lithology_geojson(request):
    realtime = request.GET.get('realtime') in ('True', 'true')
    if realtime:
        sw_long = request.query_params.get('sw_long')
        sw_lat = request.query_params.get('sw_lat')
        ne_long = request.query_params.get('ne_long')
        ne_lat = request.query_params.get('ne_lat')
        bounds = None
        bounds_sql = ''

        if sw_long and sw_lat and ne_long and ne_lat:
            bounds_sql = 'and geom @ ST_MakeEnvelope(%s, %s, %s, %s, 4326)'
            bounds = (sw_long, sw_lat, ne_long, ne_lat)

        iterator = GeoJSONIterator(
            LITHOLOGY_SQL.format(bounds=bounds_sql), LITHOLOGY_CHUNK_SIZE, connection.cursor(),
            MAX_LITHOLOGY_SQL, bounds)
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
