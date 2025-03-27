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

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase


class ExportTest(TestCase):

    # Minio and the file system are mocked out - so that we don't create any artifacts during this test.
    @patch('wells.management.commands.export.open')
    @patch('wells.management.commands.export.Minio')
    @patch('wells.management.commands.export.os')
    @patch('wells.management.commands.export.zipfile')
    @patch('wells.management.commands.export.Workbook')
    def test_export_no_exceptions(self, fake_minio, fake_os, fake_open, fake_zipfile, fake_workbook):
        # This is a very simple test, that just checks to see that the export can be run without any
        # exceptions. This should catch most of the situations that could cause an export to fail.
        out = StringIO()
        call_command('export', stdout=out)
        self.assertIn('export complete', out.getvalue())
