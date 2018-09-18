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

from rest_framework import serializers
from django.db import transaction
from gwells.models import ProvinceStateCode
from gwells.serializers import AuditModelSerializer
from wells.models import (
    ActivitySubmission,
    Casing,
    CasingMaterialCode,
    CasingCode,
    LinerPerforation,
    Screen,
    Well,
)


logger = logging.getLogger(__name__)


class CasingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CasingMaterialCode
        fields = (
            'code',
            'description'
        )


class CasingCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CasingCode
        fields = (
            'code',
            'description',
        )


class CasingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casing
        fields = (
            'start',
            'end',
            'diameter',
            'casing_code',
            'casing_material',
            'drive_shoe',
        )


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = (
            'start',
            'end',
            'internal_diameter',
            'assembly_type',
            'slot_size',
        )


class LinerPerforationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinerPerforation
        fields = (
            # SUPER IMPORTANT: Don't include ID (liner_perforation_guid, well, or submission) as part of this
            # serializer, as it will break the stacking code. If you include the guid, then it will remain
            # stuck on a particular well/submission (unless I gues you pop it during serializing/
            # deserializing) when creating legacy submissions or re-creating well records etc.
            'start',
            'end',
        )


class WellStackerSerializer(AuditModelSerializer):

    casing_set = CasingSerializer(many=True)
    screen_set = ScreenSerializer(many=True)
    linerperforation_set = LinerPerforationSerializer(many=True)

    class Meta:
        model = Well
        fields = '__all__'

    @transaction.atomic
    def update(self, instance, validated_data):
        # If there is existing related data, the easiest approach is to drop it, and re-create it
        # based on this update. Trying to match up individual records and updating them, dealing with
        # removed casing/screen/perforation records etc. etc. is not the responsibility of this section.
        # The composite section is responsible for that.
        FOREIGN_KEYS = {'casing_set': Casing, 'screen_set': Screen, 'linerperforation_set': LinerPerforation}        
        for key in FOREIGN_KEYS.keys():
            for record in getattr(instance, key).all():
                record.delete()
            records_data = validated_data.pop(key, None)
            if records_data:
                for record_data in records_data:
                    # We're re-creating this record, and binding it to the current instance, so we need
                    # to get rid of any redundant/duplicate reference that may exist in the record data
                    # in order to avoid duplications. (the well we pop, should be the same as the instance
                    # variable)
                    record_data.pop('well', None)
                    # Create new instance of of the casing/screen/whatever record.
                    obj = FOREIGN_KEYS[key].objects.create(well=instance, **record_data)
        instance = super().update(instance, validated_data)
        return instance


class WellListSerializer(serializers.ModelSerializer):
    """Serializes a well record"""

    class Meta:
        model = Well
        fields = (
            "well_guid",
            "well_tag_number",
            "identification_plate_number",
            "owner_full_name",
            # "owner_mailing_address", # temporarily disabled - required for staff, hidden for public
            # "owner_city",
            # "owner_province_state",
            # "owner_postal_code",
            "well_class",
            "well_subclass",
            "intended_water_use",
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
            "alteration_end_date",
            "decommission_start_date",
            "decommission_end_date",
            "drilling_company",
            "well_identification_plate_attached",
            "latitude",
            "longitude",
            "ground_elevation",
            "ground_elevation_method",
            "drilling_method",
            "other_drilling_method",
            "well_orientation",
            "surface_seal_material",
            "surface_seal_length",
            "surface_seal_thickness",
            "surface_seal_method",
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
            "water_supply_system_name",
            "water_supply_system_well_name",
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
            "observation_well_number",
            "observation_well_status",
            "ems",
            "utm_zone_code",
            "utm_northing",
            "utm_easting",
            "utm_accuracy_code",
            "bcgs_id",
            "decommission_reason",
            "decommission_method",
            "sealant_material",
            "backfill_material",
            "decommission_details",
        )


class WellTagSearchSerializer(serializers.ModelSerializer):
    """ serializes fields used for searching for well tags """

    class Meta:
        model = Well
        fields = ("well_tag_number", "owner_full_name")
