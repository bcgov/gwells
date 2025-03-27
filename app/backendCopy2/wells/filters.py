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
import json
import logging
from collections import OrderedDict
from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import FieldDoesNotExist
from django.db import connection
from django.contrib.gis.db import models
from django.http import HttpRequest, QueryDict
from django.contrib.gis.geos import GEOSException, Polygon, GEOSGeometry, Point
from django.contrib.gis.gdal import GDALException
from django.contrib.gis.db.models.functions import Transform
from django.contrib.gis.measure import D
from django.db.models import Max, Min, Q, QuerySet, Subquery, OuterRef, \
  Case, F, DateField, When
from django_filters import rest_framework as filters
from django_filters.widgets import BooleanWidget
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.request import clone_request
from django.db.models.functions import Coalesce

from gwells.roles import WELLS_VIEWER_ROLE
from wells.models import (
    LicencedStatusCode,
    DevelopmentMethodCode,
    DrillingMethodCode,
    WellOrientationCode,
    WaterQualityCharacteristic,
    Well,
    WellAttachment,
    PumpingTestDescriptionCode,
    BoundaryEffectCode,
    AnalysisMethodCode,
    LithologyDescription,
    Casing,
    ActivitySubmission
)
from wells.constants import (
  WELL_TAGS,
  WELL_ACTIVITY_CODE_STAFF_EDIT,
  WELL_ACTIVITY_CODE_CONSTRUCTION,
  WELL_ACTIVITY_CODE_DECOMMISSION,
  WELL_ACTIVITY_CODE_ALTERATION,
)

logger = logging.getLogger('wells_filters')

def copy_request(request, **kwargs):
    """
    Given a rest_framework.request.Request object, create a copy
    we can mutate without side effects.

    Unfortunately, the built in clone_request method doens't quite get us
    all the way there (it shares the Django HttpRequest object with the original),
    and copy.deepcopy doesn't work on WSGIRequests.
    """
    clone = clone_request(request, request.method)
    clone._request = HttpRequest()

    for attr in ('GET', 'POST', 'COOKIES', 'META', 'FILES'):
        value = getattr(request._request, attr)
        if value:
            setattr(clone._request, attr, value.copy())

    for attr in ('path', 'path_info', 'method', 'resolver_match', 'content_type',
                 'content_params', 'user', 'auth'):
        if hasattr(request._request, attr):
            setattr(clone._request, attr, getattr(request._request, attr))

    return clone


class BoundingBoxFilterBackend(BaseFilterBackend):
    """
    Filter that allows geographic filtering with a bounding box.
    """

    def filter_queryset(self, request, queryset, view):
        sw_long = request.query_params.get('sw_long')
        sw_lat = request.query_params.get('sw_lat')
        ne_long = request.query_params.get('ne_long')
        ne_lat = request.query_params.get('ne_lat')

        if sw_long and sw_lat and ne_long and ne_lat:
            try:
                bbox = Polygon.from_bbox((sw_long, sw_lat, ne_long, ne_lat))
            except (ValueError, GEOSException) as e:
                # This filter has less strict error handling because it was
                # already in use for public v1 endpoints before v2 filters
                # with stricter error responses were added.
                # To avoid a breaking change, this filter will be skipped if
                # invalid/incomplete bbox corners provided.
                logger.debug('skipped bounding box filter; coordinates provided but could not create polygon: %s', e)
            else:
                queryset = queryset.filter(geom__bboverlaps=bbox)

        return queryset


class GeometryFilterBackend(BaseFilterBackend):
    """
    Filter that allows geographic filtering on a geometry/shape using `?within=<geojson geometry>`
    """

    def filter_queryset(self, request, queryset, view):
        within = request.query_params.get('within', None)
        srid = request.query_params.get('srid', 4326)

        if within:
            try:
                shape = GEOSGeometry(within, srid=int(srid))
            except (ValueError, GEOSException, ParseException):
                raise ValidationError({
                    'within': 'Invalid geometry. Use a geojson geometry or WKT representing a polygon. Example: &within={"type": "Polygon", "coordinates": [...]}'
                })
            else:
                queryset = queryset.filter(geom__intersects=shape)

        return queryset


class RadiusFilterBackend(BaseFilterBackend):
    """
    Filter that allows searching within radius (m) of a point.
    """

    def filter_queryset(self, request, queryset, view):
        point = request.query_params.get('point', None)
        radius = request.query_params.get('radius', None)
        srid = request.query_params.get('srid', 4326)

        if point and radius:
            try:
                shape = GEOSGeometry(point, srid=int(srid))
                assert shape.geom_type == 'Point'
            except (ValueError, AssertionError, GDALException, GEOSException):
                pass
            else:
                shape.transform(3005)
                queryset = queryset.annotate(geom_albers=Transform('geom', 3005)) \
                    .filter(geom_albers__dwithin=(shape, D(m=radius)))

        return queryset


