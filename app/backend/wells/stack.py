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
import dateutil.parser

from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.db import transaction
from django.db.models import F

from gwells.models import ProvinceStateCode
from submissions.models import WellActivityCode
import submissions.serializers
from wells.models import Well, ActivitySubmission
from wells.serializers import WellStackerSerializer


logger = logging.getLogger(__name__)


def overlap(a, b):
    """
    Checks to see if two casings intersect, or have identical start/end positions.
    """
    # If the casing start/end intersects
    intersect = (a[0] > b[0] and a[0] < b[1]) or (a[1] > b[0] and a[1] < b[1])
    # If the casings start or end in the same place
    overlap = (a[0] == b[0]) or (a[1] == b[1])
    return intersect or overlap


class StackWells():

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
        # If there is as yet no well, we create one
        well = Well.objects.create()
        well = self._stack(ActivitySubmission.objects.filter(filing_number=filing_number), well)
        submission.well = well
        submission.save()
        return well

    def _create_legacy_submission(self, well: Well) -> None:
        """
        Using an existing well as a reference, create a legacy well record
        """
        # TODO: Deal with Lithology, LtsaOwner, LinerPerforation, AquiferWell, Screen etc. (This should
        # work magically if the serializers are implemented correctly)

        # Serialize the well.
        well_serializer = WellStackerSerializer(well)
        data = well_serializer.data
        # Retain the construction date.
        data['work_start_date'] = data.pop('construction_start_date', None)
        data['work_end_date'] = data.pop('construction_end_date', None)
        # Filter out None and '' values, they can interfere with validation.
        data = {k: v for (k, v) in data.items() if v is not None and v != ''}
        # Specify the submission type as legacy.
        data['well_activity_type'] = WellActivityCode.types.legacy().code
        # Retain the well reference.
        data['well'] = well.well_tag_number
        # De-serialize the well into a submission.
        submission_serializer = submissions.serializers.WellSubmissionSerializer(data=data)
        # Validate the data, throwing an exception on error.
        if submission_serializer.is_valid(raise_exception=True):
            # Save the submission.
            instance = submission_serializer.save()

    def _casing_overlaps(self, casing, casing_set):
        # Return True if a casing overlaps with a list of casings
        for other_casing in casing_set:
            if overlap((casing.get('casing_from'), casing.get('casing_to')),
                       (other_casing.get('casing_from'), other_casing.get('casing_to'))):
                return True
        return False

    def _merge_casings(self, prev_casings, next_casings):
        # Remove old records that overlap with new records
        prev_casings = [casing for casing in prev_casings if not self._casing_overlaps(casing, next_casings)]
        # Join the old with the new
        new = prev_casings + next_casings
        # Sort
        new.sort(key=lambda casing: (casing.get('casing_from'), casing.get('casing_to')))
        return new

    def _stack(self, records, well: Well) -> Well:
        records = records.order_by(F('work_start_date').asc(nulls_first=True))
        composite = {}
        # Iterate through all the submission records
        # TODO: Deal with Lithology, LtsaOwner, LinerPerforation, AquiferWell, Screen etc.
        for submission in records:
            serializer = submissions.serializers.WellSubmissionSerializer(submission)
            for key, value in serializer.data.items():
                # We only consider items with values
                if value:
                    if key == 'casing_set' and key in composite:
                        composite[key] = self._merge_casings(composite[key], value)
                    else:
                        composite[key] = value
        # Update the well view
        well_serializer = WellStackerSerializer(well, data=composite, partial=True)
        if well_serializer.is_valid(raise_exception=True):
            well = well_serializer.save()

        return well

    def _update_well_record(self, submission: ActivitySubmission) -> Well:
        """
        Used to update an existing well record.
        """
        records = ActivitySubmission.objects.filter(
            well=submission.well)
        if records.count() > 1 or self._submission_is_construction(submission):
            # If there's more than one submission, or this is a construction submission, we don't need to
            # create a legacy well, we can go ahead, iterate though the submission records and update the well.
            return self._stack(records, submission.well)
        else:
            # If there aren't prior submissions, we may create a legacy record using the current well
            # record.
            self._create_legacy_submission(submission.well)
            # We should now have multiple records
            records = ActivitySubmission.objects.filter(
                well=submission.well)
            return self._stack(records, submission.well)

    def _submission_is_construction(self, submission):
        construction_code = WellActivityCode.types.construction().code
        return submission.well_activity_type.code == construction_code
