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

from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView

from gwells.documents import MinioClient

from aquifers import models
from aquifers import serializers
from aquifers.permissions import HasAquiferEditRoleOrReadOnly


class AquiferRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """List aquifers
    get: return details of aquifers
    patch: update aquifer
    """

    permission_classes = (HasAquiferEditRoleOrReadOnly,)
    queryset = models.Aquifer.objects.all()
    lookup_field = 'aquifer_id'
    serializer_class = serializers.AquiferSerializer


class AquiferListCreateAPIView(ListCreateAPIView):
    """List aquifers
    get: return a list of aquifers
    post: create an aquifer
    """

    permission_classes = (HasAquiferEditRoleOrReadOnly,)
    queryset = models.Aquifer.objects.all()
    serializer_class = serializers.AquiferSerializer
    filter_backends = (filters.DjangoFilterBackend,
                       OrderingFilter, SearchFilter)
    filter_fields = ('aquifer_id',)
    search_fields = ('aquifer_name',)
    ordering_fields = '__all__'
    ordering = ('aquifer_id',)


class AquiferMaterialListAPIView(ListAPIView):
    """List aquifer materials codes
    get: return a list of aquifer material codes
    """

    queryset = models.AquiferMaterial.objects.all()
    serializer_class = serializers.AquiferMaterialSerializer


class QualityConcernListAPIView(ListAPIView):
    """List aquifer materials codes
    get: return a list of quality concern codes
    """

    queryset = models.QualityConcern.objects.all()
    serializer_class = serializers.QualityConcernSerializer


class AquiferVulnerabilityListAPIView(ListAPIView):
    """List aquifer vulnerability codes
    get: return a list of aquifer vulnerability codes
    """

    queryset = models.AquiferVulnerabilityCode.objects.all()
    serializer_class = serializers.AquiferVulnerabilitySerializer


class AquiferSubtypeListAPIView(ListAPIView):
    """List aquifer subtypes codes
    get: return a list of aquifer subtype codes
    """

    queryset = models.AquiferSubtype.objects.all()
    serializer_class = serializers.AquiferSubtypeSerializer


class AquiferProductivityListAPIView(ListAPIView):
    """List aquifer productivity codes
    get: return a list of aquifer productivity codes
    """

    queryset = models.AquiferProductivity.objects.all()
    serializer_class = serializers.AquiferProductivitySerializer


class AquiferDemandListAPIView(ListAPIView):
    """List aquifer demand codes
    get: return a list of aquifer demand codes
    """

    queryset = models.AquiferDemand.objects.all()
    serializer_class = serializers.AquiferDemandSerializer


class WaterUseListAPIView(ListAPIView):
    """List Water Use Codes
    get: return a list of water use codes
    """

    queryset = models.WaterUse.objects.all()
    serializer_class = serializers.WaterUseSerializer


class AquiferHomeView(TemplateView):
    """Loads the html file containing the Aquifer web app"""
    template_name = 'aquifers/aquifers.html'


class ListFiles(APIView):
    """
    List documents associated with an aquifer

    get: list files found for the aquifer identified in the uri
    """

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, aquifer_id):

        client = MinioClient(
            request=request, disable_private=True)

        documents = client.get_documents(
            int(aquifer_id), resource="aquifer", include_private=False)

        return Response(documents)
