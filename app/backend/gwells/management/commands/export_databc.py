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

# Run from command line :
# python manage.py export_databc
#
# This command runs in an OpenShift cronjob, defined in export-databc.cj.json


logger = logging.getLogger(__name__)


class LazyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Entry point for Django Command."""
        files = ('wells.json', 'aquifers.json', 'lithology.json')
        logger.info('Starting GeoJSON export.')
        try:
            self.generate_wells('wells.json')
            self.generate_lithology('lithology.json')
            self.generate_aquifers('aquifers.json')
            self.upload_files(files)
        finally:
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
        minioClient = Minio(get_env_variable('S3_HOST'),
                            access_key=get_env_variable(
                                'S3_PUBLIC_ACCESS_KEY'),
                            secret_key=get_env_variable(
                                'S3_PUBLIC_SECRET_KEY'),
                            secure=True)
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

    def write_record(self, f, record, fields, delim):
        """ Write a single record to file."""
        feature = {
            'type': 'Feature',
            'geometry': record[0],
            'properties': {}
        }
        for col, value in enumerate(record):
            if value is not None and fields[col] != 'geometry':
                feature['properties'][fields[col]] = value
        if delim:
            f.write(',')
        f.write('\r\n')
        f.write(json.dumps(feature, cls=LazyEncoder))

    def generate_geojson_chunks(self, sql, target, max_key, chunk_size):
        """Generate GeoJSON in chunks small enough that we don't run out of memory,
        or keep connections to the DB open for too long."""

        # Keep track of the start time (purely for logging).
        start = datetime.now()
        # Open JSON file to write to.
        with open(target, 'w') as f:
            # Write the header - it's always the same.
            self.write_geojson_header(f)
            logger.info('{}: fetching spatial data from database...'.format(target))
            current_index = 0
            total_row_count = 0
            more_chunks = True
            # Loop until there are no more records.
            while more_chunks:
                with connection.cursor() as cursor:
                    more_chunks = False
                    logger.info('{target}: fetching {max_key} {current_index}...{next_index} '
                                '({timestamp})'.format(target=target,
                                                       max_key=max_key,
                                                       current_index=current_index,
                                                       next_index=current_index+chunk_size,
                                                       timestamp=datetime.now() - start))
                    # Get the next chunk from database.
                    cursor.execute(sql.format(current_index, current_index+chunk_size))
                    # Get all the field names.
                    fields = []
                    for index, field in enumerate(cursor.description):
                        fieldName = field[0]
                        fields.append(fieldName)
                    # Get the first record.
                    record = cursor.fetchone()
                    # Loop until there are no more records.
                    while record:
                        # Write this particular record to file.
                        self.write_record(f, record, fields, delim=total_row_count > 0)
                        # Periodically log our progress.
                        if total_row_count % 50000 == 0:
                            logger.info('{target}: processed {rows} rows ; ({timestamp})'.format(
                                target=target,
                                rows=total_row_count,
                                timestamp=datetime.now() - start))
                        # Keep track of the total row count.
                        total_row_count += 1
                        # Get the next record.
                        record = cursor.fetchone()
                        # Tell the outer loop, to fetch another chunk.
                        more_chunks = True
                    # Move our index forward.
                    current_index += chunk_size
            logger.info('{target}: done iterating through ({total}), total time: {timestamp}'.format(
                        target=target,
                        total=total_row_count,
                        timestamp=datetime.now() - start))
            # Write the footer, it's always the same.
            f.write("]}")
        logger.info('{target}: complete, total time: {timestamp}'.format(
            target=target, timestamp=datetime.now() - start))

    def write_geojson_header(self, f):
        """Our header is always the same, a feature collection."""
        f.write("""{
    "type": "FeatureCollection",
    "features": [
""")

    def generate_lithology(self, target):
        # IMPORTANT: If the underlying data structure changes (e.g. column name changes etc.), the
        # property names have to stay the same! This endpoint is consumed by DataBC and must remain
        # stable!
        sql = ("""
select
    ST_AsGeoJSON(geom) :: json as "geometry",
    well.well_tag_number,
    identification_plate_number,
    well_status_code.description as well_status_description,
    licenced_status_code.description as licenced_status_description,
    CONCAT('https://apps.nrs.gov.bc.ca/gwells/well/',well.well_tag_number) as detail,
    lithology_description.lithology_from,
    lithology_description.lithology_to,
    lithology_colour_code.description as lithology_colour_description,
    lithology_description_code.description as lithology_description,
    lithology_material_code.description as lithology_material_description,
    lithology_observation,
    lithology_hardness_code.description as lithology_hardness_description,
    well_class_code.description as well_class_description,
    intended_water_use_code.description as intended_water_use_description,
    street_address,
    finished_well_depth,
    diameter,
    static_water_level,
    bedrock_depth,
    well_yield,
    well_yield_unit_code.description as well_yield_unit,
    aquifer_id
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
    where well.well_tag_number >= {} and well.well_tag_number < {}
    order by well.well_tag_number, lithology_description.lithology_from
""")
        self.generate_geojson_chunks(
            sql, target, 'well_tag_number', chunk_size=10000)

    def generate_aquifers(self, filename):
        # IMPORTANT: If the underlying data structure changes (e.g. column name changes etc.), the
        # property names have to stay the same! This endpoint is consumed by DataBC and must remain
        # stable!
        sql = ("""
select
    ST_AsGeoJSON(geom) :: json as "geometry",
    aquifer_id,
    aquifer_name,
    location_description,
    aquifer_material_code.description as aquifer_material_description,
    aquifer_subtype_code.description as aquifer_subtype_description,
    area,
    aquifer_vulnerability_code.description as aquifer_vulnerablity_description,
    aquifer_productivity_code.description as aquifer_productivity_description,
    aquifer_demand_code.description as aquifer_demand_description,
    water_use_code.description as water_use_description,
    quality_concern_code.description as quality_concern_description,
    litho_stratographic_unit,
    mapping_year,
    notes
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
    where aquifer.aquifer_id >= {} and aquifer.aquifer_id < {}
    order by aquifer.aquifer_id
""")
        self.generate_geojson_chunks(sql, filename, 'aquifer_id', chunk_size=10)

    def generate_wells(self, filename):
        # IMPORTANT: If the underlying data structure changes (e.g. column name changes etc.), the
        # property names have to stay the same! This endpoint is consumed by DataBC and must remain
        # stable!
        sql = ("""
select
    ST_AsGeoJSON(geom) :: json as "geometry",
    well_tag_number,
    identification_plate_number,
    well_status_code.description as well_status_description,
    licenced_status_code.description as licenced_status,
    CONCAT('https://apps.nrs.gov.bc.ca/gwells/well/',well_tag_number) as detail,
    artesian_flow, 'usGPM' as artesian_flow_units, artesian_pressure,
    well_class_code.description as well_class_description,
    intended_water_use_code.description as intended_water_use_description,
    street_address,
    finished_well_depth,
    diameter,
    static_water_level,
    bedrock_depth,
    well_yield,
    well_yield_unit_code.description as well_yield_unit,
    aquifer_id
from well
    left join well_status_code on well_status_code.well_status_code = well.well_status_code
    left join licenced_status_code on
        licenced_status_code.licenced_status_code = well.licenced_status_code
    left join well_class_code on well_class_code.well_class_code = well.well_class_code
    left join intended_water_use_code on
        intended_water_use_code.intended_water_use_code = well.intended_water_use_code
    left join well_yield_unit_code on
        well_yield_unit_code.well_yield_unit_code = well.well_yield_unit_code
    where well.well_tag_number >= {} and well.well_tag_number < {}
    order by well.well_tag_number
""")
        self.generate_geojson_chunks(sql, filename, 'well_tag_number', chunk_size=10000)
