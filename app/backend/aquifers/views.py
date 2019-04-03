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
from datetime import datetime
import logging

from django_filters import rest_framework as djfilters
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect, StreamingHttpResponse
from django.views.generic import TemplateView
from django.db.models import Q
from django.db import connection

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny

from reversion.views import RevisionMixin

from gwells.documents import MinioClient
from gwells.roles import AQUIFERS_EDIT_ROLE
from gwells.settings.base import get_env_variable

from aquifers import models
from aquifers import serializers
from aquifers.models import (
    Aquifer,
    AquiferResourceSection,
    AquiferDemand,
    AquiferMaterial,
    AquiferProductivity,
    AquiferSubtype,
    AquiferVulnerabilityCode,
    AquiferMaterial,
    QualityConcern,
    WaterUse
)
from aquifers.permissions import HasAquiferEditRoleOrReadOnly, HasAquiferEditRole
from gwells.change_history import generate_history_diff
from registries.views import AuditCreateMixin, AuditUpdateMixin
from gwells.open_api import (
    get_geojson_schema, get_model_feature_schema, GEO_JSON_302_MESSAGE, GEO_JSON_PARAMS)
from gwells.management.commands.export_databc import AQUIFERS_SQL, GeoJSONIterator, AQUIFER_CHUNK_SIZE, \
    MAX_AQUIFERS_SQL


logger = logging.getLogger(__name__)


class AquiferRetrieveUpdateAPIView(RevisionMixin, AuditUpdateMixin, RetrieveUpdateAPIView):
    """List aquifers
    get: return details of aquifers
    patch: update aquifer
    """

    permission_classes = (HasAquiferEditRoleOrReadOnly,)
    queryset = Aquifer.objects.all()
    lookup_field = 'aquifer_id'
    serializer_class = serializers.AquiferSerializer


class AquiferListCreateAPIView(RevisionMixin, AuditCreateMixin, ListCreateAPIView):
    """List aquifers
    get: return a list of aquifers
    post: create an aquifer
    """

    permission_classes = (HasAquiferEditRoleOrReadOnly,)
    serializer_class = serializers.AquiferSerializer
    filter_backends = (djfilters.DjangoFilterBackend,
                       OrderingFilter, SearchFilter)
    ordering_fields = '__all__'
    ordering = ('aquifer_id',)

    def get_queryset(self):
        """
        We have a custom search which does a case insensitive substring of aquifer_name,
        exact match on aquifer_id, and also looks at an array of provided resources attachments
        of which we require one to be present if any are specified. The front-end doesn't use
        DjangoFilterBackend's querystring array syntax, preferring ?a=1,2 rather than ?a[]=1&a[]=2,
        so again we need a custom back-end implementation.
        """
        qs = Aquifer.objects.all()
        resources__section__code = self.request.GET.get(
            "resources__section__code")
        search = self.request.GET.get('search')
        # truthy check - ignore missing and emptystring.
        if resources__section__code:
            qs = qs.filter(
                resources__section__code__in=resources__section__code.split(','))
        if search:  # truthy check - ignore missing and emptystring.
            disjunction = Q(aquifer_name__icontains=search)
            if search.isdigit():
                disjunction = disjunction | Q(pk=int(search))
            qs = qs.filter(disjunction)
        return qs.distinct()


class AquiferResourceSectionListAPIView(ListAPIView):
    """List aquifer materials codes
    get: return a list of aquifer material codes
    """

    queryset = AquiferResourceSection.objects.all()
    serializer_class = serializers.AquiferResourceSectionSerializer


class AquiferMaterialListAPIView(ListAPIView):
    """List aquifer materials codes
    get: return a list of aquifer material codes
    """

    queryset = AquiferMaterial.objects.all()
    serializer_class = serializers.AquiferMaterialSerializer


class QualityConcernListAPIView(ListAPIView):
    """List aquifer materials codes
    get: return a list of quality concern codes
    """

    queryset = models.QualityConcern.objects.all()
    serializer_class = serializers.QualityConcernSerializer


class AquiferVulnerabilityListAPIView(ListAPIView):
    """List aquifer vulnerability codes
    get: return a list of aquifer vulnerability codes
    """

    queryset = AquiferVulnerabilityCode.objects.all()
    serializer_class = serializers.AquiferVulnerabilitySerializer


class AquiferSubtypeListAPIView(ListAPIView):
    """List aquifer subtypes codes
    get: return a list of aquifer subtype codes
    """

    queryset = AquiferSubtype.objects.all()
    serializer_class = serializers.AquiferSubtypeSerializer


