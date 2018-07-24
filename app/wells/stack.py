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

from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.db import transaction

from gwells.models import ProvinceStateCode
from wells.models import ActivitySubmission, Well, WellActivityCode


logger = logging.getLogger(__name__)


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
        # TODO: Deal with Lithology, LtsaOwner, LinerPerforation, Casing, AquiferWell, Screen etc.
        # TODO: Implement some smart serialization here.
        ActivitySubmission.objects.create(
            owner_full_name=well.owner_full_name,
            owner_province_state=well.owner_province_state,
            work_start_date=well.construction_start_date,
            work_end_date=well.construction_end_date,
            well_activity_type=WellActivityCode.types.legacy(),
            well=well
        )

    def _stack(self, submissions, well: Well) -> Well:
        submissions = submissions.order_by('-work_start_date')
        composite = {}
        # Iterate through all the submissions
        # TODO: Deal with Lithology, LtsaOwner, LinerPerforation, Casing, AquiferWell, Screen etc.
        # TODO: Implement some smart serialization here.
        for submission in submissions:
            data = model_to_dict(submission)
            for key, value in data.items():
                composite[key] = value
        # Update the well view
        well.owner_full_name = composite.get('owner_full_name')
        well.owner_province_state = ProvinceStateCode.objects.get(
            province_state_code=composite.get('owner_province_state'))
        well.save()
        return well

    def _update_well_record(self, submission: ActivitySubmission) -> Well:
        """
        Used to update an existing well record.
        """
        submissions = ActivitySubmission.objects.filter(
            well=submission.well)
        if submissions.count() > 1 or self._submission_is_construction(submission):
            # If there's more than one submission, or this is a construction submission, we don't need to
            # create a legacy well, we can go ahead, iterate though the submissions and update the well.
            return self._stack(submissions, submission.well)
        else:
            # If there aren't prior submissions, we may create a legacy record using the current well
            # record.
            self._create_legacy_submission(submission.well)
            # We should now have multiple records
            submissions = ActivitySubmission.objects.filter(
                well=submission.well)
            return self._stack(submissions, submission.well)

    def _submission_is_construction(self, submission):
        construction_code = WellActivityCode.types.construction().well_activity_type_code
        return submission.well_activity_type.well_activity_type_code == construction_code
