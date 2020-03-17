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
import threading

from django.db import transaction
from rest_framework.exceptions import ValidationError, APIException
from rest_framework import serializers

from gwells.models import ProvinceStateCode, DATALOAD_USER
from submissions.models import WellActivityCode, WELL_ACTIVITY_CODE_ALTERATION,\
    WELL_ACTIVITY_CODE_CONSTRUCTION, WELL_ACTIVITY_CODE_DECOMMISSION, WELL_ACTIVITY_CODE_LEGACY,\
    WELL_ACTIVITY_CODE_STAFF_EDIT
import submissions.serializers
from wells.models import Well, ActivitySubmission, ActivitySubmissionLinerPerforation, FieldsProvided, \
    WellStatusCode, WELL_STATUS_CODE_CONSTRUCTION,\
    WELL_STATUS_CODE_DECOMMISSION, WELL_STATUS_CODE_ALTERATION, WELL_STATUS_CODE_OTHER, LithologyDescription,\
    Casing, Screen, LinerPerforation, DecommissionDescription, LithologyDescription

from wells.serializers import WellStackerSerializer, CasingStackerSerializer, ScreenStackerSerializer,\
    LinerPerforationStackerSerializer, DecommissionDescriptionStackerSerializer,\
    LithologyDescriptionStackerSerializer

import reversion

logger = logging.getLogger(__name__)

# Not sure if a lock is really needed, playing safe.
target_keys_lock = threading.Lock()
target_keys = None

# There isn't always a like to like mapping of values, sometimes the source key will differ from
# the target key:
ACTIVITY_TYPE_MAP = {
    WELL_ACTIVITY_CODE_CONSTRUCTION: {
        'work_start_date': 'construction_start_date',
        'work_end_date': 'construction_end_date'
    },
    WELL_ACTIVITY_CODE_ALTERATION: {
        'work_start_date': 'alteration_start_date',
        'work_end_date': 'alteration_end_date'
    },
    WELL_ACTIVITY_CODE_DECOMMISSION: {
        'work_start_date': 'decommission_start_date',
        'work_end_date': 'decommission_end_date'
    }
}


# Well status is set based on the most recent activity submission.
WELL_STATUS_MAP = {
    WELL_ACTIVITY_CODE_CONSTRUCTION: WELL_STATUS_CODE_CONSTRUCTION,
    WELL_ACTIVITY_CODE_ALTERATION: WELL_STATUS_CODE_ALTERATION,
    WELL_ACTIVITY_CODE_DECOMMISSION: WELL_STATUS_CODE_DECOMMISSION,
}

# Relying on django serialization/reflection is very slow, so we explicitly
# define this relationship.
FOREIGN_KEY_MODEL_LOOKUP = {
    'casing_set': Casing,
    'screen_set': Screen,
    'linerperforation_set': ActivitySubmissionLinerPerforation,
    'decommission_description_set': DecommissionDescription,
    'lithologydescription_set': LithologyDescription
}

# Relying on django serialization/reflection is very slow, so we explicitly
# define this relationship.
FOREIGN_KEY_SERIALIZER_LOOKUP = {
    'casing_set': CasingStackerSerializer,
    'screen_set': ScreenStackerSerializer,
    'linerperforation_set': LinerPerforationStackerSerializer,
    'decommission_description_set': DecommissionDescriptionStackerSerializer,
    'lithologydescription_set': LithologyDescriptionStackerSerializer
}

# Relying on django serialization/reflection is very slow, so we explicitly
# define this relationship.
MANY_TO_MANY_LOOKUP = {
    'drilling_methods': 'drilling_method_code',
    'development_methods': 'development_method_code',
    'water_quality_characteristics': 'code'
}

