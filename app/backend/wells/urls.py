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

from gwells.urls import app_root_slash
from . import views


urlpatterns = [
    # Template views
    url(r'^well/(?P<pk>[0-9]+)$',
        views.WellDetailView.as_view(), name='well_detail'),

    # API endpoints
    # Well
    url(r'^api/v1/well/(?P<well_tag_number>[0-9]+)$',
        never_cache(views.WellDetail.as_view()), name='well-detail'),

    # Well tag search
    url(r'^api/v1/wells/tags/$',
        never_cache(views.WellTagSearchAPIView.as_view()), name='well-tag-search'),

    # Documents (well records)
    url(r'^api/v1/wells/(?P<tag>[0-9]+)/files$',
        never_cache(views.ListFiles.as_view()), name='file-list'),

    # Well list
    url(r'^api/v1/wells/$',
        never_cache(views.WellListAPIView.as_view()), name='well-list'),

]
