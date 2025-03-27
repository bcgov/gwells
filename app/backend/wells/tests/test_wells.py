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
import json
import reversion
from logging import getLogger
from django.contrib.gis.geos import Point
from django.contrib.auth.models import Group, User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from gwells.settings import REST_FRAMEWORK
from wells.models import Well
from gwells.roles import roles_to_groups, WELLS_VIEWER_ROLE, WELLS_EDIT_ROLE

logger = getLogger()

class TestWellLocationsSearch(APITestCase):
    fixtures = ['gwells-codetables', 'wellsearch-codetables', 'wellsearch', 'registries', 'registries-codetables', 'aquifers']

    def test_well_locations(self):
        # Basic test to ensure that the well location search returns a non-error response
        url = reverse('well-locations-v1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_old_drilling_company_filter(self):
        # Make sure old drilling_company query string filtering still works
        url = reverse('well-locations-v1')
        response = self.client.get(url, {
            'drilling_company': 'bf5d31ea-8a5a-4363-8a5e-6c00eed03058'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_new_company_of_person_responsible_filter(self):
        # Make sure new company_of_person_responsible query string filtering
        # works the same as filtering by drilling_company
        url = reverse('well-locations-v1')
        response = self.client.get(url, {
            'company_of_person_responsible': 'bf5d31ea-8a5a-4363-8a5e-6c00eed03058'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_filtering_licensed_wells(self):
        # fixtures contain a licence for well 123
        url = reverse('well-locations-v2')
        response = self.client.get(url, {
            'licenced_status': 'LICENSED'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('results')

        # ensure all wells in response are licenced.
        for result in data:
            well = Well.objects.get(well_tag_number=result.get("well_tag_number"))
            self.assertTrue(well.licences.all().exists())


    def test_filtering_unlicensed_wells(self):
        # fixtures contain a licence for well 123
        url = reverse('well-locations-v2')
        response = self.client.get(url, {
            'licenced_status': 'UNLICENSED'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('results')

        # ensure all wells in response are licenced.
        for result in data:
            well = Well.objects.get(well_tag_number=result.get("well_tag_number"))
            self.assertFalse(well.licences.all().exists())

class TestWellHistory(APITestCase):
    fixtures = ['gwells-codetables', 'wellsearch-codetables', 'wellsearch', 'registries', 'registries-codetables']

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
        url = reverse('well-history', kwargs={'well_id': 123, 'version': 'v1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_well_history_404(self):
        """ ensure 404s are handled properly by the overridden get method on this view class"""
        url = reverse('well-history', kwargs={'well_id': 987654321, 'version': 'v1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_well_history_after_geom_update(self):
        """ ensure Point/GEOSGeometry fields are handled properly when getting well history"""

        well = Well.objects.get(pk=123)

        with reversion.create_revision():
            well.geom = Point(123, 51)
            well.save()

        url = reverse('well-history', kwargs={'well_id': 123, 'version': 'v1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestWellDetailAuthenticated(APITestCase):
    # Tbh, I don't know if all of these fixtures are necessary but I don't feel like tracing through the code to find out
    fixtures = ['gwells-codetables', 'wellsearch-codetables', 'wellsearch', 'registries', 'registries-codetables', 'well_detail_fixture', 'aquifers']

    def setUp(self):
        roles = [WELLS_VIEWER_ROLE]
        for role in roles:
            Group.objects.get_or_create(name=role)
        user, _created = User.objects.get_or_create(username='test')
        user.profile.username = user.username
        user.save()
        roles_to_groups(user, roles)
        self.client.force_authenticate(user)

    def test_well_detail_authenticated(self):
        url = reverse('well-detail', kwargs={'well_tag_number': 123, 'version': 'v1'})
        response = self.client.get(url)
        self.assertTrue('internal_comments' in response.data)

class TestWellDetailUnauthenticated(APITestCase):
    # Same comment as above
    fixtures = ['gwells-codetables', 'wellsearch-codetables', 'wellsearch', 'registries', 'registries-codetables', 'well_detail_fixture', 'aquifers']

    def test_well_detail_unauthenticated(self):
        url = reverse('well-detail', kwargs={'well_tag_number': 123, 'version': 'v1'})
        response = self.client.get(url)
        self.assertFalse('internal_comments' in response.data)