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

from aquifers import views

urlpatterns = [
    url(r'^api/v1/aquifers/$',
        never_cache(views.AquiferListAPIView.as_view()),
        name='aquifers-list'
        ),

    url(r'^api/v1/aquifers/(?P<aquifer_id>[0-9]+)/$',
        never_cache(views.AquiferRetrieveUpdateAPIView.as_view()),
        name='aquifer-retrieve-update'
        ),

    url(r'^api/v1/aquifer-codes/materials/$',
        never_cache(views.AquiferMaterialListAPIView.as_view()),
        name='aquifer-material-list'
        ),

    url(r'^api/v1/aquifer-codes/quality-concerns/$',
        never_cache(views.QualityConcernListAPIView.as_view()),
        name='quality-concern-list'
        ),

    url(r'^api/v1/aquifer-codes/vulnerability/$',
        never_cache(views.AquiferVulnerabilityListAPIView.as_view()),
        name='aquifer-vulnerability-code-list'
        ),

    url(r'^api/v1/aquifer-codes/subtypes/$',
        never_cache(views.AquiferSubtypeListAPIView.as_view()),
        name='aquifer-subtype-list'
        ),

    url(r'^api/v1/aquifer-codes/productivity/$',
        never_cache(views.AquiferProductivityListAPIView.as_view()),
        name='aquifer-productivity-code-list'
        ),

    url(r'^api/v1/aquifer-codes/demand/$',
        never_cache(views.AquiferDemandListAPIView.as_view()),
        name='aquifer-demand-list'
        ),

    url(r'^api/v1/aquifer-codes/water-use/$',
        never_cache(views.WaterUseListAPIView.as_view()),
        name='aquifer-water-use-code-list'
        ),

    url(r'^api/v1/aquifers/(?P<aquifer_id>[0-9]+)/$',
        never_cache(views.AquiferRetrieveAPIView.as_view()),
        name='aquifer-retrieve'
    ),

    # Aquifers home (loads aquifers application)
    url(r'^aquifers/', views.AquiferHomeView.as_view(), name='aquifers-home')
]
