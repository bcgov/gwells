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
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^groundwater-wells$', views.HomeView.as_view(), name='home'),
    url(r'^groundwater-wells/search$', views.well_search, name='search'),
    #url(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.DetailView.as_view(), name='detail'),
    url(r'^groundwater-wells/submission/$', views.ActivitySubmissionListView.as_view(), name='activity_submission_list'),
    url(r'^groundwater-wells/submission/(?P<pk>[0-9]+)$', views.ActivitySubmissionDetailView.as_view(), name='activity_submission_detail'),
    url(r'^groundwater-wells/well/(?P<pk>[0-9]+)$', views.WellDetailView.as_view(), name='well_detail'),
    url(r'^groundwater-wells/health$', views.health),
    url(r'^groundwater-wells/admin/', admin.site.urls),
    url(r'^groundwater-wells/additional-information', TemplateView.as_view(template_name='gwells/additional_information.html'), name='additional_information'),
    url(r'^groundwater-wells/ajax/map_well_search/$', views.map_well_search, name='map_well_search'),
]

if settings.ENABLE_DATA_ENTRY:
    urlpatterns = [
        url(r'^submission/create$', views.ActivitySubmissionWizardView.as_view(views.FORMS), name='activity_submission_create'),
    ] + urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns