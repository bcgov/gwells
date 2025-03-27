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
from decimal import Decimal
from django.db import connection
from rest_framework import serializers
from django.contrib.gis.geos import Point

from gwells.utils import isPointInsideBC
from wells.models import Well, DevelopmentMethodCode, ActivitySubmission
from aquifers.models import VerticalAquiferExtent, Aquifer

from aquifers.serializers_v2 import AquiferDetailSerializerV2
from wells.serializers import (
    ScreenSerializer,
    LithologyDescriptionSummarySerializer,
    WellDetailSerializer as WellDetailSerializerV1
)
from wells.constants import (
  WELL_ACTIVITY_CODE_STAFF_EDIT,
  WELL_ACTIVITY_CODE_CONSTRUCTION,
  WELL_ACTIVITY_CODE_DECOMMISSION,
  WELL_ACTIVITY_CODE_ALTERATION,
)

from aquifers.serializers import HYDRAULIC_SUBTYPES
COMPANY_OF_PERSON_RESPONSIBLE_NAME_FIELD = 'company_of_person_responsible.name'

logger = logging.getLogger(__name__)


class WellLocationSerializerV2(serializers.ModelSerializer):
    """ serializes well locations """

    artesian = serializers.SerializerMethodField()
    well_status = serializers.SerializerMethodField()

    class Meta:
        model = Well
        fields = (
            'well_tag_number',
            'identification_plate_number',
            'latitude',
            'longitude',
            'street_address',
            'city',
            'ems',
            'artesian',
            'well_status',
            'aquifer_id',
            'storativity',
            'transmissivity',
            'hydraulic_conductivity'
        )

    def get_artesian(self, obj):
        return obj.artesian_conditions

    def get_well_status(self, obj):
        return obj.well_status.description if obj.well_status else None