class AnyOrAllFilterSet(filters.FilterSet):
    """
    Filterset class that allows OR matches.
    """

    def get_form_class(self):
        """
        Adds a match_any filter to filters.
        """
        real_fields = [
            (name, filter_.field)
            for name, filter_ in self.filters.items()]
        match_any_field = forms.NullBooleanField(label='Match any',
                                                 help_text='If true, match any rather '
                                                 'than all of the filters given.',
                                                 required=False,
                                                 widget=BooleanWidget)
        fields = OrderedDict([('match_any', match_any_field)] + real_fields)

        return type(str('%sForm' % self.__class__.__name__),
                    (self._meta.form,), fields)

    def filter_queryset(self, queryset):
        """
        If match_any is true, build the filter queryset using union.

        This approach may be problematic. Unfortunately, django-filter doesn't
        use Q objects to build its filters, and extracting the filters from
        a QuerySet is difficult. We just | the QuerySets together.
        """
        match_any = self.form.cleaned_data.pop('match_any', False)

        if not match_any:
            return super().filter_queryset(queryset)

        filter_applied = False
        initial_queryset = queryset.all()
        queryset = queryset.none()

        for name, value in self.form.cleaned_data.items():
            filtered_queryset = self.filters[name].filter(initial_queryset, value)
            assert isinstance(filtered_queryset, QuerySet), \
                "Expected '%s.%s' to return a QuerySet, but got a %s instead." \
                % (type(self).__name__, name, type(queryset).__name__)

            # Check for identity here, as most filters just return same queryset
            # if they are inactive, and equality checks evaluate the queryset.
            if filtered_queryset is not initial_queryset:
                filter_applied = True
                queryset = queryset | filtered_queryset

        # If there were no filters, return all results, not none.
        if not filter_applied:
            queryset = initial_queryset

        return queryset


