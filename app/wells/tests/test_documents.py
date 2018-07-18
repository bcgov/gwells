import collections
from os import getenv
from unittest import TestCase
from unittest.mock import patch

from wells.documents import MinioClient


mock_env_values = {'S3_PRIVATE_EXTERNAL_HOST': 'external_host'}


def env_side_effect(*args, **kwargs):
    if args[0] in mock_env_values:
        return mock_env_values[args[0]]
    else:
        return getenv(args[0])


class DocumentTests(TestCase):

    def setUp(self):
        FileObject = collections.namedtuple(
            'FileObject', 'bucket_name object_name')
        self.file1 = FileObject(bucket_name='test-bucket',
                                object_name='test-object')
        self.file2 = FileObject(bucket_name='test-bucket',
                                object_name='test-object2')
        self.host = 'www.example.com'

    @patch('wells.documents.Minio')
    def test_create_url(self, MockMinio):
        client = MinioClient(True)
        url = client.create_url(self.file1, self.host)
        self.assertEqual(
            url, 'https://www.example.com/test-bucket/test-object')

    @patch('wells.documents.Minio')
    def test_create_url_list(self, MockMinio):
        file_list = [self.file1, self.file2]
        client = MinioClient(True)
        url_list = client.create_url_list(file_list, self.host)

        self.assertEqual(len(url_list), 2)
        self.assertEqual(url_list[1]['name'], 'test-object2')

    @patch('wells.documents.get_env_variable')
    @patch('wells.documents.Minio')
    def test_create_external_private_url(self, MockMinio, mock_get_env_variable):
        # patch MockMinio
        instance = MockMinio.return_value
        instance.presigned_get_object.return_value = 'https://www.something.com/path?query=thing'
        # patch get_env_variable
        mock_get_env_variable.side_effect = env_side_effect
        # Create instance (it's going to use the mocked instance)
        client = MinioClient(True)
        # We are expecting the hostname to be replaced by the S3_PRIVATE_EXTERNAL_HOST
        self.assertEqual(client.get_private_file('something'), 'https://external_host/path?query=thing')
