from django.test import TestCase
from urllib.parse import quote
from gwells.documents import MinioClient


class MockObject():
    def __init__(self, bucket_name, object_name):
        self.bucket_name = bucket_name
        self.object_name = object_name

class DocumentsTestCase(TestCase):

    def test_document_url_with_space(self):
        """ test creating a URL from an object with a space in the object key"""
        minio_client = MinioClient(disable_private=True)

        test_document = MockObject("test_bucket", "test key")
        test_url = minio_client.create_url(test_document, "example.com", test_document.bucket_name)

        self.assertEqual(test_url, quote("https://example.com/test_bucket/test key"))

    def test_document_url_with_plus(self):
        """ test creating a URL from and object key containing a plus sign """
        minio_client = MinioClient(disable_private=True)

        # use a key that contains a plus.
        # if this was a real plus in the filename it should be %2B in the listing.
        # spaces get encoded into + (so in this test case, this object_name originally had a space).
        test_document = MockObject("test_bucket", "test+key")

        test_url = minio_client.create_url(test_document, "example.com", test_document.bucket_name)

        self.assertEqual(test_url, quote("https://example.com/test_bucket/test key"))