class WellListFilter(AnyOrAllFilterSet):
    well = filters.CharFilter(method='filter_well_tag_or_plate',
                              label='Well tag or identification plate number')
    street_address_or_city = filters.CharFilter(method='filter_street_address_or_city',
                                                label='Street address or city')
    owner_full_name = filters.CharFilter(lookup_expr='icontains')
    legal = filters.CharFilter(method='filter_combined_legal',
                               label='Legal lot, District legal lot, Legal plan or Legal PID')
    date_of_work = filters.DateFromToRangeFilter(method='filter_date_of_work',
                                                 label='Date of work')
    well_depth = filters.RangeFilter(method='filter_well_depth',
                                     label='Well depth (finished or total)')
    filter_pack_range = filters.RangeFilter(method='filter_filter_pack_range',
                                            label='Filter pack from/to range')
    liner_range = filters.RangeFilter(method='filter_liner_range', label='Liner range')
    well_document_type = filters.CharFilter(method='filter_by_document_type',
                                             label='Contains document type')
    
    # Don't require a choice (i.e. select box) for aquifer
    aquifer = filters.NumberFilter()

    well_tag_number = filters.CharFilter(lookup_expr='iexact')
    street_address = filters.CharFilter(lookup_expr='icontains')
    city = filters.CharFilter(lookup_expr='icontains')
    well_location_description = filters.CharFilter(lookup_expr='icontains')
    construction_start_date = filters.DateFromToRangeFilter()
    construction_end_date = filters.DateFromToRangeFilter(label='Construction End Date')
    alteration_start_date = filters.DateFromToRangeFilter()
    alteration_end_date = filters.DateFromToRangeFilter(label='Alteration End Date')
    decommission_start_date = filters.DateFromToRangeFilter()
    decommission_end_date = filters.DateFromToRangeFilter()
    well_identification_plate_attached = filters.CharFilter(lookup_expr='icontains')
    water_supply_system_name = filters.CharFilter(lookup_expr='icontains')
    water_supply_system_well_name = filters.CharFilter(lookup_expr='icontains')
    driller_name = filters.CharFilter(lookup_expr='icontains')
    drilling_methods = filters.ModelChoiceFilter(queryset=DrillingMethodCode.objects.all())
    consultant_name = filters.CharFilter(lookup_expr='icontains')
    consultant_company = filters.CharFilter(lookup_expr='icontains')
    ground_elevation = filters.RangeFilter()
    surface_seal_thickness = filters.RangeFilter()
    surface_seal_depth = filters.RangeFilter()
    backfill_type = filters.CharFilter(lookup_expr='icontains')
    backfill_depth = filters.RangeFilter()
    liner_diameter = filters.RangeFilter()
    liner_thickness = filters.RangeFilter()
    liner_from = filters.RangeFilter()
    liner_to = filters.RangeFilter()
    other_screen_material = filters.CharFilter(lookup_expr='icontains')
    other_screen_bottom = filters.CharFilter(lookup_expr='icontains')
    screen_information = filters.CharFilter(lookup_expr='icontains')
    filter_pack_from = filters.RangeFilter()
    filter_pack_to = filters.RangeFilter()
    filter_pack_thickness = filters.RangeFilter()
    development_methods = filters.ModelChoiceFilter(
        queryset=DevelopmentMethodCode.objects.all())
    development_hours = filters.RangeFilter()
    development_notes = filters.CharFilter(lookup_expr='icontains')
    yield_estimation_rate = filters.RangeFilter()
    yield_estimation_duration = filters.RangeFilter()
    static_level_before_test = filters.RangeFilter()
    drawdown = filters.RangeFilter()
    hydro_fracturing_yield_increase = filters.RangeFilter()
    recommended_pump_depth = filters.RangeFilter()
    recommended_pump_rate = filters.RangeFilter()
    water_quality_characteristics = filters.ModelChoiceFilter(
        queryset=WaterQualityCharacteristic.objects.all())
    water_quality_colour = filters.CharFilter(lookup_expr='icontains')
    water_quality_odour = filters.CharFilter(lookup_expr='icontains')
    well_yield = filters.RangeFilter()
    observation_well_number = filters.CharFilter(lookup_expr='icontains')
    observation_well_number_has_value = filters.BooleanFilter(field_name='observation_well_number',
                                                              method='filter_has_value',
                                                              label='Any value for observation well number')
    utm_northing = filters.RangeFilter()
    utm_easting = filters.RangeFilter()
    decommission_reason = filters.CharFilter(lookup_expr='icontains')
    decommission_sealant_material = filters.CharFilter(lookup_expr='icontains')
    decommission_backfill_material = filters.CharFilter(lookup_expr='icontains')
    decommission_details = filters.CharFilter(lookup_expr='icontains')
    aquifer_vulnerability_index = filters.RangeFilter()
    specific_storage = filters.CharFilter(lookup_expr='icontains')

    testing_number = filters.RangeFilter(field_name='aquifer_parameters_set__testing_number')
    start_date_pumping_test = filters.DateFromToRangeFilter(label='Pumping Test Date', 
                                                 field_name='aquifer_parameters_set__start_date_pumping_test')
    pumping_test_description = filters.ModelChoiceFilter(
        queryset=PumpingTestDescriptionCode.objects.all(), field_name='aquifer_parameters_set__pumping_test_description')
    test_duration = filters.RangeFilter(field_name='aquifer_parameters_set__test_duration')
    boundary_effect = filters.ModelChoiceFilter(
        queryset=BoundaryEffectCode.objects.all(), field_name='aquifer_parameters_set__boundary_effect')
    storativity = filters.RangeFilter(field_name='aquifer_parameters_set__storativity')
    transmissivity = filters.RangeFilter(field_name='aquifer_parameters_set__transmissivity')
    hydraulic_conductivity = filters.RangeFilter(field_name='aquifer_parameters_set__hydraulic_conductivity')
    specific_yield = filters.RangeFilter(field_name='aquifer_parameters_set__specific_yield')
    specific_capacity = filters.RangeFilter(field_name='aquifer_parameters_set__specific_capacity')
    analysis_method = filters.ModelChoiceFilter(
        queryset=AnalysisMethodCode.objects.all(), field_name='aquifer_parameters_set__analysis_method')
    comments = filters.CharFilter(lookup_expr='icontains', 
                                          field_name='aquifer_parameters_set__comments')
    final_casing_stick_up = filters.RangeFilter()
    bedrock_depth = filters.RangeFilter()
    static_water_level = filters.RangeFilter()
    artesian_flow = filters.RangeFilter()
    artesian_flow_has_value = filters.BooleanFilter(field_name='artesian_flow',
                                                    method='filter_has_value',
                                                    label='Any value for artesian flow')
    artesian_pressure = filters.RangeFilter()
    artesian_pressure_has_value = filters.BooleanFilter(field_name='artesian_pressure',
                                                        method='filter_has_value',
                                                        label='Any value for artesian pressure')
    artesian_conditions = filters.BooleanFilter()
    artesian_conditions_has_value = filters.BooleanFilter(field_name='artesian_conditions',
                                                          method='filter_has_value',
                                                          label='Any value for artesian conditions')
    well_cap_type = filters.CharFilter(lookup_expr='icontains')
    comments = filters.CharFilter(lookup_expr='icontains')
    ems_has_value = filters.BooleanFilter(field_name='ems',
                                          method='filter_has_value',
                                          label='Any value for EMS id')
    diameter = filters.RangeFilter()
    finished_well_depth = filters.RangeFilter()
    total_depth_drilled = filters.RangeFilter()

    well_orientation_status = filters.ModelChoiceFilter(queryset=WellOrientationCode.objects.all())
    alternative_specs_submitted = filters.BooleanFilter(widget=BooleanWidget)
    technical_report = filters.BooleanFilter(widget=BooleanWidget)
    drinking_water_protection_area_ind = filters.BooleanFilter(widget=BooleanWidget)
    hydro_fracturing_performed = filters.BooleanFilter(widget=BooleanWidget)

    company_of_person_responsible = filters.UUIDFilter(field_name='company_of_person_responsible')
    # Alias for any old API requests now that DrillingCompany doesn't exist
    drilling_company = filters.UUIDFilter(field_name='company_of_person_responsible')

    company_of_person_responsible_name = filters.CharFilter(
        field_name='company_of_person_responsible__name',
        lookup_expr='icontains'
    )
    person_responsible_name = filters.CharFilter(field_name='person_responsible',
                                                 method='filter_person_responsible_name',
                                                 label='Person responsible')

    licenced_status = filters.ModelChoiceFilter(queryset=LicencedStatusCode.objects.all(),
                                                method='filter_licenced_status',
                                                label='Licence status'
    )
    licence_number = filters.NumberFilter(field_name='licence_number',
                                          method="filter_licence_number",
                                          label="Licence Number"
                                          )
    class Meta:
        model = Well
        fields = [
            'alteration_end_date',
            'alteration_start_date',
            'alternative_specs_submitted',
            'technical_report',
            'drinking_water_protection_area_ind',
            'analytic_solution_type',
            'aquifer',
            'aquifer_lithology',
            'aquifer_vulnerability_index',
            'artesian_flow',
            'artesian_pressure',
            'artesian_conditions',
            'backfill_depth',
            'backfill_type',
            'bcgs_id',
            'bedrock_depth',
            'boundary_effect',
            'city',
            'comments',
            'construction_end_date',
            'construction_start_date',
            'coordinate_acquisition_code',
            'date_of_work',
            'decommission_backfill_material',
            'decommission_details',
            'decommission_end_date',
            'decommission_method',
            'decommission_reason',
            'decommission_sealant_material',
            'decommission_start_date',
            'development_hours',
            'development_methods',
            'development_notes',
            'diameter',
            'drawdown',
            'driller_name',
            'drilling_company',
            'company_of_person_responsible',
            'company_of_person_responsible_name',
            'drilling_methods',
            'ems',
            'filter_pack_from',
            'filter_pack_material',
            'filter_pack_material_size',
            'filter_pack_thickness',
            'filter_pack_to',
            'final_casing_stick_up',
            'finished_well_depth',
            'ground_elevation',
            'ground_elevation_method',
            'hydraulic_conductivity',
            'hydro_fracturing_performed',
            'hydro_fracturing_yield_increase',
            'id_plate_attached_by',
            'identification_plate_number',
            'intended_water_use',
            'land_district',
            'legal',
            'legal_block',
            'legal_district_lot',
            'legal_lot',
            'legal_pid',
            'legal_plan',
            'legal_range',
            'legal_section',
            'legal_township',
            'licence_number',
            'licenced_status',
            'liner_diameter',
            'liner_from',
            'liner_material',
            'liner_thickness',
            'liner_to',
            'observation_well_number',
            'observation_well_status',
            'other_screen_bottom',
            'other_screen_material',
            'owner_full_name',
            'person_responsible',
            'person_responsible_name',
            'recommended_pump_depth',
            'recommended_pump_rate',
            'screen_bottom',
            'screen_information',
            'screen_intake_method',
            'screen_material',
            'screen_opening',
            'screen_type',
            'specific_storage',
            'specific_yield',
            'static_level_before_test',
            'static_water_level',
            'storativity',
            'street_address',
            'street_address_or_city',
            'surface_seal_depth',
            'surface_seal_material',
            'surface_seal_method',
            'surface_seal_thickness',
            'testing_duration',
            'testing_method',
            'total_depth_drilled',
            'transmissivity',
            'utm_easting',
            'utm_northing',
            'utm_zone_code',
            'water_quality_characteristics',
            'water_quality_colour',
            'water_quality_odour',
            'water_supply_system_name',
            'water_supply_system_well_name',
            'well',
            'well_cap_type',
            'well_class',
            'well_depth',
            'well_disinfected_status',
            'well_document_type',
            'well_identification_plate_attached',
            'well_location_description',
            'well_orientation_status',
            'well_status',
            'well_subclass',
            'well_tag_number',
            'well_yield',
            'well_yield_unit',
            'yield_estimation_duration',
            'yield_estimation_method',
            'yield_estimation_rate',
        ]

    def filter_licenced_status(self, queryset, name, value):
        licence_status = None
        try:
            licence_status = str(value.licenced_status_code)
        except:
            pass


        # If searching for status LICENSED, exclude any wells with an empty `licences` set.
        # If searching for UNLICENSED, only return wells with an empty `licences` set.
        if licence_status == 'LICENSED':
            return queryset.exclude(licences=None)
        elif licence_status == 'UNLICENSED':
            return queryset.filter(licences=None)

        # since only LicencedStatusCode objects (either LICENSED or UNLICENSED) options are presented or accepted,
        # the user should not reach this point unless something is changed in the filter class behavior or 
        # additional LicencedStatusCode entries are added.
        raise ValidationError({
            "licenced_status": "If searching by licence status, valid statuses are LICENSED or UNLICENSED."
        })

    def filter_well_tag_or_plate(self, queryset, name, value):
        return queryset.filter(Q(well_tag_number=value) |
                               Q(identification_plate_number=value))

    def filter_street_address_or_city(self, queryset, name, value):
        return queryset.filter(Q(street_address__icontains=value) |
                               Q(city__icontains=value))

    def filter_licence_number(self, queryset, name, value):
        raw_query = """
        SELECT DISTINCT
        wl.well_id
        FROM well_licences wl 
        LEFT JOIN aquifers_waterrightslicence aw 
        ON aw.wrl_sysid = wl.waterrightslicence_id
        WHERE aw.licence_number = %s
        """
        params = [value]
        try:
            if int(value):
                with connection.cursor() as cursor:
                    cursor.execute(raw_query, params)
                    result = cursor.fetchall()
                well_ids = [row[0] for row in result]
                print(well_ids)
                return queryset.filter(well_tag_number__in=well_ids)
        except:
            pass
        logger.warning(f"[FILTER SEARCH]: invalid licence_number '{value}' was inputted.")
        return queryset.filter(well_tag_number=None)

    def filter_by_document_type(self, queryset, name, value):
        if any(value == entry["value"] for entry in WELL_TAGS):
            filter_condition = {f"{value.lower().replace(' ', '_')}__gt": 0}
            attachments = WellAttachment.objects.filter(**filter_condition).values_list('well_tag_number', flat=True)
            attachments = list(map(int, attachments))
            return queryset.filter(well_tag_number__in=attachments)
        logger.warning(f"[FILTER SEARCH]: invalid document_type '{value}' was inputted.")
        return queryset.filter(well_tag_number=None)

    def filter_combined_legal(self, queryset, name, value):
        lookups = (
            Q(legal_lot__iexact=value) |
            Q(legal_plan__iexact=value) |
            Q(legal_district_lot__iexact=value)
        )
        # Check if we have a positive integer before querying the
        # legal_pid field.
        try:
            int_value = int(value.replace("-", ""))
        except (TypeError, ValueError):
            pass
        else:
            if int_value >= 0:
                lookups = lookups | Q(legal_pid=int_value)

        return queryset.filter(lookups)

    def filter_date_of_work(self, queryset, name, value):
        if value.start is not None and value.stop is not None:
            range_dates = (value.start.date(), value.stop.date())
            queryset = queryset.filter(
                Q(construction_start_date__range=range_dates) |
                Q(construction_end_date__range=range_dates) |
                Q(alteration_start_date__range=range_dates) |
                Q(alteration_end_date__range=range_dates) |
                Q(decommission_start_date__range=range_dates) |
                Q(decommission_end_date__range=range_dates)
            )
        elif value.start is not None:
            after_date = value.start.date()
            queryset = queryset.filter(
                Q(construction_start_date__gte=after_date) |
                Q(construction_end_date__gte=after_date) |
                Q(alteration_start_date__gte=after_date) |
                Q(alteration_end_date__gte=after_date) |
                Q(decommission_start_date__gte=after_date) |
                Q(decommission_end_date__gte=after_date)
            )
        elif value.stop is not None:
            before_date = value.stop.date()
            queryset = queryset.filter(
                Q(construction_start_date__lte=before_date) |
                Q(construction_end_date__lte=before_date) |
                Q(alteration_start_date__lte=before_date) |
                Q(alteration_end_date__lte=before_date) |
                Q(decommission_start_date__lte=before_date) |
                Q(decommission_end_date__lte=before_date)
            )

        return queryset

    def filter_well_depth(self, queryset, name, value):
        if value.start is not None and value.stop is not None:
            queryset = queryset.filter(
                Q(finished_well_depth__range=(value.start, value.stop)) |
                Q(total_depth_drilled__range=(value.start, value.stop))
            )
        elif value.start is not None:
            queryset = queryset.filter(
                Q(finished_well_depth__gte=value.start) |
                Q(total_depth_drilled__gte=value.start)
            )
        elif value.stop is not None:
            queryset = queryset.filter(
                Q(finished_well_depth__lte=value.stop) |
                Q(total_depth_drilled__lte=value.stop)
            )

        return queryset

    def filter_filter_pack_range(self, queryset, name, value):
        if value.start is not None and value.stop is not None:
            queryset = queryset.filter(
                Q(filter_pack_from__range=(value.start, value.stop)) |
                Q(filter_pack_to__range=(value.start, value.stop))
            )
        elif value.start is not None:
            queryset = queryset.filter(
                Q(filter_pack_from__gte=value.start) |
                Q(filter_pack_to__gte=value.start)
            )
        elif value.stop is not None:
            queryset = queryset.filter(
                Q(filter_pack_from__lte=value.stop) |
                Q(filter_pack_to__lte=value.stop)
            )

        return queryset

    def filter_liner_range(self, queryset, name, value):
        if value.start is not None and value.stop is not None:
            queryset = queryset.filter(
                Q(liner_from__range=(value.start, value.stop)) |
                Q(liner_to__range=(value.start, value.stop))
            )
        elif value.start is not None:
            queryset = queryset.filter(
                Q(liner_from__gte=value.start) |
                Q(liner_to__gte=value.start)
            )
        elif value.stop is not None:
            queryset = queryset.filter(
                Q(liner_from__lte=value.stop) |
                Q(liner_to__lte=value.stop)
            )

        return queryset

    def filter_has_value(self, queryset, name, value):
        if value:
            lookup = '__'.join([name, 'isnull'])
            return queryset.filter(**{lookup: False})

        return queryset

    def filter_person_responsible_name(self, queryset, name, value):
        lookups = (
            Q(person_responsible__first_name__icontains=value) |
            Q(person_responsible__surname__icontains=value)
        )
        return queryset.filter(lookups)


