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

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from logging import getLogger
logger = getLogger("test")


class DataBCTest(TestCase):

    # Minio and the file system are mocked out - so that we don't create any artifacts during this test.
    @patch('gwells.management.commands.export_databc.open')
    @patch('gwells.management.commands.export_databc.Minio')
    @patch('gwells.management.commands.export_databc.os')
    def test_export_no_exceptions(self, fake_os, fake_minio, fake_open):
        # This is a very simple test, that just checks to see that the export can be run without any
        # exceptions. This should catch most of the situations that could cause an export to fail.
        out = StringIO()
        call_command('export_databc', stdout=out)
        self.assertIn('GeoJSON export complete.', out.getvalue())


class ImportLicencesTest(TestCase):
    """ tests functions used by `./manage.py import_licences` """
    fixtures = ['gwells-codetables', 'wellsearch-codetables', 'wellsearch', 'registries', 'registries-codetables']

    def test_import_using_fixture_file(self):
        out = StringIO()

        TEST_LICENCES = os.path.join(os.path.dirname(__file__), 'import_licences_test_licences.csv')

        call_command('import_licences', '-d', filename=TEST_LICENCES, stdout=out)
        val = out.getvalue()
        self.assertIn('Licence import complete with 0 errors.', val)
