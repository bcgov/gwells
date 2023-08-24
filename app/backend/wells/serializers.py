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
from django.db import transaction
from django.core.validators import MinValueValidator

from gwells.models import ProvinceStateCode
from gwells.serializers import AuditModelSerializer
from aquifers.serializers import HYDRAULIC_SUBTYPES
from registries.serializers import PersonNameSerializer, OrganizationNameListSerializer
from wells.models import (
    ActivitySubmission,
    ActivitySubmissionLinerPerforation,
    AquiferLithologyCode,
    Casing,
    CasingMaterialCode,
    CasingCode,
    DecommissionDescription,
    DrillingMethodCode,
    LinerPerforation,
    LithologyDescription,
    Screen,
    Well,
    AquiferParameters
)
from submissions.models import WellActivityCode


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


class CasingSummarySerializer(serializers.ModelSerializer):
    """Serializes casings for well summary (using descriptions instead of codes)"""
    casing_material = serializers.ReadOnlyField(source='casing_material.description')
    casing_code = serializers.ReadOnlyField(source='casing_code.description')

    class Meta:
        model = Casing
        fields = (
            'start',
            'end',
            'diameter',
            'casing_code',
            'casing_material',
            'drive_shoe_status',
            'wall_thickness'
        )


class CasingSerializer(serializers.ModelSerializer):
    length_required = serializers.BooleanField(required=False)

    class Meta:
        model = Casing
        fields = (
            'start',
            'end',
            'length_required',
            'diameter',
            'casing_code',
            'casing_material',
            'drive_shoe_status',
            'wall_thickness'
        )
        extra_kwargs = {
            'start': {'required': False},
            'end': {'required': False},
            'diameter': {'required': True}
        }

    def to_representation(self, instance):
        """
        Fetch many details related to a aquifer, used to generate its' summary page.
        """

        ret = super().to_representation(instance)
        ret['length_required'] = instance.start is not None and instance.end is not None
        return ret

    def validate(self, data):
        """
        Check that start and end are set when the `requiredLength` parameter is true.
        """
        data = super().validate(data)

        if bool(data.get('length_required', True)):
            errors = {}
            start = data.get('start', None)
            end = data.get('end', None)
            if start == '' or start is None:
                errors['start'] = 'This field is required.'
            if end == '' or end is None:
                errors['end'] = 'This field is required.'
            if len(errors) != 0:
                raise serializers.ValidationError(errors)
        if 'length_required' in data:
            del data['length_required']
        return data


class CasingStackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casing
        fields = (
            'start',
            'end',
            'diameter',
            'casing_code',
            'casing_material',
            'drive_shoe_status',
            'wall_thickness',
            'create_user',
            'update_user'
        )
        extra_kwargs = {
            'start': {'required': True},
            'end': {'required': True},
            'diameter': {'required': True},
            'start': {'required': True},
            'end': {'required': True},
            'create_user': {'required': True},
            'update_user': {'required': True}
        }


class LegacyCasingSerializer(serializers.ModelSerializer):

    # Serializers without validators:
    start = serializers.DecimalField(max_digits=7, decimal_places=2, allow_null=True)
    end = serializers.DecimalField(max_digits=7, decimal_places=2, allow_null=True)
    diameter = serializers.DecimalField(max_digits=8, decimal_places=3, allow_null=True)
    wall_thickness = serializers.DecimalField(max_digits=6, decimal_places=3, allow_null=True)

    class Meta:
        model = Casing
        fields = (
            'start',
            'end',
            'diameter',
            'casing_code',
            'casing_material',
            'drive_shoe_status',
            'wall_thickness'
        )
        extra_kwargs = {
            'start': {'required': False},
            'end': {'required': False},
            'diameter': {'required': False},
            'casing_code': {'required': False},
            'casing_material': {'required': False},
            'drive_shoe_status': {'required': False, 'allow_null': True},
            'wall_thickness': {'required': False}
        }