class AquiferProductivityListAPIView(ListAPIView):
    """List aquifer productivity codes
    get: return a list of aquifer productivity codes
    """

    queryset = AquiferProductivity.objects.all()
    serializer_class = serializers.AquiferProductivitySerializer


class AquiferDemandListAPIView(ListAPIView):
    """List aquifer demand codes
    get: return a list of aquifer demand codes
    """

    queryset = AquiferDemand.objects.all()
    serializer_class = serializers.AquiferDemandSerializer


class WaterUseListAPIView(ListAPIView):
    """List Water Use Codes
    get: return a list of water use codes
    """

    queryset = models.WaterUse.objects.all()
    serializer_class = serializers.WaterUseSerializer


class ListFiles(APIView):
    """
    List documents associated with an aquifer

    get: list files found for the aquifer identified in the uri
    """

    @swagger_auto_schema(responses={200: openapi.Response('OK',
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
    def get(self, request, aquifer_id):
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
    queryset = Aquifer.objects.all()
    pagination_class = None

    filter_backends = (filters.SearchFilter,)
    ordering = ('aquifer_id',)
    search_fields = (
        'aquifer_id',
        'aquifer_name',
    )

    def get(self, request):
        search = self.request.query_params.get('search', None)
        if not search or len(search) < 3:
            # avoiding responding with excess results
            return Response([])
        else:
            return super().get(request)


class AquiferHistory(APIView):
    """
    get: returns a history of changes to a Aquifer model record
    """
    permission_classes = (HasAquiferEditRole,)
    queryset = Aquifer.objects.all()
    swagger_schema = None

    def get(self, request, aquifer_id):
        """
        Retrieves version history for the specified Aquifer record and creates a list of diffs
        for each revision.
        """

        try:
            aquifer = Aquifer.objects.get(aquifer_id=aquifer_id)
        except Aquifer.DoesNotExist:
            raise Http404("Aquifer not found")

        # query records in history for this model.
        aquifer_history = [obj for obj in aquifer.history.all().order_by(
            '-revision__date_created')]

        aquifer_history_diff = generate_history_diff(
            aquifer_history, 'aquifer ' + aquifer_id)

        history_diff = sorted(aquifer_history_diff,
                              key=lambda x: x['date'], reverse=True)

        return Response(history_diff)


class PreSignedDocumentKey(APIView):
    """
    Get a pre-signed document key to upload into an S3 compatible document store

    post: obtain a URL that is pre-signed to allow client-side uploads
    """

    permission_classes = (HasAquiferEditRole,)

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, aquifer_id):
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
    def delete(self, request, aquifer_id):
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


AQUIFER_PROPERTIES = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title='GeoJSON Feature properties.',
    description='See: https://tools.ietf.org/html/rfc7946#section-3.2',
    properties={
        'aquifer_id': get_model_feature_schema(Aquifer, 'aquifer_id'),
        'name': get_model_feature_schema(Aquifer, 'aquifer_name'),
        'location': get_model_feature_schema(Aquifer, 'location_description'),
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
    operation_description=('Get GeoJSON (see https://tools.ietf.org/html/rfc7946) dump of aquifers.'),
    method='get',
    manual_parameters=GEO_JSON_PARAMS,
    responses={
        302: openapi.Response(GEO_JSON_302_MESSAGE),
        200: openapi.Response(
            'GeoJSON data for aquifers.',
            get_geojson_schema(AQUIFER_PROPERTIES, 'Polygon'))
        })
@api_view(['GET'])
def aquifer_geojson(request):
    realtime = request.GET.get('realtime') in ('True', 'true')
    if realtime:
        sw_long = request.query_params.get('sw_long')
        sw_lat = request.query_params.get('sw_lat')
        ne_long = request.query_params.get('ne_long')
        ne_lat = request.query_params.get('ne_lat')

        if sw_long and sw_lat and ne_long and ne_lat:
            bounds_sql = 'and geom @ ST_Transform(ST_MakeEnvelope(%s, %s, %s, %s, 4326), 3005)'
            bounds = (sw_long, sw_lat, ne_long, ne_lat)

        iterator = GeoJSONIterator(AQUIFERS_SQL.format(bounds=bounds_sql),
                                   AQUIFER_CHUNK_SIZE,
                                   connection.cursor(),
                                   MAX_AQUIFERS_SQL,
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

