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
from django.test import TestCase

from wells.models import ActivitySubmission, Well
from wells.stack import StackWells


class StackTest(TestCase):

    def test_construction_submission_to_well(self):
        # Creating a brand new well, we only have a construction submission for.
        owner_full_name = 'Bob'
        submission = ActivitySubmission.objects.create(owner_full_name=owner_full_name)
        stacker = StackWells()
        well = stacker.create(stacker.filing_number)
        Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(owner_full_name, well.owner_full_name)

    def test_alteration_to_construction(self):
        # The well already exists, and has a construction submission.
        pass

    def test_alteration_to_well(self):
        # The well already exists, but has no construction submission.
        pass
