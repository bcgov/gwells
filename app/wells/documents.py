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
import sys
import os
import logging
from datetime import timedelta
from django.urls import reverse
from urllib.parse import quote
from minio import Minio
from gwells.settings.base import get_env_variable

logger = logging.getLogger(__name__)


class MinioClient():
    """ Load a minio client to handle public and/or private file requests

    Requires environment variables:
        S3_HOST: hostname for public document storage
        S3_ROOT_BUCKET: public document storage bucket
        MINIO_ACCESS_KEY: private storage account
        MINIO_SECRET_KEY: private storage secret
        S3_PRIVATE_HOST: private storage host (must be specified even if same as public storage)
        S3_PRIVATE_BUCKET: private storage bucket

    The optional "request" param can be set to the request that requires the minio client.
    This allows generation of full URIs including domain name.
    This is only required for generating private, local links.

    e.g.:
    def get(self, request):
        client = MinioClient(request)

    """

    def __init__(self, request=None, disable_public=False, disable_private=False):
        self.request = request

        if not disable_public:
            self.public_host = get_env_variable('S3_HOST', strict=True)
            self.public_bucket = get_env_variable(
                'S3_ROOT_BUCKET', strict=True)
            self.public_access_key = get_env_variable(
                'S3_PUBLIC_ACCESS_KEY', warn=False)
            self.public_secret_key = get_env_variable(
                'S3_PUBLIC_SECRET_KEY', warn=False)

            self.public_client = Minio(
                self.public_host,
                access_key=self.public_access_key,
                secret_key=self.public_secret_key,
                secure=True
            )
        self.disable_private = disable_private

    def create_private_client(self):
        self.private_access_key = get_env_variable('MINIO_ACCESS_KEY')
        self.private_secret_key = get_env_variable('MINIO_SECRET_KEY')
        self.private_host = get_env_variable('S3_PRIVATE_HOST')
        self.private_bucket = get_env_variable('S3_PRIVATE_BUCKET')

        return Minio(
            self.private_host,
            access_key=self.private_access_key,
            secret_key=self.private_secret_key,
            secure=True
        )

    def get_private_file(self, object_name: str):
        """ Generates a link to a private document with name "object_name" (name includes prefixes) """
        return self.private_client.presigned_get_object(
            self.private_bucket,
            object_name,
            expires=timedelta(minutes=12))

    def create_url(self, obj, host, private=False):
        """Generate a URL for a file/document

        obj: the file object returned by Minio.list_objects()
        host: the host where the file was found
        tag: well tag number
        private: private file permissions are handled by externally. when private=True,
            an external link will be generated.
        """

        if private:
            return self.get_private_file(obj.object_name)

        return 'https://{}/{}/{}'.format(
            host,
            quote(obj.bucket_name),
            quote(obj.object_name)
        )

    def create_url_list(self, objects, host, private=False):
        """Generate a list of documents with name and url"""
        urls = list(
            map(
                lambda document: {
                    'url': self.create_url(document, host, private),

                    # split on last occurrence of '/' and return last item (supports any or no prefixes)
                    'name': document.object_name.rsplit('/', 1)[-1]
                }, objects)
        )
        return urls

    def get_documents(self, well_tag_number: int, include_private=False):
        """Retrieves a list of available documents for a given well tag number"""

        # prefix well tag numbers with a 6 digit "folder" id
        # e.g. WTA 23456 goes into prefix 020000/
        prefix = str(str('{:0<6}'.format('{:0>2}'.format(well_tag_number//10000))) + '/WTN ' +
                     str(well_tag_number) + '_')

        objects = {}

        # provide all requests with a "public" collection of documents
        if self.public_client:
            pub_objects = []
            try:
                pub_objects = self.create_url_list(
                    self.public_client.list_objects(
                        self.public_bucket, prefix=prefix, recursive=True),
                    self.public_host)
            except:
                logger.error(
                    "Could not retrieve files from public file server")

            objects['public'] = pub_objects

        # authenticated requests also receive a "private" collection
        self.private_client = self.create_private_client()
        if include_private and self.private_client:
            priv_objects = []
            try:
                priv_objects = self.create_url_list(
                    self.private_client.list_objects(
                        self.private_bucket, prefix=prefix, recursive=True),
                    self.private_host, private=True)
            except:
                logger.error(
                    "Could not retrieve files from private file server", exc_info=sys.exc_info())

            objects['private'] = priv_objects

        return objects
