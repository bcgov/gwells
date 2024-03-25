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
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import os
from registries import permissions
from . import views
from . import views_v2
from gwells.urls import api_path_prefix
LOCAL = os.environ.get('LOCAL', False)
API_URL = 'http://localhost:8000/gwells/' if LOCAL else 'https://apps.nrs.gov.bc.ca/gwells/'
schema_view = get_schema_view(
    openapi.Info(
        title="Groundwater Wells, Aquifers and Registry API",
        default_version='v1',
        description=str("The groundwater wells, aquifers and registry API contains information "
                        "related to groundwater wells and aquifers as well as a register of qualified "
                        "well drillers and well pump installers registered to operate in B.C."),
        terms_of_service="http://www2.gov.bc.ca/gov/content?id=D1EE0A405E584363B205CD4353E02C88",
        contact=openapi.Contact(email="groundwater@gov.bc.ca"),
        license=openapi.License(name="Open Government License - British Columbia",
                                url="https://www2.gov.bc.ca/gov/content?id=A519A56BC2BF44E4A008B33FCF527F61"),
    ),
    url=API_URL,
    public=LOCAL,
    permission_classes=(permissions.RegistriesEditOrReadOnly,)
)

urlpatterns = [

    # Organization note endpoints
    url(api_path_prefix() + r'/organizations/(?P<org_guid>[-\w]+)/notes$',
        views.OrganizationNoteListView.as_view(), name='org-note-list'),
    url(api_path_prefix() + r'/organizations/(?P<org_guid>[-\w]+)/notes/(?P<note_guid>[-\w]+)$',
        views.OrganizationNoteDetailView.as_view(), name='org-note-detail'),

    # Organization endpoints
    url(api_path_prefix() + r'/organizations/names$',
        never_cache(views.OrganizationNameListView.as_view()),
        name='organization-names'),
    url(api_path_prefix() + r'/organizations/(?P<org_guid>[-\w]+)/history$',
        never_cache(views.OrganizationHistory.as_view()), name='organization-history'),
    url(api_path_prefix() + r'/organizations/(?P<org_guid>[-\w]+)$',
        never_cache(views.OrganizationDetailView.as_view()),
        name='organization-detail'),
    url(api_path_prefix() + r'/organizations$',
        never_cache(views.OrganizationListView.as_view()),
        name='organization-list'),


    url(r'api/v2/drillers/csv$',
        never_cache(views_v2.CSVExportV2.as_view()),
        name='drillers-list-csv'
        ),
    url(r'api/v2/drillers/xlsx$',
        never_cache(views_v2.XLSXExportV2.as_view()),
        name='drillers-list-xlsx'
        ),

    # Document Uploading (driller records)
    url(api_path_prefix() + r'/drillers/(?P<person_guid>[-\w]+)/presigned_put_url$',
        never_cache(views.PreSignedDocumentKey.as_view()), name='drillers-pre-signed-url'),

    # Document Deleting (driller records)
    url(api_path_prefix() + r'/drillers/(?P<person_guid>[-\w]+)/delete_document$',
        never_cache(views.DeleteDrillerDocument.as_view()), name='driller-delete-document'),

    url(api_path_prefix() + r'/drillers/(?P<person_guid>[-\w]+)/files$',
        never_cache(views.ListFiles.as_view()), name='drillers-file-list'),

    # Person note endpoints
    url(api_path_prefix() + r'/drillers/(?P<person_guid>[-\w]+)/notes$',
        never_cache(views.PersonNoteListView.as_view()), name='person-note-list'),
    url(api_path_prefix() + r'/drillers/(?P<person_guid>[-\w]+)/notes/(?P<note_guid>[-\w]+)$',
        views.PersonNoteDetailView.as_view(), name='person-note-detail'),

    # Person endpoints (drillers, well installers, and other instances of Person model)
    # TODO: There's some confusion between drillers and persons. Sometimes we're looking only for drillers,
    # sometimes we're actually looking for people (pump installers, drillers etc.)
    url(api_path_prefix() + r'/drillers/names$',
        never_cache(views.PersonNameSearch.as_view()), name='person-search'),
    url(api_path_prefix() + r'/drillers/options$',
        views.PersonOptionsView.as_view(), name='person-options'),
    url(api_path_prefix() + r'/drillers/(?P<person_guid>[-\w]+)/history$',
        never_cache(views.PersonHistory.as_view()), name='person-history'),
    url(api_path_prefix() + r'/drillers/(?P<person_guid>[-\w]+)$',
        never_cache(views.PersonDetailView.as_view()),
        name='person-detail'),
    url(api_path_prefix() + r'/drillers$',
        never_cache(views.PersonListView.as_view()), name='person-list'),

    # Registration endpoints (a person may register as a driller or well pump installer)
    url(api_path_prefix() + r'/registrations/(?P<register_guid>[-\w]+)$',
        never_cache(views.RegistrationDetailView.as_view()),
        name='register-detail'),
    url(api_path_prefix() + r'/registrations$',
        never_cache(views.RegistrationListView.as_view()), name='register-list'),

    # Applications (applications to be qualified for a drilling activity)
    url(api_path_prefix() + r'/applications/(?P<application_guid>[-\w]+)$',
        never_cache(views.ApplicationDetailView.as_view()),
        name='application-detail'),
    url(api_path_prefix() + r'/applications$', never_cache(views.ApplicationListView.as_view()),
        name='application-list'),

    # List of cities that currently have registered drillers, pump installers etc.
    url(api_path_prefix() + r'/cities/drillers$',
        never_cache(views.CitiesListView.as_view()),
        {'activity': 'drill'},
        name='city-list-drillers'),
    url(api_path_prefix() + r'/cities/installers$',
        never_cache(views.CitiesListView.as_view()),
        {'activity': 'install'},
        name='city-list-installers'),

    # Swagger documentation endpoint
    url(r'^api/$', schema_view.with_ui('swagger', cache_timeout=None), name='api-docs'),

]
