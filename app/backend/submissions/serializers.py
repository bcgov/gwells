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
from django.contrib.gis.geos import Point

from rest_framework import exceptions

from gwells.models import ProvinceStateCode
from gwells.serializers import AuditModelSerializer
import wells.stack

from registries.serializers import PersonNameSerializer, OrganizationNameListSerializer

from gwells.models.lithology import (
    LithologyColourCode, LithologyHardnessCode,
    LithologyMaterialCode, LithologyMoistureCode, LithologyDescriptionCode)

from wells.models import Well, ActivitySubmission, FieldsProvided
from wells.serializers import (
    ActivitySubmissionLinerPerforationSerializer,
    CasingSerializer,
    DecommissionDescriptionSerializer,
    LegacyCasingSerializer,
    LegacyDecommissionDescriptionSerializer,
    LegacyLinerPerforationSerializer,
    LegacyLithologyDescriptionSerializer,
    LegacyScreenSerializer,
    LinerPerforationSerializer,
    LithologyDescriptionSerializer,
    ScreenSerializer,
)
from wells.models import (
    ActivitySubmission,
    ActivitySubmissionLinerPerforation,
    Casing,
    CoordinateAcquisitionCode,
    DecommissionDescription,
    DecommissionMaterialCode,
    DecommissionMethodCode,
    DevelopmentMethodCode,
    DrillingMethodCode,
    WellDisinfectedCode,
    WellOrientationCode,
    BoundaryEffectCode,
    DriveShoeCode,
    FilterPackMaterialCode,
    FilterPackMaterialSizeCode,
    GroundElevationMethodCode,
    IntendedWaterUseCode,
    LandDistrictCode,
    LicencedStatusCode,
    LinerMaterialCode,
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
    WellPublicationStatusCode,
    WellYieldUnitCode,
    YieldEstimationMethodCode,
    ObsWellStatusCode,
    AquiferLithologyCode,
)

from .models import WellActivityCode


logger = logging.getLogger(__name__)