class WellListAdminFilter(WellListFilter):
    create_user = filters.CharFilter(lookup_expr='icontains')
    create_date = filters.DateFromToRangeFilter()
    update_user = filters.CharFilter(lookup_expr='icontains')
    update_date = filters.DateFromToRangeFilter()
    owner_mailing_address = filters.CharFilter(lookup_expr='icontains')
    owner_city = filters.CharFilter(lookup_expr='icontains')
    owner_postal_code = filters.CharFilter(lookup_expr='icontains')
    internal_comments = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Well
        fields = WellListFilter.Meta.fields + [
            'create_user',
            'create_date',
            'update_user',
            'update_date',
            'well_publication_status',
            'owner_mailing_address',
            'owner_city',
            'owner_province_state',
            'owner_postal_code',
            'internal_comments',
        ]


class WellListFilterBackend(filters.DjangoFilterBackend):
    """
    Custom well list filtering logic.

    Returns a different filterset class for admin users, and allows additional
    'filter_group' params.
    """

    def get_filterset(self, request, queryset, view):
        filterset_class = WellListFilter
        filterset_kwargs = super().get_filterset_kwargs(request, queryset, view)

        if (request.user and request.user.is_authenticated and
                request.user.groups.filter(name=WELLS_VIEWER_ROLE).exists()):
            filterset_class = WellListAdminFilter

        return filterset_class(**filterset_kwargs)

    def filter_queryset(self, request, queryset, view):
        filtered_queryset = super().filter_queryset(request, queryset, view)

        filter_groups = request.query_params.getlist('filter_group', [])
        for group in filter_groups:
            try:
                group_params = json.loads(group)
                if 'legal_pid' in group_params.keys():
                    group_params['legal_pid'] = group_params['legal_pid'].replace("-", "")
            except ValueError as exc:
                raise ValidationError({
                    'filter_group': 'Error parsing JSON data: {}'.format(exc),
                })

            if not group_params:
                continue

            request_querydict = QueryDict(mutable=True)
            request_querydict.update(group_params)
            request_clone = copy_request(request)
            request_clone._request.GET = request_querydict

            group_filterset = self.get_filterset(request_clone, filtered_queryset, view)
            if not group_filterset.is_valid():
                raise ValidationError({"filter_group": group_filterset.errors})

            filtered_queryset = group_filterset.qs

        return filtered_queryset


