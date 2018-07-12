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

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Prefetch
from django.http import Http404
from django.views import generic
from rest_framework.generics import ListCreateAPIView

from gwells import settings
from gwells.models import Survey
from gwells.roles import WELLS_ROLES
from registries.views import APILimitOffsetPagination

from wells.models import Well
from wells.documents import MinioClient
from wells.permissions import WellsDocumentPermissions, WellsPermissions
from wells.serializers import WellListSerializer


class WellDetailView(generic.DetailView):
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


class ListFiles(APIView):
    """
    List documents associated with a well (e.g. well construction report)

    get: list files found for the well identified in the uri
    """

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, tag):
        user_is_staff = self.request.user.groups.filter(
            name__in=WELLS_ROLES).exists()

        client = MinioClient(
            request=request, disable_private=(not user_is_staff))

        documents = client.get_documents(
            int(tag), include_private=user_is_staff)

        return Response(documents)


class WellListAPIView(ListCreateAPIView):
    """List and create wells

    get: returns a list of wells
    post: adds a new well
    """

    permission_classes = (WellsPermissions,)
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
            )
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
