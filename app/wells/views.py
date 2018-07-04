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
from django.http import Http404
from django.views import generic
from django.shortcuts import redirect

from gwells.models import Survey
from gwells.roles import WELLS_ROLES
from wells.models import Well
from wells.documents import MinioClient
from wells.permissions import WellsDocumentPermissions

from gwells import settings


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


class RetrieveFile(APIView):
    """ Redirects user to a protected document on an S3-compliant host (AWS or Minio) """

    permission_classes = (WellsDocumentPermissions,)

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, file: str):
        """ returns a redirect to a private document """
        client = MinioClient(disable_public=True)
        authorized_link = client.get_private_file(file)

        if not authorized_link:
            raise Http404

        return redirect(authorized_link)