class AquiferParametersSerializer(serializers.ModelSerializer):
    """Serializes aquifer parameters for well"""
    class Meta:
        model = AquiferParameters
        fields = (
            'testing_number',
            'well',
            'start_date_pumping_test',
            'pumping_test_description',
            'test_duration',
            'boundary_effect',
            'storativity',
            'transmissivity',
            'hydraulic_conductivity',
            'specific_yield',
            'specific_capacity',
            'analysis_method',
            'comments'
        )


class AquiferParametersSummarySerializer(serializers.ModelSerializer):
    """Serializes aquifer parameters for well summary"""
    class Meta:
        model = AquiferParameters
        fields = (
            'testing_number',
            'well',
            'start_date_pumping_test',
            'pumping_test_description',
            'test_duration',
            'boundary_effect',
            'storativity',
            'transmissivity',
            'hydraulic_conductivity',
            'specific_yield',
            'specific_capacity',
            'analysis_method',
            'comments'
        )

class AquiferParametersStackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AquiferParameters
        fields = (
            'testing_number',
            'well',
            'start_date_pumping_test',
            'pumping_test_description',
            'test_duration',
            'boundary_effect',
            'storativity',
            'transmissivity',
            'hydraulic_conductivity',
            'specific_yield',
            'specific_capacity',
            'analysis_method',
            'comments',
            'create_user',
            'update_user'
        )
        extra_kwargs = {
            'create_user': {'required': True},
            'update_user': {'required': True}
        }

class DecommissionDescriptionSerializer(serializers.ModelSerializer):
    """Serializes Decommission Descriptions"""

    class Meta:
        model = DecommissionDescription
        fields = (
            'start',
            'end',
            'material',
            'observations'
        )
        extra_kwargs = {
            'start': {'required': True},
            'end': {'required': True},
        }


class DecommissionDescriptionStackerSerializer(serializers.ModelSerializer):
    """Serializes Decommission Descriptions"""

    class Meta:
        model = DecommissionDescription
        fields = (
            'start',
            'end',
            'material',
            'observations',
            'create_user',
            'update_user'
        )
        extra_kwargs = {
            'start': {'required': True},
            'end': {'required': True},
            'create_user': {'required': True},
            'update_user': {'required': True}
        }


class LegacyDecommissionDescriptionSerializer(serializers.ModelSerializer):
    """Serializes Decommission Descriptions"""

    class Meta:
        model = DecommissionDescription
        fields = (
            'start',
            'end',
            'material',
            'observations'
        )
        extra_kwargs = {
            'start': {'required': False},
            'end': {'required': False},
        }


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = (
            'start',
            'end',
            'diameter',
            'assembly_type',
            'slot_size',
        )
        extra_kwargs = {
            'start': {'required': True},
            'end': {'required': True},
            'assembly_type': {'required': True}
        }


class ScreenStackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = (
            'start',
            'end',
            'diameter',
            'assembly_type',
            'slot_size',
            'create_user',
            'update_user'
        )
        extra_kwargs = {
            'start': {'required': True},
            'end': {'required': True},
            'assembly_type': {'required': True},
            'create_user': {'required': True},
            'update_user': {'required': True}
        }


class LegacyScreenSerializer(serializers.ModelSerializer):

    start = serializers.DecimalField(max_digits=7, decimal_places=2, allow_null=True)
    end = serializers.DecimalField(max_digits=7, decimal_places=2, allow_null=True)
    diameter = serializers.DecimalField(max_digits=7, decimal_places=2, allow_null=True)
    slot_size = serializers.DecimalField(max_digits=7, decimal_places=2, allow_null=True)

    class Meta:
        model = Screen
        fields = (
            'start',
            'end',
            'diameter',
            'assembly_type',
            'slot_size',
        )
        extra_kwargs = {
            'start': {'required': False},
            'end': {'required': False},
            'assembly_type': {'required': False}
        }


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


