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

import geojson
from geojson import Feature, FeatureCollection, Point

import logging

from reversion.views import RevisionMixin

from django.db import transaction
from django.db.models import Func, TextField
from django.db.models.functions import Cast
from django.http import HttpResponse, Http404
from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from gwells.roles import WELLS_EDIT_ROLE
from gwells.pagination import apiLimitedPagination

from wells.filters import (
    BoundingBoxFilterBackend,
    WellListFilterBackend,
    WellListOrderingFilter,
    GeometryFilterBackend
)
from wells.models import Well
from wells.serializers_v2 import WellLocationSerializerV2, WellVerticalAquiferExtentSerializerV2
from wells.permissions import WellsEditOrReadOnly

from aquifers.models.vertical_aquifer_extents import VerticalAquiferExtent
from aquifers.permissions import HasAquiferEditRole


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
                       filters.SearchFilter, WellListOrderingFilter, GeometryFilterBackend)
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

    def get(self, request, **kwargs):
        """
        Returns geojson if requested, otherwise handles request as normal.
        """

        geojson_requested = self.request.query_params.get('geojson') == 'true'

        # if geojson requested, create a query that returns each well's geometry as GeoJSON
        # so that we can easily create a FeatureCollection.
        # This might be more performant in the database using json_agg and ST_AsGeoJSON
        # vs creating geojson Features here in Python.
        if geojson_requested:
            qs = self.get_queryset()
            locations = self.filter_queryset(qs)
            count = locations.count()
            # return an empty response if there are too many wells to display
            if count > self.MAX_LOCATION_COUNT:
                raise PermissionDenied('Too many wells to display on map. '
                                       'Please zoom in or change your search criteria.')

            locations = locations.annotate(
                geometry=Cast(Func('geom', function='ST_AsGeoJSON'), output_field=TextField())
            ).values("well_tag_number", "identification_plate_number", "geometry",
                     "street_address", "city")

            # create a group of features
            features = [
                Feature(geometry=geojson.loads(x.pop('geometry')), properties=dict(x)) for x in locations
            ]

            return HttpResponse(geojson.dumps(FeatureCollection(features)))

        return super().get(request)



class WellAquiferListV2APIView(RevisionMixin, ListAPIView):
    """
    Returns a list of aquifers with depth information for a well
    """
    permission_classes = (HasAquiferEditRole,)
    # model = VerticalAquiferExtent
    ordering = ('start',)
    serializer_class = WellVerticalAquiferExtentSerializerV2
    pagination_class = None

    def get_queryset(self):
        """
        Excludes Aquifer 3D points that relate to unpublished wells for users without edit permissions
        """
        well = self.getWell()

        qs = VerticalAquiferExtent.objects.filter(well=well)

        if not self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = qs.exclude(well__well_publication_status='Unpublished')

        return qs

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    @transaction.atomic
    def post(self, request, well_tag_number, *args, **kwargs):
        username = self.request.user.profile.username
        timestamp = timezone.now()

        serializer_class = self.get_serializer_class()

        # we expect a list
        if not isinstance(request.data, list):
            raise Http404()

        # get the well and 404 if it doesn't exist
        well = self.getWell()
        ids = []
        items = []
        errors = []
        hasErrors = False
        for item in request.data: # go through each vertical aquifer extent
            item['well_id'] = well.well_tag_number

            vertical_aquifer_extent = None
            vertical_aquifer_extent = item.get('id', None)
            if vertical_aquifer_extent: # has an id - then it must be an existing one
                vertical_aquifer_extent = VerticalAquiferExtent.objects.get(pk=vertical_aquifer_extent)

            serializer = WellVerticalAquiferExtentSerializerV2(instance=vertical_aquifer_extent, data=item)
            if serializer.is_valid():
                # add user audit information
                serializer.validated_data['update_user'] = username
                serializer.validated_data['update_date'] = timestamp
                if not vertical_aquifer_extent:
                    serializer.validated_data['create_user'] = username
                    serializer.validated_data['create_date'] = timestamp

                if self.hasChanged(vertical_aquifer_extent, serializer.validated_data):
                    vertical_aquifer_extent = serializer.save()

                ids.append(vertical_aquifer_extent.id) # keep track existing ids and any newly added IDs
                items.append(serializer.data)
            else:
                hasErrors = True
            errors.append(serializer.errors) # always add to keep the index correct for web app

        # roll back on errors and undo any changes
        if hasErrors:
            transaction.set_rollback(True)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # delete any ids not in the POST-ed list
        self.get_queryset().exclude(id__in=ids).delete()

        return Response(items, status=status.HTTP_201_CREATED)

    def getWell(self):
        well_tag_number = int(self.kwargs['well_tag_number'])
        try:
            return Well.objects.get(pk=well_tag_number)
        except:
            raise NotFound(f'Well {well_tag_number} could not be found')

    def hasChanged(self, existing_vertical_aquifer_extent, new_data):
        if existing_vertical_aquifer_extent is None:
            return True

        if existing_vertical_aquifer_extent.start != new_data['start']:
            return True

        if existing_vertical_aquifer_extent.end != new_data['end']:
            return True

        if existing_vertical_aquifer_extent.aquifer_id != new_data['aquifer_id']:
            return True

        if existing_vertical_aquifer_extent.geom and new_data['geom']:
            if existing_vertical_aquifer_extent.geom.x != new_data['geom'].x:
                return True

            if existing_vertical_aquifer_extent.geom.y != new_data['geom'].y:
                return True
        else:
            return True

        return False
