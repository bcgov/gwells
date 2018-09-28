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
from wells.models import Well, ActivitySubmission
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

from submissions.models import WellActivityCode

logger = logging.getLogger(__name__)


class WellSubmissionSerializer(serializers.ModelSerializer):
    """Serializes a well activity submission"""

    casing_set = CasingSerializer(many=True, required=False)
    decommission_description_set = DecommissionDescriptionSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    linerperforation_set = LinerPerforationSerializer(many=True, required=False)

    class Meta:
        model = ActivitySubmission
        fields = (
            "filing_number",
            "activity_submission_guid",
            "well",
            "well_activity_type",
            "well_class",
            "well_subclass",
            "intended_water_use",
            "driller_responsible",
            "driller_name",
            "consultant_name",
            "consultant_company",
            "work_start_date",
            "work_end_date",
            "owner_full_name",
            "owner_mailing_address",  # temporarily disabled
            "owner_city",
            "owner_province_state",
            "owner_postal_code",
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
            "identification_plate_number",
            "well_plate_attached",
            "latitude",
            "longitude",
            "ground_elevation",
            "ground_elevation_method",
            "drilling_method",
            "other_drilling_method",
            "water_supply_system_name",
            "water_supply_system_well_name",
            "surface_seal_material",
            "surface_seal_depth",
            "surface_seal_thickness",
            "surface_seal_method",
            "backfill_above_surface_seal",
            "backfill_above_surface_seal_depth",
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
            "filter_pack_from",
            "filter_pack_to",
            "filter_pack_thickness",
            "filter_pack_material",
            "filter_pack_material_size",
            "development_method",
            "development_hours",
            "development_notes",
            "water_quality_characteristics",
            "water_quality_colour",
            "water_quality_odour",
            "total_depth_drilled",
            "finished_well_depth",
            "final_casing_stick_up",
            "bedrock_depth",
            "static_water_level",
            "well_yield",
            "artesian_flow",
            "artesian_pressure",
            "well_cap_type",
            "well_disinfected",
            "comments",
            "alternative_specs_submitted",
            "well_yield_unit",
            "diameter",
            "casing_set",
            "linerperforation_set",
            "screen_set",
            "decommission_reason",
            "decommission_method",
            "sealant_material",
            "backfill_material",
            "decommission_details",
        )

    @transaction.atomic
    def create(self, validated_data):
        # Pop foreign key records
        FOREIGN_KEYS = {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
            'decommission_description_set': DecommissionDescription,
        }
        foreign_keys_data = {}
        for key in FOREIGN_KEYS.keys():
            foreign_keys_data[key] = validated_data.pop(key, None)
        # Create submission
        instance = super().create(validated_data)
        # Create foreign key records
        for key, value in foreign_keys_data.items():
            if value:
                for data in value:
                    FOREIGN_KEYS[key].objects.create(activity_submission=instance, **data)
        # Update the well record
        stacker = wells.stack.StackWells()
        stacker.process(instance.filing_number)
        # The instance may have been updated with a well tag number
        instance.refresh_from_db()
        return instance


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
