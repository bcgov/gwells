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

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


class TestWellLocationsSearch(APITestCase):

    def test_well_locations(self):
        # Basic test to ensure that the well location search returns a non-error response
        url = reverse('well-locations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
