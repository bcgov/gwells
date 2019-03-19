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
import json
import os
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import connection

from minio import Minio

from gwells.settings.base import get_env_variable
from wells.models import Well

"""
Run from command line :
python manage.py export_databc

This command runs in an OpenShift cronjob, defined in export.cj.json
"""


logger = logging.getLogger(__name__)


# IMPORTANT: If the underlying data structure changes (e.g. column name changes etc.), the
# property names have to stay the same! This endpoint is consumed by DataBC and must remain
# stable!
# Casing diameter: For now, grab the smallest diameter (should be using type, but we don't have 
# date right now.)
WELLS_SQL = ("""
select
    ST_AsGeoJSON(ST_Transform(geom, 4326)) :: json as "geometry",
    well.well_tag_number,
    well.identification_plate_number,
    SUBSTRING(well_status_code.description for 255) as well_status,
    SUBSTRING(licenced_status_code.description for 255) as licenced_status,
    SUBSTRING(CONCAT('https://apps.nrs.gov.bc.ca/gwells/well/', well.well_tag_number) for 255) as detail,
    well.artesian_flow,
    SUBSTRING('usGPM' for 255) as artesian_flow_units,
    well.artesian_pressure,
    SUBSTRING(well_class_code.description for 100) as well_class,
    SUBSTRING(intended_water_use_code.description for 100) as intended_water_use,
    SUBSTRING(well.street_address for 100) as street_address,
    well.finished_well_depth,
    casing.diameter,
    well.static_water_level,
    well.bedrock_depth,
    well.well_yield as yield,
    SUBSTRING(well_yield_unit_code.description for 100) as yield_unit,
    well.aquifer_id as aquifer_id
from well
    left join well_status_code on well_status_code.well_status_code = well.well_status_code
    left join licenced_status_code on
        licenced_status_code.licenced_status_code = well.licenced_status_code
    left join well_class_code on well_class_code.well_class_code = well.well_class_code
    left join intended_water_use_code on
        intended_water_use_code.intended_water_use_code = well.intended_water_use_code
    left join well_yield_unit_code on
        well_yield_unit_code.well_yield_unit_code = well.well_yield_unit_code
    left join casing on
        casing.well_tag_number = well.well_tag_number and casing.casing_guid = (
            select casing.casing_guid from casing
            where casing.well_tag_number = well.well_tag_number
            order by casing.diameter asc limit 1)
    where well.well_tag_number >= %s and well.well_tag_number < %s
        and (well.well_publication_status_code = 'Published' or well.well_publication_status_code = null)
        and well.geom is not null
    order by well.well_tag_number
""")
MAX_WELLS_SQL = 'select max(well_tag_number) from well'
WELL_CHUNK_SIZE = 10000


# IMPORTANT: If the underlying data structure changes (e.g. column name changes etc.), the
# property names have to stay the same! This endpoint is consumed by DataBC and must remain
# stable!
LITHOLOGY_SQL = ("""
select
    ST_AsGeoJSON(ST_Transform(geom, 4326)) :: json as "geometry",
    well.well_tag_number,
    identification_plate_number,
    SUBSTRING(well_status_code.description for 255) as well_status,
    SUBSTRING(licenced_status_code.description for 255) as licenced_status,
    SUBSTRING(CONCAT('https://apps.nrs.gov.bc.ca/gwells/well/', well.well_tag_number) for 255) as detail,
    lithology_description.lithology_from as from,
    lithology_description.lithology_to as to,
    SUBSTRING(lithology_colour_code.description for 100) as colour,
    SUBSTRING(lithology_description_code.description for 255) as description,
    SUBSTRING(lithology_material_code.description for 255) as material,
    SUBSTRING(lithology_description.lithology_observation for 250) as observation,
    SUBSTRING(lithology_hardness_code.description for 100) as hardness,
    SUBSTRING(well_class_code.description for 100) as well_class,
    SUBSTRING(intended_water_use_code.description for 100) as intended_water_use,
    SUBSTRING(well.street_address for 100) as street_address,
    well.finished_well_depth,
    casing.diameter,
    well.static_water_level,
    well.bedrock_depth,
    well.well_yield as yield,
    SUBSTRING(well_yield_unit_code.description for 100) as yield_unit,
    well.aquifer_id as aquifer
from well
    inner join lithology_description on
        lithology_description.well_tag_number = well.well_tag_number
    left join well_status_code on
        well_status_code.well_status_code = well.well_status_code
    left join licenced_status_code on
        licenced_status_code.licenced_status_code = well.licenced_status_code
    left join lithology_material_code on
        lithology_material_code.lithology_material_code =
            lithology_description.lithology_material_code
    left join lithology_colour_code on
        lithology_colour_code.lithology_colour_code = lithology_description.lithology_colour_code
    left join lithology_description_code on
        lithology_description_code.lithology_description_code =
            lithology_description.lithology_description_code
    left join lithology_hardness_code on
        lithology_hardness_code.lithology_hardness_code =
            lithology_description.lithology_hardness_code
    left join well_class_code on well_class_code.well_class_code = well.well_class_code
    left join intended_water_use_code on
        intended_water_use_code.intended_water_use_code = well.intended_water_use_code
    left join well_yield_unit_code on
        well_yield_unit_code.well_yield_unit_code = well.well_yield_unit_code
    left join casing on
        casing.well_tag_number = well.well_tag_number and casing.casing_guid = (
            select casing.casing_guid from casing
            where casing.well_tag_number = well.well_tag_number
            order by casing.diameter asc limit 1)
    where well.well_tag_number >= %s and well.well_tag_number < %s
        and (well.well_publication_status_code = 'Published' or well.well_publication_status_code = null)
        and well.geom is not null
    order by well.well_tag_number, lithology_description.lithology_from
""")
MAX_LITHOLOGY_SQL = MAX_WELLS_SQL
LITHOLOGY_CHUNK_SIZE = 10000

