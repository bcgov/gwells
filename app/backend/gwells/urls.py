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
import os

import debug_toolbar

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, re_path

from django.shortcuts import redirect
from django.views.decorators.cache import never_cache 

from gwells.views import SurveyListCreateView, SurveyUpdateDeleteView, HealthView, index, api
from gwells.views.bulk import BulkWellAquiferCorrelation, BulkVerticalAquiferExtents
from gwells.views.admin import *
from gwells.settings.base import get_env_variable

# Creating 2 versions of the app_root. One without and one with trailing slash
# This will allow for any or no additional app_root context to be provided
app_root = settings.APP_CONTEXT_ROOT
if app_root:
    app_root_slash = app_root + '/'
else:
    app_root_slash = app_root


DJANGO_ADMIN_URL = get_env_variable(
    'DJANGO_ADMIN_URL',
    # safe value used for development when DJANGO_ADMIN_URL might not be set
    'admin',
    strict=True
)

def api_path_prefix():
    api_version_url_re = '(?P<version>(v1|v2))'
    return r'api/' + api_version_url_re


urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^' + app_root_slash, include('submissions.urls')),

    url(r'^' + app_root_slash + 'robots\.txt$',
        TemplateView.as_view(template_name='robots.txt',
                             content_type='text/plain'),
        name='robots'),


    url(r'^' + app_root_slash + 'health$', HealthView.health, name='health'),
    url(r'^' +
        app_root_slash +
        'site_admin/survey/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
        SurveyView.as_view(), name='survey'),  # survey details view
    url(r'^' + app_root_slash + 'site_admin/survey',
        SurveyView.as_view(), name='survey'),  # survey api view
    url(r'^' + app_root_slash + 'site_admin',
        AdminView.as_view(),
        name='site_admin'),  # editable list view of surveys and other site admin features

    # API routes
    url(r'^' + app_root_slash + api_path_prefix() + r'/surveys/(?P<survey_guid>[-\w]+)$',
        SurveyUpdateDeleteView.as_view(), name='survey-detail'),
    url(r'^' + app_root_slash + api_path_prefix() + r'/surveys$',
        SurveyListCreateView.as_view(), name='survey-list'),

    url(r'^' + app_root_slash + DJANGO_ADMIN_URL + '/', admin.site.urls),
    url(r'^' + app_root_slash + 'accounts/',
        include('django.contrib.auth.urls')),
    url(r'^' + app_root_slash + api_path_prefix() + r'/keycloak$',
        api.KeycloakConfig.as_view(), name='keycloak'),
    url(r'^' + app_root_slash + api_path_prefix() + r'/config',
        api.GeneralConfig.as_view(), name='configuration'),
    url(r'^' + app_root_slash + api_path_prefix() + r'/gis/insidebc',
        api.InsideBC.as_view(), name='insidebc'),
    url(r'^' + app_root_slash + api_path_prefix() + r'/geocoding/v\d/.+\.places/(?P<query>.+)\.json$',
        api.DataBCGeocoder.as_view(), name='insidebc'),
    url(r'^' + app_root_slash, include('registries.urls')),
    url(r'^' + app_root_slash, include('wells.urls')),
    url(r'^' + app_root_slash, include('aquifers.urls')),

    # Bulk
    url(r'^' + app_root_slash + 'api/v2/bulk/well-aquifer-correlation$',
        never_cache(BulkWellAquiferCorrelation.as_view()), name='bulk-well-aquifer-correlation'),
    url(r'^' + app_root_slash + 'api/v2/bulk/vertical-aquifer-extents$',
        never_cache(BulkVerticalAquiferExtents.as_view()), name='bulk-vertical-aquifer-extents'),

    # Catch all other cases to api/ and 404 them
    re_path(r'' + app_root_slash + api_path_prefix() + '/*', api.api_404, name='api-404'),

    # Catch all other cases and push it to the SPA
    re_path(r'' + app_root_slash + '*', index, name='spa'),
]
