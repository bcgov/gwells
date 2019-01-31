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

from django.db.models import Prefetch, Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from django_filters import rest_framework as restfilters

from functools import reduce
import operator

from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from drf_yasg.utils import swagger_auto_schema

from minio import Minio

from gwells import settings
from gwells.documents import MinioClient
from gwells.models import Survey
from gwells.roles import WELLS_VIEWER_ROLE, WELLS_EDIT_ROLE
from gwells.pagination import APILimitOffsetPagination
from gwells.settings.base import get_env_variable

from wells.models import Well
from wells.serializers import (
    WellListSerializer,
    WellTagSearchSerializer,
    WellDetailSerializer,
    WellDetailAdminSerializer,
    WellLocationSerializer)
from wells.permissions import WellsEditPermissions


class WellSearchFilter(restfilters.FilterSet):
    well = restfilters.CharFilter(method='filter_well_tag_or_plate',
                                  label='Well tag or identification plate number')
    well_tag_number = restfilters.CharFilter()
    identification_plate_number = restfilters.CharFilter()
    street_address_or_city = restfilters.CharFilter(method='filter_street_address_or_city',
                                                    label='Street address or city')
    street_address = restfilters.CharFilter(lookup_expr='icontains')
    owner_full_name = restfilters.CharFilter(lookup_expr='icontains')
    legal_lot = restfilters.CharFilter()
    legal_plan = restfilters.CharFilter()
    legal_district_lot = restfilters.CharFilter()
    land_district = restfilters.CharFilter(field_name='land_district_id',
                                           label='Land district code')
    legal_pid = restfilters.NumberFilter()

    well_status = restfilters.CharFilter(field_name='well_status_id',
                                         label='Well status')
    licenced_status = restfilters.CharFilter(field_name='licenced_status_id',
                                             label='Licenced status')
    company_of_person_responsible = restfilters.UUIDFilter()
    person_responsible = restfilters.UUIDFilter()

    # TODO:
    # - start date of work / end date of work range
    # - well depth (finished or final combined as range)

    aquifer_id = restfilters.NumberFilter()

    # TODO: all other fields :)

    def filter_well_tag_or_plate(self, queryset, name, value):
        return queryset.filter(Q(well_tag_number=value) |
                               Q(identification_plate_number=value))

    def filter_street_address_or_city(self, queryset, name, value):
        return queryset.filter(Q(street_address__icontains=value) |
                               Q(city__icontains=value))


class WellLocationFilter(WellSearchFilter, restfilters.FilterSet):
    ne_lat = restfilters.NumberFilter(field_name='latitude', lookup_expr='lte')
    ne_long = restfilters.NumberFilter(field_name='longitude', lookup_expr='lte')
    sw_lat = restfilters.NumberFilter(field_name='latitude', lookup_expr='gte')
    sw_long = restfilters.NumberFilter(field_name='longitude', lookup_expr='gte')


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

    queryset = Well.objects.all()
    lookup_field = 'well_tag_number'

    def get_serializer(self, *args, **kwargs):
        """ returns a different serializer for admin users """

        serializer = self.serializer_class

        if (self.request.user and self.request.user.is_authenticated and
                self.request.user.groups.filter(name=WELLS_VIEWER_ROLE).exists()):
            serializer = WellDetailAdminSerializer
        return serializer(*args, **kwargs)


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
                            access_key=get_env_variable('S3_PUBLIC_ACCESS_KEY'),
                            secret_key=get_env_variable('S3_PUBLIC_SECRET_KEY'),
                            secure=use_secure)
        objects = minioClient.list_objects(get_env_variable('S3_WELL_EXPORT_BUCKET'))
        urls = list(
            map(
                lambda document: {
                    'url': 'https://{}/{}/{}'.format(host,
                                                     quote(document.bucket_name),
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


class ListFiles(APIView):
    """
    List documents associated with a well (e.g. well construction report)

    get: list files found for the well identified in the uri
    """

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, tag):
        user_is_staff = self.request.user.groups.filter(
            name=WELLS_VIEWER_ROLE).exists()

        client = MinioClient(
            request=request, disable_private=(not user_is_staff))

        documents = client.get_documents(
            int(tag), include_private=user_is_staff)

        return Response(documents)


class WellListAPIView(ListAPIView):
    """List and create wells

    get: returns a list of wells
    """

    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    model = Well
    queryset = Well.objects.all()
    pagination_class = APILimitOffsetPagination
    serializer_class = WellListSerializer

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (restfilters.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering = ('well_tag_number',)
    filterset_class = WellSearchFilter
    search_fields = ('legal_pid', 'legal_plan', 'legal_district_lot', 'legal_block', 'legal_section', 'legal_township', 'legal_range')

    def get_queryset(self):
        qs = self.queryset
        qs = qs \
            .select_related(
                "bcgs_id",
            ).prefetch_related(
                Prefetch("water_quality_characteristics")
            ) \
            .order_by("well_tag_number")

        return qs

    def list(self, request):
        """ List wells with pagination """
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = WellListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = WellListSerializer(filtered_queryset, many=True)
        return Response(serializer.data)


class WellTagSearchAPIView(ListAPIView):
    """ seach for wells by tag or owner """

    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    model = Well
    queryset = Well.objects.only('well_tag_number', 'owner_full_name').all()
    pagination_class = None
    serializer_class = WellTagSearchSerializer
    lookup_field = 'well_tag_number'

    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('well_tag_number',)
    search_fields = (
        'well_tag_number',
        'owner_full_name',
    )

    def get(self, request):
        search = self.request.query_params.get('search', None)
        if not search or len(search) < 3:
            # avoiding responding with entire collection of wells
            return Response([])
        else:
            return super().get(request)


class WellLocationListAPIView(ListAPIView):
    """ returns well locations for a given search

        get: returns a list of wells with locations only
    """

    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    model = Well
    queryset = Well.objects.all()
    serializer_class = WellLocationSerializer

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (restfilters.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering = ('well_tag_number',)
    filterset_class = WellLocationFilter
    pagination_class = None

    # search_fields and get_queryset are fragile here.
    # they need to match up with the search results returned by WellListAPIView.
    # an attempt was made to factor out filtering logic into WellSearchFilter (which WellLocationFilter inherits),
    # but so far, not all the searchable fields have been put into that class.
    # Please note the difference between "searchable fields" (one query param will return results that are valid
    # for any of these fields) and "filter fields" (search by a single individual fields)
    search_fields = ('legal_pid', 'legal_plan', 'legal_district_lot', 'legal_block', 'legal_section', 'legal_township', 'legal_range')

    def get_queryset(self):
        qs = self.queryset

        well_tag_or_plate = self.request.query_params.get('well', None)
        if well_tag_or_plate:
            qs = qs.filter(Q(well_tag_number=well_tag_or_plate) | Q(identification_plate_number=well_tag_or_plate))

        return qs

    def get(self, request):
        """ cancels request if too many wells are found"""

        count = WellLocationFilter(request.GET, queryset=Well.objects.all()).qs.count()
        # return an empty response if there are too many wells to display
        if count > 2000:
            return Response([])
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
            request=request, disable_private=True)

        object_name = request.GET.get("filename")
        filename = "WTN_%s_%s" % (well.well_tag_number, object_name)
        url = client.get_presigned_put_url(filename, bucket_name=get_env_variable("S3_WELLS_BUCKET"))

        return JsonResponse({"object_name": object_name, "url": url})
