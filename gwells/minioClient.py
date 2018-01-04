

import os
from minio import Minio

# NOTE 's3-ca-central-1.amazonaws.com' didn't work:
# minio.error.ResponseError: ResponseError: code: AuthorizationHeaderMalformed, message: The authorization header is malformed; the region 'us-east-1' is wrong; expecting 'ca-central-1', bucket_name: None, object_name: None, request_id: 3841822DCB7F7FC6, host_id: dk3GUWHqhX6gEiE6iONYAIfIpQNvbzExauHhCCoE4uTQOW6NygKY6yPdEsODXmChlO8Auk14ftg=, region:
#

class MinioClient():

    def __init__(self):
        self.minio_access_key = os.getenv('MINIO_ACCESS_KEY')
        self.minio_secret_key = os.getenv('MINIO_SECRET_KEY')
        self.host = os.getenv('S3_HOST')
        self.link_host = os.getenv('S3_LINK_HOST')
        self.minio_client = Minio(self.host, access_key=self.minio_access_key, secret_key=self.minio_secret_key, secure=True)
        self.top_bucket = os.getenv('S3_ROOT_BUCKET')

    def get_documents(self, well_tag_number):

        prefix = str('{:0<6}'.format('{:0>2}'.format(well_tag_number//10000))) + '/WTN ' + str(well_tag_number)

        objects = self.minio_client.list_objects(self.top_bucket, prefix=prefix, recursive=True)
        documents =[]

        for obj in objects:

            documents.append('https://' + self.link_host + '/' +  obj.bucket_name + '/' + obj.object_name.replace(' ', '+'))

        return documents
