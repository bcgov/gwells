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
from urllib.parse import quote
from minio import Minio
from gwells.settings.base import get_env_variable

# NOTE Well Summary page uses publicly-viewable S3 bucket, so no credentials are needed
#


class MinioClient():

    def __init__(self):
        self.public_host = get_env_variable('S3_HOST', strict=True)
        self.public_bucket = get_env_variable('S3_ROOT_BUCKET', strict=True)
        self.public_client = Minio(
            self.public_host,
            access_key=None,
            secret_key=None,
            secure=True
        )

        self.private_access_key = get_env_variable('S3_PRIVATE_ACCESS_KEY')
        self.private_secret_key = get_env_variable('S3_PRIVATE_SECRET_KEY')
        self.private_host = get_env_variable('S3_PRIVATE_HOST', strict=True)
        self.private_bucket = get_env_variable('S3_PRIVATE_BUCKET')
        self.private_client = Minio(
            self.private_host,
            access_key=self.private_access_key,
            secret_key=self.private_secret_key,
            secure=True
        )

    def create_url(self, obj, host):
        """Generate URL for a document """
        return 'https://{}/{}/{}'.format(
            host,
            quote(obj.bucket_name),
            quote(obj.object_name)
        )

    def create_url_list(self, objects, host):
        """Generate a list of document objects"""
        urls = list(
            map(
                lambda document: {
                    'url': self.create_url(document, host),
                    'name': document.object_name.split('/', 1)[1],
                }, objects)
        )
        return urls

    def get_documents(self, well_tag_number: int, include_private=False):
        """Retrieves a list of available documents for a given well tag number"""

        prefix = str(str('{:0<6}'.format('{:0>2}'.format(well_tag_number//10000))) + '/WTN ' +
                     str(well_tag_number) + '_')

        # provide all requests with a "public" collection of documents
        objects = {
            "public": self.create_url_list(
                self.public_client.list_objects(
                    self.public_bucket, prefix=prefix, recursive=True),
                self.public_host
            )}

        # authenticated requests also receive a "private" collection
        if include_private:
            priv_objects = self.create_url_list(
                self.private_client.list_objects(
                    self.private_bucket, prefix=prefix, recursive=True),
                self.private_host)
            objects['private'] = priv_objects

        return objects
