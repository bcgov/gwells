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
import logging
import csv
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook

from django_filters import rest_framework as djfilters
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect, StreamingHttpResponse
from django.db.models import Q
from django.db import connection
from django.views.decorators.cache import cache_page
from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from reversion.views import RevisionMixin

from gwells.documents import MinioClient
from gwells.roles import AQUIFERS_EDIT_ROLE
from gwells.settings.base import get_env_variable
from gwells.views import AuditCreateMixin, AuditUpdateMixin
from gwells.open_api import (
    get_geojson_schema,
    get_model_feature_schema,
    GEO_JSON_302_MESSAGE,
    GEO_JSON_PARAMS
)
from gwells.management.commands.export_databc import (
    AQUIFERS_SQL_V1,
    GeoJSONIterator,
    AQUIFER_CHUNK_SIZE,
)

from aquifers import models, serializers
from aquifers.change_history import get_aquifer_history_diff
from aquifers.models import (
    Aquifer,
    AquiferResourceSection,
    AquiferDemand,
    AquiferMaterial,
    AquiferProductivity,
    AquiferSubtype,
    AquiferVulnerabilityCode,
    QualityConcern,
    WaterUse
)
from aquifers.filters import BoundingBoxFilterBackend
from aquifers.permissions import HasAquiferEditRoleOrReadOnly, HasAquiferEditRole

logger = logging.getLogger(__name__)

class AquiferEditDetailsAPIViewV1(RetrieveAPIView):
    """List aquifers
    get: return details of aquifers
    """
    permission_classes = (HasAquiferEditRole,)
    swagger_schema = None
    lookup_field = 'aquifer_id'
    serializer_class = serializers.AquiferEditDetailSerializerV1

    def get_queryset(self):
        now = timezone.now()
        qs = Aquifer.objects.all()
        # filter out any non-published aquifer if the user doesn't have the `aquifers_edit` perm
        if not self.request.user.groups.filter(name=AQUIFERS_EDIT_ROLE).exists():
            qs = qs.filter(effective_date__lte=now, expiry_date__gt=now)
        return qs


class AquiferRetrieveUpdateAPIView(RevisionMixin, AuditUpdateMixin, RetrieveUpdateAPIView):
    """List aquifers
    get: return details of aquifers
    patch: update aquifer
    """
    permission_classes = (HasAquiferEditRoleOrReadOnly,)
    queryset = Aquifer.objects.all()
    lookup_field = 'aquifer_id'

    def get_serializer_class(self):
        return serializers.AquiferDetailSerializerV1

    def get_queryset(self):
        now = timezone.now()
        qs = Aquifer.objects.all()
        # filter out any non-published aquifer if the user doesn't have the `aquifers_edit` perm
        if not self.request.user.groups.filter(name=AQUIFERS_EDIT_ROLE).exists():
            qs = qs.filter(effective_date__lte=now, expiry_date__gt=now)
        return qs


