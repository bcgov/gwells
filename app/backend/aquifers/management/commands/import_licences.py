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
import csv
from django.conf import settings

from aquifers.models import WaterRightsLicence, WaterRightsPurpose, Aquifer
from wells.models import Well

# Run from command line :
# python manage.py load_shapefile <filename>
from django.core.management.base import BaseCommand

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        with open(options['filename'], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # used in DEBUG mode only.
            counter = 0
            num_wells = Well.objects.count()

            for row in reader:

                if row['PD_SBTYPE'] not in ['PWD', 'PG']:
                    # [Nicole]: (we are only concerned with PWD and PG data – exclude any
                    # rows with POD. POD refers to surface water which is out of scope for GWELLS)
                    continue

                logging.info("importing: {}".format(row))

                # In dev envs, desecrate the data so it fits our fake fixtures.
                if settings.DEBUG:
                    counter += 1
                    well = Well.objects.all()[counter % num_wells:][0]
                    # we need our wells to actually have an aquifir for nontrivial testing.
                    if not well.aquifer:
                        well.aquifer = Aquifer.objects.first()
                        well.save()
                else:
                    # Check the Licence is for a valid Aquifer
                    if not row['SOURCE_NM'].isdigit():
                        continue
                    Aquifer.objects.get(pk=row['SOURCE_NM'])
                    well = Well.objects.get(pk=row['WLL_TG_NMR'])

                # Maintaina code table with water rights purpose.
                purpose, is_new = WaterRightsPurpose.objects.get_or_create(
                    code=row['PRPS_S_CD'],
                    description=row['PRPS_SE'])

                try:
                    # Update existing licences with changes.
                    licence = WaterRightsLicence.objects.get(
                        licence_number=row['LCNC_NMBR'])
                except WaterRightsLicence.DoesNotExist:
                    licence = WaterRightsLicence(
                        licence_number=row['LCNC_NMBR']
                    )
                licence.purpose = purpose
                licence.quantity = row['QUANTITY']
                licence.well = well
                print(licence.well)
                licence.save()
