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
from django.conf.urls import url
from django.views.decorators.cache import never_cache

from submissions.views import (SubmissionsOptions, SubmissionListAPIView, SubmissionConstructionAPIView,
                               SubmissionAlterationAPIView, SubmissionDecommissionAPIView,
                               SubmissionsHomeView, SubmissionGetAPIView
                               )


urlpatterns = [

    # Submissions form options
    url(r'^api/v1/submissions/options/$',
        never_cache(SubmissionsOptions.as_view()), name='submissions-options'),

    # Submissions list
    url(r'^api/v1/submissions/$',
        never_cache(SubmissionListAPIView.as_view()), name='submissions-list'),
    # Submission
    url(r'^api/v1/submissions/(?P<filing_number>[0-9]+)$',
        never_cache(SubmissionGetAPIView.as_view())),
    # Construction submission
    url(r'^api/v1/submissions/construction$',
        never_cache(SubmissionConstructionAPIView.as_view())),
    # Alteration submission
    url(r'^api/v1/submissions/alteration$',
        never_cache(SubmissionAlterationAPIView.as_view())),
    # Decommission submission
    url(r'^api/v1/submissions/decommission$',
        never_cache(SubmissionDecommissionAPIView.as_view())),

    # Submissions home (loads Submissions application)
    url(r'^submissions/', SubmissionsHomeView.as_view(), name='submissions-home')
]
