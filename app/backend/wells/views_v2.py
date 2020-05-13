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
import geojson
from geojson import Feature, FeatureCollection
from drf_yasg.utils import swagger_auto_schema

from django.db import transaction
from django.db.models import Func, TextField
from django.db.models.functions import Cast
from django.utils import timezone
from django.http import FileResponse, HttpResponse, StreamingHttpResponse

from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

from gwells.roles import WELLS_VIEWER_ROLE, WELLS_EDIT_ROLE
from gwells.pagination import apiLimitedPagination, APILimitOffsetPagination

from wells.filters import (
    BoundingBoxFilterBackend,
    WellListFilterBackend,
    WellListOrderingFilter,
    GeometryFilterBackend
)
from wells.models import Well
from wells.serializers_v2 import (
    WellLocationSerializerV2,
    WellVerticalAquiferExtentSerializerV2,
    WellListSerializerV2,
    WellListAdminSerializerV2,
    WellExportSerializerV2,
    WellExportAdminSerializerV2,
)
from wells.permissions import WellsEditOrReadOnly
from wells.renderers import WellListCSVRenderer, WellListExcelRenderer

from aquifers.models import (
    Aquifer,
    VerticalAquiferExtent,
    VerticalAquiferExtentsHistory
)
from aquifers.permissions import HasAquiferEditRole


logger = logging.getLogger(__name__)


class WellLocationListV2APIView(ListAPIView):
    """ returns well locations for a given search

        get: returns a list of wells with locations only
    """
    MAX_LOCATION_COUNT = 5000
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

        # check to see if we should filter wells by which ones intersect an aquifer
        intersects_aquifer_id = self.request.query_params.get('intersects_aquifer_id', None)
        if intersects_aquifer_id:
            aquifer = Aquifer.objects.filter(aquifer_id=int(intersects_aquifer_id)).first()

            if not aquifer:
                raise NotFound(f'Unknown aquifer {intersects_aquifer_id}')

            # Simplify polygon and expand it by 1km
            aquifer_geom = aquifer.geom.simplify(40, preserve_topology=True).buffer(1000)

            qs = qs.exclude(geom=None)
            # find all wells that intersect this simplified aquifer polygon
            qs = qs.filter(geom__intersects=aquifer_geom)

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

            qs = qs.exclude(geom=None)

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


class WellAquiferListV2APIView(ListAPIView):
    """
    Returns a list of aquifers with depth information for a well
    """
    permission_classes = (HasAquiferEditRole,)
    ordering = ('start',)
    serializer_class = WellVerticalAquiferExtentSerializerV2
    pagination_class = None

    def get_queryset(self):
        """
        Excludes Aquifer 3D points that relate to unpublished wells for users without edit permissions
        """
        well = self.get_well()

        qs = VerticalAquiferExtent.objects.filter(well=well).select_related('aquifer')

        if not self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = qs.exclude(well__well_publication_status='Unpublished')

        return qs

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        username = self.request.user.profile.username
        timestamp = timezone.now()

        # we expect a list
        if not isinstance(request.data, list):
            raise NotFound()

        # get the well and 404 if it doesn't exist
        well = self.get_well()
        max_depth = float('-inf')
        ids = []
        items = []
        errors = []
        has_errors = False
        for item in request.data: # go through each vertical aquifer extent
            item['well_tag_number'] = well.well_tag_number

            vertical_aquifer_extent = None
            vae_id = item.get('id', None)
            if vae_id: # has an id - then it must be an existing one
                vertical_aquifer_extent = VerticalAquiferExtent.objects.get(pk=vae_id)

            serializer = WellVerticalAquiferExtentSerializerV2(instance=vertical_aquifer_extent,
                                                               data=item)
            serializer_errors = {}
            if serializer.is_valid():
                # add user audit information
                serializer.validated_data['update_user'] = username
                serializer.validated_data['update_date'] = timestamp
                if not vertical_aquifer_extent:
                    serializer.validated_data['create_user'] = username
                    serializer.validated_data['create_date'] = timestamp

                if self.has_changed(vertical_aquifer_extent, serializer.validated_data):
                    vertical_aquifer_extent = serializer.save()

                # keep track existing ids and any newly added IDs
                ids.append(vertical_aquifer_extent.id)
                items.append(serializer.data)
            else:
                serializer_errors = serializer.errors
                has_errors = True

            if vertical_aquifer_extent is not None:
                self.log_history(vertical_aquifer_extent, username, timestamp)

                if vertical_aquifer_extent.start < max_depth:
                    has_errors = True
                    serializer_errors.setdefault('start', []) \
                        .append('Start depth overlaps with another')

                max_depth = vertical_aquifer_extent.end

            errors.append(serializer_errors) # always add to keep the index correct for web app

        # roll back on errors and undo any changes
        if has_errors:
            transaction.set_rollback(True)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # delete any ids not in the POST-ed list
        self.get_queryset().exclude(id__in=ids).delete()

        return Response(items, status=status.HTTP_201_CREATED)

    def get_well(self):
        well_tag_number = int(self.kwargs['well_tag_number'])
        try:
            return Well.objects.get(pk=well_tag_number)
        except:
            raise NotFound(f'Well {well_tag_number} could not be found')

    def has_changed(self, existing_vertical_aquifer_extent, new_data):
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

    def log_history(self, vertical_aquifer_extent, username, timestamp):
        # Whenever a VerticalAquiferExtent is saved - insert a copy of the data into the
        # vertical_aquifer_extents_history table
        VerticalAquiferExtentsHistory.objects.create(
            create_user=username,
            create_date=timestamp,
            update_user=username,
            update_date=timestamp,
            well_tag_number=vertical_aquifer_extent.well_id,
            aquifer_id=vertical_aquifer_extent.aquifer_id,
            geom=vertical_aquifer_extent.geom,
            start=vertical_aquifer_extent.start,
            end=vertical_aquifer_extent.end
        )


