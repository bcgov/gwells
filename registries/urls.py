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
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from registries import permissions
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Well Driller and Pump Installer Registry API",
        default_version='v1',
        description=str("The Well Driller and Pump Installer Registry is a database of qualified well "
                        "drillers and pump installers registered to operate in British Columbia."),
        terms_of_service="http://www2.gov.bc.ca/gov/content?id=D1EE0A405E584363B205CD4353E02C88",
        contact=openapi.Contact(email="groundwater@gov.bc.ca"),
        license=openapi.License(name="Open Government License - British Columbia",
                                url="https://www2.gov.bc.ca/gov/content?id=A519A56BC2BF44E4A008B33FCF527F61"),
    ),
    public=False,
    permission_classes=(permissions.IsAdminOrReadOnly,),
)

# wrap obtain_jwt_token view in a function that excludes it from swagger documentation.
obtain_jwt_token_noswagger = swagger_auto_schema(
    method='post', auto_schema=None)(obtain_jwt_token)

urlpatterns = [
    url(r'^api/v1/organizations/names/$',
        views.OrganizationNameListView.as_view(),
        name='organization-names'),
    url(r'^api/v1/organizations/(?P<org_guid>[-\w]+)/$',
        views.OrganizationDetailView.as_view(),
        name='organization-detail'),
    url(r'^api/v1/organizations/$',
        views.OrganizationListView.as_view(),
        name='organization-list'),

    # Person note endpoints
    url(r'^api/v1/drillers/(?P<person_guid>[-\w]+)/notes/$',
        views.PersonNoteListView.as_view(), name='person-note-list'),
    url(r'^api/v1/drillers/(?P<person_guid>[-\w]+)/notes/(?P<note_guid>[-\w]+)/$',
        views.PersonNoteDetailView.as_view(), name='person-note-detail'),

    # Person resource endpoints (drillers, well installers, and other instances of Person model)
    url(r'^api/v1/drillers/(?P<person_guid>[-\w]+)/$',
        views.PersonDetailView.as_view(),
        name='person-detail'),
    url(r'^api/v1/drillers/$', views.PersonListView.as_view(), name='person-list'),

    # Registration endpoints (a person may register as a driller or well pump installer)
    url(r'api/v1/registrations/(?P<register_guid>[-\w]+)/$',
        views.RegistrationDetailView.as_view(),
        name='register-detail'),
    url(r'api/v1/registrations/',
        views.RegistrationListView.as_view(), name='register-list'),

    # Applications (applications to be qualified for a drilling activity)
    url(r'api/v1/applications/(?P<application_guid>[-\w]+)/$',
        views.ApplicationDetailView.as_view(),
        name='application-detail'),
    url(r'api/v1/applications/', views.ApplicationListView.as_view(),
        name='application-list'),

    # List of cities that currently have registered drillers, pump installers etc.
    url(r'^api/v1/cities/drillers/$',
        views.CitiesListView.as_view(),
        {'activity': 'drill'},
        name='city-list-drillers'),
    url(r'^api/v1/cities/installers/$',
        views.CitiesListView.as_view(),
        {'activity': 'install'},
        name='city-list-installers'),

    # Temporary development login endpoint
    url(r'^api/v1/api-token-auth/', obtain_jwt_token_noswagger, name='get-token'),

    # Swagger documentation endpoint
    url(r'^api/', schema_view.with_ui('swagger',
                                      cache_timeout=None), name='api-docs'),

    # Deprecated old URL endpoints. NOTE: These may be linked from API catalogue

    # Organization resource endpoints
    url(r'^registries/api/v1/organizations/(?P<org_guid>[-\w]+)/$',
        views.OrganizationDetailView.as_view(), name='organization-detail'),
    url(r'^registries/api/v1/organizations/$',
        views.OrganizationListView.as_view(),
        name='organization-list'),

    # Person resource endpoints (drillers, well installers, and other instances of Person model)
    url(r'^registries/api/v1/drillers/(?P<person_guid>[-\w]+)/$',
        views.PersonDetailView.as_view(),
        name='person-detail'),
    url(r'^registries/api/v1/drillers/$',
        views.PersonListView.as_view(),
        name='person-list'),

    # List of cities that currently have registered drillers, pump installers etc.
    url(r'^registries/api/v1/cities/drillers/$',
        views.CitiesListView.as_view(),
        {'activity': 'drill'},
        name='city-list-drillers'),
    url(r'^registries/api/v1/cities/installers/$',
        views.CitiesListView.as_view(),
        {'activity': 'install'},
        name='city-list-installers'),

    # Temporary development login endpoint
    url(r'^registries/api/v1/api-token-auth/',
        obtain_jwt_token_noswagger, name='get-token'),

    # Swagger documentation endpoint
    url(r'^registries/api/', schema_view.with_ui('swagger',
                                                 cache_timeout=None), name='api-docs'),

    # Deprecated API docs link
    url(r'^registries/docs/$', schema_view.with_ui('swagger',
                                                   cache_timeout=None), name='api-docs-old'),

    # Registries frontend webapp loader (html page that contains header, footer, and a SPA in between)
    url(r'^registries/', views.RegistriesIndexView.as_view(), name='registries-home'),
]
