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

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from gwells.settings import REST_FRAMEWORK


class TestWellsSpatial(APITestCase):

    def test_geodjango(self):
        # Currently we're re-directing to a static file.
        url = reverse('well-geojson', kwargs={'version': 'v1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_geodjango_bounds(self):
        # Currently we're re-directing to a static file.
        url = reverse('well-geojson', kwargs={'version': 'v1'})
        response = self.client.get(
            url,
            {
                'realtime': 'true', 'sw_lat': 49, 'sw_long': -125, 'ne_lat': 49, 'ne_long': -124
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWellsLithologySpatial(APITestCase):

    def test_geodjango(self):
        # Currently we're re-directing to a static file.
        url = reverse('well-lithology-geojson', kwargs={'version': 'v1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_geodjango_bounds(self):
        # Currently we're re-directing to a static file.
        url = reverse('well-lithology-geojson', kwargs={'version': 'v1'})
        response = self.client.get(
            url,
            {
                'realtime': 'true', 'sw_lat': 49, 'sw_long': -125, 'ne_lat': 49, 'ne_long': -124
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
