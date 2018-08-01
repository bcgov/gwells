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
from datetime import date

from django.test import TestCase

from gwells.models import ProvinceStateCode
from wells.models import Well, ActivitySubmission
from submissions.models import WellActivityCode
from wells.stack import StackWells
from registries.models import Person


class StackTest(TestCase):

    def setUp(self):
        self.driller = Person.objects.create(
            first_name='Bobby',
            surname='Driller'
        )

        self.province = ProvinceStateCode.objects.get_or_create(
            province_state_code='BC',
            description='British Columbia',
            display_order=1
        )[0]

        # These codes should already exists in the db (they are placed there as part of migrations)
        self.well_activity_construction = WellActivityCode.objects.get(well_activity_type_code='CON')
        self.well_activity_legacy = WellActivityCode.objects.get(well_activity_type_code='LEGACY')
        self.well_activity_alteration = WellActivityCode.objects.get(well_activity_type_code='ALT')

    def test_new_submission_gets_well_tag_number(self):
        # Test that when a constrction submission is processed, it is asigned a well_tag_number
        submission = ActivitySubmission.objects.create(
            owner_full_name='Bob',
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            driller_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=self.well_activity_construction,
            )
        stacker = StackWells()
        well = stacker.process(submission.filing_number)
        submission = ActivitySubmission.objects.get(filing_number=submission.filing_number)
        self.assertEqual(well.well_tag_number, submission.well.well_tag_number)

    def test_construction_submission_no_current_well(self):
        # Creating a brand new well that we only have a construction submission for.
        owner_full_name = 'Bob'
        submission = ActivitySubmission.objects.create(
            owner_full_name=owner_full_name,
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            driller_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=self.well_activity_construction,
            )
        stacker = StackWells()
        well = stacker.process(submission.filing_number)
        Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(owner_full_name, well.owner_full_name)

    def test_alteration_after_construction(self):
        # Create a brand new well with a construction
        owner_full_name = 'Bob'
        new_owner_full_name = 'Joe'
        construction = ActivitySubmission.objects.create(
            owner_full_name=owner_full_name,
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            driller_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=self.well_activity_construction,
            )
        stacker = StackWells()
        well = stacker.process(construction.filing_number)
        # Update the well with an alteration
        alteration = ActivitySubmission.objects.create(
            owner_full_name=new_owner_full_name,
            work_start_date=date(2018, 2, 1),
            work_end_date=date(2018, 3, 1),
            driller_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=self.well_activity_alteration,
            well=well
            )
        well = stacker.process(alteration.filing_number)
        self.assertEqual(new_owner_full_name, well.owner_full_name)

    def test_alteration_submission_to_legacy_well(self):
        # The well already exists, but has no construction submission.
        original_full_name = 'Bob'
        new_full_name = 'Jimbo'
        # This is the original well record
        well = Well.objects.create(
            owner_full_name=original_full_name,
            owner_province_state=self.province)
        # Create a submission
        submission = ActivitySubmission.objects.create(
            owner_full_name=new_full_name,
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            driller_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=self.well_activity_alteration,
            well=well
            )

        stacker = StackWells()
        stacker.process(submission.filing_number)
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        submissions = ActivitySubmission.objects.filter(well=well)
        self.assertEqual(submissions.count(), 2, "It is expected that a legacy submission be created")
        self.assertEqual(new_full_name, well.owner_full_name)

    def test_construction_submission_to_legacy_well(self):
        # The well already exists, and we're applying a construction submission to it.
        original_full_name = 'Bob'
        new_full_name = 'Jimbo'
        # This is the original well record.
        well = Well.objects.create(
            owner_full_name=original_full_name,
            owner_province_state=self.province)
        # Create a submission.
        submission = ActivitySubmission.objects.create(
            owner_full_name=new_full_name,
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            driller_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=self.well_activity_construction,
            well=well
            )

        stacker = StackWells()
        stacker.process(submission.filing_number)

        # Load all the submissions.
        submissions = ActivitySubmission.objects.filter(well=well)
        # Load the updated well record.
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(submissions.count(), 1, "It is expected that no legacy submission be created")
        self.assertEqual(new_full_name, well.owner_full_name)