def _aquifer_qs(request):
    """
    We have a custom search which does a case insensitive substring of aquifer_name,
    exact match on aquifer_id, and also looks at an array of provided resources attachments
    of which we require one to be present if any are specified. The front-end doesn't use
    DjangoFilterBackend's querystring array syntax, preferring ?a=1,2 rather than ?a[]=1&a[]=2,
    so again we need a custom back-end implementation.

    @param request - the request object
    """
    query = request.GET
    qs = Aquifer.objects.all()
    resources__section__code = query.get("resources__section__code")
    hydraulic = query.get('hydraulically_connected')
    search = query.get('search')

    match_any = True
    now = timezone.now()

    # build a list of filters from qs params
    filters = []
    if hydraulic:
        filters.append(Q(subtype__code__in=serializers.HYDRAULIC_SUBTYPES))

    # ignore missing and empty string for resources__section__code qs param
    if resources__section__code:
        for code in resources__section__code.split(','):
            filters.append(Q(resources__section__code=code))

    if match_any:
        if len(filters) > 0:
            disjunction = filters.pop()

            # combine all disjunctions using `|` a.k.a. SQL `OR`
            for filter in filters:
                disjunction |= filter
            qs = qs.filter(disjunction)
    else:
        # calling .filter() one after another combines `Q`s using SQL `AND`
        for filter in filters:
            qs = qs.filter(filter)

    if search: # only search if the search query is set to something
        disjunction = Q(aquifer_name__icontains=search)
        # if a number is searched, assume it could be an Aquifer ID.
        if search.isdigit():
            disjunction = disjunction | Q(pk=int(search))
        qs = qs.filter(disjunction)

    # exclude non-published and non-retired aquifer if the user doesn't have `aquifers_edit` perm
    if not request.user.groups.filter(name=AQUIFERS_EDIT_ROLE).exists():
        qs = qs.filter(effective_date__lte=timezone.now(), expiry_date__gt=timezone.now(), retire_date__gt=now)

    qs = qs.select_related(
        'demand',
        'material',
        'productivity',
        'subtype',
        'vulnerability')

    qs = qs.distinct()

    return qs


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class AquiferListCreateAPIView(RevisionMixin, AuditCreateMixin, ListCreateAPIView):
    """List aquifers
    get: return a list of aquifers
    post: create an aquifer
    """
    pagination_class = LargeResultsSetPagination
    permission_classes = (HasAquiferEditRoleOrReadOnly,)
    filter_backends = (djfilters.DjangoFilterBackend,
                       OrderingFilter, SearchFilter, BoundingBoxFilterBackend)
    ordering_fields = '__all__'
    ordering = ('aquifer_id',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.AquiferSerializer
        else:
            return serializers.AquiferDetailSerializerV1

    def get_queryset(self):
        return _aquifer_qs(self.request).values(
            'aquifer_id',
            'aquifer_name',
            'location_description',

            'demand__description',
            'material__description',
            'subtype__description',
            'vulnerability__description',
            'productivity__description',

            'area',
            'mapping_year',
            'litho_stratographic_unit',
        )


class AquiferResourceSectionListAPIView(ListAPIView):
    """List aquifer materials codes
    get: return a list of aquifer material codes
    """

    swagger_schema = None
    queryset = AquiferResourceSection.objects.all()
    serializer_class = serializers.AquiferResourceSectionSerializer


class AquiferMaterialListAPIView(ListAPIView):
    """List aquifer materials codes
    get: return a list of aquifer material codes
    """
    swagger_schema = None
    queryset = AquiferMaterial.objects.all()
    serializer_class = serializers.AquiferMaterialSerializer


class QualityConcernListAPIView(ListAPIView):
    """List aquifer materials codes
    get: return a list of quality concern codes
    """

    swagger_schema = None
    queryset = models.QualityConcern.objects.all()
    serializer_class = serializers.QualityConcernSerializer


class AquiferVulnerabilityListAPIView(ListAPIView):
    """List aquifer vulnerability codes
    get: return a list of aquifer vulnerability codes
    """

    swagger_schema = None
    queryset = AquiferVulnerabilityCode.objects.all()
    serializer_class = serializers.AquiferVulnerabilitySerializer


class AquiferSubtypeListAPIView(ListAPIView):
    """List aquifer subtypes codes
    get: return a list of aquifer subtype codes
    """

    swagger_schema = None
    queryset = AquiferSubtype.objects.all()
    serializer_class = serializers.AquiferSubtypeSerializer


class AquiferProductivityListAPIView(ListAPIView):
    """List aquifer productivity codes
    get: return a list of aquifer productivity codes
    """

    swagger_schema = None
    queryset = AquiferProductivity.objects.all()
    serializer_class = serializers.AquiferProductivitySerializer


class AquiferDemandListAPIView(ListAPIView):
    """List aquifer demand codes
    get: return a list of aquifer demand codes
    """

    swagger_schema = None
    queryset = AquiferDemand.objects.all()
    serializer_class = serializers.AquiferDemandSerializer


class WaterUseListAPIView(ListAPIView):
    """List Water Use Codes
    get: return a list of water use codes
    """

    swagger_schema = None
    queryset = models.WaterUse.objects.all()
    serializer_class = serializers.WaterUseSerializer


class ListFiles(APIView):
    """
    List documents associated with an aquifer

    get: list files found for the aquifer identified in the uri
    """

    @swagger_auto_schema(responses={200: openapi.Response(
        'OK',
        openapi.Schema(type=openapi.TYPE_OBJECT, properties={
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
    )})
    def get(self, request, aquifer_id, **kwargs):
        user_is_staff = self.request.user.groups.filter(
            name=AQUIFERS_EDIT_ROLE).exists()

        client = MinioClient(
            request=request, disable_private=(not user_is_staff))

        documents = client.get_documents(
            int(aquifer_id), resource="aquifer", include_private=user_is_staff)

        return Response(documents)


class AquiferNameList(ListAPIView):
    """ List all aquifers in a simplified format """

    serializer_class = serializers.AquiferSerializerBasic
    model = Aquifer
    pagination_class = None

    filter_backends = (filters.SearchFilter,)
    ordering = ('aquifer_id',)
    search_fields = (
        'aquifer_id',
        'aquifer_name',
    )

    def get_queryset(self):
        now = timezone.now()
        qs = Aquifer.objects.all()
        # filter out any non-published aquifer if the user doesn't have the `aquifers_edit` perm
        if not self.request.user.groups.filter(name=AQUIFERS_EDIT_ROLE).exists():
            qs = qs.filter(effective_date__lte=now, expiry_date__gt=now, retire_date__gt=now)
        return qs

    def get(self, request, **kwargs):
        search = self.request.query_params.get('search', None)
        if not search:
            # avoiding responding with excess results
            return Response([])
        results = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer_class()
        return Response(serializer(results[:20], many=True).data)


class AquiferHistory(APIView):
    """
    get: returns a history of changes to a Aquifer model record
    """
    permission_classes = (HasAquiferEditRole,)
    queryset = Aquifer.objects.all()
    swagger_schema = None

    def get(self, request, aquifer_id, **kwargs):
        """
        Retrieves version history for the specified Aquifer record and creates a list of diffs
        for each revision.
        """

        try:
            aquifer = Aquifer.objects.get(aquifer_id=aquifer_id)
        except Aquifer.DoesNotExist:
            raise Http404("Aquifer not found")

        history_diff = get_aquifer_history_diff(aquifer)

        return Response(history_diff)


class PreSignedDocumentKey(APIView):
    """
    Get a pre-signed document key to upload into an S3 compatible document store

    post: obtain a URL that is pre-signed to allow client-side uploads
    """

    permission_classes = (HasAquiferEditRole,)

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, aquifer_id, **kwargs):
        client = MinioClient(
            request=request, disable_private=False)

        object_name = request.GET.get("filename")
        filename = client.format_object_name(
            object_name, int(aquifer_id), "aquifer")
        bucket_name = get_env_variable("S3_AQUIFER_BUCKET")

        is_private = False
        if request.GET.get("private") == "true":
            is_private = True
            bucket_name = get_env_variable("S3_PRIVATE_AQUIFER_BUCKET")

        url = client.get_presigned_put_url(
            filename, bucket_name=bucket_name, private=is_private)

        return JsonResponse({"object_name": object_name, "url": url})


class DeleteAquiferDocument(APIView):
    """
    Delete a document from a S3 compatible store

    delete: remove the specified object from the S3 store
    """

    permission_classes = (HasAquiferEditRole,)

    @swagger_auto_schema(auto_schema=None)
    def delete(self, request, aquifer_id, **kwargs):
        client = MinioClient(
            request=request, disable_private=False)

        is_private = False
        bucket_name = get_env_variable("S3_AQUIFER_BUCKET")

        if request.GET.get("private") == "true":
            is_private = True
            bucket_name = get_env_variable("S3_PRIVATE_AQUIFER_BUCKET")

        object_name = client.get_bucket_folder(
            int(aquifer_id), "aquifer") + "/" + request.GET.get("filename")
        client.delete_document(
            object_name, bucket_name=bucket_name, private=is_private)

        return HttpResponse(status=204)


class SaveAquiferGeometry(APIView):
    """

    """
    permission_classes = (HasAquiferEditRole,)
    parser_class = (FileUploadParser,)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request, aquifer_id, **kwargs):
        logger.info(request.data)
        if 'geometry' not in request.data:
            raise ParseError("Empty content")

        f = request.data['geometry']
        aquifer = Aquifer.objects.get(pk=aquifer_id)
        try:
            aquifer.load_shapefile(f)
        except Aquifer.BadShapefileException as e:
            return Response({
                'message': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST)
        aquifer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, aquifer_id, **kwargs):
        aquifer = Aquifer.objects.get(pk=aquifer_id)
        del aquifer.geom
        aquifer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


AQUIFER_PROPERTIES = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title='GeoJSON Feature properties.',
    description='See: https://tools.ietf.org/html/rfc7946#section-3.2',
    properties={
        'aquifer_id': get_model_feature_schema(Aquifer, 'aquifer_id'),
        'name': get_model_feature_schema(Aquifer, 'aquifer_name'),
        'location': get_model_feature_schema(Aquifer, 'location_description'),
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            max_length=255,
            title='Detail',
            description=('Link to aquifer summary report within the Groundwater Wells and Aquifer (GWELLS)'
                         ' application. The aquifer summary provides the overall desription and history of the'
                         ' aquifer.')),
        'material': get_model_feature_schema(AquiferMaterial, 'description'),
        'subtype': get_model_feature_schema(AquiferSubtype, 'description'),
        'vulnerability': get_model_feature_schema(AquiferVulnerabilityCode, 'description'),
        'productivity': get_model_feature_schema(AquiferProductivity, 'description'),
        'demand': get_model_feature_schema(AquiferDemand, 'description'),
        'water_use': get_model_feature_schema(WaterUse, 'description'),
        'quality_concern': get_model_feature_schema(QualityConcern, 'description'),
        'litho_stratographic_unit': get_model_feature_schema(Aquifer, 'litho_stratographic_unit'),
        'mapping_year': get_model_feature_schema(Aquifer, 'mapping_year'),
        'notes': get_model_feature_schema(Aquifer, 'notes')
    })


