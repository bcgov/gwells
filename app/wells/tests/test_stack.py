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
from wells.models import ActivitySubmission, Well, WellActivityCode
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

        self.well_activity_construction = WellActivityCode.objects.get_or_create(
            well_activity_type_code='CON',
            description='Construction',
            display_order=0
        )[0]

        self.well_activity_legacy = WellActivityCode.objects.get_or_create(
            well_activity_type_code='LEGACY',
            description='Legacy',
            display_order=0
        )[0]

        self.well_activity_alteration = WellActivityCode.objects.get_or_create(
            well_activity_type_code='ALT',
            description='Alteration',
            display_order=0
        )[0]

    def test_construction_submission_no_current_well(self):
        # Creating a brand new well, we only have a construction submission for.
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
            well_tag_number=well
            )

        stacker = StackWells()
        stacker.process(submission.filing_number)
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        submissions = ActivitySubmission.objects.filter(well_tag_number=well)
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
            well_tag_number=well
            )

        stacker = StackWells()
        stacker.process(submission.filing_number)

        # Load all the submissions.
        submissions = ActivitySubmission.objects.filter(well_tag_number=well)
        # Load the updated well record.
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(submissions.count(), 1, "It is expected that no legacy submission be created")
        self.assertEqual(new_full_name, well.owner_full_name)
