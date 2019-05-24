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

from django.core.management.base import BaseCommand

from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.contrib.gis.geos.prototypes.io import wkt_w
from django.contrib.gis.gdal import DataSource

import ijson

from gwells.models import WaterBody


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # with open('/Users/sstrauss/Workspace/lakes/BCGW_7113060B_1558727917382_5536/FWA_LAKES_POLY.geojson', 'r') as json_data:
        #     # parser = ijson.parse(json_data)
        #     # for prefix, event, value in parser:
        #     #     logger.info('{}, {}, {}'.format(prefix, event, value))
        #     features = ijson.items(json_data, 'features.item')
        #     for feature in features:

        #         properties = feature.get('properties')
        #         logger.info('{}'.format(properties['WATERBODY_POLY_ID']))

        ds = DataSource('/Users/sstrauss/Workspace/lakes/BCGW_7113060B_1558727876780_2752/FWA_LAKES_POLY/FWLKSPL_polygon.shp')
        for layer in ds:
            logger.info('layer: {}'.format(layer))
            for feat in layer:
                # logger.info('feature: {}'.format(feat))
                waterbody_poly_id = feat.get("WTRBDPLD")
                # geom = feat.geom
                # wkt = wkt_w(dim=2).write(GEOSGeometry(geom.wkt, srid=4326)).decode()
                # geos_geom = GEOSGeometry(wkt, srid=4326)

                geom = GEOSGeometry(feat.geom.wkt, srid=4326)
                if isinstance(geom, geos.Polygon):
                    geom = MultiPolygon(geom)
                else:
                    geom = GEOSGeometry(feat.geom.wkt, srid=4326)
                logger.info('id: {}'.format(waterbody_poly_id))

                WaterBody.objects.create(waterbody_poly_id=waterbody_poly_id, geom=geom)

        # self.stdout.write(self.style.SUCCESS('Lake import complete.'))
