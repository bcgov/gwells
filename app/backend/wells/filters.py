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
from collections import OrderedDict

from django import forms
from django.core.exceptions import FieldDoesNotExist
from django.http import QueryDict
from django.contrib.gis.geos import GEOSException, Polygon
from django.db.models import Max, Min, Q, QuerySet
from django_filters import rest_framework as filters
from django_filters.widgets import BooleanWidget
from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.request import clone_request

from gwells.roles import WELLS_VIEWER_ROLE
from wells.models import (
    DevelopmentMethodCode,
    DrillingMethodCode,
    WaterQualityCharacteristic,
    Well,
)


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
            except (ValueError, GEOSException):
                pass
            else:
                queryset = queryset.filter(geom__bboverlaps=bbox)

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

    # Don't require a choice (i.e. select box) for aquifer
    aquifer = filters.NumberFilter()

    well_tag_number = filters.CharFilter(lookup_expr='icontains')
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
    surface_seal_length = filters.RangeFilter()
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
    storativity = filters.RangeFilter()
    transmissivity = filters.RangeFilter()
    hydraulic_conductivity = filters.CharFilter(lookup_expr='icontains')
    specific_storage = filters.CharFilter(lookup_expr='icontains')
    specific_yield = filters.RangeFilter()
    testing_method = filters.CharFilter(lookup_expr='icontains')
    testing_duration = filters.RangeFilter()
    analytic_solution_type = filters.RangeFilter()
    boundary_effect = filters.RangeFilter()
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
    well_cap_type = filters.CharFilter(lookup_expr='icontains')
    comments = filters.CharFilter(lookup_expr='icontains')
    ems_has_value = filters.BooleanFilter(field_name='ems',
                                          method='filter_has_value',
                                          label='Any value for EMS id')
    diameter = filters.RangeFilter()
    finished_well_depth = filters.RangeFilter()
    total_depth_drilled = filters.RangeFilter()

    class Meta:
        model = Well
        fields = [
            'alteration_end_date',
            'alteration_start_date',
            'alternative_specs_submitted',
            'analytic_solution_type',
            'aquifer',
            'aquifer_lithology',
            'aquifer_vulnerability_index',
            'artesian_flow',
            'artesian_pressure',
            'backfill_depth',
            'backfill_type',
            'bcgs_id',
            'bedrock_depth',
            'boundary_effect',
            'city',
            'comments',
            'company_of_person_responsible',
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
            'surface_seal_length',
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
            'well_disinfected',
            'well_identification_plate_attached',
            'well_location_description',
            'well_orientation',
            'well_status',
            'well_subclass',
            'well_tag_number',
            'well_yield',
            'well_yield_unit',
            'yield_estimation_duration',
            'yield_estimation_method',
            'yield_estimation_rate',
        ]

    def filter_well_tag_or_plate(self, queryset, name, value):
        return queryset.filter(Q(well_tag_number=value) |
                               Q(identification_plate_number=value))

    def filter_street_address_or_city(self, queryset, name, value):
        return queryset.filter(Q(street_address__icontains=value) |
                               Q(city__icontains=value))

    def filter_combined_legal(self, queryset, name, value):
        lookups = (
            Q(legal_lot=value) |
            Q(legal_plan=value) |
            Q(legal_district_lot=value)
        )
        # Check if we have a positive integer before querying the
        # legal_pid field.
        try:
            int_value = int(value)
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
            except ValueError:
                # We ignore malformed JSON, so it doesn't break the request
                pass

            if not group_params:
                continue

            request_querydict = QueryDict(mutable=True)
            request_querydict.update(group_params)
            request_clone = clone_request(request, 'GET')
            request_clone._request.GET = request_querydict
            group_filterset = self.get_filterset(request_clone, filtered_queryset, view)
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
        elif related_field.name == 'person_responsible':
            return ['person_responsible__name']
        elif related_field.name == 'company_of_person_responsible':
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
