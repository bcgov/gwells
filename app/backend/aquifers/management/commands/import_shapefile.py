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
from aquifers.models import Aquifer
import csv
import zipfile

# Run from command line :
# python manage.py load_shapefile <aquifer_id> <shapefile name>
from django.core.management.base import BaseCommand

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('aquifer_id', type=int)
        parser.add_argument('shapefile', type=str)

    def handle(self, *args, **options):
        logging.info("Getting aquifer with ID {}".format(
            options['aquifer_id']))
        aquifer = Aquifer.objects.get(pk=options['aquifer_id'])
        logger.info('starting')
        logging.info("Loading shapefile {}".format(options['shapefile']))
        aquifer.load_shapefile(open(options['shapefile'], 'rb'))
        aquifer.save()
