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

from django.db.models import Prefetch
from django.http import Http404
from django.views.generic import DetailView

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
from wells.serializers import WellListSerializer, WellTagSearchSerializer, WellDetailSerializer
from wells.permissions import WellsEditPermissions


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


class ListExtracts(APIView):
    """
    List well extracts

    get: list well extracts
    """
    @swagger_auto_schema(auto_schema=None)
    def get(self, request):
        host = get_env_variable('S3_HOST')
        minioClient = Minio(host,
                            access_key=get_env_variable('S3_PUBLIC_ACCESS_KEY'),
                            secret_key=get_env_variable('S3_PUBLIC_SECRET_KEY'),
                            secure=True)
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
        print(extension)
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
    queryset = Well.objects.all()
    pagination_class = None
    serializer_class = WellTagSearchSerializer
    lookup_field = 'well_tag_number'

    filter_backends = (filters.SearchFilter,)
    ordering = ('well_tag_number',)
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
