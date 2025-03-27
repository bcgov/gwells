from aquifers.models import Aquifer
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
import zipfile
import os

from django.conf import settings

from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource


import logging

logger = logging.getLogger(__name__)

# Run from command line :
# python manage.py import_bulk_shapefile <folder containing shapefiles>


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        logging.info("Inspecting {}".format(options['path']))

        # Recursively unzip ugly masses of zipped shapfiles.
        found_zip = True
        while found_zip:
            found_zip = False
            for root, directories, filenames in os.walk(options['path']):
                for filename in filenames:
                    if filename.lower().endswith(".zip"):
                        logging.info("unzipping {}".format(filename))
                        zip_ref = zipfile.ZipFile(os.path.join(root, filename))
                        zip_ref.extractall(root)
                        zip_ref.close()
                        os.remove(os.path.join(root, filename))
                        found_zip = True

        # Recursively search for shapefiles and import them.
        self.shp_idx = 0
        for root, directories, filenames in os.walk(options['path']):
            for filename in filenames:
                if filename.lower().endswith(".shp"):
                    logging.info("processing shapefile".format(filename))
                    ds = DataSource(os.path.join(root, filename))
                    for layer in ds:
                        for feat in layer:
                            self.add_aquifer(feat)

    def add_aquifer(self, feat):
        if "AQ_NUMBER" not in feat.fields:
            logging.info(
                "Feature with no AQ_NUMBER attribute found skipping import.")
            return

        aquifer_id = feat.get("AQ_NUMBER")
        # In dev environments, just assign these geometries to random aquifers.
        if settings.DEBUG:
            ct = Aquifer.objects.count() - 1
            aquifer = Aquifer.objects.all()[self.shp_idx % ct:][0]
            self.shp_idx += 1
        else:
            try:
                aquifer = Aquifer.objects.get(pk=int(aquifer_id))
            except Aquifer.DoesNotExist:
                logging.info(
                    "Aquifer {} not found in database, skipping import.".format(aquifer_id))
                return

        logging.info('importing {}'.format(aquifer_id))
        aquifer.update_geom_from_feature(feat)

        aquifer.save()