class LinerPerforationStackerSerializer(serializers.ModelSerializer):
    """ This serializer is used for data->perforation(on well) and perforation(on well)->data.
    """
    class Meta:
        model = LinerPerforation
        fields = (
            # SUPER IMPORTANT: Don't include ID (liner_perforation_guid, well, or submission) as part of this
            # serializer, as it will break the stacking code. If you include the guid, then it will remain
            # stuck on a particular well/submission (unless I gues you pop it during serializing/
            # deserializing) when creating legacy submissions or re-creating well records etc.
            'start',
            'end',
            'create_user',
            'update_user'
        )
        extra_kwargs = {
            'create_user': {'required': True},
            'update_user': {'required': True}
        }


class ActivitySubmissionLinerPerforationSerializer(serializers.ModelSerializer):
    """ This serializer is used for data->perforation(on submission) and perforation(on submission)->data.
    """
    class Meta:
        model = ActivitySubmissionLinerPerforation
        fields = (
            # SUPER IMPORTANT: Don't include ID (liner_perforation_guid, well, or submission) as part of this
            # serializer, as it will break the stacking code. If you include the guid, then it will remain
            # stuck on a particular well/submission (unless I gues you pop it during serializing/
            # deserializing) when creating legacy submissions or re-creating well records etc.
            'start',
            'end',
        )


class LegacyLinerPerforationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitySubmissionLinerPerforation
        fields = (
            # SUPER IMPORTANT: Don't include ID (liner_perforation_guid, well, or submission) as part of this
            # serializer, as it will break the stacking code. If you include the guid, then it will remain
            # stuck on a particular well/submission (unless I gues you pop it during serializing/
            # deserializing) when creating legacy submissions or re-creating well records etc.
            'start',
            'end',
        )

        extra_kwargs = {
            'start': {'required': False},
            'end': {'required': False},
        }


class LithologyDescriptionSummarySerializer(serializers.ModelSerializer):
    """Serializes lithology description records for the well summary, using descriptions instead of codes"""

    lithology_description = serializers.ReadOnlyField(source='lithology_description.description')
    lithology_colour = serializers.ReadOnlyField(source='lithology_colour.description')
    lithology_hardness = serializers.ReadOnlyField(source='lithology_hardness.description')
    lithology_moisture = serializers.ReadOnlyField(source='lithology_moisture.description')

    class Meta:
        model = LithologyDescription
        fields = (
            'start',
            'end',
            'lithology_raw_data',
            'lithology_colour',
            'lithology_hardness',
            'lithology_moisture',
            'lithology_description',
            'lithology_observation',
            'water_bearing_estimated_flow',
        )


class LithologyDescriptionSerializer(serializers.ModelSerializer):

    start = serializers.DecimalField(
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))])
    end = serializers.DecimalField(
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))])

    """Serializes lithology description records"""
    class Meta:
        model = LithologyDescription
        fields = (
            'start',
            'end',
            'lithology_raw_data',
            'lithology_colour',
            'lithology_hardness',
            'lithology_moisture',
            'lithology_description',
            'lithology_observation',
            'water_bearing_estimated_flow',
        )


class LithologyDescriptionStackerSerializer(serializers.ModelSerializer):

    start = serializers.DecimalField(
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))])
    end = serializers.DecimalField(
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))])

    """Serializes lithology description records"""
    class Meta:
        model = LithologyDescription
        fields = (
            'start',
            'end',
            'lithology_raw_data',
            'lithology_colour',
            'lithology_hardness',
            'lithology_moisture',
            'lithology_description',
            'lithology_observation',
            'water_bearing_estimated_flow',
            'create_user',
            'update_user'
        )
        extra_kwargs = {
            'start': {'required': True},
            'end': {'required': True},
            'create_user': {'required': True},
            'update_user': {'required': True}
        }


class LegacyLithologyDescriptionSerializer(serializers.ModelSerializer):

    end = serializers.DecimalField(max_digits=7, decimal_places=2, allow_null=True)

    """Serializes lithology description records"""
    class Meta:
        model = LithologyDescription
        fields = (
            'start',
            'end',
            'lithology_raw_data',
            'lithology_colour',
            'lithology_hardness',
            'lithology_moisture',
            'lithology_description',
            'lithology_observation',
            'water_bearing_estimated_flow',
        )
        extra_kwargs = {
            'end': {'required': False, 'allow_null': True},
        }


