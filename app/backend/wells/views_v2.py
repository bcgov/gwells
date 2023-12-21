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

from django.db import transaction
from django.utils import timezone
from django.http import FileResponse, StreamingHttpResponse
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSException, GEOSGeometry
from django.contrib.gis.gdal import GDALException
from django.db.models.functions import Cast
from django.db.models import FloatField, Q, Case, When, F, Value, DateField

from rest_framework import status, filters
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from gwells.roles import WELLS_VIEWER_ROLE, WELLS_EDIT_ROLE
from gwells.pagination import apiLimitedPagination, APILimitOffsetPagination
from gwells.geojson import GeoJSONIterator

from wells.filters import (
    BoundingBoxFilterBackend,
    WellListFilterBackend,
    WellListOrderingFilter,
    GeometryFilterBackend,
    RadiusFilterBackend
)
from wells.models import Well, WellAttachment, \
  WELL_STATUS_CODE_ALTERATION, WELL_STATUS_CODE_CONSTRUCTION, WELL_STATUS_CODE_DECOMMISSION
from wells.serializers_v2 import (
    WellLocationSerializerV2,
    WellVerticalAquiferExtentSerializerV2,
    WellListSerializerV2,
    WellListAdminSerializerV2,
    WellExportSerializerV2,
    WellExportAdminSerializerV2,
    WellSubsurfaceSerializer,
    WellDetailSerializer,
    MislocatedWellsSerializer,
    CrossReferencingSerializer,
    RecordComplianceSerializer
)
from wells.permissions import WellsEditOrReadOnly
from wells.renderers import WellListCSVRenderer, WellListExcelRenderer

from aquifers.models import (
    Aquifer,
    VerticalAquiferExtent,
    VerticalAquiferExtentsHistory
)
from aquifers.permissions import HasAquiferEditRole
from wells.views import WellDetail as WellDetailV1
from wells.constants import MAX_EXPORT_COUNT, MAX_LOCATION_COUNT

logger = logging.getLogger(__name__)


class WellLocationListV2APIView(ListAPIView):
    """ returns well locations for a given search

        get: returns a list of wells with locations only
    """
    swagger_schema = None
    permission_classes = (WellsEditOrReadOnly,)
    model = Well
    pagination_class = apiLimitedPagination(MAX_LOCATION_COUNT)

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, WellListOrderingFilter, GeometryFilterBackend)
    ordering = ('well_tag_number',)

    search_fields = ('well_tag_number', 'identification_plate_number',
                     'street_address', 'city', 'owner_full_name', 'ems')

    TOO_MANY_ERROR_MESSAGE = "Too many wells to display on map. Please zoom in or change your search criteria."

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

            if not aquifer.geom:
                # if the aquifer has no/null geometry, it might be an aquifer
                # that the business area has created but has not delineated an area
                # for (for example, the special "holding" aquifer 1143).
                qs = qs.none()
                
            else:
                # Find wells that intersect this simplified aquifer polygon (excluding wells
                # with null geom)
                qs = qs.exclude(geom=None)
                qs = qs.filter(geom__intersects=aquifer.geom)

        well_tag_numbers = self.request.query_params.get('well_tag_numbers', '')
        if well_tag_numbers:
            well_tag_numbers = well_tag_numbers.split(',')
            qs = qs.filter(well_tag_number__in=well_tag_numbers)

        return qs

    def get(self, request, *args, **kwargs):
        """
        Returns geojson if requested, otherwise handles request as normal.
        """

        geojson_requested = self.request.query_params.get('geojson') == 'true'

        # if geojson requested, create a query that returns each well's geometry as GeoJSON
        # so that we can easily create a FeatureCollection.
        # This might be more performant in the database using json_agg and ST_AsGeoJSON
        # vs creating geojson Features here in Python.
        if geojson_requested:
            return self.geoJSONResponse()

        return super().get(request)

    def geoJSONResponse(self):
        """
        Returns a streaming GeoJSON HTTP response of the searched wells
        """
        qs = self.get_queryset()
        qs = qs.exclude(geom=None)

        fields = [
            "geom",
            "well_tag_number",
            "identification_plate_number",
            "street_address",
            "city",
            "artesian_conditions",
            "storativity",
            "transmissivity",
            "hydraulic_conductivity"
        ]

        locations = self.filter_queryset(qs)

        # If the user can edit wells then we can add the `is_published` property to the response
        if self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            locations = locations.extra(select={'is_published': "well_publication_status_code = 'Published'"})
            fields.append("is_published")

        locations = locations.values(*fields)
        locations = list(locations[:MAX_LOCATION_COUNT + 1])

        # return a 403 response if there are too many wells to display
        if len(locations) > MAX_LOCATION_COUNT:
            raise PermissionDenied(self.TOO_MANY_ERROR_MESSAGE)

        # turn the list of locations into a generator so the GeoJSONIterator can use it
        locations_iter = (location for location in locations)
        iterator = GeoJSONIterator(locations_iter)

        return StreamingHttpResponse(iterator, content_type="application/json")


