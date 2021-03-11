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
import os
import logging
from collections import defaultdict
import urllib.parse

from django.core.management.base import BaseCommand
from minio import Minio

from gwells.settings.base import get_env_variable

# Run from command line :
# python manage.py export_welltags_documents_csv
#
# For development/debugging, it's useful to skip upload and cleanup
# python manage.py export_welltags_documents_csv --cleanup=0 --upload=0

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def __init__(self):
        """
        define our custom variables class wide
        """
        super().__init__()
        self.gwells_url_prefix = get_env_variable('WATER_1651_GWELLS_URL_PREFIX')
        self.gwells_s3_prefix = get_env_variable('WATER_1651_GWELLS_S3_PREFIX')
        self.output_filename = 'gwells_export_welltags_documents.csv'

    def add_arguments(self, parser):
        # Arguments added for debugging purposes.
        # e.g. don't cleanup, don't upload: python manage.py export_welltags_documents_csv --cleanup=0 --upload=0
        parser.add_argument('--cleanup', type=int, nargs='?', help='If 1, remove file when done', default=1)
        parser.add_argument('--upload', type=int, nargs='?', help='If 1, upload the file', default=1)

    def handle(self, *args, **options):
        """
        primary entrypoint
        """
        logger.info('starting export_welltags_documents_csv')
        self.export(self.output_filename)

        if options['upload'] == 1:
            self.upload_file(self.output_filename)
        if options['cleanup'] == 1:
            logger.info('cleaning up')
            if os.path.exists(self.output_filename):
                os.remove(self.output_filename)

        logger.info('export_welltags_documents_csv complete')
        self.stdout.write(self.style.SUCCESS('export_welltags_documents_csv complete'))

    def export(self, filename):
        """
        using the minio client, list all objects in the S3_WELL_BUCKET recursively
        place the values into a dict
        take those values from the dict and place them into a defaultdict(list) to get unique well tags per row
            and multiple document urls for that unique well tag
        """
        if os.path.exists(filename):
            os.remove(filename)

        # recursively walk the minio bucket
        client = Minio(get_env_variable('S3_HOST'),
                       access_key=get_env_variable('S3_PUBLIC_ACCESS_KEY'),
                       secret_key=get_env_variable('S3_PUBLIC_SECRET_KEY'))
        objects = client.list_objects(get_env_variable('S3_WELL_BUCKET'), recursive=True)
        wells = []
        unique_well_dict = defaultdict(list)
        for o in objects:
            try:
                well_tag = o.object_name[o.object_name.find('/WTN '):o.object_name.find('_')].replace('/WTN ', '')
                if well_tag is not None and well_tag != '':
                    well_output = {'well_tag': well_tag,
                                   'well_url': f'{self.gwells_url_prefix}{well_tag}',
                                   'document_url': f'{self.gwells_s3_prefix}{get_env_variable("S3_WELL_BUCKET")}/{o.object_name.replace(" ", "%20")}'
                                   }
                    wells.append(well_output)
            except:
                pass

        # write our wells out to a unique welltag per row!
        for well in wells:
            if well['well_url'] not in unique_well_dict[well['well_tag']]:
                unique_well_dict[well['well_tag']].append(well['well_url'])
            unique_well_dict[well['well_tag']].append(well['document_url'])

        # write our well tags and their child array items to csvfile
        with open(filename, 'w') as csvfile:
            for well_tag in unique_well_dict:
                csvfile.write(f'{well_tag},')
                for array_item in unique_well_dict[well_tag]:
                    csvfile.write(f'{array_item},')
                csvfile.write('\n')

        self.stdout.write(self.style.SUCCESS(f'wrote file to: {os.getcwd()}/{filename}'))

    def upload_file(self, filename):
        """
        upload our file to S3_HOST, secure, S3_WELL_BUCKET export/filename
        """
        client = Minio(get_env_variable('S3_HOST'),
                       access_key=get_env_variable('S3_PUBLIC_ACCESS_KEY'),
                       secret_key=get_env_variable('S3_PUBLIC_SECRET_KEY'),
                       secure='1')
        logger.info('uploading {}'.format(filename))

        # write our file to minio
        with open(filename, 'rb') as file_data:
            file_stat = os.stat(filename)
            target = f'export/{filename}'
            client.put_object(get_env_variable('S3_WELL_BUCKET'),
                              target,
                              file_data,
                              file_stat.st_size)

        self.stdout.write(self.style.SUCCESS(f'uploaded file to: {get_env_variable("S3_HOST")}/{get_env_variable("S3_WELL_BUCKET")}/{target}'))