class WellVerticalAquiferExtentSerializerV2(serializers.ModelSerializer):
    aquifer_id = serializers.IntegerField()
    aquifer_name = serializers.CharField(source='aquifer.aquifer_name', read_only=True)
    well_tag_number = serializers.IntegerField(write_only=True)

    class Meta:
        model = VerticalAquiferExtent
        fields = (
            'id',
            'aquifer_id',
            'aquifer_name',
            'well_tag_number',
            'start',
            'end',
            'geom'
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.geom:
            ret['lat'] = Decimal(instance.geom.y)
            ret['lng'] = Decimal(instance.geom.x)
        del ret['geom']
        return ret

    def to_internal_value(self, data):
        latitude = data.pop('lat', None)
        longitude = data.pop('lng', None)
        well_tag_number = data.get('well_tag_number', None)

        errors = {}
        # If lat and lng are not in the payload then we want to use the well's lat lng
        if latitude is None and longitude is None and well_tag_number:
            well = Well.objects.get(well_tag_number=well_tag_number)
            if well.geom:
                longitude = well.geom.x
                latitude = well.geom.y

        if latitude == '' or latitude is None:
            errors['lat'] = ['This field is required.']
        if longitude == '' or longitude is None:
            errors['lng'] = ['This field is required.']

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        point = Point(-abs(float(longitude)), float(latitude), srid=4326)

        data['geom'] = point
        return super(WellVerticalAquiferExtentSerializerV2, self).to_internal_value(data)

    def validate(self, attrs):
        errors = {}

        start_depth = attrs.get('start', None)
        end_depth = attrs.get('end', None)
        if start_depth is not None and end_depth is not None:
            if start_depth > end_depth:
                errors['end'] = 'To can not be above from'
            if abs(end_depth - start_depth) < Decimal('0.1'):
                errors['end'] = 'End must be more then 0.1m from start'

        point = attrs.get('geom')
        if point:
            isInside = isPointInsideBC(point.y, point.x)
            if not isInside:
                errors['lat'] = 'Latitude is not inside BC'
                errors['lng'] = 'Longitude is not inside BC'

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        well_tag_number = validated_data.pop('well_tag_number', None)
        well = Well.objects.get(well_tag_number=well_tag_number)
        validated_data['well'] = well
        return super().create(validated_data)
        
class WellListSerializerV2(serializers.ModelSerializer):
    """Serializes a well record"""
    licence_number = serializers.SerializerMethodField(source='get_licence_number')
    legal_pid = serializers.SerializerMethodField()
    drilling_company = serializers.ReadOnlyField(
        source='company_of_person_responsible.org_guid')
    company_of_person_responsible = serializers.ReadOnlyField(
        source='company_of_person_responsible.org_guid')
    company_of_person_responsible_name = serializers.ReadOnlyField(
        source=COMPANY_OF_PERSON_RESPONSIBLE_NAME_FIELD)
    person_responsible = serializers.ReadOnlyField(
        source='person_responsible.person_guid')
    person_responsible_name = serializers.ReadOnlyField(source='person_responsible.name')
    licenced_status = serializers.ReadOnlyField(source='licenced_status.licenced_status_code')

    def get_legal_pid(self, instance):
        if instance.legal_pid is None:
            return instance.legal_pid
        return "{0:0>9}".format(instance.legal_pid)
    
    def get_licence_number(self, instance):
        licence_numbers = instance.licences.values_list('licence_number', flat=True).distinct()
        return list(licence_numbers)

    class Meta:
        model = Well
        fields = (
            "well_guid",
            "well_tag_number",
            "identification_plate_number",
            "owner_full_name",
            "well_class",
            "well_subclass",
            "well_status",
            "intended_water_use",
            "licenced_status",
            "street_address",
            "city",
            "legal_lot",
            "legal_plan",
            "legal_district_lot",
            "legal_block",
            "legal_section",
            "legal_township",
            "legal_range",
            "land_district",
            "legal_pid",
            "well_location_description",
            "construction_start_date",
            "construction_end_date",
            "alteration_start_date",
            "alteration_end_date",
            "decommission_start_date",
            "decommission_end_date",
            "drilling_company",  # old name of company_of_person_responsible
            "company_of_person_responsible",
            "company_of_person_responsible_name",
            "person_responsible",
            "person_responsible_name",
            "driller_name",
            "well_identification_plate_attached",
            "id_plate_attached_by",
            "water_supply_system_name",
            "water_supply_system_well_name",
            "latitude",
            "longitude",
            "coordinate_acquisition_code",
            "ground_elevation",
            "ground_elevation_method",
            "drilling_methods",
            "well_orientation_status",
            "surface_seal_material",
            "surface_seal_thickness",
            "surface_seal_method",
            "surface_seal_depth",
            "backfill_type",
            "backfill_depth",
            "liner_material",
            "liner_diameter",
            "liner_thickness",
            "liner_from",
            "liner_to",
            "screen_intake_method",
            "screen_type",
            "screen_material",
            "other_screen_material",
            "screen_opening",
            "screen_bottom",
            "other_screen_bottom",
            "screen_information",
            "filter_pack_from",
            "filter_pack_to",
            "filter_pack_thickness",
            "filter_pack_material",
            "filter_pack_material_size",
            "development_methods",
            "development_hours",
            "development_notes",
            "yield_estimation_method",
            "yield_estimation_rate",
            "yield_estimation_duration",
            "well_yield_unit",
            "static_level_before_test",
            "drawdown",
            "hydro_fracturing_performed",
            "hydro_fracturing_yield_increase",
            "recommended_pump_depth",
            "recommended_pump_rate",
            "water_quality_characteristics",
            "water_quality_colour",
            "water_quality_odour",
            "total_depth_drilled",
            "finished_well_depth",
            "well_yield",
            "diameter",
            "observation_well_number",
            "observation_well_status",
            "ems",
            "aquifer",
            "utm_zone_code",
            "utm_northing",
            "utm_easting",
            "bcgs_id",
            "decommission_reason",
            "decommission_method",
            "decommission_sealant_material",
            "decommission_backfill_material",
            "decommission_details",
            "aquifer_vulnerability_index",
            "aquifer_lithology",
            "storativity",
            "transmissivity",
            "hydraulic_conductivity",
            "specific_storage",
            "specific_yield",
            "testing_method",
            "testing_duration",
            "analytic_solution_type",
            "boundary_effect",
            "final_casing_stick_up",
            "bedrock_depth",
            "artesian_flow",
            "artesian_pressure",
            "artesian_pressure_head",
            "artesian_conditions",
            "well_cap_type",
            "well_disinfected_status",
            "static_water_level",
            "alternative_specs_submitted",
            "technical_report",
            "drinking_water_protection_area_ind",
            "licence_number"
        )

class WellListAdminSerializerV2(WellListSerializerV2):
    class Meta:
        model = Well
        fields = WellListSerializerV2.Meta.fields + (
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
        )


class WellExportSerializerV2(WellListSerializerV2):
    """Serializes a well for export (using display names for codes, etc)"""
    well_class = serializers.SlugRelatedField(read_only=True, slug_field='description')
    well_subclass = serializers.SlugRelatedField(read_only=True, slug_field='description')
    well_status = serializers.SlugRelatedField(read_only=True, slug_field='description')
    licenced_status = serializers.SlugRelatedField(read_only=True, slug_field='description')
    land_district = serializers.SlugRelatedField(read_only=True, slug_field='name')
    drilling_company = serializers.CharField(read_only=True,
                                             source=COMPANY_OF_PERSON_RESPONSIBLE_NAME_FIELD)
    ground_elevation_method = serializers.SlugRelatedField(read_only=True,
                                                           slug_field='description')
    surface_seal_material = serializers.SlugRelatedField(read_only=True, slug_field='description')
    surface_seal_method = serializers.SlugRelatedField(read_only=True, slug_field='description')
    liner_material = serializers.SlugRelatedField(read_only=True, slug_field='description')
    screen_intake_method = serializers.SlugRelatedField(read_only=True, slug_field='description')
    screen_type = serializers.SlugRelatedField(read_only=True, slug_field='description')
    screen_material = serializers.SlugRelatedField(read_only=True, slug_field='description')
    screen_opening = serializers.SlugRelatedField(read_only=True, slug_field='description')
    screen_bottom = serializers.SlugRelatedField(read_only=True, slug_field='description')
    well_yield_unit = serializers.SlugRelatedField(read_only=True, slug_field='description')
    observation_well_status = serializers.SlugRelatedField(read_only=True, slug_field='description')
    coordinate_acquisition_code = serializers.SlugRelatedField(read_only=True,
                                                               slug_field='description')
    bcgs_id = serializers.SlugRelatedField(read_only=True, slug_field='bcgs_number')
    decommission_method = serializers.SlugRelatedField(read_only=True, slug_field='description')
    aquifer = serializers.PrimaryKeyRelatedField(read_only=True)
    aquifer_lithology = serializers.SlugRelatedField(read_only=True, slug_field='description')
    yield_estimation_method = serializers.SlugRelatedField(read_only=True, slug_field='description')

    development_methods = serializers.SlugRelatedField(many=True, read_only=True,
                                                       slug_field='description')
    drilling_methods = serializers.SlugRelatedField(many=True, read_only=True,
                                                    slug_field='description')
    water_quality_characteristics = serializers.SlugRelatedField(many=True, read_only=True,
                                                                 slug_field='description')
    hydro_fracturing_performed = serializers.CharField(read_only=True,
                                                       source='get_hydro_fracturing_performed_display')

    m2m_relations = {
        field.name
        for field in Well._meta.get_fields()
        if field.many_to_many and not field.auto_created
    }

    def __init__(self, *args, **kwargs):
        """
        Limit responses to requested fields

        If we get a 'fields' context kwarg, then limit results to the included
        fields.
        """
        super().__init__(*args, **kwargs)

        context = kwargs.get('context', {})
        fields = context.get('fields', None)
        if fields is not None:
            excluded_fields = set(self.fields) - set(fields)
            for field_name in excluded_fields:
                self.fields.pop(field_name)

    def to_representation(self, instance):
        """
        Instead of arrays, return comma delimited strings for export.
        """
        data = super().to_representation(instance)

        for field_name in self.m2m_relations:
            if field_name in data:
                data[field_name] = ','.join(data[field_name])

        return data


class WellExportAdminSerializerV2(WellExportSerializerV2):
    """Serializes a well for export (using display names for codes, etc)"""
    owner_province_state = serializers.SlugRelatedField(read_only=True,
                                                        slug_field='description')
    well_publication_status = serializers.SlugRelatedField(read_only=True,
                                                           slug_field='description')

    class Meta:
        model = Well
        fields = WellListAdminSerializerV2.Meta.fields


class WellAquiferSerializer(serializers.ModelSerializer):
    subtype_desc = serializers.ReadOnlyField(source='subtype.description')
    material_desc = serializers.ReadOnlyField(source='material.description')

    class Meta:
        model = Aquifer
        fields = (
            "aquifer_id",
            "subtype",
            "subtype_desc",
            "material",
            "material_desc",
            "litho_stratographic_unit"
        )


class WellSubsurfaceSerializer(serializers.ModelSerializer):
    screen_set = ScreenSerializer(many=True)
    lithologydescription_set = LithologyDescriptionSummarySerializer(many=True)
    intended_water_use = serializers.ReadOnlyField(source='intended_water_use.description')
    distance = serializers.FloatField(required=False)
    aquifer = WellAquiferSerializer()

    class Meta:
        model = Well
        fields = (
            "well_tag_number",
            "static_water_level",
            "screen_set",
            "lithologydescription_set",
            "well_yield",
            "diameter",
            "aquifer",
            "distance",
            "latitude",
            "longitude",
            "well_yield_unit",
            "finished_well_depth",
            "street_address",
            "intended_water_use",
            "aquifer_lithology"
        )

    def to_representation(self, instance):
        details = super().to_representation(instance)
        if instance.aquifer and instance.aquifer.subtype:
            details[
                'aquifer_hydraulically_connected'] = instance.aquifer.subtype.code in HYDRAULIC_SUBTYPES
        return details


class DevelopmentMethodsSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DevelopmentMethodCode
        fields = ('description',)


class WellDetailSerializer(WellDetailSerializerV1):
    development_methods = DevelopmentMethodsSummarySerializer(many=True)
    yield_estimation_method = serializers.ReadOnlyField(source='yield_estimation_method.description')

    class Meta(WellDetailSerializerV1.Meta):
        ref_name = "well_detail_v2"


class ActivitySubmissionMixin:
    def get_last_activity(self, obj):
        # Cache the last activity in the instance to avoid repeated queries.
        if not hasattr(obj, '_last_activity'):
            obj._last_activity = ActivitySubmission.objects.filter(
                well=obj
            ).exclude(
                well_activity_type__code=WELL_ACTIVITY_CODE_STAFF_EDIT
            ).order_by('-work_end_date').first()
        return obj._last_activity

    def get_well_activity_type(self, obj):
        last_activity = self.get_last_activity(obj)
        return last_activity.well_activity_type.code if last_activity else None

    def get_work_start_date(self, obj):
        activity_type = self.get_well_activity_type(obj)
        if activity_type == WELL_ACTIVITY_CODE_CONSTRUCTION:
            order_field = '-construction_start_date'
        elif activity_type == WELL_ACTIVITY_CODE_ALTERATION:
            order_field = '-alteration_start_date'
        elif activity_type == WELL_ACTIVITY_CODE_DECOMMISSION:
            order_field = '-decommission_start_date'
        else:
            order_field = '-work_start_date' # Default order field if none of the conditions are met

        filter_field = order_field.strip('-')
        last_activity = ActivitySubmission.objects.filter(
            well=obj,
            **{f'{filter_field}__isnull': False}
        ).order_by(order_field).first()
        return getattr(last_activity, order_field.strip('-'), None) if last_activity else None

    def get_work_end_date(self, obj):
        activity_type = self.get_well_activity_type(obj)
        if activity_type == WELL_ACTIVITY_CODE_CONSTRUCTION:
            order_field = '-construction_end_date'
        elif activity_type == WELL_ACTIVITY_CODE_ALTERATION:
            order_field = '-alteration_end_date'
        elif activity_type == WELL_ACTIVITY_CODE_DECOMMISSION:
            order_field = '-decommission_end_date'
        else:
            order_field = '-work_end_date' # Default order field if none of the conditions are met

        filter_field = order_field.strip('-')
        last_activity = ActivitySubmission.objects.filter(
            well=obj,
            **{f'{filter_field}__isnull': False}
        ).order_by(order_field).first()
        return getattr(last_activity, order_field.strip('-'), None) if last_activity else None


class MislocatedWellsSerializer(ActivitySubmissionMixin, serializers.ModelSerializer):
    company_of_person_responsible_name = serializers.ReadOnlyField(
        source=COMPANY_OF_PERSON_RESPONSIBLE_NAME_FIELD)
    
    well_activity_type = serializers.SerializerMethodField()
    work_start_date = serializers.SerializerMethodField()
    work_end_date = serializers.SerializerMethodField()

    class Meta:
        model = Well
        fields = [
            'well_tag_number',
            'geocode_distance',
            'distance_to_pid',
            'score_address',
            'score_city',
            'well_activity_type',
            'work_start_date',
            'work_end_date',
            'company_of_person_responsible_name',
            'natural_resource_region',
            'create_date',
            'create_user',
            'internal_comments'
        ]


class CrossReferencingSerializer(ActivitySubmissionMixin, serializers.ModelSerializer):
    well_activity_type = serializers.SerializerMethodField()
    work_start_date = serializers.SerializerMethodField()
    work_end_date = serializers.SerializerMethodField()

    class Meta:
        model = Well
        fields = [
            'well_tag_number',
            'well_activity_type',
            'work_start_date',
            'work_end_date',
            'create_user',
            'create_date',
            'update_date',
            'update_user',
            'natural_resource_region',
            'comments',
            'internal_comments',
            'cross_referenced',
            'cross_referenced_date',
            'cross_referenced_by'
        ]


class RecordComplianceSerializer(ActivitySubmissionMixin, serializers.ModelSerializer):
    company_of_person_responsible_name = serializers.ReadOnlyField(
        source=COMPANY_OF_PERSON_RESPONSIBLE_NAME_FIELD)
    person_responsible_name = serializers.ReadOnlyField(source='person_responsible.name')

    # Serializer methods for the last ActivitySubmission's work types
    well_activity_type = serializers.SerializerMethodField()
    work_start_date = serializers.SerializerMethodField()
    work_end_date = serializers.SerializerMethodField()

    # last_lithology_raw_data
    aquifer_lithology = serializers.SerializerMethodField()
    # Serializer method field for the last casing's diameter
    diameter = serializers.SerializerMethodField()
    # Expose well_subclass uuid to convert to string
    well_subclass = serializers.SerializerMethodField()

    def get_well_subclass(self, obj):
        # This method will convert the UUID to a string
        return str(obj.well_subclass) if obj.well_subclass else None

    def get_aquifer_lithology(self, obj):
      # Fetch the last LithologyDescription based on the sequence number
      last_lithology = obj.lithologydescription_set.order_by('-end').first()
      # Return the raw data if it exists, otherwise return None
      return last_lithology.lithology_raw_data if last_lithology else None
    
    def get_diameter(self, obj):
        # Fetch the last Casing based on the 'end' field
        last_casing = obj.casing_set.order_by('-end').first()
        # Return the diameter if it exists, otherwise return None
        return last_casing.diameter if last_casing else None

    class Meta:
        model = Well
        fields = [
          'well_tag_number',
          'identification_plate_number',
          'well_subclass',
          'well_class',
          'latitude',
          'longitude',
          'finished_well_depth',
          'diameter',
          'surface_seal_depth',
          'surface_seal_thickness',
          'aquifer_lithology',
          'well_activity_type',
          'work_start_date',
          'work_end_date',
          'person_responsible_name',
          'company_of_person_responsible_name',
          'create_date',
          'create_user',
          'natural_resource_region',
          'internal_comments'
        ]