class WellListOrderingFilter(OrderingFilter):
    """
    Custom ordering filter to ignore model ordering, and use the description field.

    We also avoid duplicate results when ordering by a ManyToManyField, by
    annotating and sorting on the annotated field.
    """
    relations = {
        field.name: field
        for field in Well._meta.get_fields()
        if field.is_relation and not field.auto_created
    }
    m2m_relations = {
        field.name
        for field in Well._meta.get_fields()
        if field.many_to_many and not field.auto_created
    }
    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        updated_ordering = []

        for order in ordering:
            is_desc = order.startswith('-')
            field_name = order.lstrip('-')
            if field_name in self.relations:
                field = self.relations[field_name]
                related_ordering = self.get_related_field_ordering(field)
                for related_order in related_ordering:
                    if is_desc:
                        related_order = '-{}'.format(related_order)
                    updated_ordering.append(related_order)
            else:
                updated_ordering.append(order)

        return updated_ordering

    def get_related_field_ordering(self, related_field):
        if related_field.name == 'land_district_code':
            return ['land_district__land_district_code', 'land_district__name']
        elif related_field.name == 'well_subclass':
            return ['well_class__description', 'well_subclass__description']
        elif related_field.name == 'person_responsible__name':
            return ['person_responsible__name']
        elif related_field.name == 'company_of_person_responsible__name':
            return ['company_of_person_responsible__name']

        # Check if the description column actually exists
        try:
            related_field.related_model._meta.get_field('description')
        except (FieldDoesNotExist):
            # Fallback to the 'id' column
            return ['{}_id'.format(related_field.name)]
        else:
            return ['{}__description'.format(related_field.name)]

    def filter_queryset(self, request, queryset, view):
        """
        If we get an m2m field, annotate with max or min to avoid
        duplicate results.
        """
        ordering = self.get_ordering(request, queryset, view)

        for index, order in enumerate(ordering):
            field, *_ = order.lstrip('-').split('__')
            if field in self.m2m_relations:
                is_desc = order.startswith('-')
                if is_desc:
                    aggregate_class = Max
                else:
                    aggregate_class = Min
                aggregate = aggregate_class(order.lstrip('-'))
                annotation_kwargs = {
                    '{}_order_annotation'.format(field): aggregate
                }
                queryset = queryset.annotate(**annotation_kwargs)
                order = '{}_order_annotation'.format(field)
                if is_desc:
                    order = '-{}'.format(order)
                ordering[index] = order

        if ordering:
            return queryset.order_by(*ordering)

        return queryset


