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

from rest_framework import serializers
from django.contrib.gis.geos import Point

from gwells.utils import isPointInsideBC
from wells.models import Well
from aquifers.models import VerticalAquiferExtent


logger = logging.getLogger(__name__)


class WellLocationSerializerV2(serializers.ModelSerializer):
    """ serializes well locations """

    artesian = serializers.SerializerMethodField()

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
            'aquifer_id'
        )

    def get_artesian(self, obj):
        if obj.artesian_flow is not None and obj.artesian_flow > 0:
            return True
        return False


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

    legal_pid = serializers.SerializerMethodField()
    drilling_company = serializers.ReadOnlyField(
        source='company_of_person_responsible.org_guid')
    company_of_person_responsible = serializers.ReadOnlyField(
        source='company_of_person_responsible.org_guid')
    company_of_person_responsible_name = serializers.ReadOnlyField(
        source='company_of_person_responsible.name')
    person_responsible = serializers.ReadOnlyField(
        source='person_responsible.person_guid')
    person_responsible_name = serializers.ReadOnlyField(source='person_responsible.name')

    def get_legal_pid(self, instance):
        if instance.legal_pid is None:
            return instance.legal_pid
        return "{0:0>9}".format(instance.legal_pid)

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
            "drilling_company", # old name of company_of_person_responsible
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
            "surface_seal_length",
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
            "well_cap_type",
            "well_disinfected_status",
            "static_water_level",
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
    drilling_company = serializers.CharField(read_only=True, source='company_of_person_responsible.name')
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


class WellAquiferSerializerV2(serializers.ModelSerializer):
    """Serializes aquifer info for a selection of wells"""
    aquifer_subtype = serializers.ReadOnlyField(source='aquifer.subtype.description')

    class Meta:
        model = Well
        fields = (
            "well_tag_number",
            "aquifer",
            "aquifer_subtype"
        )