class WellSubmissionListSerializer(serializers.ModelSerializer):
    """ Class used for listing well submissions.
    """
    well_activity_description = serializers.ReadOnlyField(
        source='well_activity_type.description')
    casing_set = CasingSerializer(many=True, required=False)
    decommission_description_set = DecommissionDescriptionSerializer(
        many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    linerperforation_set = LinerPerforationSerializer(
        many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(
        many=True, required=False)

    class Meta:
        fields = '__all__'
        model = ActivitySubmission


class WellSubmissionSerializerBase(AuditModelSerializer):
    """ Base class for well submission serialisation. """

    create_user = serializers.ReadOnlyField()
    create_date = serializers.ReadOnlyField()
    update_user = serializers.ReadOnlyField()
    update_date = serializers.ReadOnlyField()

    def get_foreign_key_sets(self):
        raise NotImplementedError()  # Implement in base class!

    def get_well_activity_type(self):
        raise NotImplementedError()  # Implement in base class!

    def validate(self, attrs):
        # Legacy records have inconsistent data, but we can't stop new submissions
        # or edits based on past data issues.  Stricter validation will be applied to
        # records submitted through GWELLS.
        if isinstance(self, WellSubmissionLegacySerializer):
            return attrs

        errors = {}

        if attrs.get('well_class'):
            if attrs.get('well_class').well_class_code == 'WATR_SPPLY':
                if not attrs.get('intended_water_use'):
                    errors['intended_water_use'] = 'Intended water use is required when the well class is Water Supply.'
            else:
                if attrs.get('intended_water_use') and attrs.get('intended_water_use').intended_water_use_code != 'NA':
                    errors['intended_water_use'] = 'Intended water use only valid for a well class of Water Supply.'

        # Check ground elevation fields for mutual requirement
        if 'ground_elevation' in attrs or 'ground_elevation_method' in attrs:
            if attrs.get('ground_elevation', None) is None and attrs.get('ground_elevation_method', None) is not None:
                if attrs['ground_elevation_method'].description != 'Unknown':
                    errors['ground_elevation'] = 'Both ground elevation and method are required.'
            if attrs.get('ground_elevation', None) is not None and attrs.get('ground_elevation_method', None) is None:
                errors['ground_elevation_method'] = 'Both ground elevation and method are required.'

        # Check latitude longitude for mutual requirement
        # lat/lng are on the request body, not the "attrs" object
        # this is assumed to be because lat/long are not model properties, since we
        # convert them to "geom" instead of storing them as latitude and longitude.
        data = None
        if self.context.get('request', None):
            data = self.context['request'].data

        if data.get('latitude') and data.get('longitude'):
            lat = float(data['latitude'])
            lng = float(data['longitude'])
            # there is also validation elsewhere that the point is inside BC.
            # this is a second sanity check to make sure the coordinates are roughly valid.
            if not 48 < lat < 60:
                errors['latitude'] = 'Coordinates are outside British Columbia.  Please double check well location.'
            if not -140 < -abs(lng) < -110:
                errors['longitude'] = 'Coordinates are outside British Columbia.  Please double check well location.'

        # date validation checks mutual requirement and start date less than end date
        dates = ['work', 'construction', 'alteration', 'decommission']
        for i in range(len(dates)):
            start_date = dates[i] + '_start_date'
            end_date = dates[i] + '_end_date'
            if start_date in attrs or end_date in attrs:
                s = attrs.get(start_date, None)
                e = attrs.get(end_date, None)
                if s is None and e is None:
                    continue
                if s is None or e is None:
                    errors[start_date] = 'Both ' + dates[i] + ' start date and end date are required.'
                else:
                    if s > e:
                        errors[start_date] = dates[i] + ' start date must be before end date'

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        try:
            # Pop foreign key records from validated data (we need to create them ourselves).
            foreign_keys = self.get_foreign_key_sets()
            foreign_keys_data = {}
            for key in foreign_keys.keys():
                foreign_keys_data[key] = validated_data.pop(key, None)
            # Create submission.
            validated_data['well_activity_type'] = self.get_well_activity_type()

            data = None

            if self.context.get('request', None):
                data = self.context['request'].data

                # Convert lat long values into geom object stored on model
                # Values are BC Albers. but we are using WGS84 Lat Lon to avoid rounding errors
                if 'latitude' in data and 'longitude' in data:
                    if not data.get('latitude') and not data.get('longitude'):
                        validated_data['geom'] = None
                        data['geom'] = None
                    else:
                        point = Point(-abs(data['longitude']), data['latitude'], srid=4326)
                        validated_data['geom'] = point
                        data['geom'] = point

            # Remove the latitude and longitude fields if they exist
            validated_data.pop('latitude', None)
            validated_data.pop('longitude', None)

            # If the yield_estimation_rate is specified, we default to USGPM
            if validated_data.get('yield_estimation_rate', None) and \
                    not validated_data.get('well_yield_unit', None):
                validated_data['well_yield_unit'] = WellYieldUnitCode.objects.get(
                    well_yield_unit_code='USGPM')

            instance = super().create(validated_data)

            # keep a map of the fields that were provided in the activity report submission
            if data and self.get_well_activity_type() == WellActivityCode.types.staff_edit():
                edited_fields_data = {k: True for k in data.keys() if k in [field.name for field in FieldsProvided._meta.get_fields()]}
                edited_fields = FieldsProvided(activity_submission=instance, **edited_fields_data)
                edited_fields.save()

            # Create foreign key records.
            for key, value in foreign_keys_data.items():
                if value:
                    model = type(self).Meta.model
                    field = model._meta.get_field(key)
                    foreign_class = foreign_keys[key]
                    if field.one_to_many:
                        for data in value:
                            # Usually audit information is injected by the view, but the view doesn't
                            # know about these associated records.
                            data['create_user'] = validated_data['create_user']
                            data['update_user'] = validated_data['update_user']
                            foreign_class.objects.create(
                                activity_submission=instance, **data)
                    else:
                        raise 'UNEXPECTED FIELD! {}'.format(field)
        except exceptions.ValidationError as e:
            # We don't bubble validation errors on the legacy submission up. It just causes confusion!
            # If there's a validation error on this level, it has to go up as a 500 error. Validation
            # error here, means we are unable to create a legacy record using old well data. The
            # users can't do anything to fix this, we have to fix a bug!
            if isinstance(self, WellSubmissionLegacySerializer):
                logger.error(e, exc_info=True)
                raise APIException()
            else:
                raise
        # Update the well record.
        stacker = wells.stack.StackWells()
        stacker.process(instance.filing_number)
        # The instance may have been updated with a well tag number, so we refresh.
        instance.refresh_from_db()
        return instance


class WellSubmissionLegacySerializer(WellSubmissionSerializerBase):
    """ Class with no validation, and all possible fields, used by stacker to create legacy records """

    casing_set = LegacyCasingSerializer(many=True, required=False)
    screen_set = LegacyScreenSerializer(many=True, required=False)
    linerperforation_set = LegacyLinerPerforationSerializer(
        many=True, required=False)
    decommission_description_set = LegacyDecommissionDescriptionSerializer(
        many=True, required=False)
    lithologydescription_set = LegacyLithologyDescriptionSerializer(
        many=True, required=False)
    # It seems that all the audit fields have to be explicitly added. Assumption is that it's because
    # they're on a base class?
    update_user = serializers.CharField()
    create_user = serializers.CharField()
    update_date = serializers.DateTimeField()
    create_date = serializers.DateTimeField()

    # Use decimal fields without any validators.
    yield_estimation_duration = serializers.DecimalField(max_digits=9, decimal_places=2, required=False)
    surface_seal_thickness = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    static_level_before_test = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    drawdown = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    hydro_fracturing_yield_increase = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    recommended_pump_depth = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    recommended_pump_rate = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    # Use CharField, to switch off validation.
    owner_email = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    def get_well_activity_type(self):
        return WellActivityCode.types.legacy()

    def get_foreign_key_sets(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': ActivitySubmissionLinerPerforation,
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
            'owner_city': {'required': False, 'allow_blank': True},
            'yield_estimation_duration': {'required': False},
            'owner_email': {'required': False},
            'static_level_before_test': {'min_value': None}
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
    linerperforation_set = ActivitySubmissionLinerPerforationSerializer(
        many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(
        many=True, required=False)

    coordinate_acquisition_code = serializers.PrimaryKeyRelatedField(
        queryset=CoordinateAcquisitionCode.objects.all(),
        required=False, allow_null=True)

    def create(self, validated_data):
        # Whenever we create a Construction record, we default to H (gps) for the source.
        validated_data['coordinate_acquisition_code'] = CoordinateAcquisitionCode.objects.get(
            code='H')
        return super().create(validated_data)

    def get_foreign_key_sets(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': ActivitySubmissionLinerPerforation,
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
                  'well_orientation_status', 'lithologydescription_set', 'casing_set',
                  'surface_seal_material', 'surface_seal_depth', 'surface_seal_thickness',
                  'surface_seal_method', 'backfill_type', 'backfill_depth',
                  'liner_material', 'liner_diameter', 'liner_thickness', 'liner_from', 'liner_to',
                  'linerperforation_set', 'screen_intake_method', 'screen_type', 'screen_material',
                  'other_screen_material', 'screen_opening', 'screen_bottom', 'other_screen_bottom',
                  'screen_information',
                  'screen_set', 'filter_pack_from', 'filter_pack_to', 'filter_pack_thickness',
                  'filter_pack_material', 'filter_pack_material_size', 'development_methods',
                  'development_hours', 'yield_estimation_method', 'yield_estimation_rate',
                  'yield_estimation_duration', 'well_yield_unit', 'static_level_before_test',
                  'drawdown', 'hydro_fracturing_performed', 'hydro_fracturing_yield_increase',
                  'recommended_pump_depth', 'recommended_pump_rate', 'development_notes',
                  'water_quality_characteristics',
                  'water_quality_colour', 'water_quality_odour', 'ems', 'total_depth_drilled',
                  'finished_well_depth', 'final_casing_stick_up', 'bedrock_depth', 'static_water_level',
                  'well_yield', 'artesian_flow', 'artesian_pressure', 'artesian_pressure_head', 'artesian_conditions',
                  'well_cap_type', 'well_disinfected_status',
                  'comments', 'internal_comments', 'alternative_specs_submitted', 'consultant_company', 'consultant_name',
                  'driller_name', 'person_responsible', 'company_of_person_responsible',
                  'coordinate_acquisition_code',
                  'create_user', 'create_date',
                  )
        extra_kwargs = {
            # TODO: reference appropriate serializer as above
            'well_activity_type': {'required': False},
        }


class WellAlterationSubmissionSerializer(WellSubmissionSerializerBase):
    """ Serializes a well alteration submission. """

    casing_set = CasingSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    linerperforation_set = ActivitySubmissionLinerPerforationSerializer(
        many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(
        many=True, required=False)

    def get_foreign_key_sets(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': ActivitySubmissionLinerPerforation,
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
            'well_orientation_status',
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
            'ems',
            'total_depth_drilled',
            'finished_well_depth',
            'final_casing_stick_up',
            'bedrock_depth',
            'static_water_level',
            'well_yield',
            'artesian_flow',
            'artesian_pressure',
            'artesian_pressure_head',
            'artesian_conditions',
            'well_cap_type',
            'well_disinfected_status',
            'comments',
            'internal_comments',
            'alternative_specs_submitted',
            'create_user', 'create_date',
        )
        extra_kwargs = {
            # TODO: reference appropriate serializer as above
            'well_activity_type': {'required': False},
        }


class WellStaffEditSubmissionSerializer(WellSubmissionSerializerBase):

    well = serializers.PrimaryKeyRelatedField(queryset=Well.objects.all())
    linerperforation_set = ActivitySubmissionLinerPerforationSerializer(
        many=True, required=False)
    casing_set = CasingSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    decommission_description_set = DecommissionDescriptionSerializer(
        many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(
        many=True, required=False)

    # Sets person_responsible and company_of back to object, otherwise client view only gets guid
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['person_responsible'] = PersonNameSerializer(instance.person_responsible).data
        response['company_of_person_responsible'] = OrganizationNameListSerializer(
            instance.company_of_person_responsible).data
        return response

    def get_well_activity_type(self):
        return WellActivityCode.types.staff_edit()

    def get_foreign_key_sets(self):
        return {
            'casing_set': Casing,
            'screen_set': Screen,
            'linerperforation_set': ActivitySubmissionLinerPerforation,
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
            'well_publication_status',
            'intended_water_use',
            'identification_plate_number',
            'well_identification_plate_attached',
            'id_plate_attached_by',
            'water_supply_system_name',
            'water_supply_system_well_name',
            'construction_start_date',
            'construction_end_date',
            'alteration_start_date',
            'alteration_end_date',
            'decommission_start_date',
            'decommission_end_date',
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
            'well_orientation_status',
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
            'ems',
            'aquifer',
            'total_depth_drilled',
            'finished_well_depth',
            'decommission_reason',
            'decommission_method',
            'decommission_sealant_material',
            'decommission_backfill_material',
            'decommission_details',
            'final_casing_stick_up',
            'bedrock_depth',
            'static_water_level',
            'well_yield',
            'artesian_flow',
            'artesian_pressure',
            'artesian_pressure_head',
            'artesian_conditions',
            'well_cap_type',
            'well_disinfected_status',
            'comments',
            'internal_comments',
            'alternative_specs_submitted',
            'decommission_description_set',
            'observation_well_number',
            'observation_well_status',
            'aquifer_vulnerability_index',
            'aquifer_lithology',
            'storativity',
            'transmissivity',
            'hydraulic_conductivity',
            'specific_storage',
            'specific_yield',
            'testing_method',
            'testing_duration',
            'analytic_solution_type',
            'boundary_effect',
            'create_user', 'create_date',
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
            'well_orientation_status',
            'decommission_reason',
            'decommission_method',
            'decommission_sealant_material',
            'decommission_backfill_material',
            'decommission_details',
            'casing_set',
            'decommission_description_set',
            'comments',
            'internal_comments',
            'alternative_specs_submitted',
            'create_user', 'create_date',
        )
        extra_kwargs = {
            'well_activity_type': {'required': False},
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

    wellsubclasscode_set = WellSubclassCodeSerializer(source='all_well_subclass_codes', many=True, read_only=True)

    class Meta:
        model = WellClassCode
        fields = ('well_class_code', 'description', 'wellsubclasscode_set')


class WellDisinfectedCodeSerializer(serializers.ModelSerializer):
    """Serializes Well Disinfected codes/descriptions"""

    class Meta:
        model = WellDisinfectedCode
        fields = ('well_disinfected_code', 'description')


class WellOrientationCodeSerializer(serializers.ModelSerializer):
    """Serializes Well Orientation codes/descriptions"""

    class Meta:
        model = WellOrientationCode
        fields = ('well_orientation_code', 'description')


class BoundaryEffectCodeSerializer(serializers.ModelSerializer):
    """Serializes Boundary Effect codes/descriptions"""

    class Meta:
        model = BoundaryEffectCode
        fields = ('boundary_effect_code', 'description')


class DriveShoeCodeSerializer(serializers.ModelSerializer):
    """Serializes Drive Shoe codes/descriptions"""

    class Meta:
        model = DriveShoeCode
        fields = ('drive_shoe_code', 'description')


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


class AquiferLithologySerializer(serializers.ModelSerializer):
    class Meta:
        model = AquiferLithologyCode
        fields = (
            'aquifer_lithology_code',
            'description'
        )


class WellStatusCodeSerializer(serializers.ModelSerializer):
    """ Serializes well status codes """

    class Meta:
        model = WellStatusCode
        fields = (
            'well_status_code', 'description'
        )


class WellPublicationStatusCodeSerializer(serializers.ModelSerializer):
    """ Serializes well publication status codes """

    class Meta:
        model = WellPublicationStatusCode
        fields = (
            'well_publication_status_code', 'description'
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


class ConstructionSubmissionDisplaySerializer(serializers.ModelSerializer):
    """ serializes a construction submission to display to users (human readable data)"""

    well_activity_type = serializers.ReadOnlyField(
        source='well_activity_type.description')
    well_class = serializers.ReadOnlyField(source='well_class.description')
    well_subclass = serializers.ReadOnlyField(
        source='well_subclass.description')
    intended_water_use = serializers.ReadOnlyField(
        source='intended_water_use.description')
    ground_elevation_method = serializers.ReadOnlyField(
        source='ground_elevation_method.description')
    well_orientation_status = serializers.ReadOnlyField(
        source='well_orientation_status.description')
    surface_seal_material = serializers.ReadOnlyField(
        source='surface_seal_material.description')
    person_responsible = serializers.ReadOnlyField(
        source='person_responsible.name')
    company_of_person_responsible = serializers.ReadOnlyField(
        source='company_of_person_responsible.name')
    yield_estimation_method = serializers.ReadOnlyField(
        source='yield_estimation_method.description')
    hydro_fracturing_performed = serializers.SerializerMethodField()
    water_quality_colour = serializers.ReadOnlyField(
        source='water_quality_colour.description')
    alternative_specs_submitted = serializers.SerializerMethodField()
    surface_seal_method = serializers.ReadOnlyField(
        source='surface_seal_method.description')
    liner_material = serializers.ReadOnlyField(
        source='liner_material.description')
    screen_material = serializers.ReadOnlyField(
        source='screen_material.description')
    screen_type = serializers.ReadOnlyField(
        source='screen_type.description')
    screen_bottom = serializers.ReadOnlyField(
        source='screen_bottom.description')
    screen_intake_method = serializers.ReadOnlyField(
        source='screen_intake_method.description')
    screen_opening = serializers.ReadOnlyField(
        source='screen_opening.description')
    filter_pack_material = serializers.ReadOnlyField(
        source='filter_pack_material.description')
    filter_pack_material_size = serializers.ReadOnlyField(
        source='filter_pack_material_size.description')

    class Meta:
        model = ActivitySubmission
        fields = (
            'filing_number', 'well_activity_type', 'well', 'well_class', 'well_subclass',
            'intended_water_use', 'identification_plate_number', 'well_identification_plate_attached',
            'work_start_date', 'work_end_date', 'owner_full_name', 'owner_mailing_address',
            'owner_province_state', 'owner_city', 'owner_postal_code', 'owner_email',
            'owner_tel', 'street_address', 'city',
            'legal_lot', 'legal_plan', 'legal_district_lot', 'legal_block', 'legal_section',
            'legal_township', 'legal_range', 'land_district', 'legal_pid', 'well_location_description',
            'latitude', 'longitude', 'ground_elevation', 'ground_elevation_method', 'drilling_methods',
            'well_orientation_status', 'lithologydescription_set', 'casing_set',
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
            'water_quality_colour', 'water_quality_odour', 'ems', 'total_depth_drilled',
            'finished_well_depth', 'final_casing_stick_up', 'bedrock_depth', 'static_water_level',
            'well_yield', 'artesian_flow', 'artesian_pressure', 'artesian_pressure_head', 'artesian_conditions',
            'well_cap_type', 'well_disinfected_status',
            'comments', 'alternative_specs_submitted', 'consultant_company', 'consultant_name',
            'driller_name', 'person_responsible', 'company_of_person_responsible',
            'coordinate_acquisition_code',
            'create_user', 'create_date',
        )

    def get_hydro_fracturing_performed(self, obj):
        return "Yes" if obj.hydro_fracturing_performed else "No"

    def get_alternative_specs_submitted(self, obj):
        return "Yes" if obj.alternative_specs_submitted else "No"


class AlterationSubmissionDisplaySerializer(serializers.ModelSerializer):
    """ serializes an Alteration submission to display to users (human readable data)"""

    well_activity_type = serializers.ReadOnlyField(
        source='well_activity_type.description')
    well_class = serializers.ReadOnlyField(source='well_class.description')
    well_subclass = serializers.ReadOnlyField(
        source='well_subclass.description')
    intended_water_use = serializers.ReadOnlyField(
        source='intended_water_use.description')
    ground_elevation_method = serializers.ReadOnlyField(
        source='ground_elevation_method.description')
    well_orientation_status = serializers.ReadOnlyField(
        source='well_orientation_status.description')
    surface_seal_material = serializers.ReadOnlyField(
        source='surface_seal_material.description')
    person_responsible = serializers.ReadOnlyField(
        source='person_responsible.name')
    company_of_person_responsible = serializers.ReadOnlyField(
        source='company_of_person_responsible.name')
    yield_estimation_method = serializers.ReadOnlyField(
        source='yield_estimation_method.description')
    hydro_fracturing_performed = serializers.SerializerMethodField()
    water_quality_colour = serializers.ReadOnlyField(
        source='water_quality_colour.description')
    alternative_specs_submitted = serializers.SerializerMethodField()
    surface_seal_method = serializers.ReadOnlyField(
        source='surface_seal_method.description')
    liner_material = serializers.ReadOnlyField(
        source='liner_material.description')
    screen_material = serializers.ReadOnlyField(
        source='screen_material.description')
    screen_type = serializers.ReadOnlyField(
        source='screen_type.description')
    screen_bottom = serializers.ReadOnlyField(
        source='screen_bottom.description')
    screen_intake_method = serializers.ReadOnlyField(
        source='screen_intake_method.description')
    screen_opening = serializers.ReadOnlyField(
        source='screen_opening.description')
    filter_pack_material = serializers.ReadOnlyField(
        source='filter_pack_material.description')
    filter_pack_material_size = serializers.ReadOnlyField(
        source='filter_pack_material_size.description')

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
            'well_orientation_status',
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
            'ems',
            'total_depth_drilled',
            'finished_well_depth',
            'final_casing_stick_up',
            'bedrock_depth',
            'static_water_level',
            'well_yield',
            'artesian_flow',
            'artesian_pressure',
            'artesian_pressure_head',
            'artesian_conditions',
            'well_cap_type',
            'well_disinfected_status',
            'comments',
            'alternative_specs_submitted',
            'create_user', 'create_date',
        )

    def get_hydro_fracturing_performed(self, obj):
        return "Yes" if obj.hydro_fracturing_performed else "No"

    def get_alternative_specs_submitted(self, obj):
        return "Yes" if obj.alternative_specs_submitted else "No"


class DecommissionSubmissionDisplaySerializer(serializers.ModelSerializer):
    """ serializes a Decommission submission to display to users (human readable data)"""

    well_activity_type = serializers.ReadOnlyField(
        source='well_activity_type.description')
    well_class = serializers.ReadOnlyField(source='well_class.description')
    well_subclass = serializers.ReadOnlyField(
        source='well_subclass.description')
    intended_water_use = serializers.ReadOnlyField(
        source='intended_water_use.description')
    ground_elevation_method = serializers.ReadOnlyField(
        source='ground_elevation_method.description')
    well_orientation_status = serializers.ReadOnlyField(
        source='well_orientation_status.description')
    decommission_method = serializers.ReadOnlyField(
        source='decommission_method.description')
    decommission_sealant_material = serializers.ReadOnlyField(
        source='decommission_sealant_material.description')
    decommission_backfill_material = serializers.ReadOnlyField(
        source='decommission_backfill_material.description')
    alternative_specs_submitted = serializers.SerializerMethodField()

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
            'well_orientation_status',
            'decommission_reason',
            'decommission_method',
            'decommission_sealant_material',
            'decommission_backfill_material',
            'decommission_details',
            'casing_set',
            'decommission_description_set',
            'comments',
            'alternative_specs_submitted',
            'create_user', 'create_date',
        )

    def get_alternative_specs_submitted(self, obj):
        return "Yes" if obj.alternative_specs_submitted else "No"


class LegacyWellDisplaySerializer(serializers.ModelSerializer):
    """ serializes legacy well data to display to users"""
    well = serializers.PrimaryKeyRelatedField(queryset=Well.objects.all())
    linerperforation_set = LinerPerforationSerializer(
        many=True, required=False)
    casing_set = CasingSerializer(many=True, required=False)
    screen_set = ScreenSerializer(many=True, required=False)
    decommission_description_set = DecommissionDescriptionSerializer(
        many=True, required=False)
    lithologydescription_set = LithologyDescriptionSerializer(
        many=True, required=False)

    # related objects:  use human readable fields for display (e.g. well_class.description
    # instead of the well_class id)
    well_class = serializers.ReadOnlyField(source='well_class.description')
    well_subclass = serializers.ReadOnlyField(
        source='well_subclass.description')
    intended_water_use = serializers.ReadOnlyField(
        source='intended_water_use.description')
    ground_elevation_method = serializers.ReadOnlyField(
        source='ground_elevation_method.description')
    well_orientation_status = serializers.ReadOnlyField(
        source='well_orientation_status.description')
    surface_seal_material = serializers.ReadOnlyField(
        source='surface_seal_material.description')
    person_responsible = serializers.ReadOnlyField(
        source='person_responsible.name')
    company_of_person_responsible = serializers.ReadOnlyField(
        source='company_of_person_responsible.name')
    yield_estimation_method = serializers.ReadOnlyField(
        source='yield_estimation_method.description')
    hydro_fracturing_performed = serializers.SerializerMethodField()
    water_quality_colour = serializers.ReadOnlyField(
        source='water_quality_colour.description')
    alternative_specs_submitted = serializers.SerializerMethodField()
    surface_seal_method = serializers.ReadOnlyField(
        source='surface_seal_method.description')
    liner_material = serializers.ReadOnlyField(
        source='liner_material.description')
    screen_material = serializers.ReadOnlyField(
        source='screen_material.description')
    screen_type = serializers.ReadOnlyField(
        source='screen_type.description')
    screen_bottom = serializers.ReadOnlyField(
        source='screen_bottom.description')
    screen_intake_method = serializers.ReadOnlyField(
        source='screen_intake_method.description')
    screen_opening = serializers.ReadOnlyField(
        source='screen_opening.description')
    filter_pack_material = serializers.ReadOnlyField(
        source='filter_pack_material.description')
    filter_pack_material_size = serializers.ReadOnlyField(
        source='filter_pack_material_size.description')
    decommission_method = serializers.ReadOnlyField(
        source='decommission_method.description')
    decommission_sealant_material = serializers.ReadOnlyField(
        source='decommission_sealant_material.description')
    decommission_backfill_material = serializers.ReadOnlyField(
        source='decommission_backfill_material.description')
    artesian_conditions = serializers.SerializerMethodField()

    def get_hydro_fracturing_performed(self, obj):
        return "Yes" if obj.hydro_fracturing_performed else "No"

    def get_alternative_specs_submitted(self, obj):
        return "Yes" if obj.alternative_specs_submitted else "No"

    def get_artesian_conditions(self, obj):
        return "Yes" if obj.artesian_conditions else "No"

    class Meta:
        model = ActivitySubmission
        fields = (
            'well',
            'well_class',
            'well_subclass',
            'well_status',
            'well_publication_status',
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
            'well_orientation_status',
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
            'ems',
            'aquifer',
            'total_depth_drilled',
            'finished_well_depth',
            'decommission_reason',
            'decommission_method',
            'decommission_sealant_material',
            'decommission_backfill_material',
            'decommission_details',
            'final_casing_stick_up',
            'bedrock_depth',
            'static_water_level',
            'well_yield',
            'artesian_flow',
            'artesian_pressure',
            'artesian_pressure_head',
            'artesian_conditions',
            'well_cap_type',
            'well_disinfected_status',
            'comments',
            'internal_comments',
            'alternative_specs_submitted',
            'decommission_description_set',
            'observation_well_number',
            'observation_well_status',
            'aquifer_vulnerability_index',
            'aquifer_lithology',
            'storativity',
            'transmissivity',
            'hydraulic_conductivity',
            'specific_storage',
            'specific_yield',
            'testing_method',
            'testing_duration',
            'analytic_solution_type',
            'boundary_effect',
            'create_user', 'create_date',
        )

    def get_hydro_fracturing_performed(self, obj):
        return "Yes" if obj.hydro_fracturing_performed else "No"

    def get_alternative_specs_submitted(self, obj):
        return "Yes" if obj.alternative_specs_submitted else "No"


class LicencedStatusCodeSerializer(serializers.ModelSerializer):
    """
    Serializes licenced status codes.
    """

    class Meta:
        model = LicencedStatusCode
        fields = (
            'licenced_status_code',
            'description',
        )