class DrillingMethodSummarySerializer(serializers.ModelSerializer):
    """ serializes drilling methods for well summary display """
    class Meta:
        model = DrillingMethodCode
        fields = ('description',)


class WellDetailSerializer(AuditModelSerializer):
    casing_set = CasingSummarySerializer(many=True)
    aquifer_parameters_set = AquiferParametersSummarySerializer(many=True)
    screen_set = ScreenSerializer(many=True)
    linerperforation_set = LinerPerforationSerializer(many=True)
    decommission_description_set = DecommissionDescriptionSerializer(many=True)
    person_responsible = PersonNameSerializer()
    company_of_person_responsible = OrganizationNameListSerializer()
    lithologydescription_set = LithologyDescriptionSummarySerializer(many=True)
    drilling_methods = DrillingMethodSummarySerializer(many=True)

    # well vs. well_tag_number ; on submissions, we refer to well
    well = serializers.IntegerField(source='well_tag_number')

    # convert codes to their human-readable descriptions
    well_class = serializers.ReadOnlyField(source='well_class.description')
    well_subclass = serializers.ReadOnlyField(source='well_subclass.description')
    intended_water_use = serializers.ReadOnlyField(source='intended_water_use.description')
    well_status = serializers.ReadOnlyField(source='well_status.description')
    well_publication_status = serializers.ReadOnlyField(source='well_publication_status.description')
    licenced_status = serializers.ReadOnlyField(source='licenced_status.description')
    coordinate_acquisition_code = serializers.ReadOnlyField(source='coordinate_acquisition_code.description')
    intended_water_use = serializers.ReadOnlyField(source='intended_water_use.description')
    ground_elevation_method = serializers.ReadOnlyField(source='ground_elevation_method.description')
    surface_seal_material = serializers.ReadOnlyField(source='surface_seal_material.description')
    surface_seal_method = serializers.ReadOnlyField(source='surface_seal_method.description')
    liner_material = serializers.ReadOnlyField(source='liner_material.description')
    screen_intake_method = serializers.ReadOnlyField(source='screen_intake_method.description')
    screen_type = serializers.ReadOnlyField(source='screen_type.description')
    screen_material = serializers.ReadOnlyField(source='screen_material.description')
    screen_opening = serializers.ReadOnlyField(source='screen_opening.description')
    screen_bottom = serializers.ReadOnlyField(source='screen_bottom.description')
    alternative_specs_submitted = serializers.ReadOnlyField(source='get_alternative_specs_submitted_display')
    drilling_company = serializers.ReadOnlyField(source='company_of_person_responsible.org_guid')
    company_of_person_responsible = serializers.ReadOnlyField(source='company_of_person_responsible.org_guid')

    submission_work_dates = serializers.SerializerMethodField()

    legal_pid = serializers.SerializerMethodField()

    is_published = serializers.SerializerMethodField()

    def get_legal_pid(self, instance):
        if instance.legal_pid is None:
            return instance.legal_pid
        return "{0:0>9}".format(instance.legal_pid)

    def get_submission_work_dates(self, instance):
        records = instance.activitysubmission_set \
            .exclude(well_activity_type='STAFF_EDIT') \
            .order_by('create_date')

        records = sorted(records, key=lambda record:
                         (record.well_activity_type.code != WellActivityCode.types.legacy().code,
                          record.well_activity_type.code != WellActivityCode.types.construction().code,
                          record.create_date), reverse=True)

        return SubmissionWorkDatesByWellSerializer(records, many=True).data

    def get_is_published(self, instance):
        return instance.well_publication_status.well_publication_status_code == 'Published'

    class Meta:
        ref_name = "well_detail_v1"
        model = Well
        fields = (
            "well_guid",
            "well",
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
            "well_publication_status",
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
            "person_responsible",
            "driller_name",
            "drilling_company", # old name for company_of_person_responsible
            "company_of_person_responsible",
            "consultant_name",
            "consultant_company",
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
            "artesian_pressure_head",
            "artesian_conditions",
            "well_cap_type",
            "well_disinfected_status",
            "comments",
            "alternative_specs_submitted",
            "technical_report",
            "drinking_water_protection_area_ind",
            "well_yield_unit",
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
            "casing_set",
            "aquifer_parameters_set",
            "screen_set",
            "linerperforation_set",
            "decommission_description_set",
            "lithologydescription_set",
            "submission_work_dates",
            "is_published",
        )


