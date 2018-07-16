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
from wells.models import (
    Well,
    ActivitySubmission
)

from gwells.serializers import AuditModelSerializer


class WellSubmissionSerializer(serializers.ModelSerializer):
    """Serializes a well activity submission"""

    class Meta:
        model = ActivitySubmission
        fields = (
            "filing_number",
            "activity_submission_guid",
            "well_tag_number",
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
        )
