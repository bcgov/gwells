import collections
from django.test import TestCase
from wells.documents import MinioClient


class DocumentTests(TestCase):

    def setUp(self):
        self.client = MinioClient(disable_private=True, disable_public=True)
        FileObject = collections.namedtuple(
            'FileObject', 'bucket_name object_name')
        self.file1 = FileObject(bucket_name='test-bucket',
                                object_name='test-object')
        self.file2 = FileObject(bucket_name='test-bucket',
                                object_name='test-object2')
        self.host = 'www.example.com'

    def test_create_url(self):
        url = self.client.create_url(self.file1, self.host)
        self.assertEqual(
            url, 'https://www.example.com/test-bucket/test-object')

    def test_create_url_list(self):
        file_list = [self.file1, self.file2]
        url_list = self.client.create_url_list(file_list, self.host)

        self.assertEqual(len(url_list), 2)
        self.assertEqual(url_list[1]['name'], 'test-object2')
