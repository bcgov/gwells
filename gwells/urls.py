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

# Creating 2 versions of the app_root. One without and one with trailing slash
# This will allow for any or no additional app_root context to be provided
app_root = settings.APP_CONTEXT_ROOT
if app_root:
   app_root_slash = app_root + '/'
else:
   app_root_slash = app_root

urlpatterns = [
    # url(r'^'+ app_root +'$', views.HomeView.as_view(), name='home'),
    url(r'^'+ app_root_slash +'robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^'+ app_root_slash +'$', views.well_search, name='home'),
    url(r'^'+ app_root_slash +'search$', views.well_search, name='search'),
    # url(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.DetailView.as_view(), name='detail'),
    url(r'^'+ app_root_slash +'well/(?P<pk>[0-9]+)$', views.WellDetailView.as_view(), name='well_detail'),
    url(r'^'+ app_root_slash +'registry$', views.registry, name='registry'),
    url(r'^'+ app_root_slash +'submission/(?P<pk>[0-9]+)$', views.ActivitySubmissionDetailView.as_view(), name='activity_submission_detail'),
    url(r'^'+ app_root_slash +'health$', views.health),
    url(r'^'+ app_root_slash +'groundwater-information', TemplateView.as_view(template_name='gwells/groundwater_information.html'), name='groundwater_information'),
    url(r'^'+ app_root_slash +'ajax/map_well_search/$', views.map_well_search, name='map_well_search'),
    url(r'^'+ app_root_slash +'500.html$', views.test_500_view),
    url(r'^'+ app_root_slash +'404.html$', views.test_500_view),
]

if settings.ENABLE_DATA_ENTRY:
    urlpatterns = [
        url(r'^'+ app_root_slash +'submission/$', views.ActivitySubmissionListView.as_view(), name='activity_submission_list'),
        url(r'^'+ app_root_slash +'submission/create$', views.ActivitySubmissionWizardView.as_view(views.FORMS), name='activity_submission_create'),
    ] + urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^'+ app_root_slash +'admin/', admin.site.urls),
    ] + urlpatterns
