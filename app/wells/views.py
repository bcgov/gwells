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
import json
from urllib.parse import quote
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.views import generic

from gwells.models import Survey
from wells.models import Well
from wells.minio import MinioClient
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

        if settings.ENABLE_ADDITIONAL_DOCUMENTS:
            # Generic error Handling for now
            try:

                minio_client = MinioClient()

                context['host'] = minio_client.host
                context['documents'] = []

                documents = minio_client.get_documents(
                    context['well'].well_tag_number)

                for doc in documents:
                    document = {}
                    document['bucket_name'] = doc.bucket_name
                    object_name = doc.object_name
                    document['object_name'] = object_name.replace(' ', '+')
                    document['display_name'] = object_name[object_name.find(
                        '/')+1: object_name.find('/') + 1 + len(object_name)]
                    context['documents'].append(document)
                    context['documents'] = sorted(
                        context['documents'], key=lambda k: k['display_name'])
            except Exception as exception:
                context['file_client_error'] = 'Error retrieving documents.'
                print("Document access exception: " + str(exception))
        return context


class ListFiles(APIView):

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, tag):
        client = MinioClient()
        documents = client.get_documents(int(tag))
        result = []
        for doc in documents:
            document = {
                "url": 'https://{}/{}/{}'.format(client.host,
                                                 quote(doc.bucket_name),
                                                 quote(doc.object_name)),
                "name": doc.object_name[doc.object_name.find("/")+1:]
            }
            result.append(document)

        return Response(result)
