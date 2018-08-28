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

from gwells.models import ProvinceStateCode
from gwells.serializers import AuditModelSerializer
from django.db import transaction

from wells.models import Well, ActivitySubmission
from wells.serializers import CasingSerializer
import wells.stack
from wells.models import (
    ActivitySubmission,
    DrillingMethodCode,
    Casing,
    IntendedWaterUseCode,
    GroundElevationMethodCode,
    SurfaceSealMaterialCode,
    SurfaceSealMethodCode,
    SurficialMaterialCode,
    Well,
    WellClassCode,
    WellSubclassCode,
    LandDistrictCode)

from submissions.models import WellActivityCode


class WellSubmissionSerializer(serializers.ModelSerializer):
    """Serializes a well activity submission"""

    casing_set = CasingSerializer(many=True, required=False)

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
        )

    @transaction.atomic
    def create(self, validated_data):
        casings_data = validated_data.pop('casing_set', None)
        instance = super().create(validated_data)
        if casings_data:
            for casing_data in casings_data:
                Casing.objects.create(
                    activity_submission=instance, **casing_data)
        # Update the well record
        stacker = wells.stack.StackWells()
        stacker.process(instance.filing_number)
        # The instance may have been updated with a well tag number
        instance.refresh_from_db()
        return instance


class WellActivityCodeSerializer(serializers.ModelSerializer):
    """ serializes well activity codes """

    class Meta:
        model = WellActivityCode
        fields = ('code', 'description')


class WellSubclassCodeSerializer(serializers.ModelSerializer):
    """ serializes well subclass codes """

    class Meta:
        model = WellSubclassCode
        fields = ('well_subclass_guid', 'well_subclass_code', 'description')


class WellClassCodeSerializer(serializers.ModelSerializer):
    """ serializes well class codes """

    wellsubclasscode_set = WellSubclassCodeSerializer(
        many=True, read_only=True)

    class Meta:
        model = WellClassCode
        fields = ('well_class_code', 'description', 'wellsubclasscode_set')


class IntendedWaterUseCodeSerializer(serializers.ModelSerializer):
    """ serializes intended water use codes """

    class Meta:
        model = IntendedWaterUseCode
        fields = ('intended_water_use_code', 'description')


class LandDistrictSerializer(serializers.ModelSerializer):
    """ serializes Land District codes/descriptions """

    class Meta:
        model = LandDistrictCode
        fields = ('land_district_code', 'name')


class GroundElevationMethodCodeSerializer(serializers.ModelSerializer):
    """ serializes codes for methods of obtaining ground elevations """

    class Meta:
        model = GroundElevationMethodCode
        fields = ('ground_elevation_method_code', 'description')


class DrillingMethodCodeSerializer(serializers.ModelSerializer):
    """ serializes drilling method codes """

    class Meta:
        model = DrillingMethodCode
        fields = ('drilling_method_code', 'description')


class SurfaceSealMethodCodeSerializer(serializers.ModelSerializer):
    """ serializes surface seal method codes """

    class Meta:
        model = SurfaceSealMethodCode
        fields = ('surface_seal_method_code', 'description')


class SurfaceSealMaterialCodeSerializer(serializers.ModelSerializer):
    """ serializes surface seal method codes """

    class Meta:
        model = SurfaceSealMaterialCode
        fields = ('surface_seal_material_code', 'description')


class SurficialMaterialCodeSerializer(serializers.ModelSerializer):
    """ serializes surficial material codes """

    class Meta:
        model = SurficialMaterialCode
        fields = ('surficial_material_code', 'description')
