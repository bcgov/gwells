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
from django.db.models import OneToOneField
from rest_framework import serializers

from gwells.models import ProvinceStateCode
from gwells.serializers import AuditModelSerializer
import wells.stack

from gwells.models.lithology import (
    LithologyColourCode, LithologyHardnessCode,
    LithologyMaterialCode, LithologyMoistureCode, LithologyDescriptionCode)

from wells.models import Well, ActivitySubmission, WellActivityCode
from wells.serializers import (
    CasingSerializer,
    DecommissionDescriptionSerializer,
    ScreenSerializer,
    LinerPerforationSerializer,
    LithologyDescriptionSerializer,
)
from wells.models import (
    ActivitySubmission,
    Casing,
    CoordinateAcquisitionCode,
    DecommissionDescription,
    DecommissionMaterialCode,
    DecommissionMethodCode,
    DevelopmentMethodCode,
    DrillingMethodCode,
    FilterPackMaterialCode,
    FilterPackMaterialSizeCode,
    GroundElevationMethodCode,
    IntendedWaterUseCode,
    LandDistrictCode,
    LinerMaterialCode,
    LinerPerforation,
    LithologyDescription,
    Screen,
    ScreenAssemblyTypeCode,
    ScreenBottomCode,
    ScreenIntakeMethodCode,
    ScreenMaterialCode,
    ScreenOpeningCode,
    ScreenTypeCode,
    SurfaceSealMaterialCode,
    SurfaceSealMethodCode,
    SurficialMaterialCode,
    WaterQualityCharacteristic,
    WaterQualityColour,
    Well,
    WellClassCode,
    WellSubclassCode,
    WellStatusCode,
    WellYieldUnitCode,
    YieldEstimationMethodCode,
    ObsWellStatusCode,
)

logger = logging.getLogger(__name__)