class WellAquiferListV2APIView(ListAPIView):
    """
    Returns a list of aquifers with depth information for a well
    """
    swagger_schema = None
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

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
        for item in request.data:  # go through each vertical aquifer extent
            item['well_tag_number'] = well.well_tag_number

            vertical_aquifer_extent = None
            vae_id = item.get('id', None)
            if vae_id:  # has an id - then it must be an existing one
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

            errors.append(serializer_errors)  # always add to keep the index correct for web app

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
        except Exception:
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

    swagger_schema = None
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
    swagger_schema = None
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

    SELECT_RELATED_OPTIONS = [
        'well_class',
        'well_subclass',
        'well_status',
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        # return an empty response if there are too many wells to display
        if count > MAX_EXPORT_COUNT:
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


class WellSubsurface(ListAPIView):
    """ Returns well subsurface info within a gemoetry or a list of wells """
    """ This replaces WellScreen with the additional aquifer and lithology info"""

    model = Well
    serializer_class = WellSubsurfaceSerializer
    filter_backends = (GeometryFilterBackend, RadiusFilterBackend)
    swagger_schema = None

    def get_queryset(self):
        qs = Well.objects.all() \
            .select_related('intended_water_use', 'aquifer', 'aquifer__material',
                            'aquifer__subtype') \
            .prefetch_related('screen_set')

        if not self.request.user.groups.filter(name=WELLS_EDIT_ROLE).exists():
            qs = qs.exclude(well_publication_status='Unpublished')

        # check if a point was supplied (note: actual filtering will be by
        # the filter_backends classes).  If so, add distances from the point.
        point = self.request.query_params.get('point', None)
        srid = self.request.query_params.get('srid', 4326)
        radius = self.request.query_params.get('radius', None)
        if point and radius:
            try:
                shape = GEOSGeometry(point, srid=int(srid))
                radius = float(radius)
                assert shape.geom_type == 'Point'
            except (ValueError, AssertionError, GDALException, GEOSException):
                raise ValidationError({
                    'point': 'Invalid point geometry. Use geojson geometry or WKT. Example: {"type": "Point", "coordinates": [-123,49]}'
                })
            else:
                qs = qs.annotate(
                    distance=Cast(Distance('geom', shape), output_field=FloatField())
                ).order_by('distance')

        # can also supply a comma separated list of wells
        wells = self.request.query_params.get('wells', None)

        if wells:
            wells = wells.split(',')

            for w in wells:
                if not w.isnumeric():
                    raise ValidationError(detail='Invalid well')

            wells = map(int, wells)
            qs = qs.filter(well_tag_number__in=wells)

        return qs


class WellDetail(WellDetailV1):
    """
    Return well detail.
    This view is open to all, and has no permissions.
    """
    serializer_class = WellDetailSerializer


class MislocatedWellsListView(ListAPIView):
    """
    API view to retrieve mislocated wells.
    """
    serializer_class = MislocatedWellsSerializer

    def get_queryset(self):
        """
        This view should return a list of all mislocated wells
        for the currently authenticated user.
        """
        return Well.objects.filter(Q(geom__isnull=True) | Q(incorrect_location_flag=True))

    def get(self, request, *args, **kwargs):
        """
        Optionally restricts the returned mislocated wells to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.get_queryset()

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    

class RecordComplianceListView(ListAPIView):
    serializer_class = RecordComplianceSerializer

    swagger_schema = None
    permission_classes = (WellsEditOrReadOnly,)
    model = Well
    pagination_class = APILimitOffsetPagination

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, WellListOrderingFilter, GeometryFilterBackend)
    ordering = ('well_tag_number',)

    def get_queryset(self):
        """
        Retrieves wells that are missing information in any of the specified fields.
        """
        queryset = Well.objects.all()

        queryset = Well.objects.select_related('well_status').annotate(
            work_start_date=Case(
                When(well_status__well_status_code=WELL_STATUS_CODE_CONSTRUCTION, then=F('construction_start_date')),
                When(well_status__well_status_code=WELL_STATUS_CODE_ALTERATION, then=F('alteration_start_date')),
                When(well_status__well_status_code=WELL_STATUS_CODE_DECOMMISSION, then=F('decommission_start_date')),
                default=Value(None),
                output_field=DateField()
            ),
            work_end_date=Case(
                When(well_status__well_status_code=WELL_STATUS_CODE_CONSTRUCTION, then=F('construction_end_date')),
                When(well_status__well_status_code=WELL_STATUS_CODE_ALTERATION, then=F('alteration_end_date')),
                When(well_status__well_status_code=WELL_STATUS_CODE_DECOMMISSION, then=F('decommission_end_date')),
                default=Value(None),
                output_field=DateField()
            )
        )

        # Filtering for records missing any of the specified fields
        missing_info_filter = (
            Q(well_tag_number__isnull=True) |
            Q(identification_plate_number__isnull=True) |
            Q(well_class__isnull=True) |
            Q(geom__isnull=True) | # for latitude and longitude
            Q(finished_well_depth__isnull=True) |
            Q(surface_seal_depth__isnull=True) |
            Q(surface_seal_thickness__isnull=True) |
            Q(aquifer_lithology__isnull=True) |
            Q(well_status__isnull=True) |
            Q(work_start_date__isnull=True) |
            Q(work_end_date__isnull=True) |
            Q(person_responsible__isnull=True) |
            Q(company_of_person_responsible__isnull=True) |
            Q(create_date__isnull=True) |
            Q(create_user__isnull=True)
            # Q(natural_resource_region__isnull=True) |
            # Q(internal_comments__isnull=True)
        )

        queryset = queryset.filter(missing_info_filter)

        # Additional filtering based on query parameters
        work_start_date = self.request.query_params.get('work_start_date')
        work_end_date = self.request.query_params.get('work_end_date')

        if work_start_date:
            queryset = queryset.filter(work_start_date__gte=work_start_date)
        if work_end_date:
            queryset = queryset.filter(work_end_date__lte=work_end_date)

        return queryset
    

class CrossReferencingListView(ListAPIView):
    serializer_class = CrossReferencingSerializer

    swagger_schema = None
    permission_classes = (WellsEditOrReadOnly,)
    model = Well
    pagination_class = APILimitOffsetPagination

    # Allow searching on name fields, names of related companies, etc.
    filter_backends = (WellListFilterBackend, BoundingBoxFilterBackend,
                       filters.SearchFilter, WellListOrderingFilter, GeometryFilterBackend)
    ordering = ('well_tag_number',)

    def get_queryset(self):
        """
        Optionally restricts the returned wells to those that have certain keywords like 'x-ref'd' or 'cross-ref'
        in their internal_comments.
        """
        queryset = Well.objects.all()

        queryset = Well.objects.select_related('well_status').annotate(
            work_start_date=Case(
                When(well_status__well_status_code=WELL_STATUS_CODE_CONSTRUCTION, then=F('construction_start_date')),
                When(well_status__well_status_code=WELL_STATUS_CODE_ALTERATION, then=F('alteration_start_date')),
                When(well_status__well_status_code=WELL_STATUS_CODE_DECOMMISSION, then=F('decommission_start_date')),
                default=Value(None),
                output_field=DateField()
            ),
            work_end_date=Case(
                When(well_status__well_status_code=WELL_STATUS_CODE_CONSTRUCTION, then=F('construction_end_date')),
                When(well_status__well_status_code=WELL_STATUS_CODE_ALTERATION, then=F('alteration_end_date')),
                When(well_status__well_status_code=WELL_STATUS_CODE_DECOMMISSION, then=F('decommission_end_date')),
                default=Value(None),
                output_field=DateField()
            )
        )

        search_terms = ["x-ref'd", "x-ref", "cross-ref"]
        
        # Build a Q object for the search terms
        comments_query = Q()
        for term in search_terms:
            comments_query |= Q(internal_comments__icontains=term)

        # Filter the queryset based on the search terms
        queryset = queryset.filter(comments_query)

        return queryset