# Relying on django serialization/reflection is very slow, so we explicitly
# define this relationship.
KEY_VALUE_LOOKUP = {
    'well_publication_status': 'well_publication_status_code',
    'boundary_effect': 'boundary_effect_code',
    'well_disinfected_status': 'well_disinfected_code',
    'well_orientation_status': 'well_orientation_code',
    'drive_shoe_status': 'drive_shoe_code',
    'owner_province_state': 'province_state_code',
    'well_class': 'well_class_code',
    'well_subclass': 'well_subclass_guid',
    'intended_water_use': 'intended_water_use_code',
    'land_district': 'land_district_code',
    'coordinate_acquisition_code': 'code',
    'aquifer_lithology': 'aquifer_lithology_code',
    'well_yield_unit': 'well_yield_unit_code',
    'surface_seal_material': 'surface_seal_material_code',
    'surface_seal_method': 'surface_seal_method_code',
    'liner_material': 'code',
    'screen_intake_method': 'screen_intake_code',
    'screen_type': 'screen_type_code',
    'screen_material': 'screen_material_code',
    'screen_opening': 'screen_opening_code',
    'screen_bottom': 'screen_bottom_code',
    'filter_pack_material': 'filter_pack_material_code',
    'filter_pack_material_size': 'filter_pack_material_size_code',
    'decommission_method': 'decommission_method_code',
    'aquifer': 'aquifer_id',
    'person_responsible': 'person_guid',
    'company_of_person_responsible': 'org_guid',
    'yield_estimation_method': 'yield_estimation_method_code',
    'ground_elevation_method': 'ground_elevation_method_code',
    'observation_well_status': 'obs_well_status_code',
    'well_status': 'well_status_code'
}


def is_staff_edit(submission):
    return submission.well_activity_type.code == WELL_ACTIVITY_CODE_STAFF_EDIT


def overlap(a, b):
    """
    Checks to see if two series intersect, or have identical start/end positions.
    """
    # if any start / end is None then it doesn't overlap
    if a[0] is None or a[1] is None or b[0] is None or b[1] is None:
        return False
    # If the casing start/end intersects
    records_intersect = (a[0] > b[0] and a[0] < b[1]) or (a[1] > b[0] and a[1] < b[1])
    # If the series start or end in the same place
    records_overlap = (a[0] == b[0]) or (a[1] == b[1])
    return records_intersect or records_overlap

def series_overlaps(record, record_set):
    """
    Return True if a record overlaps with a list of records
    """
    record_start = record.get('start')
    record_end = record.get('end')
    for other_record in record_set:
        other_record_start = other_record.get('start')
        other_record_end = other_record.get('end')
        if overlap((record_start, record_end), (other_record_start, other_record_end)):
            return True
    return False

def merge_series(prev_series, next_series):
    """
    Merges two start / end series if there are overlaps
    """
    # Remove old records that overlap with new records
    prev_series = [record for record in prev_series if not series_overlaps(record, next_series)]
    # Join the old with the new
    new = prev_series + next_series
    new.sort(key=lambda record: (record.get('start'), record.get('end')))
    return new

