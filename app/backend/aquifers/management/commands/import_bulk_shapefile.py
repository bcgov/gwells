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

from django.contrib.gis.geos.prototypes.io import wkt_w

# Run from command line :
# python manage.py load_shapefile <folder containing shapefiles>
from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis import geos

import logging

logger = logging.getLogger(__name__)


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
        for root, directories, filenames in os.walk(options['path']):
            for filename in filenames: 
                if filename.lower().endswith(".shp"):
                    logging.info("processing shapefile".format(filename))
                    ds = DataSource(os.path.join(root, filename))
                    for layer in ds:
                        for feat in layer:
                            geom = feat.geom
                            #logging.debug(' '.join(['{}:{}'.format(f, feat.get(f)) for f in feat.fields]))
                            if "AQ_NUMBER" not in feat.fields:
                                logging.info("Feature with no AQ_NUMBER attribute found skipping import.")
                                continue

                            # Make a GEOSGeometry object using the string representation.
                            if not geom.srid == 3005:
                                logging.info("Non BC-albers feature, skipping.")
                                continue

                            aquifer_id = feat.get("AQ_NUMBER")
                            try:
                                aquifer = Aquifer.objects.get(pk=int(aquifer_id))
                            except Aquifer.DoesNotExist:
                                logging.info("Aquifer {} not found in database, skipping import.".format(aquifer_id))
                                continue

                            wkt = wkt_w(dim=2).write( GEOSGeometry(geom.wkt, srid=3005)).decode()
                            geos_geom = GEOSGeometry(wkt, srid=3005)
                            if isinstance(geos_geom, geos.MultiPolygon):
                                geos_geom_out = geos_geom[0]
                                for g in geos_geom:
                                    if len(g.wkt) > len(geos_geom_out.wkt):
                                        geos_geom_out = g
                            elif isinstance(geos_geom, geos.Polygon):
                                geos_geom_out = geos_geom
                            else:
                                logging.info("Bad geometry type: {}, skipping.".format(geos_geom.__class__))
                                continue
                            
                            try:
                                aquifer.geom = geos_geom_out
                            except Exception as e:
                                logging.info("import failed. {}, droppin into shell for inspection".format(e))
                                import code; code.interact(local = locals())
                                sys.exit(1)

                            aquifer.save()
