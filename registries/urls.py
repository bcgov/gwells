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
from rest_framework_swagger.views import get_swagger_view
from . import views

urlpatterns = [
    url(r'^drillers/(?P<org_guid>[-\w]+)', views.APIDrillerRetrieveUpdateDestroyView.as_view(), name='driller-detail'),
    url(r'^drillers/$', views.APIDrillerListCreateView.as_view(), name='driller-list'),
    url(r'^docs/$', get_swagger_view(title='GWELLS Driller registry'), name='api-docs'),
    url(r'^$', views.index, name='index'),
]
