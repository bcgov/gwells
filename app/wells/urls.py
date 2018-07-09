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

from gwells.urls import app_root_slash
from . import views


urlpatterns = [
    # Template views
    url(r'^' + app_root_slash + \
        'well/(?P<pk>[0-9]+)$', views.WellDetailView.as_view(), name='well_detail'),

    # Private documents
    url(r'^wells/files/(?P<file>[\w\ \./]+)$',
        views.RetrieveFile.as_view(), name='private-document'),

    # API endpoints
    url(r'^api/v1/wells/(?P<tag>[0-9]+)/files$',
        views.ListFiles.as_view(), name='file-list'),
    url(r'^api/v1/wells/$',
        views.WellListAPIView.as_view(), name='well-list'),

]