class SubmissionReportsByWellSerializer(serializers.ModelSerializer):
    """ serializes a list of submission reports for a given well, with basic info about each report """

    well_activity_description = serializers.ReadOnlyField(
        source='well_activity_type.description')

    class Meta:
        model = ActivitySubmission
        fields = ("well", "well_activity_type", "create_user",
                  "create_date", "well_activity_description", "filing_number")


class SubmissionWorkDatesByWellSerializer(serializers.ModelSerializer):
    """ serializes a list of submission report work done information """

    well_activity_description = serializers.ReadOnlyField(
        source='well_activity_type.description')
    drilling_company = serializers.ReadOnlyField(
        source='company_of_person_responsible.name')

    class Meta:
        model = ActivitySubmission
        fields = ("well", "create_date", "well_activity_description",
                  "work_start_date", "work_end_date", "drilling_company")


class WellDetailAdminSerializer(AuditModelSerializer):
    casing_set = CasingSerializer(many=True)
    aquifer_parameters_set = AquiferParametersSerializer(many=True)
    screen_set = ScreenSerializer(many=True)
    linerperforation_set = LinerPerforationSerializer(many=True)
    decommission_description_set = DecommissionDescriptionSerializer(many=True)
    person_responsible = PersonNameSerializer()
    company_of_person_responsible = OrganizationNameListSerializer()
    lithologydescription_set = LithologyDescriptionSerializer(many=True)
    submission_reports = serializers.SerializerMethodField()

    # well vs. well_tag_number ; on submissions, we refer to well
    well = serializers.IntegerField(source='well_tag_number')

    legal_pid = serializers.SerializerMethodField()

    is_published = serializers.SerializerMethodField()

    class Meta:
        model = Well
        fields = '__all__'
        extra_fields = ['latitude', 'longitude']

    def get_legal_pid(self, instance):
        if instance.legal_pid is None:
            return instance.legal_pid
        return "{0:0>9}".format(instance.legal_pid)

    # this allows us to call model methods on top of __all__
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(WellDetailAdminSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def get_submission_reports(self, instance):
        records = instance.activitysubmission_set \
            .exclude(well_activity_type='STAFF_EDIT') \
            .order_by('create_date')

        records = sorted(records, key=lambda record:
                         (record.well_activity_type.code != WellActivityCode.types.legacy().code,
                          record.well_activity_type.code != WellActivityCode.types.construction().code,
                          record.create_date), reverse=True)

        return SubmissionReportsByWellSerializer(records, many=True).data

    def get_is_published(self, instance):
        return instance.well_publication_status.well_publication_status_code == 'Published'


class WellStackerSerializer(AuditModelSerializer):
    casing_set = CasingStackerSerializer(many=True)
    aquifer_parameters_set = AquiferParametersStackerSerializer(many=True)
    screen_set = ScreenStackerSerializer(many=True)
    linerperforation_set = LinerPerforationStackerSerializer(many=True)
    decommission_description_set = DecommissionDescriptionStackerSerializer(many=True)
    lithologydescription_set = LithologyDescriptionStackerSerializer(many=True)
    # Audit fields have to be added explicitly, because they are on a base class
    update_user = serializers.CharField(required=True)
    create_user = serializers.CharField(required=True)
    update_date = serializers.DateTimeField()

    class Meta:
        model = Well
        fields = '__all__'

    @transaction.atomic
    def update(self, instance, validated_data):
        # If there is existing related data, the easiest approach is to drop it, and re-create many to
        # many fields based on this update. Trying to match up individual records and updating them,
        # dealing with removed casing/screen/perforation records etc. etc. is not the responsibility
        # of this section. The composite section is responsible for that.
        FOREIGN_KEYS = {
            'casing_set': Casing,
            'aquifer_parameters_set': AquiferParameters,
            'screen_set': Screen,
            'linerperforation_set': LinerPerforation,
            'decommission_description_set': DecommissionDescription,
            'lithologydescription_set': LithologyDescription,
        }

        for key in FOREIGN_KEYS.keys():
            # Is the field one to many, or many to many?
            model = type(self).Meta.model
            field = model._meta.get_field(key)
            records_data = validated_data.pop(key, None)
            foreign_class = FOREIGN_KEYS[key]
            if field.one_to_many:
                # We just delete the one to many records. It would be too complicated to match them up.
                for record in getattr(instance, key).all():
                    record.delete()
                if records_data:
                    for record_data in records_data:
                        # We're re-creating this record, and binding it to the current instance, so we need
                        # to get rid of any redundant/duplicate reference that may exist in the record data
                        # in order to avoid duplications. (the well we pop, should be the same as the instance
                        # variable)
                        record_data.pop('well', None)
                        # Create new instance of of the casing/screen/whatever record.
                        obj = foreign_class.objects.create(
                            well=instance, **record_data)
            else:
                raise 'UNEXPECTED FIELD! {}'.format(field)
        instance = super().update(instance, validated_data)
        return instance


class WellListSerializerV1(serializers.ModelSerializer):
    """Serializes a well record"""

    legal_pid = serializers.SerializerMethodField()
    drilling_company = serializers.ReadOnlyField(
        source='company_of_person_responsible.org_guid')
    company_of_person_responsible = serializers.ReadOnlyField(
        source='company_of_person_responsible.org_guid')
    licenced_status = serializers.ReadOnlyField(source='licenced_status.licenced_status_code')

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
        )


