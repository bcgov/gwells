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

from rest_framework import serializers
import logging

from gwells.models import ProvinceStateCode
from gwells.serializers import AuditModelSerializer
from django.db import transaction
import wells.stack
from wells.models import Well, ActivitySubmission, WellActivityCode
from wells.serializers import (
    CasingSerializer,
    DecommissionDescriptionSerializer,
    ScreenSerializer,
    LinerPerforationSerializer
)
from wells.models import (
    ActivitySubmission,
    Casing,
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
    YieldEstimationMethodCode,
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

    class Meta:
        fields = '__all__'
        model = ActivitySubmission


class WellSubmissionSerializerBase(serializers.ModelSerializer):
    """ Bass class for well submission serialisation. """

    def get_foreign_keys(self):
        raise NotImplementedError()  # Implement in base class!

    def get_well_activity_type(self):
        raise NotImplementedError()  # Implement in base class!

    @transaction.atomic
    def create(self, validated_data):
        # Pop foreign key records from validated data (we need to create them ourselves).
        foreign_keys = self.get_foreign_keys()
        foreign_keys_data = {}
        for key in foreign_keys.keys():
            foreign_keys_data[key] = validated_data.pop(key, None)
        # Create submission.
        validated_data['well_activity_type'] = self.get_well_activity_type()
        instance = super().create(validated_data)
        # Create foreign key records.
        for key, value in foreign_keys_data.items():
            if value:
                for data in value:
                    thing = foreign_keys[key].objects.create(
                        activity_submission=instance, **data)
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

    def get_foreign_keys(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
            'decommission_description_set': DecommissionDescription,
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

    def get_well_activity_type(self):
        return WellActivityCode.types.legacy()

    def get_foreign_keys(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
            'decommission_description_set': DecommissionDescription,
        }

    class Meta:
        model = ActivitySubmission
        extra_kwargs = {
            'lithologydescription_set': {'required': False},
            # This field might not be present
            'create_user': {'required': False},
            # This is autopopulated during create
            'well_activity_type': {'required': False},
        }
        fields = '__all__'


class WellConstructionSubmissionSerializer(WellSubmissionSerializerBase):
    """ Serializes a well construction submission. """

    casing_set = CasingSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    linerperforation_set = LinerPerforationSerializer(
        many=True, required=False)

    def get_foreign_keys(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
        }

    def get_well_activity_type(self):
        return WellActivityCode.types.construction()

    class Meta:
        model = ActivitySubmission
        fields = ('filing_number', 'well_activity_type', 'well', 'well_class', 'well_subclass',
                  'intended_water_use', 'identification_plate_number', 'well_plate_attached',
                  'work_start_date', 'work_end_date', 'owner_full_name', 'owner_mailing_address',
                  'owner_province_state', 'owner_city', 'owner_postal_code', 'street_address', 'city',
                  'legal_lot', 'legal_plan', 'legal_district_lot', 'legal_block', 'legal_section',
                  'legal_township', 'legal_range', 'land_district', 'legal_pid', 'well_location_description',
                  'latitude', 'longitude', 'ground_elevation', 'ground_elevation_method', 'drilling_method',
                  'other_drilling_method', 'well_orientation', 'lithologydescription_set', 'casing_set',
                  'surface_seal_material', 'surface_seal_depth', 'surface_seal_thickness',
                  'surface_seal_method', 'backfill_above_surface_seal', 'backfill_above_surface_seal_depth',
                  'liner_material', 'liner_diameter', 'liner_thickness', 'liner_from', 'liner_to',
                  'linerperforation_set', 'screen_intake_method', 'screen_type', 'screen_material',
                  'other_screen_material', 'screen_opening', 'screen_bottom', 'other_screen_bottom',
                  'screen_set', 'filter_pack_from', 'filter_pack_to', 'filter_pack_thickness',
                  'filter_pack_material', 'filter_pack_material_size', 'development_method',
                  'development_hours', 'development_notes', 'water_quality_characteristics',
                  'water_quality_colour', 'water_quality_odour', 'ems_id', 'total_depth_drilled',
                  'finished_well_depth', 'final_casing_stick_up', 'bedrock_depth', 'static_water_level',
                  'well_yield', 'artesian_flow', 'artesian_pressure', 'well_cap_type', 'well_disinfected',
                  'comments', 'alternative_specs_submitted', 'consultant_company', 'consultant_name',
                  'driller_name', 'driller_responsible',)
        extra_kwargs = {
            # TODO: reference appropriate serializer as above
            'lithologydescription_set': {'required': False},
            'well_activity_type': {'required': False}
        }


class WellAlterationSubmissionSerializer(WellSubmissionSerializerBase):
    """ Serializes a well alteration submission. """

    casing_set = CasingSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    linerperforation_set = LinerPerforationSerializer(
        many=True, required=False)

    def get_foreign_keys(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
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
            'well_plate_attached',
            'work_start_date',
            'work_end_date',
            'owner_full_name',
            'owner_mailing_address',
            'owner_province_state',
            'owner_city',
            'owner_postal_code',
            'street_address',
            'city',
            'consultant_company',
            'consultant_name',
            'driller_name',
            'driller_responsible',
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
            'drilling_method',
            'other_drilling_method',
            'well_orientation',
            'lithologydescription_set',
            'casing_set',
            'surface_seal_material',
            'surface_seal_depth',
            'surface_seal_thickness',
            'surface_seal_method',
            'backfill_above_surface_seal',
            'backfill_above_surface_seal_depth',
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
            'filter_pack_from',
            'filter_pack_to',
            'filter_pack_thickness',
            'filter_pack_material',
            'filter_pack_material_size',
            'development_method',
            'development_hours',
            'development_notes',
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
            'lithologydescription_set': {'required': False},
            'well_activity_type': {'required': False}
        }


class WellStaffEditSubmissionSerializer(WellSubmissionSerializerBase):

    well = serializers.PrimaryKeyRelatedField(queryset=Well.objects.all())

    def get_well_activity_type(self):
        return WellActivityCode.types.staff_edit()

    def get_foreign_keys(self):
        return {}

    class Meta:
        model = ActivitySubmission
        fields = (
            'well',
            'driller_name',
            'consultant_name',
            'consultant_company',
            'driller_responsible',
        )


class WellDecommissionSubmissionSerializer(WellSubmissionSerializerBase):
    """ Serializes a well decommission submission. """

    casing_set = CasingSerializer(many=True, required=False)
    decommission_description_set = DecommissionDescriptionSerializer(
        many=True, required=False)

    def get_well_activity_type(self):
        return WellActivityCode.types.decommission()

    def get_foreign_keys(self):
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
            'well_plate_attached',
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
            'drilling_method',
            'other_drilling_method',
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
