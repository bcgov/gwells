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
from django.views.decorators.cache import never_cache, cache_page

from aquifers import views

CACHE_TTL = 60*15

urlpatterns = [
    url(r'^api/v1/aquifers/$',
        never_cache(views.AquiferListCreateAPIView.as_view()),
        name='aquifers-list-create'
        ),

    url(r'^api/v1/aquifers/(?P<aquifer_id>[0-9]+)/$',
        never_cache(views.AquiferRetrieveUpdateAPIView.as_view()),
        name='aquifer-retrieve-update'
        ),

    url(r'^api/v1/aquifer-codes/materials/$',
        cache_page(CACHE_TTL)(views.AquiferMaterialListAPIView.as_view()),
        name='aquifer-material-list'
        ),

    url(r'^api/v1/aquifer-codes/quality-concerns/$',
        cache_page(CACHE_TTL)(views.QualityConcernListAPIView.as_view()),
        name='quality-concern-list'
        ),

    url(r'^api/v1/aquifer-codes/vulnerability/$',
        cache_page(CACHE_TTL)(views.AquiferVulnerabilityListAPIView.as_view()),
        name='aquifer-vulnerability-code-list'
        ),

    url(r'^api/v1/aquifer-codes/subtypes/$',
        cache_page(CACHE_TTL)(views.AquiferSubtypeListAPIView.as_view()),
        name='aquifer-subtype-list'
        ),

    url(r'^api/v1/aquifer-codes/productivity/$',
        cache_page(CACHE_TTL)(views.AquiferProductivityListAPIView.as_view()),
        name='aquifer-productivity-code-list'
        ),

    url(r'^api/v1/aquifer-codes/demand/$',
        cache_page(CACHE_TTL)(views.AquiferDemandListAPIView.as_view()),
        name='aquifer-demand-list'
        ),

    url(r'^api/v1/aquifer-codes/water-use/$',
        cache_page(CACHE_TTL)(views.WaterUseListAPIView.as_view()),
        name='aquifer-water-use-code-list'
        ),

    # Aquifers home (loads aquifers application)
    url(r'^aquifers/', views.AquiferHomeView.as_view(), name='aquifers-home')
]
