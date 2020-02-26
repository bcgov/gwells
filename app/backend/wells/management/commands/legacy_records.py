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
from timeit import default_timer as timer

from django.core.management.base import BaseCommand
from django.db import transaction

from wells.models import Well
from wells.stack import StackWells

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Run from command line:
    python manage.py legacy_records
    """

    def add_arguments(self, parser):
        # Arguments added for debugging purposes.
        parser.add_argument('--start', type=int, nargs='?', help='Well to start at', default=1)
        parser.add_argument('--end', type=int, nargs='?', help='Well to end at', default=50)
        parser.add_argument('--next', type=int, nargs='?', help='Process n wells', default=50)

    def handle(self, *args, **options):
        start = options['start']
        end = options['end']
        to_do_amount = options['next']

        num_wells = 0
        if to_do_amount:
            wells = self.find_next_n_wells_without_legacy_records(start, to_do_amount)
        else:
            wells = self.find_wells_without_legacy_records(start, end)

        num_wells = len(wells)
        print(f'Creating {num_wells} legacy records from well_tag_number {wells[0].well_tag_number} to {wells[len(wells) - 1].well_tag_number}')

        start = timer()
        for well in wells:
            try:
                self.create_legacy_record(well)
            except Exception as err:
                print(f'Error creating legacy record for well_tag_number {well.well_tag_number}')
                raise err
        end = timer()

        success_msg = 'Created {} legacy reports in {:.2f}s'.format(num_wells, end - start)
        self.stdout.write(self.style.SUCCESS(success_msg))

    def find_wells_without_legacy_records(self, start, end):
        wells = Well.objects \
            .filter(well_tag_number__gte=start,
                    well_tag_number__lte=end,
                    activitysubmission__isnull=True) \
            .order_by('well_tag_number')
        return wells

    def find_next_n_wells_without_legacy_records(self, start, num):
        wells = Well.objects \
            .filter(well_tag_number__gte=start, activitysubmission__isnull=True) \
            .order_by('well_tag_number') \
            [0:num]
        return wells

    @transaction.atomic
    def create_legacy_record(self, well):
        # NOTE that _create_legacy_submission() will create the LEGACY activity
        # submission but then when the `submission_serializer.save()` is called
        # inside of `_create_legacy_submission()` this will trigger a
        # `StackWells().process()` call which will in turn call
        # `_update_well_record()` which checks to see if it should create a new
        # legacy record (it shouldn't). Instead it will just call
        # `self._stack(records, submission.well)` for this one legacy record.
        StackWells()._create_legacy_submission(well)
