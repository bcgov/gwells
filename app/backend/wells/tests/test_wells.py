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

import reversion

from django.contrib.gis.geos import Point
from django.contrib.auth.models import Group, User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from gwells.settings import REST_FRAMEWORK
from wells.models import Well
from gwells.roles import roles_to_groups, WELLS_VIEWER_ROLE, WELLS_EDIT_ROLE


API_VERSION = 'v1'


class TestWellLocationsSearch(APITestCase):
    fixtures = ['gwells-codetables', 'wellsearch-codetables', 'wellsearch']

    def test_well_locations(self):
        # Basic test to ensure that the well location search returns a non-error response
        url = reverse('well-locations', kwargs={'version': API_VERSION})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWellHistory(APITestCase):
    fixtures = ['gwells-codetables', 'wellsearch-codetables', 'wellsearch']

    def setUp(self):
        roles = [WELLS_VIEWER_ROLE, WELLS_EDIT_ROLE]
        for role in roles:
            Group.objects.get_or_create(name=role)
        user, _created = User.objects.get_or_create(username='test')
        user.profile.username = user.username
        user.save()
        roles_to_groups(user, roles)
        self.client.force_authenticate(user)

    def test_well_history(self):
        url = reverse('well-history', kwargs={'well_id': 123, 'version': API_VERSION})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_well_history_404(self):
        """ ensure 404s are handled properly by the overridden get method on this view class"""
        url = reverse('well-history', kwargs={'well_id': 987654321, 'version': API_VERSION})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_well_history_after_geom_update(self):
        """ ensure Point/GEOSGeometry fields are handled properly when getting well history"""

        well = Well.objects.get(pk=123)

        with reversion.create_revision():
            well.geom = Point(123, 51)
            well.save()

        url = reverse('well-history', kwargs={'well_id': 123, 'version': API_VERSION})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