# IMPORTANT: If the underlying data structure changes (e.g. column name changes etc.), the
# property names have to stay the same! This endpoint is consumed by DataBC and must remain
# stable!
AQUIFERS_SQL = ("""
select
    ST_AsGeoJSON(ST_Transform(geom, 4326)) :: json as "geometry",
    aquifer.aquifer_id as aquifer_id,
    SUBSTRING(aquifer.aquifer_name for 100) as name,
    SUBSTRING(aquifer.location_description for 100) as location,
    SUBSTRING(aquifer_material_code.description for 100) as material,
    SUBSTRING(aquifer_subtype_code.description for 100) as subtype,
    SUBSTRING(aquifer_vulnerability_code.description for 100) as vulnerability,
    SUBSTRING(aquifer_productivity_code.description for 100) as productivity,
    SUBSTRING(aquifer_demand_code.description for 100) as demand,
    SUBSTRING(water_use_code.description for 100) as water_use,
    SUBSTRING(quality_concern_code.description for 100) as quality_concern,
    SUBSTRING(aquifer.litho_stratographic_unit for 100) as litho_stratographic_unit,
    aquifer.mapping_year,
    SUBSTRING(aquifer.notes for 2000) as notes
from aquifer
    left join aquifer_material_code on
        aquifer_material_code.aquifer_material_code = aquifer.aquifer_material_code
    left join aquifer_subtype_code on
        aquifer_subtype_code.aquifer_subtype_code = aquifer.aquifer_subtype_code
    left join aquifer_vulnerability_code on
        aquifer_vulnerability_code.aquifer_vulnerability_code = aquifer.aquifer_vulnerablity_code
    left join aquifer_productivity_code on
        aquifer_productivity_code.aquifer_productivity_code = aquifer.aquifer_productivity_code
    left join aquifer_demand_code on
        aquifer_demand_code.aquifer_demand_code = aquifer.aquifer_demand_code
    left join water_use_code on
        water_use_code.water_use_code = aquifer.water_use_code
    left join quality_concern_code on
        quality_concern_code.quality_concern_code = aquifer.quality_concern_code
    where aquifer.aquifer_id >= %s and aquifer.aquifer_id < %s
        and aquifer.geom is not null
    order by aquifer.aquifer_id
""")
MAX_AQUIFERS_SQL = 'select max(aquifer_id) from aquifer'
AQUIFER_CHUNK_SIZE = 100


class LazyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class GeoJSONIterator():

    def __init__(self, sql, chunk_size, cursor, max_query):
        # Keep track of the start time (purely for logging).
        self.send_header = True
        self.done = False
        self.current_index = 0
        self.first_record = True
        self.current_index = 0
        self.chunk_size = chunk_size
        self.sql = sql
        self.cursor = cursor
        self.max_index = self.get_max_index(max_query)
        self.get_chunk()
        self.fields = self.get_fields()

    def get_max_index(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        if row[0] is None:
            return 0
        return row[0]

    def get_chunk(self):
        logger.info('fetching {current_index}...{next_index}'.format(
            current_index=self.current_index,
            next_index=self.current_index+self.chunk_size))
        self.cursor.execute(self.sql, (self.current_index, self.current_index+self.chunk_size))

    def get_header(self):
        return """{"type": "FeatureCollection","features": ["""

    def get_footer(self):
        return ']}'

    def format_record(self, record):
        """ Write a single record to file."""
        feature = {
            'type': 'Feature',
            'geometry': record[0],
            'properties': {}
        }
        for col, value in enumerate(record):
            if self.fields[col] != 'geometry':
                feature['properties'][self.fields[col]] = value
        return json.dumps(feature, cls=LazyEncoder)

    def get_fields(self):
        fields = []
        for index, field in enumerate(self.cursor.description):
            fieldName = field[0]
            fields.append(fieldName)
        return fields

    def get_record(self):
        record = self.cursor.fetchone()
        while not record and self.current_index + self.chunk_size < self.max_index:
            # Move the cursor along..
            self.current_index += self.chunk_size
            self.get_chunk()
            record = self.cursor.fetchone()
        if record:
            return self.format_record(record)
        return None

    def __iter__(self):
        return self

    def __next__(self):
        # If we're right at the start, send the header.
        if self.send_header:
            self.send_header = False
            return self.get_header()
        # If we're chugging along, send a record.
        record = self.get_record()
        if record:
            if self.first_record:
                self.first_record = False
            else:
                record = ',{}'.format(record)
            return record
        if self.done:
            # If we're done, be done!
            raise StopIteration
        # This means we sent our last record
        self.done = True
        return self.get_footer()


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Arguments added for debugging purposes.
        # e.g. don't cleanup, don't upload: python manage.py export_databc --cleanup=0 --upload=0
        parser.add_argument('--cleanup', type=int, nargs='?', help='If 1, remove file when done', default=1)
        parser.add_argument('--upload', type=int, nargs='?', help='If 1, upload the file', default=1)

    def handle(self, *args, **options):
        """Entry point for Django Command."""
        files = ('wells.json', 'aquifers.json', 'lithology.json')
        print(options)
        logger.info('Starting GeoJSON export.')
        try:
            self.generate_wells('wells.json')
            self.generate_lithology('lithology.json')
            self.generate_aquifers('aquifers.json')
            if options['upload'] == 1:
                self.upload_files(files)
        finally:
            if options['cleanup'] == 1:
                self.cleanup(files)
        logger.info('GeoJSON export complete.')
        self.stdout.write(self.style.SUCCESS('GeoJSON export complete.'))

    def cleanup(self, files):
        """Delete all local files GeoJSON files."""
        for filename in files:
            if os.path.exists(filename):
                os.remove(filename)

    def upload_files(self, files):
        """Upload files to S3 bucket."""
        is_secure = get_env_variable('S3_USE_SECURE', '1', warn=False) is '1'
        minioClient = Minio(get_env_variable('S3_HOST'),
                            access_key=get_env_variable(
                                'S3_PUBLIC_ACCESS_KEY'),
                            secret_key=get_env_variable(
                                'S3_PUBLIC_SECRET_KEY'),
                            secure=is_secure)
        for filename in files:
            logger.info('uploading {}'.format(filename))
            with open(filename, 'rb') as file_data:
                file_stat = os.stat(filename)
                target = 'api/v1/gis/{}'.format(filename)
                bucket = get_env_variable('S3_WELL_EXPORT_BUCKET')
                logger.debug(
                    'uploading {} to {}/{}'.format(filename, bucket, target))
                minioClient.put_object(bucket,
                                       target,
                                       file_data,
                                       file_stat.st_size)

    def generate_geojson_chunks(self, sql, target, chunk_size, max_query):
        logger.info('Generating GeoJSON for {}'.format(target))
        # Open JSON file to write to.
        with connection.cursor() as cursor:
            with open(target, 'w') as f:
                reader = GeoJSONIterator(sql, chunk_size, cursor, max_query)
                count = 0
                for item in reader:
                    f.write('{}\r\n'.format(item))
                    count += 1

    def generate_lithology(self, target):
        self.generate_geojson_chunks(LITHOLOGY_SQL, target, LITHOLOGY_CHUNK_SIZE, MAX_LITHOLOGY_SQL)

    def generate_aquifers(self, filename):
        self.generate_geojson_chunks(AQUIFERS_SQL, filename, AQUIFER_CHUNK_SIZE, MAX_AQUIFERS_SQL)

    def generate_wells(self, filename):
        self.generate_geojson_chunks(WELLS_SQL, filename, WELL_CHUNK_SIZE, MAX_WELLS_SQL)
