import os
from minio import Minio

# NOTE Well Summary page uses publicly-viewable S3 bucket, so no credentials are needed
#

class MinioClient():

    def __init__(self):
        self.access_key = ""
        self.secret_key = ""
        self.host = os.getenv('S3_HOST')
        self.minio_client = Minio(self.host, access_key=self.access_key, secret_key=self.secret_key, secure=True)
        self.top_bucket = os.getenv('S3_ROOT_BUCKET')

    def get_documents(self, well_tag_number):

        prefix = str('{:0<6}'.format('{:0>2}'.format(well_tag_number//10000))) + '/WTN ' + str(well_tag_number)

        objects = self.minio_client.list_objects(self.top_bucket, prefix=prefix, recursive=True)

        return objects
