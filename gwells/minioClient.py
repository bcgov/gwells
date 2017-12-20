
import os
from minio import Minio
from minio.error import ResponseError

# NOTE 's3-ca-central-1.amazonaws.com' didn't work:
# minio.error.ResponseError: ResponseError: code: AuthorizationHeaderMalformed, message: The authorization header is malformed; the region 'us-east-1' is wrong; expecting 'ca-central-1', bucket_name: None, object_name: None, request_id: 3841822DCB7F7FC6, host_id: dk3GUWHqhX6gEiE6iONYAIfIpQNvbzExauHhCCoE4uTQOW6NygKY6yPdEsODXmChlO8Auk14ftg=, region:
#

class MinioClient():

    def __init__(self):
        minio_access_key = os.getenv('MINIO_ACCESS_KEY')
        minio_secret_key = os.getenv('MINIO_SECRET_KEY')
        self.host = 's3.amazonaws.com'
        self.link_host = 's3.ca-central-1.amazonaws.com'
        self.minioClient = Minio(self.host, access_key=minio_access_key, secret_key=minio_secret_key)

    def getDocuments(self, well_tag_number):

        print('WTN: ' + str(well_tag_number))

        prefix = str('{:0<6}'.format('{:0>2}'.format(well_tag_number//10000))) + '/WTN ' + str(well_tag_number)

        print('***PREFIX***: ' + prefix)
        objects = self.minioClient.list_objects('gwells-documents', prefix=prefix, recursive=True)
        documents =[]

        for obj in objects:
            documents.append('https://' + self.link_host + '/' + obj.bucket_name + '/' + obj.object_name)

        return documents
