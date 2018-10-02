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

from django.shortcuts import render
from django_filters import rest_framework as filters
from django.views.generic import TemplateView

from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from aquifers.models import Aquifer
from aquifers.serializers import AquiferSerializer

class AquiferRetrieveAPIView(RetrieveAPIView):
    """List aquifers
    get: return details of aquifers
    """

    queryset = Aquifer.objects.all()
    lookup_field = 'aquifer_id'
    serializer_class = AquiferSerializer

class AquiferListAPIView(ListAPIView):
    """List aquifers
    get: return a list of aquifers
    """

    queryset = Aquifer.objects.all()
    serializer_class = AquiferSerializer
    filter_backends = (filters.DjangoFilterBackend,SearchFilter)
    filter_fields = ('aquifer_id',)
    search_fields = ('aquifer_name',)

class AquiferHomeView(TemplateView):
    """Loads the html file containing the Aquifer web app"""
    template_name = 'aquifers/aquifers.html'