class WellSubmissionListSerializer(serializers.ModelSerializer):
    """ Class used for listing well submissions.
    """

    casing_set = CasingSerializer(many=True, required=False)
    decommission_description_set = DecommissionDescriptionSerializer(
        many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    linerperforation_set = LinerPerforationSerializer(
        many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(many=True, required=False)

    class Meta:
        fields = '__all__'
        model = ActivitySubmission


class WellSubmissionSerializerBase(serializers.ModelSerializer):
    """ Bass class for well submission serialisation. """

    def get_foreign_key_sets(self):
        raise NotImplementedError()  # Implement in base class!

    def get_well_activity_type(self):
        raise NotImplementedError()  # Implement in base class!

    @transaction.atomic
    def create(self, validated_data):
        # Pop foreign key records from validated data (we need to create them ourselves).
        foreign_keys = self.get_foreign_key_sets()
        foreign_keys_data = {}
        for key in foreign_keys.keys():
            foreign_keys_data[key] = validated_data.pop(key, None)
        # Create submission.
        validated_data['well_activity_type'] = self.get_well_activity_type()

        # If the yield_estimation_rate is specified, we default to USGPM
        if validated_data.get('yield_estimation_rate', None) and \
                not validated_data.get('well_yield_unit', None):
            validated_data['well_yield_unit'] = WellYieldUnitCode.objects.get(well_yield_unit_code='USGPM')

        instance = super().create(validated_data)
        # Create foreign key records.
        for key, value in foreign_keys_data.items():
            if value:
                model = type(self).Meta.model
                field = model._meta.get_field(key)
                foreign_class = foreign_keys[key]
                if field.one_to_many:
                    for data in value:
                        foreign_class.objects.create(activity_submission=instance, **data)
                else:
                    raise 'UNEXPECTED FIELD! {}'.format(field)
        # Update the well record.
        stacker = wells.stack.StackWells()
        stacker.process(instance.filing_number)
        # The instance may have been updated with a well tag number, so we refresh.
        instance.refresh_from_db()
        return instance


class WellSubmissionStackerSerializer(WellSubmissionSerializerBase):
    """ Class with no validation, and all possible fields, used by stacker to serialize. """

    casing_set = CasingSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    linerperforation_set = LinerPerforationSerializer(
        many=True, required=False)
    decommission_description_set = DecommissionDescriptionSerializer(
        many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(many=True, required=False)

    def get_foreign_key_sets(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
            'decommission_description_set': DecommissionDescription,
            'lithologydescription_set': LithologyDescription,
        }

    class Meta:
        model = ActivitySubmission
        fields = '__all__'


class WellSubmissionLegacySerializer(WellSubmissionSerializerBase):
    """ Class with no validation, and all possible fields, used by stacker to create legacy records """

    casing_set = CasingSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    linerperforation_set = LinerPerforationSerializer(
        many=True, required=False)
    decommission_description_set = DecommissionDescriptionSerializer(
        many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(many=True, required=False)

    def get_well_activity_type(self):
        return WellActivityCode.types.legacy()

    def get_foreign_key_sets(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
            'decommission_description_set': DecommissionDescription,
            'lithologydescription_set': LithologyDescription,
        }

    class Meta:
        model = ActivitySubmission
        extra_kwargs = {
            # This field might not be present
            'create_user': {'required': False},
            # This is autopopulated during create
            'well_activity_type': {'required': False},
        }
        fields = '__all__'


class CoordinateAcquisitionCodeSerializer(serializers.ModelSerializer):
    """ Serializes coordinate acquisition codes """

    class Meta:
        model = CoordinateAcquisitionCode
        fields = ('code', 'description')


class WellConstructionSubmissionSerializer(WellSubmissionSerializerBase):
    """ Serializes a well construction submission. """

    casing_set = CasingSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    linerperforation_set = LinerPerforationSerializer(
        many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(many=True, required=False)

    coordinate_acquisition_code = serializers.PrimaryKeyRelatedField(
        queryset=CoordinateAcquisitionCode.objects.all(),
        required=False, allow_null=True)

    def create(self, validated_data):
        # Whenever we create a Construction record, we default to H (gps) for the source.
        if 'coordinate_acquisition_code' not in validated_data:
            validated_data['coordinate_acquisition_code'] = CoordinateAcquisitionCode.objects.get(code='H')
        return super().create(validated_data)

    def get_foreign_key_sets(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
            'lithologydescription_set': LithologyDescription,
        }

    def get_well_activity_type(self):
        return WellActivityCode.types.construction()

    class Meta:
        model = ActivitySubmission
        fields = ('filing_number', 'well_activity_type', 'well', 'well_class', 'well_subclass',
                  'intended_water_use', 'identification_plate_number', 'well_identification_plate_attached',
                  'work_start_date', 'work_end_date', 'owner_full_name', 'owner_mailing_address',
                  'owner_province_state', 'owner_city', 'owner_postal_code', 'owner_email',
                  'owner_tel', 'street_address', 'city',
                  'legal_lot', 'legal_plan', 'legal_district_lot', 'legal_block', 'legal_section',
                  'legal_township', 'legal_range', 'land_district', 'legal_pid', 'well_location_description',
                  'latitude', 'longitude', 'ground_elevation', 'ground_elevation_method', 'drilling_methods',
                  'well_orientation', 'lithologydescription_set', 'casing_set',
                  'surface_seal_material', 'surface_seal_depth', 'surface_seal_thickness',
                  'surface_seal_method', 'backfill_type', 'backfill_depth',
                  'liner_material', 'liner_diameter', 'liner_thickness', 'liner_from', 'liner_to',
                  'linerperforation_set', 'screen_intake_method', 'screen_type', 'screen_material',
                  'other_screen_material', 'screen_opening', 'screen_bottom', 'other_screen_bottom',
                  'screen_set', 'filter_pack_from', 'filter_pack_to', 'filter_pack_thickness',
                  'filter_pack_material', 'filter_pack_material_size', 'development_methods',
                  'development_hours', 'yield_estimation_method', 'yield_estimation_rate',
                  'yield_estimation_duration', 'well_yield_unit', 'static_level_before_test',
                  'drawdown', 'hydro_fracturing_performed', 'hydro_fracturing_yield_increase',
                  'recommended_pump_depth', 'recommended_pump_rate', 'development_notes',
                  'water_quality_characteristics',
                  'water_quality_colour', 'water_quality_odour', 'ems_id', 'total_depth_drilled',
                  'finished_well_depth', 'final_casing_stick_up', 'bedrock_depth', 'static_water_level',
                  'well_yield', 'artesian_flow', 'artesian_pressure', 'well_cap_type', 'well_disinfected',
                  'comments', 'alternative_specs_submitted', 'consultant_company', 'consultant_name',
                  'driller_name', 'person_responsible', 'company_of_person_responsible',
                  'coordinate_acquisition_code',)
        extra_kwargs = {
            # TODO: reference appropriate serializer as above
            'well_activity_type': {'required': False}
        }


class WellAlterationSubmissionSerializer(WellSubmissionSerializerBase):
    """ Serializes a well alteration submission. """

    casing_set = CasingSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    linerperforation_set = LinerPerforationSerializer(
        many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(many=True, required=False)

    def get_foreign_key_sets(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
            'lithologydescription_set': LithologyDescription,
        }

    def get_well_activity_type(self):
        return WellActivityCode.types.alteration()

    class Meta:
        model = ActivitySubmission
        fields = (
            'filing_number',
            'well_activity_type',
            'well',
            'well_class',
            'well_subclass',
            'intended_water_use',
            'identification_plate_number',
            'well_identification_plate_attached',
            'work_start_date',
            'work_end_date',
            'owner_full_name',
            'owner_mailing_address',
            'owner_province_state',
            'owner_city',
            'owner_postal_code',
            'owner_email',
            'owner_tel',
            'street_address',
            'city',
            'consultant_company',
            'consultant_name',
            'driller_name',
            'person_responsible',
            'company_of_person_responsible',
            'legal_lot',
            'legal_plan',
            'legal_district_lot',
            'legal_block',
            'legal_section',
            'legal_township',
            'legal_range',
            'land_district',
            'legal_pid',
            'well_location_description',
            'latitude',
            'longitude',
            'ground_elevation',
            'ground_elevation_method',
            'drilling_methods',
            'well_orientation',
            'lithologydescription_set',
            'casing_set',
            'surface_seal_material',
            'surface_seal_depth',
            'surface_seal_thickness',
            'surface_seal_method',
            'backfill_type',
            'backfill_depth',
            'liner_material',
            'liner_diameter',
            'liner_thickness',
            'liner_from',
            'liner_to',
            'linerperforation_set',
            'screen_intake_method',
            'screen_type',
            'screen_material',
            'other_screen_material',
            'screen_opening',
            'screen_bottom',
            'other_screen_bottom',
            'screen_information',
            'screen_set',
            'filter_pack_from',
            'filter_pack_to',
            'filter_pack_thickness',
            'filter_pack_material',
            'filter_pack_material_size',
            'development_methods',
            'development_hours',
            'development_notes',
            'yield_estimation_method',
            'yield_estimation_rate',
            'yield_estimation_duration',
            'well_yield_unit',
            'static_level_before_test',
            'drawdown',
            'hydro_fracturing_performed',
            'hydro_fracturing_yield_increase',
            'recommended_pump_depth',
            'recommended_pump_rate',
            'water_quality_characteristics',
            'water_quality_colour',
            'water_quality_odour',
            'ems_id',
            'total_depth_drilled',
            'finished_well_depth',
            'final_casing_stick_up',
            'bedrock_depth',
            'static_water_level',
            'well_yield',
            'artesian_flow',
            'artesian_pressure',
            'well_cap_type',
            'well_disinfected',
            'comments',
            'alternative_specs_submitted',
        )
        extra_kwargs = {
            # TODO: reference appropriate serializer as above
            'well_activity_type': {'required': False}
        }


class WellStaffEditSubmissionSerializer(WellSubmissionSerializerBase):

    well = serializers.PrimaryKeyRelatedField(queryset=Well.objects.all())
    linerperforation_set = LinerPerforationSerializer(
        many=True, required=False)
    casing_set = CasingSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    decommission_description_set = DecommissionDescriptionSerializer(many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(many=True, required=False)

    def get_well_activity_type(self):
        return WellActivityCode.types.staff_edit()

    def get_foreign_key_sets(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
            'lithologydescription_set': LithologyDescription,
            'decommission_description_set': DecommissionDescription
        }

    class Meta:
        model = ActivitySubmission
        fields = (
            'well',
            'well_class',
            'well_subclass',
            'well_status',
            'intended_water_use',
            'identification_plate_number',
            'well_identification_plate_attached',
            'id_plate_attached_by',
            'water_supply_system_name',
            'water_supply_system_well_name',
            'work_start_date',
            'work_end_date',
            'owner_full_name',
            'owner_mailing_address',
            'owner_province_state',
            'owner_city',
            'owner_postal_code',
            'owner_email',
            'owner_tel',
            'street_address',
            'city',
            'consultant_company',
            'consultant_name',
            'driller_name',
            'person_responsible',
            'company_of_person_responsible',
            'legal_lot',
            'legal_plan',
            'legal_district_lot',
            'legal_block',
            'legal_section',
            'legal_township',
            'legal_range',
            'land_district',
            'legal_pid',
            'well_location_description',
            'latitude',
            'longitude',
            'coordinate_acquisition_code',
            'ground_elevation',
            'ground_elevation_method',
            'drilling_methods',
            'well_orientation',
            'lithologydescription_set',
            'casing_set',
            'surface_seal_material',
            'surface_seal_depth',
            'surface_seal_thickness',
            'surface_seal_method',
            'backfill_type',
            'backfill_depth',
            'liner_material',
            'liner_diameter',
            'liner_thickness',
            'liner_from',
            'liner_to',
            'linerperforation_set',
            'screen_intake_method',
            'screen_type',
            'screen_material',
            'other_screen_material',
            'screen_opening',
            'screen_bottom',
            'other_screen_bottom',
            'screen_set',
            'screen_information',
            'filter_pack_from',
            'filter_pack_to',
            'filter_pack_thickness',
            'filter_pack_material',
            'filter_pack_material_size',
            'development_methods',
            'development_hours',
            'development_notes',
            'yield_estimation_method',
            'yield_estimation_rate',
            'yield_estimation_duration',
            'well_yield_unit',
            'static_level_before_test',
            'drawdown',
            'hydro_fracturing_performed',
            'hydro_fracturing_yield_increase',
            'recommended_pump_depth',
            'recommended_pump_rate',
            'water_quality_characteristics',
            'water_quality_colour',
            'water_quality_odour',
            'ems_id',
            'aquifer',
            'total_depth_drilled',
            'finished_well_depth',
            'decommission_reason',
            'decommission_method',
            'sealant_material',
            'backfill_material',
            'decommission_details',
            'final_casing_stick_up',
            'bedrock_depth',
            'static_water_level',
            'well_yield',
            'artesian_flow',
            'artesian_pressure',
            'well_cap_type',
            'well_disinfected',
            'comments',
            'internal_comments',
            'alternative_specs_submitted',
            'decommission_description_set',
            'observation_well_number',
            'observation_well_status',
            'aquifer_vulnerability_index',
            'storativity',
            'transmissivity',
            'hydraulic_conductivity',
            'specific_storage',
            'specific_yield',
            'testing_method',
            'testing_duration',
            'analytic_solution_type',
            'boundary_effect',
        )


class WellDecommissionSubmissionSerializer(WellSubmissionSerializerBase):
    """ Serializes a well decommission submission. """

    casing_set = CasingSerializer(many=True, required=False)
    decommission_description_set = DecommissionDescriptionSerializer(
        many=True, required=False)

    def get_well_activity_type(self):
        return WellActivityCode.types.decommission()

    def get_foreign_key_sets(self):
        return {
            'casing_set': Casing,
            'decommission_description_set': DecommissionDescription,
        }

    class Meta:
        model = ActivitySubmission
        # Decommission has fewer fields
        fields = (
            'filing_number',
            'well_activity_type',
            'well',
            'well_class',
            'well_subclass',
            'intended_water_use',
            'identification_plate_number',
            'well_identification_plate_attached',
            'work_start_date',
            'work_end_date',
            'owner_full_name',
            'owner_mailing_address',
            'owner_province_state',
            'owner_city',
            'owner_postal_code',
            'street_address',
            'city',
            'legal_lot',
            'legal_plan',
            'legal_district_lot',
            'legal_block',
            'legal_section',
            'legal_township',
            'legal_range',
            'land_district',
            'legal_pid',
            'well_location_description',
            'latitude',
            'longitude',
            'ground_elevation',
            'ground_elevation_method',
            'drilling_methods',
            'well_orientation',
            'decommission_reason',
            'decommission_method',
            'sealant_material',
            'backfill_material',
            'decommission_details',
            'casing_set',
            'decommission_description_set',
            'comments',
            'alternative_specs_submitted',
        )
        extra_kwargs = {
            'well_activity_type': {'required': False}
        }


class WellActivityCodeSerializer(serializers.ModelSerializer):
    """Serializes well activity codes"""

    class Meta:
        model = WellActivityCode
        fields = ('code', 'description')


class WellSubclassCodeSerializer(serializers.ModelSerializer):
    """Serializes well subclass codes"""

    class Meta:
        model = WellSubclassCode
        fields = ('well_subclass_guid', 'well_subclass_code', 'description')


class WellClassCodeSerializer(serializers.ModelSerializer):
    """Serializes well class codes"""

    wellsubclasscode_set = WellSubclassCodeSerializer(
        many=True, read_only=True)

    class Meta:
        model = WellClassCode
        fields = ('well_class_code', 'description', 'wellsubclasscode_set')


class FilterPackMaterialCodeSerializer(serializers.ModelSerializer):
    """Serializes Filter Pack codes/descriptions"""

    class Meta:
        model = FilterPackMaterialCode
        fields = ('filter_pack_material_code', 'description')


class FilterPackMaterialSizeCodeSerializer(serializers.ModelSerializer):
    """Serializes Filter Pack codes/descriptions"""

    class Meta:
        model = FilterPackMaterialSizeCode
        fields = ('filter_pack_material_size_code', 'description')


class IntendedWaterUseCodeSerializer(serializers.ModelSerializer):
    """Serializes intended water use codes"""

    class Meta:
        model = IntendedWaterUseCode
        fields = ('intended_water_use_code', 'description')


class LandDistrictSerializer(serializers.ModelSerializer):
    """Serializes Land District codes/descriptions"""

    class Meta:
        model = LandDistrictCode
        fields = ('land_district_code', 'name')


class LinerMaterialCodeSerializer(serializers.ModelSerializer):
    """ serializes Liner Material code/description """

    class Meta:
        model = LinerMaterialCode
        fields = ('code', 'description')


class ScreenIntakeMethodSerializer(serializers.ModelSerializer):
    """Serializes screen intake method codes"""

    class Meta:
        model = ScreenIntakeMethodCode
        fields = ('screen_intake_code', 'description')


class GroundElevationMethodCodeSerializer(serializers.ModelSerializer):
    """Serializes codes for methods of obtaining ground elevations"""

    class Meta:
        model = GroundElevationMethodCode
        fields = ('ground_elevation_method_code', 'description')


class DrillingMethodCodeSerializer(serializers.ModelSerializer):
    """Serializes drilling method codes"""

    class Meta:
        model = DrillingMethodCode
        fields = ('drilling_method_code', 'description')


class SurfaceSealMethodCodeSerializer(serializers.ModelSerializer):
    """Serializes surface seal method codes"""

    class Meta:
        model = SurfaceSealMethodCode
        fields = ('surface_seal_method_code', 'description')


class SurfaceSealMaterialCodeSerializer(serializers.ModelSerializer):
    """Serializes surface seal method codes"""

    class Meta:
        model = SurfaceSealMaterialCode
        fields = ('surface_seal_material_code', 'description')


class SurficialMaterialCodeSerializer(serializers.ModelSerializer):
    """Serializes surficial material codes"""

    class Meta:
        model = SurficialMaterialCode
        fields = ('surficial_material_code', 'description')


class ScreenTypeCodeSerializer(serializers.ModelSerializer):
    """Serializes screen type codes"""

    class Meta:
        model = ScreenTypeCode
        fields = ('screen_type_code', 'description')


class ScreenMaterialCodeSerializer(serializers.ModelSerializer):
    """Serializes screen material codes"""

    class Meta:
        model = ScreenMaterialCode
        fields = ('screen_material_code', 'description')


class ScreenOpeningCodeSerializer(serializers.ModelSerializer):
    """Serializes screen opening codes"""

    class Meta:
        model = ScreenOpeningCode
        fields = ('screen_opening_code', 'description')


class ScreenBottomCodeSerializer(serializers.ModelSerializer):
    """Serializes screen bottom codes"""

    class Meta:
        model = ScreenBottomCode
        fields = ('screen_bottom_code', 'description')


class ScreenAssemblyTypeCodeSerializer(serializers.ModelSerializer):
    """Serializes screen assembly codes"""

    class Meta:
        model = ScreenAssemblyTypeCode
        fields = ('screen_assembly_type_code', 'description')


class DevelopmentMethodCodeSerializer(serializers.ModelSerializer):
    """Serializes well development methods"""

    class Meta:
        model = DevelopmentMethodCode
        fields = ('development_method_code', 'description')


class YieldEstimationMethodCodeSerializer(serializers.ModelSerializer):
    """Serializes well production yield estimation method codes"""

    class Meta:
        model = YieldEstimationMethodCode
        fields = ('yield_estimation_method_code', 'description')


class WaterQualityCharacteristicSerializer(serializers.ModelSerializer):
    """Serializes water quality characteristic codes"""

    class Meta:
        model = WaterQualityCharacteristic
        fields = ('code', 'description')


class WaterQualityColourSerializer(serializers.ModelSerializer):
    """Serializes water colour codes"""

    class Meta:
        model = WaterQualityColour
        fields = ('code', 'description')


class DecommissionMethodCodeSerializer(serializers.ModelSerializer):
    """ Serializes decommission methods """

    class Meta:
        model = DecommissionMethodCode
        fields = ('decommission_method_code', 'description')


class DecommissionMaterialCodeSerializer(serializers.ModelSerializer):
    """ Serializes decommission material codes """

    class Meta:
        model = DecommissionMaterialCode
        fields = ('code', 'description')


class LithologyHardnessSerializer(serializers.ModelSerializer):
    """Serializes lithology hardness options"""

    class Meta:
        model = LithologyHardnessCode
        fields = (
            'lithology_hardness_code',
            'description'
        )


class LithologyColourSerializer(serializers.ModelSerializer):
    """Serializes lithology colour options"""

    class Meta:
        model = LithologyColourCode
        fields = (
            'lithology_colour_code',
            'description'
        )


class LithologyMaterialSerializer(serializers.ModelSerializer):
    """Serializes lithology material options"""

    class Meta:
        model = LithologyMaterialCode
        fields = (
            'lithology_material_code',
            'description'
        )


class LithologyMoistureSerializer(serializers.ModelSerializer):
    """Serializes lithology moisture options"""

    class Meta:
        model = LithologyMoistureCode
        fields = (
            'lithology_moisture_code',
            'description'
        )


class WellStatusCodeSerializer(serializers.ModelSerializer):
    """ Serializes well status codes """

    class Meta:
        model = WellStatusCode
        fields = (
            'well_status_code', 'description'
        )


class ObservationWellStatusCodeSerializer(serializers.ModelSerializer):
    """ serializes observation well status codes """

    class Meta:
        model = ObsWellStatusCode
        fields = (
            'obs_well_status_code', 'description'
        )


class LithologyDescriptionCodeSerializer(serializers.ModelSerializer):
    """ serializes lithology descriptor codes """

    class Meta:
        model = LithologyDescriptionCode
        fields = (
            'lithology_description_code',
            'description',
        )