class WellListAPIViewV2(ListAPIView):
    """List and create wells

    get: returns a list of wells
    """

    permission_classes = (WellsEditOrReadOnly,)
    model = Well
    pagination_class = APILimitOffsetPagination

    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, WellListOrderingFilter, GeometryFilterBackend)
    ordering = ('well_tag_number',)
    search_fields = ('well_tag_number', 'identification_plate_number',
                     'street_address', 'city', 'owner_full_name')
    default_limit = 10

    def get_serializer_class(self):
        """Returns a different serializer class for admin users."""
        serializer_class = WellListSerializerV2
        if (self.request.user and self.request.user.is_authenticated and
                self.request.user.groups.filter(name=WELLS_VIEWER_ROLE).exists()):
            serializer_class = WellListAdminSerializerV2

        return serializer_class

    def get_queryset(self):
        """ Excludes Unpublished wells for users without edit permissions """
        if self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = Well.objects.all()
        else:
            qs = Well.objects.all().exclude(well_publication_status='Unpublished')

        qs = qs \
            .select_related(
                "bcgs_id",
            ).prefetch_related(
                "water_quality_characteristics",
                "drilling_methods",
                "development_methods"
            )

        return qs


class WellExportListAPIViewV2(ListAPIView):
    """Returns CSV or Excel data for wells.
    """
    permission_classes = (WellsEditOrReadOnly,)
    model = Well

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering = ('well_tag_number',)
    pagination_class = None

    search_fields = ('well_tag_number', 'identification_plate_number',
                     'street_address', 'city', 'owner_full_name')
    renderer_classes = (WellListCSVRenderer, WellListExcelRenderer)
    MAX_EXPORT_COUNT = 5000

    SELECT_RELATED_OPTIONS = [
        'well_class',
        'well_subclass',
        'well_status',
        'licenced_status',
        'land_district',
        'company_of_person_responsible',
        'ground_elevation_method',
        'surface_seal_material',
        'surface_seal_method',
        'liner_material',
        'screen_intake_method',
        'screen_type',
        'screen_material',
        'screen_opening',
        'screen_bottom',
        'well_yield_unit',
        'observation_well_status',
        'coordinate_acquisition_code',
        'bcgs_id',
        'decommission_method',
        'aquifer',
        'aquifer_lithology',
        'yield_estimation_method',
        'well_disinfected_status',
    ]
    PREFETCH_RELATED_OPTIONS = [
        'development_methods',
        'drilling_methods',
        'water_quality_characteristics',
    ]

    def get_fields(self):
        raw_fields = self.request.query_params.get('fields')
        return raw_fields.split(',') if raw_fields else None

    def get_queryset(self):
        """Excludes unpublished wells for users without edit permissions.
        """
        if self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = Well.objects.all()
        else:
            qs = Well.objects.all().exclude(well_publication_status='Unpublished')

        included_fields = self.get_fields()

        if included_fields:
            select_relateds = [
                relation for relation in self.SELECT_RELATED_OPTIONS
                if relation in included_fields
            ]
            prefetches = [
                relation for relation in self.PREFETCH_RELATED_OPTIONS
                if relation in included_fields
            ]

            if select_relateds:
                qs = qs.select_related(*select_relateds)
            if prefetches:
                qs = qs.prefetch_related(*prefetches)
        elif included_fields is None:
            # If no fields are passed, then include everything
            qs = qs.select_related(*self.SELECT_RELATED_OPTIONS)
            qs = qs.prefetch_related(*self.PREFETCH_RELATED_OPTIONS)

        return qs

    def get_serializer_class(self):
        """Returns a different serializer class for admin users."""
        serializer_class = WellExportSerializerV2
        if (self.request.user and self.request.user.is_authenticated and
                self.request.user.groups.filter(name=WELLS_VIEWER_ROLE).exists()):
            serializer_class = WellExportAdminSerializerV2

        return serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()

        fields = self.get_fields()
        if fields:
            context['fields'] = fields

        return context

    def get_renderer_context(self):
        context = super().get_renderer_context()

        fields = self.get_fields()
        if fields:
            context['header'] = fields

        return context

    def batch_iterator(self, queryset, count, batch_size=200):
        """Batch a queryset into chunks of batch_size, and serialize the results

        Allows iterative processing while taking advantage of prefetching many
        to many relations.
        """
        for offset in range(0, count, batch_size):
            end = min(offset + batch_size, count)
            batch = queryset[offset:end]

            serializer = self.get_serializer(batch, many=True)
            for item in serializer.data:
                yield item

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        # return an empty response if there are too many wells to display
        if count > self.MAX_EXPORT_COUNT:
            raise PermissionDenied(
                'Too many wells to export. Please change your search criteria.'
            )
        elif count == 0:
            raise NotFound('No well records could be found.')

        renderer = request.accepted_renderer
        if renderer.format == 'xlsx':
            response_class = FileResponse
        else:
            response_class = StreamingHttpResponse

        context = self.get_renderer_context()
        data_iterator = self.batch_iterator(queryset, count)
        render_result = renderer.render(data_iterator, renderer_context=context)

        response = response_class(render_result, content_type=renderer.media_type)
        response['Content-Disposition'] = 'attachment; filename="search-results.{ext}"'.format(ext=renderer.format)

        return response
