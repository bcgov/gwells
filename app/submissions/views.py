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

from rest_framework.response import Response
from django.views.generic import TemplateView

from rest_framework.generics import ListCreateAPIView

from gwells import settings
from gwells.models import Survey
from gwells.roles import WELLS_ROLES
from gwells.pagination import APILimitOffsetPagination

from wells.models import Well, ActivitySubmission
from wells.permissions import WellsPermissions

from submissions.serializers import WellSubmissionSerializer


class SubmissionListAPIView(ListCreateAPIView):
    """List and create submissions

    get: returns a list of well activity submissions
    post: adds a new submission
    """

    permission_classes = (WellsPermissions,)
    model = ActivitySubmission
    queryset = ActivitySubmission.objects.all()
    pagination_class = APILimitOffsetPagination
    serializer_class = WellSubmissionSerializer

    def get_queryset(self):
        qs = self.queryset
        qs = qs.order_by("filing_number")
        return qs

    def list(self, request):
        """ List activity submissions with pagination """
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = WellSubmissionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = WellSubmissionSerializer(filtered_queryset, many=True)
        return Response(serializer.data)


class SubmissionsHomeView(TemplateView):
    """Loads the html file container the Submissions web app"""
    template_name = 'submissions/submissions.html'
