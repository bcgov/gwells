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
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view
from . import views

urlpatterns = [
    # Organization resource endpoints
    url(r'^api/v1/organizations/(?P<org_guid>[-\w]+)/$', views.APIOrganizationRetrieveUpdateDestroyView.as_view(), name='organization-detail'),
    url(r'^api/v1/organizations/$', views.APIOrganizationListCreateView.as_view(), name='organization-list'),

    # Person resource endpoints (drillers, well installers, and other instances of Person model)
    url(r'^api/v1/drillers/(?P<person_guid>[-\w]+)/$', views.APIPersonRetrieveUpdateDestroyView.as_view(), name='person-detail'),
    url(r'^api/v1/drillers/$', views.APIPersonListCreateView.as_view(), name='person-list'),

    # List of cities that currently have registered drillers, pump installers etc.
    url(r'^api/v1/cities/drillers/$', views.APICitiesList.as_view(), {'activity':'drill'}, name='city-list-drillers'),
    url(r'^api/v1/cities/installers/$', views.APICitiesList.as_view(), {'activity': 'install'}, name='city-list-installers'),

    # Temporary JWT Auth endpoint
    url(r'^api/v1/api-token-auth/', obtain_jwt_token, name='get-token'),

    # Swagger documentation endpoint
    url(r'^api/v1/$', get_swagger_view(title='GWELLS Driller registry'), name='api-docs'),

    # Deprecated API docs link
    url(r'^docs/$', get_swagger_view(title='GWELLS Driller registry'), name='api-docs'),

    # Registries frontend webapp loader (html page that contains header, footer, and a SPA in between)
    url(r'^$', views.RegistriesIndexView.as_view(), name='registries-home'),

    # RegistriesApplication resource endpoints (applications from individuals to be registered as a driller, well installer etc.)
    # url(r'^applications/(?P<application_guid>[-\w]+)/$', views.APIApplicationRetrieveUpdateDestroyView.as_view(), name='application-detail'),
    # url(r'^applications/$', views.APIApplicationListCreateView.as_view(), name='application-list'),
]