class WellQaQcFilterBackend(filters.DjangoFilterBackend):
    """
    Custom well list filtering logic for the QaQc Dashboard.
    allows additional 'filter_group' params.
    """
    def parse_datetime_with_fallback(self, date_str):
        try:
            # First, try to parse with full datetime format
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            # If it fails, parse with date-only format and assume midnight
            return datetime.strptime(date_str, "%Y-%m-%d")
    

    def filter_queryset(self, request, queryset, view):
        try:
            filter_groups = request.query_params.getlist('filter_group', [])
            for group in filter_groups:
                try:
                    group_params = json.loads(group)
                except ValueError as exc:
                    raise ValidationError({
                        'filter_group': 'Error parsing JSON data: {}'.format(exc),
                    })

                if not group_params:
                    continue
                
                q_objects = Q()
                q_fields = [
                    'well_tag_number', 'identification_plate_number', 'natural_resource_region',
                    'cross_referenced_by', 'create_user', 'update_user', 'internal_comments', 
                    'comments'
                ]
                date_fields = [
                    'create_date_before', 'create_date_after', 
                    'update_date_before', 'update_date_after',
                    'cross_referenced_date_before', 'cross_referenced_date_after'
                ]

                for field, value in group_params.items():
                    if field in q_fields and value != 'null':
                        q_objects &= Q(**{f'{field}__icontains': value})

                    # Set filter date fields
                    elif field in date_fields:
                        suffix = field.split('_')[-1]  # after or before
                        date_field = '_'.join(field.split('_')[:-1])  # remove _after or _before
                        # Use the new parsing function with fallback
                        date_value = self.parse_datetime_with_fallback(value)
                        if suffix == 'after':
                            # Set to the start of the day if only a date is provided
                            if len(value) <= 10:  # YYYY-MM-DD is 10 characters
                                start_of_day = date_value
                            else:
                                start_of_day = date_value
                            q_objects &= Q(**{f'{date_field}__gte': start_of_day})
                        elif suffix == 'before':
                            # Set to the end of the day if only a date is provided
                            if len(value) <= 10:  # YYYY-MM-DD is 10 characters
                                end_of_day = datetime.combine(date_value, datetime.max.time())
                            else:
                                end_of_day = date_value
                            q_objects &= Q(**{f'{date_field}__lte': end_of_day})

                    # Apply range filters
                    elif field.endswith('min') or field.endswith('max'):
                        range_field = '_'.join(field.split('_')[:-1])  # remove _min or _max
                        suffix = field.split('_')[-1]  # min or max
                        if suffix == 'min':
                            q_objects &= Q(**{f'{range_field}__gte': value})
                        elif suffix == 'max':
                            q_objects &= Q(**{f'{range_field}__lte': value})

                    # Directly handle special cases for fields like latitude and longitude
                    elif field in ['latitude', 'longitude'] and value == 'null':
                        q_objects &= Q(**{'geom__isnull': True})
                        
                    elif field == 'intended_water_use':
                        q_objects &= Q(intended_water_use__intended_water_use_code=value)

                    # Person responsible checks
                    elif field == 'person_responsible_name' and value != 'null':
                        q_objects &= (
                            Q(person_responsible__first_name__icontains=value) |
                            Q(person_responsible__surname__icontains=value)
                        )

                    elif field == 'person_responsible_name' and value == 'null':
                        q_objects &= (Q(person_responsible__isnull=True) | Q(person_responsible__first_name__isnull=True) |
                                      Q(person_responsible__first_name='') | Q(person_responsible__first_name=' '))

                    elif field == 'company_of_person_responsible_name' and value != 'null':
                        q_objects &= Q(company_of_person_responsible__name__icontains=value)

                    elif field == 'company_of_person_responsible_name' and value == 'null':
                        q_objects &= (Q(company_of_person_responsible__isnull=True) |
                                      Q(company_of_person_responsible__name__isnull=True) |
                                      Q(company_of_person_responsible__name='') | Q(company_of_person_responsible__name=' '))

                    elif field == 'well_class':
                        q_objects &= Q(well_class__well_class_code=value)

                    elif field == 'well_subclass' and value != '00000000-0000-0000-0000-000000000000':
                        q_objects &= Q(well_subclass__well_subclass_guid=value)

                    # Check for null 'well_subclass'
                    elif field == 'well_subclass' and value == '00000000-0000-0000-0000-000000000000':
                        q_objects &= Q(well_subclass__well_subclass_guid__isnull=True)

                    # Check for null or empty 'aquifer_lithology'
                    elif field == 'aquifer_lithology' and value == 'null':
                        # Subquery to get the last lithology description's raw data for each well
                        last_lithology_raw_data = Subquery(
                            LithologyDescription.objects.filter(
                                well=OuterRef('pk')
                            ).order_by('-end').values('lithology_raw_data')[:1]
                        )
                        queryset = queryset.annotate(
                            last_lithology_raw_data=last_lithology_raw_data
                        )
                        q_objects &= (
                            Q(last_lithology_raw_data__isnull=True) |
                            Q(last_lithology_raw_data='') |
                            Q(last_lithology_raw_data=' ')
                        )

                    # Check for null or empty 'casing_diameter' using the subquery
                    elif field == 'diameter' and value == 'null':
                        # Subquery to get the last casing's diameter for each well
                        last_casing_diameter = Subquery(
                            Casing.objects.filter(
                                well=OuterRef('pk')
                            ).order_by('-end').values('diameter')[:1]
                        )
                        queryset = queryset.annotate(
                            last_casing_diameter=last_casing_diameter
                        )
                        q_objects &= Q(last_casing_diameter__isnull=True)

                    elif field == 'well_activity_type':
                        # Subquery to get the well_activity_type__code of the latest ActivitySubmission
                        # for each well, excluding 'STAFF_EDIT'
                        latest_well_activity_type_code = Subquery(
                            ActivitySubmission.objects.filter(
                                well=OuterRef('pk')  # Reference the outer Well's primary key
                            ).exclude(
                                well_activity_type__code="STAFF_EDIT"
                            ).order_by(
                                '-work_end_date'  # Ensure the latest activity comes first
                            ).values(
                                'well_activity_type__code'  # Select the well_activity_type__code field
                            )[:1]  # Limit to the first (latest) entry
                        )
                        # Annotate the queryset with the result of the subquery
                        queryset = queryset.annotate(
                            latest_well_activity_type_code=latest_well_activity_type_code
                        )
                        # Apply filters based on the annotated 'latest_well_activity_type_code'
                        if value == 'null':
                            q_objects &= Q(latest_well_activity_type_code__isnull=True)
                        else:
                            q_objects &= Q(latest_well_activity_type_code=value)

                    elif field == 'work_start_date' and value == 'null':
                        queryset = queryset.annotate(
                            last_work_start_date=Subquery(
                                ActivitySubmission.objects.filter(
                                    well=OuterRef('pk')
                                ).exclude(
                                    well_activity_type__code=WELL_ACTIVITY_CODE_STAFF_EDIT
                                ).order_by('-work_end_date').annotate(
                                    correct_start_date=Case(
                                        When(
                                            well_activity_type__code=WELL_ACTIVITY_CODE_CONSTRUCTION,
                                            construction_start_date__isnull=False,
                                            then=F('construction_start_date')
                                        ),
                                        When(
                                            well_activity_type__code=WELL_ACTIVITY_CODE_ALTERATION,
                                            alteration_start_date__isnull=False,
                                            then=F('alteration_start_date')
                                        ),
                                        When(
                                            well_activity_type__code=WELL_ACTIVITY_CODE_DECOMMISSION,
                                            decommission_start_date__isnull=False,
                                            then=F('decommission_start_date')
                                        ),
                                        default=Coalesce(
                                            'work_start_date',
                                            'construction_start_date',
                                            'alteration_start_date',
                                            'decommission_start_date',
                                            output_field=DateField()
                                        ),
                                        output_field=DateField()
                                    )
                                ).values('correct_start_date')[:1],
                                output_field=DateField()
                            )
                        )
                        q_objects &= Q(last_work_start_date__isnull=True)

                    elif field == 'work_end_date' and value == 'null':
                        queryset = queryset.annotate(
                            last_work_end_date=Subquery(
                                ActivitySubmission.objects.filter(
                                    well=OuterRef('pk')
                                ).exclude(
                                    well_activity_type__code=WELL_ACTIVITY_CODE_STAFF_EDIT
                                ).order_by('-work_end_date').annotate(
                                    correct_end_date=Case(
                                        When(
                                            well_activity_type__code=WELL_ACTIVITY_CODE_CONSTRUCTION,
                                            construction_end_date__isnull=False,
                                            then=F('construction_end_date')
                                        ),
                                        When(
                                            well_activity_type__code=WELL_ACTIVITY_CODE_ALTERATION,
                                            alteration_end_date__isnull=False,
                                            then=F('alteration_end_date')
                                        ),
                                        When(
                                            well_activity_type__code=WELL_ACTIVITY_CODE_DECOMMISSION,
                                            decommission_end_date__isnull=False,
                                            then=F('decommission_end_date')
                                        ),
                                        default=Coalesce(
                                            'work_end_date',
                                            'construction_end_date',
                                            'alteration_end_date',
                                            'decommission_end_date',
                                            output_field=DateField()
                                        ),
                                        output_field=DateField()
                                    )
                                ).values('correct_end_date')[:1],
                                output_field=DateField()
                            )
                        )
                        q_objects &= Q(last_work_end_date__isnull=True)

                    # This acts as a catch all for all null field checks
                    elif value == 'null':
                        # Check if the field exists in the model
                        try:
                            field_obj = queryset.model._meta.get_field(field)
                        except models.FieldDoesNotExist:
                            continue
                        
                        # Now handling CharField, including checks for empty strings and spaces
                        if isinstance(field_obj, models.CharField):
                            q_objects &= (Q(**{f'{field}__isnull': True}) | Q(**{f'{field}': ''}) | Q(**{f'{field}': ' '}))
                        else:
                            # For other field types, just check for null
                            q_objects &= Q(**{f'{field}__isnull': True})
                
                # Apply the combined Q object filters to the queryset
                queryset = queryset.filter(q_objects)

            # Apply any custom sorting
            queryset = self.sort_ordering(request, queryset)

        except Exception as e:
            print(e)
        return queryset

    def sort_ordering(self, request, queryset):
        # Apply custom ordering on the calculated annotation fields
        # If not a custom field set here, ordering will fall back 
        # to WellListOrderingFilter class, set in serializer
        # Get ordering params
        order_value = request.query_params.get('ordering', 'well_tag_number')
        order_field = order_value.lstrip('-')

        # Handle custom ordering for well_subclass
        if order_field == 'well_subclass':
            # Annotate queryset with the description of the well subclass for ordering
            queryset = queryset.annotate(
                well_subclass_description=models.F('well_subclass__description')
            )
            
            # Determine if we are ordering in descending order
            if order_value.startswith('-'):
                order_value = '-well_subclass_description'
            else:
                order_value = 'well_subclass_description'
            
            # Return the queryset ordered by the annotated well subclass description
            return queryset.order_by(order_value)

        if order_field not in ['aquifer_lithology', 'diameter', 'well_activity_type', 
                               'work_start_date', 'work_end_date']:
            return queryset

        # Mapping of fields to their related order fields
        related_order_mapping = {
            'aquifer_lithology': 'last_lithology_raw_data',
            'diameter': 'last_casing_diameter',
            'well_activity_type': 'latest_well_activity_type_code',
            'work_start_date': 'last_activity_start_date',
            'work_end_date': 'last_activity_end_date'
        }

        # Get mapped annoation name
        related_order = related_order_mapping.get(order_field, '')

        # if we're descending, then add the negative sign prefix
        if order_value.startswith('-'):
            related_order = f'-{related_order}'

        # print(f"ORDER VALUES: {order_value}, Descending: {order_value.startswith('-')}, Field: {order_field}")
        
        # Apply sorting field annotations
        queryset = self.annotate_custom_fields(queryset, order_field)

        # Return ordered queryset
        return queryset.order_by(related_order)
    

    def annotate_custom_fields(self, queryset, field_name):
        # Apply annotations for calculated fields if they are not already annotated
        if field_name == 'aquifer_lithology' and not queryset.query.annotations.get('last_lithology_raw_data'):
            queryset = queryset.annotate(last_lithology_raw_data=Subquery(
                LithologyDescription.objects.filter(
                    well=OuterRef('pk')
                ).order_by('-end').values('lithology_raw_data')[:1]
            ))

        if field_name == 'diameter' and not queryset.query.annotations.get('last_casing_diameter'):
            queryset = queryset.annotate(last_casing_diameter=Subquery(
                Casing.objects.filter(
                    well=OuterRef('pk')
                ).order_by('-end').values('diameter')[:1]
            ))

        if field_name == 'well_activity_type' and not queryset.query.annotations.get('latest_well_activity_type_code'):
            queryset = queryset.annotate(latest_well_activity_type_code=Subquery(
                ActivitySubmission.objects.filter(
                    well=OuterRef('pk')
                ).exclude(
                    well_activity_type__code="STAFF_EDIT"
                ).order_by(
                    '-work_end_date'
                ).values(
                    'well_activity_type__code'
                )[:1]
            ))

        if field_name == 'work_start_date' and not queryset.query.annotations.get('last_activity_start_date'):
            queryset = queryset.annotate(last_activity_start_date=Subquery(
                ActivitySubmission.objects.filter(
                    well=OuterRef('pk')
                ).order_by('-work_start_date').values('work_start_date')[:1]
            ))
        
        if field_name == 'work_end_date' and not queryset.query.annotations.get('last_activity_end_date'):
            queryset = queryset.annotate(last_activity_end_date=Subquery(
                ActivitySubmission.objects.filter(
                    well=OuterRef('pk')
                ).order_by('-work_end_date').values('work_end_date')[:1]
            ))

        return queryset
