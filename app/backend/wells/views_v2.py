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
import logging

from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

from gwells.roles import WELLS_EDIT_ROLE
from gwells.pagination import apiLimitedPagination

from wells.filters import (
    BoundingBoxFilterBackend,
    WellListFilterBackend,
    WellListOrderingFilter,
)
from wells.models import Well
from wells.serializers_v2 import WellLocationSerializerV2
from wells.permissions import WellsEditOrReadOnly


logger = logging.getLogger(__name__)


class WellLocationListV2APIView(ListAPIView):
    """ returns well locations for a given search

        get: returns a list of wells with locations only
    """
    permission_classes = (WellsEditOrReadOnly,)
    model = Well
    pagination_class = apiLimitedPagination(5000)

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, WellListOrderingFilter)
    ordering = ('well_tag_number',)

    search_fields = ('well_tag_number', 'identification_plate_number',
                     'street_address', 'city', 'owner_full_name', 'ems')

    def get_serializer_class(self):
        return WellLocationSerializerV2

    def get_queryset(self):
        """ Excludes Unpublished wells for users without edit permissions """
        if self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = Well.objects.all()
        else:
            qs = Well.objects.all().exclude(well_publication_status='Unpublished')

        return qs