@swagger_auto_schema(
    operation_description=(
        'Get GeoJSON (see https://tools.ietf.org/html/rfc7946) dump of aquifers.'),
    method='get',
    manual_parameters=GEO_JSON_PARAMS,
    responses={
        302: openapi.Response(GEO_JSON_302_MESSAGE),
        200: openapi.Response(
            'GeoJSON data for aquifers.',
            get_geojson_schema(AQUIFER_PROPERTIES, 'Polygon'))
    })
@api_view(['GET'])
def aquifer_geojson_v1(request, **kwargs):
    realtime = request.GET.get('realtime') in ('True', 'true')
    if realtime:

        sw_long = request.query_params.get('sw_long')
        sw_lat = request.query_params.get('sw_lat')
        ne_long = request.query_params.get('ne_long')
        ne_lat = request.query_params.get('ne_lat')

        if sw_long and sw_lat and ne_long and ne_lat:
            bounds_sql = 'and geom @ ST_Transform(ST_MakeEnvelope(%s, %s, %s, %s, 4326), 3005)'
            bounds = (sw_long, sw_lat, ne_long, ne_lat)
        else:
            bounds = None
            bounds_sql = ''

        iterator = GeoJSONIterator(AQUIFERS_SQL_V1.format(bounds=bounds_sql),
                                   AQUIFER_CHUNK_SIZE,
                                   connection.cursor(),
                                   bounds)
        response = StreamingHttpResponse((item for item in iterator),
                                         content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="aquifers.json"'
        return response
    else:
        # Generating spatial data realtime is much too slow,
        # so we have to redirect to a pre-generated instance.
        url = 'https://{}/{}/{}'.format(
            get_env_variable('S3_HOST'),
            get_env_variable('S3_WELL_EXPORT_BUCKET'),
            'api/v1/gis/aquifers.json')
        return HttpResponseRedirect(url)


@api_view(['GET'])
@cache_page(60*15)
def aquifer_geojson_simplified_v1(request, **kwargs):
    """
    Sadly, GeoDjango's ORM doesn't seem to directly support a call to
    ST_AsGEOJSON, but the latter performs much better than processing WKT
    in Python, so we must generate SQL here.
    """

    sql = """
    SELECT
        ST_AsGeoJSON((ST_GeometryN(geom_simplified, 1)), 8) :: json AS "geometry",
        aquifer.aquifer_id AS id
    FROM aquifer
    """

    if not request.user.groups.filter(name=AQUIFERS_EDIT_ROLE).exists():
        sql += "WHERE effective_date <= NOW() AND expiry_date >= NOW() AND retire_date >= NOW()"

    iterator = GeoJSONIterator(
        sql,
        AQUIFER_CHUNK_SIZE,
        connection.cursor())
    response = StreamingHttpResponse(
        (item for item in iterator),
        content_type='application/json')
    return response


AQUIFER_EXPORT_FIELDS = [
    'aquifer_id',
    'aquifer_name',
    'location_description',
    'material',
    'litho_stratographic_unit',
    'subtype',
    'vulnerability',
    'area',
    'productivity',
    'demand',
    'mapping_year',
]


def csv_export(request, **kwargs):
    """
    Export aquifers as CSV. This is done in a vanilla functional Django view instead of DRF,
    because DRF doesn't have native CSV support.
    """

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aquifers.csv"'
    writer = csv.writer(response)
    writer.writerow(AQUIFER_EXPORT_FIELDS)

    queryset = _aquifer_qs(request)
    for aquifer in queryset:
        writer.writerow([getattr(aquifer, f) for f in AQUIFER_EXPORT_FIELDS])

    return response


def xlsx_export(request, **kwargs):
    """
    Export aquifers as XLSX.
    """

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(AQUIFER_EXPORT_FIELDS)
    queryset = _aquifer_qs(request)
    for aquifer in queryset:
        ws.append([str(getattr(aquifer, f)) for f in AQUIFER_EXPORT_FIELDS])
    response = HttpResponse(content=save_virtual_workbook(
        wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=aquifers.xlsx'
    return response
