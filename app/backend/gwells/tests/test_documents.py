from django.test import TestCase
from gwells.documents import MinioClient


class DocumentsTestCase(TestCase):

    def test_document_url_with_space(self):
        minio_client = MinioClient(disable_private=True)

        test_document = {
            "bucket_name": "test_bucket",
            "object_name": "test key"
        }

        test_url = minio_client.create_url(test_document, "example.com", test_document.get("bucket_name"))

        self.assertEqual(test_url, "https://example.com/test_bucket/test key")

    def test_document_url_with_plus(self):
        minio_client = MinioClient(disable_private=True)

        test_document = {
            "bucket_name": "test_bucket",

            # if this was a real plus in the filename it should be %2B in the listing.
            # spaces get encoded into + (so in this test case, this object_name originally had a space).
            "object_name": "test+key" 
        }

        test_url = minio_client.create_url(test_document, "example.com", test_document.get("bucket_name"))

        self.assertEqual(test_url, "https://example.com/test_bucket/test key")
