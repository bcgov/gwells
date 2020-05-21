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
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook

from django_filters import rest_framework as djfilters
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.db import connection
from django.db.models import Q, Func, TextField
from django.db.models.functions import Cast
from django.contrib.gis.db.models.functions import Transform
from django.views.decorators.cache import cache_page

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import filters
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination

from reversion.views import RevisionMixin

from gwells.settings.base import get_env_variable
from gwells.views import AuditCreateMixin, AuditUpdateMixin
from gwells.management.commands.export_databc import (
    AQUIFERS_SQL_V2,
    GeoJSONIterator,
    AQUIFER_CHUNK_SIZE,
)

from aquifers import serializers, serializers_v2
from aquifers.models import Aquifer
from aquifers.filters import BoundingBoxFilterBackend
from aquifers.permissions import HasAquiferEditRoleOrReadOnly

logger = logging.getLogger(__name__)


class AquiferRetrieveUpdateAPIViewV2(RevisionMixin, AuditUpdateMixin, RetrieveUpdateAPIView):
    """List aquifers
    get: return details of aquifers
    patch: update aquifer
    """
    swagger_schema = None
    permission_classes = (HasAquiferEditRoleOrReadOnly,)
    queryset = Aquifer.objects.all()
    lookup_field = 'aquifer_id'

    def get_serializer_class(self):
        return serializers_v2.AquiferDetailSerializerV2


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

    # V2 changes to `and`-ing the filters by default unless "match_any" is explicitly set to 'true'
    match_any = query.get('match_any') == 'true'

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


class AquiferListCreateAPIViewV2(RevisionMixin, AuditCreateMixin, ListCreateAPIView):
    """List aquifers
    get: return a list of aquifers
    post: create an aquifer
    """
    swagger_schema = None
    pagination_class = LargeResultsSetPagination
    permission_classes = (HasAquiferEditRoleOrReadOnly,)
    filter_backends = (djfilters.DjangoFilterBackend,
                       OrderingFilter, SearchFilter, BoundingBoxFilterBackend)
    ordering_fields = '__all__'
    ordering = ('aquifer_id',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers_v2.AquiferSerializerV2
        else:
            return serializers_v2.AquiferDetailSerializerV2

    def get_queryset(self):
        qs = _aquifer_qs(self.request)

        qs = qs.annotate(extent=Cast(Transform(Func('geom', function='ST_Envelope'), 4326), output_field=TextField()))

        return qs.values(
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
            'extent'
        )


class AquiferNameListV2(ListAPIView):
    """ List all aquifers in a simplified format """

    swagger_schema = None
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

    def get(self, request, **kwargs):
        serializer = self.get_serializer_class()

        ids = self.request.query_params.get('aquifer_ids', '')
        search = self.request.query_params.get('search', None)

        # avoiding responding with excess results
        results = []
        if ids:
            results = self.queryset.filter(aquifer_id__in=ids.split(','))
        elif search:
            results = self.filter_queryset(self.get_queryset())
        return Response(serializer(results[:20], many=True).data)


@api_view(['GET'])
@schema(None)
def aquifer_geojson_v2(request, **kwargs):
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

        iterator = GeoJSONIterator(AQUIFERS_SQL_V2.format(bounds=bounds_sql),
                                   AQUIFER_CHUNK_SIZE,
                                   connection.cursor(),
                                   bounds)
        response = StreamingHttpResponse((item for item in iterator),
                                         content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="aquifers.json"'
        return response
    else:
        # TODO: Update export_databc command to upload a v2 version of the aquifers JSON:
        # https://apps.nrs.gov.bc.ca/int/jira/browse/WATER-1049
        # Generating spatial data realtime is much too slow,
        # so we have to redirect to a pre-generated instance.
        url = 'https://{}/{}/{}'.format(
            get_env_variable('S3_HOST'),
            get_env_variable('S3_WELL_EXPORT_BUCKET'),
            'api/v1/gis/aquifers.json')
        return HttpResponseRedirect(url)