class StackWells():

    def _get_target_keys(self):
        # This is an expensive call, so we cache it (running normally we'll mostly have misses, but
        # during testing, this can massively speed things up.)
        global target_keys
        try:
            target_keys_lock.acquire()
            if not target_keys:
                target_keys = WellStackerSerializer().get_fields().keys()
        finally:
            target_keys_lock.release()
        return target_keys

    def _getattr(self, submission, key):
        if key in FOREIGN_KEY_MODEL_LOOKUP:
            model = FOREIGN_KEY_MODEL_LOOKUP[key]
            return model.objects.filter(activity_submission=submission)
        return getattr(submission, key)

    @transaction.atomic
    def process(self, filing_number) -> Well:
        """
        Take a submission, and use it to create/update a well entry.
        As a side effect of calling this method, a legacy well record may be created if required.
        """
        submission = ActivitySubmission.objects.get(
            filing_number=filing_number)
        if submission.well is not None:
            # If there's already a well, we update it
            return self._update_well_record(submission)
        # If there is as yet no well, we create one (basing audit information on submission)
        well = Well.objects.create(
            update_user=submission.update_user,
            create_user=submission.create_user,
            create_date=submission.create_date,
            update_date=submission.update_date)
        # If there's no well as yet - then this necessarily has to be the 1st submission, so we just
        # re-query it as a collection, and call stack.
        submissions = ActivitySubmission.objects.filter(filing_number=filing_number)
        well = self._stack(submissions, well)
        submission.well = well
        submission.save()
        return well

    @transaction.atomic
    def _create_legacy_submission(self, well: Well) -> None:
        """
        Using an existing well as a reference, create a legacy well record
        """
        # Serialize the well.
        well_serializer = WellStackerSerializer(well)
        data = well_serializer.data
        # Retain the construction date.
        data['work_start_date'] = data.pop('construction_start_date', None)
        data['work_end_date'] = data.pop('construction_end_date', None)
        # Retain the create and update user.
        if well.create_user:
            data['create_user'] = well.create_user
        else:
            # If for whatever reason, the original well record doesn't have a create_user, we assigned
            # DATALOAD_USER to the legacy record.
            logger.warning('Well {} does not have a create_user!'.format(well.well_tag_number))
            data['create_user'] = DATALOAD_USER
        if well.update_user:
            data['update_user'] = well.update_user
        else:
            # If for whatever reason, the original well record doesn't have an update_user, we assigned
            # DATALOAD_USER to the legacy record.
            logger.warning('Well {} does not have an update_user!'.format(well.well_tag_number))
            data['update_user'] = DATALOAD_USER
        data['create_date'] = well.create_date
        data['update_data'] = well.update_date
        # Filter out None and '' values, they can interfere with validation.
        data = {k: v for (k, v) in data.items() if v is not None and v != ''}
        # Retain the well reference.
        data['well'] = well.well_tag_number

        submission_serializer = submissions.serializers.WellSubmissionLegacySerializer(data=data)

        is_valid = submission_serializer.is_valid(raise_exception=False)
        if is_valid:
            # Save the submission.
            # NOTE: Validation may now fail, calling save here, will result in the well record being updated,
            # the legacy submission may be valid, but that doesn't mean the resultant well record is going
            # to be valid!
            legacy = submission_serializer.save()

            # keep track of which fields were originally populated on the legacy well records
            original_data_provided = {
                k: True for k in data.keys() if
                k in [field.name for field in FieldsProvided._meta.get_fields()]
            }
            FieldsProvided.objects.create(activity_submission=legacy, **original_data_provided)

            return legacy
        logger.info('invalid legacy data: {}'.format(data))
        logger.error(submission_serializer.errors)
        # We don't bubble validation errors on the legacy submission up. It just causes confusion!
        # If there's a validation error on this level, it has to go up as a 500 error. Validation
        # error here, means we are unable to create a legacy record using old well data. The
        # users can't do anything to fix this, we have to fix a bug!
        logger.error('submission_serializer validation error')
        raise APIException()

    def transform_value(self, value, source_key):
        if value is None:
            return None
        if source_key in FOREIGN_KEY_SERIALIZER_LOOKUP:
            Serializer = FOREIGN_KEY_SERIALIZER_LOOKUP[source_key]
            value = Serializer(value, many=True).data
        elif source_key in MANY_TO_MANY_LOOKUP:
            new_value = []
            for item in value.all():
                new_value.append(getattr(item, MANY_TO_MANY_LOOKUP[source_key]))
            value = new_value
        elif source_key in KEY_VALUE_LOOKUP:
            value = getattr(value, KEY_VALUE_LOOKUP[source_key])
        return value

    @transaction.atomic
    def _stack(self, records, well: Well) -> Well:
        # It's helpful for debugging, to limit the fields we consider only to target keys, for example
        # there are some values that don't actually map from the submission to the well (e.g. create_date,
        # filing number, well_activity_code etc.)
        target_keys = self._get_target_keys()

        # Iterate through all the submission records
        # We can't strictly order by the create date, we need to consider that construction/legacy well
        # submission have to go 1st - in the following order:
        # 1: legacy submissions
        #   1.1: reason: Scenario. There is an existing well, a construction submission comes in, we have
        #           to create a legacy submission to retain the wells information, and apply the
        #           construction on top of that.
        # 2: construction submissions
        #   2.1: reason: A well should ideally always start with a construction submission. See 1.1 for
        #           the exception to this rule.
        # 3: create_date
        #   3.1 reason: Submissions need to be considered in order.
        #   3.2 exceptions: It may be, that two alterations are capture in the incorrect order. Logically,
        #           the record dated earlier by the "work_start_date" should be considered 1st, and should
        #           be captured 1st. We do however not have control over the order in which records are
        #           captured. WE CURRENTLY DO NOT HANDLE THIS EXCEPTION. It is important that and EDIT be
        #           processed ONLY based on it's create_date, not it's work_start_date.
        records = records.order_by('create_date')
        records = sorted(records, key=lambda record:
                         (record.well_activity_type.code != WellActivityCode.types.legacy().code,
                          record.well_activity_type.code != WellActivityCode.types.construction().code,
                          record.create_date))

        # these are depth-specific sets that have a "start" and "end" value
        FOREIGN_KEYS = (
            'casing_set',
            'screen_set',
            'linerperforation_set',
            'decommission_description_set',
            'lithologydescription_set')

        composite = {}

        for index, submission in enumerate(records):
            if index == 0:
                # The create user & date of the very 1st submission record, is taken to be the
                # create user and date of the well.
                create_user = submission.create_user
                create_date = submission.create_date
            update_date = submission.update_date
            # add a well_status based on the current activity submission
            # a staff edit could still override this with a different value.
            if submission.well_activity_type.code != 'STAFF_EDIT':
                composite['well_status'] = WELL_STATUS_MAP.get(
                    submission.well_activity_type.code, WellStatusCode.types.other().well_status_code)
            source_target_map = ACTIVITY_TYPE_MAP.get(submission.well_activity_type.code, {})
            for field in ActivitySubmission._meta.get_fields():

                # fields_provided is a dict of fields that were included in the original activity submission
                # or staff edit. We don't need to include this field in the composite, so we skip it here.
                # we'll use it in other iterations (for other fields) to see if the user updated that field or not.
                if field.name == 'fields_provided':
                    continue

                # We only consider items with values, and keys that are in our target
                # an exception is STAFF_EDIT submissions (we need to be able to accept empty values)
                source_key = field.name
                value = self._getattr(submission, source_key)

                # ManyToMany values need to be checked using the transform_value method.
                # if the number of values in a manytomany lookup is zero, and this field
                # wasn't included in a staff edit, we can skip to the next field.
                if (is_staff_edit(submission) and
                    source_key in MANY_TO_MANY_LOOKUP and
                    len(self.transform_value(value, source_key)) == 0 and
                    getattr(submission, 'fields_provided', None) and
                        not getattr(submission.fields_provided, source_key, None)):
                    continue

                # Evaluate if this field needs to be updated on the composite view of the well.
                # it needs to be updated if there is a valid value in the current report, or
                # if we are iterating through a staff edit and the value was provided by a user
                # (tracked in the fields_provided property)
                if (
                        value or
                        value is False or
                        value == 0 or
                        value == '' or (
                            is_staff_edit(submission) and
                            getattr(submission, 'fields_provided', None) and
                            getattr(submission.fields_provided, source_key, None)
                        )):

                    target_key = source_target_map.get(source_key, source_key)
                    if target_key in target_keys:
                        # The composite dict is built up by applying the set of submissions/edits in order.
                        #
                        # There are several cases for handling values:
                        #
                        # The first cases involve related foreign key sets (other tables that
                        # have records that reference the current submission/well). These are handled
                        # differently for staff edits (can replace the entire previous set), or for
                        # sets that reference a depth along the drilled well (must be merged checking for
                        # overlap).
                        #
                        # If the target_key is not in one of the foreign key sets (i.e., it's a property/
                        # column of a well), then the value can overwrite the previous composite value.
                        if (is_staff_edit(submission) and
                                target_key in composite and
                                (target_key in FOREIGN_KEYS)):
                            # staff edits come in with the entire set of values and thus can replace
                            # the composite value
                            value = self.transform_value(value, source_key)
                            composite[target_key] = value
                        elif target_key in composite and target_key in FOREIGN_KEYS:
                            # foreign key sets are based on depth and need special merge handling.
                            value = self.transform_value(value, source_key)
                            composite[target_key] = merge_series(composite[source_key], value)
                        elif target_key in composite and target_key in MANY_TO_MANY_LOOKUP:
                            value = self.transform_value(value, source_key)

                            # Only update if there's a new value (except if a staff edit that
                            # included this field in the edit
                            if (len(value) > 0 or
                                    (is_staff_edit(submission) and
                                        getattr(submission.fields_provided, source_key, None))):
                                composite[target_key] = value
                        else:
                            value = self.transform_value(value, source_key)
                            composite[target_key] = value

            composite['update_user'] = submission.create_user or composite['update_user']

        # The create user & date of the well, has to be the same as the wells legacy record,
        # or construction record.
        composite['create_user'] = create_user
        composite['create_date'] = create_date
        # The update date, has to match whatever the late update_date was
        composite['update_Date'] = update_date

        # Update the well view.
        well = self._update_well_view(well, composite)
        return well

    def _update_well_view(self, well, composite):
        well_serializer = WellStackerSerializer(well, data=composite, partial=True)
        if well_serializer.is_valid(raise_exception=True):
            with reversion.create_revision():
                well = well_serializer.save()
        return well

    @transaction.atomic
    def _update_well_record(self, submission: ActivitySubmission) -> Well:
        """
        Used to update an existing well record.
        """
        records = ActivitySubmission.objects.filter(well=submission.well) \
            .prefetch_related(
                'well_status',
                'well_activity_type'
        )

        # 1) only 1 legacy record created from a previous _create_legacy_submission call [*no* legacy creation]
        # 2) (previous behaviour) - 1 non-legacy record created (e.g. staff_edit) [*yes* legacy creation]
        # 3) (previous behaviour) - 2 records exist (1 legacy, one previous non-legacy) = [*no* legacy creation]

        legacy_record_creation_needed = False
        if records.count() == 1:
            if records[0].well_activity_type.code == WELL_ACTIVITY_CODE_LEGACY:
                # if there is only one activity submission and it is LEGACY type then we know that
                # we don't need to process the stack. This one ActivitySubmission was created by the
                # legacy_records command from an existing well and therefore we don't need to update
                # the Well via the self._stack() call. The reason why we don't want to allow the
                # stack to be processed is that saving a Well could fail because the current well's
                # data is invalid according to the model validators.
                return records[0].well
            else:
                legacy_record_creation_needed = True
        if not legacy_record_creation_needed:
            # If there's more than one submission we don't need to create a legacy well, we can
            # safely assume that the 1st submission is either a legacy or construction report
            # submission.
            return self._stack(records, submission.well)
        else:
            # If there aren't prior submissions, we may create a legacy record using the current
            # well record.
            # Edge case of note:
            # Re. discussion with Lindsay on Oct 15 2018: There may be an instance, where there is a
            # pre-existing well, and a construct report is submitted. In this instance, we may end
            # up with a LEGACY record and a CONSTRUCTION record. This is odd, but we don't want to
            # lose the information stored in the existing well record. It is imerative that we
            # always create a legacy record.
            self._create_legacy_submission(submission.well)
            # We should now have multiple records
            records = ActivitySubmission.objects.filter(well=submission.well)
            return self._stack(records, submission.well)