class WellListAdminSerializerV1(WellListSerializerV1):

    class Meta:
        model = Well
        fields = WellListSerializerV1.Meta.fields + (
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


class WellExportSerializerV1(WellListSerializerV1):
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


class WellExportAdminSerializerV1(WellExportSerializerV1):
    """Serializes a well for export (using display names for codes, etc)"""
    owner_province_state = serializers.SlugRelatedField(read_only=True,
                                                        slug_field='description')
    well_publication_status = serializers.SlugRelatedField(read_only=True,
                                                           slug_field='description')

    class Meta:
        model = Well
        fields = WellListAdminSerializerV1.Meta.fields


class WellTagSearchSerializer(serializers.ModelSerializer):
    """ serializes fields used for searching for well tags """

    class Meta:
        model = Well
        fields = ("well_tag_number", "owner_full_name")


class WellLocationSerializerV1(serializers.ModelSerializer):
    """ serializes well locations v1 """

    class Meta:
        model = Well
        fields = ("well_tag_number", "identification_plate_number",
                  "latitude", "longitude", "street_address", "city")


class WellDrawdownSerializer(serializers.ModelSerializer):
    screen_set = ScreenSerializer(many=True)
    intended_water_use = serializers.ReadOnlyField(source='intended_water_use.description')
    aquifer_subtype = serializers.ReadOnlyField(source='aquifer.subtype.description')
    distance = serializers.FloatField(required=False)

    class Meta:
        model = Well
        fields = (
            "well_tag_number",
            "static_water_level",
            "screen_set",
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
            "aquifer_subtype"
        )

    def to_representation(self, instance):
        details = super().to_representation(instance)
        if instance.aquifer and instance.aquifer.subtype:
            details['aquifer_hydraulically_connected'] = instance.aquifer.subtype.code in HYDRAULIC_SUBTYPES
        return details


class WellLithologySerializer(serializers.ModelSerializer):
    lithologydescription_set = LithologyDescriptionSummarySerializer(many=True)

    class Meta:
            model = Well
            fields = (
                "well_tag_number",
                "latitude",
                "longitude",
                "lithologydescription_set"
            )
