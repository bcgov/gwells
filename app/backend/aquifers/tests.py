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
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

from rest_framework.test import APITestCase
from rest_framework import status

from aquifers.models import Aquifer
from gwells.roles import roles_to_groups, AQUIFERS_EDIT_ROLE

# Create your tests here.


class TestPostNotAuthenticated(APITestCase):
    def test_not_authenticated_attempts_patch(self):
        url = reverse('aquifer-retrieve-update', kwargs={'aquifer_id': 1})
        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAquifersEditRole(APITestCase):
    def setUp(self):
        roles = [AQUIFERS_EDIT_ROLE]
        for role in roles:
            group = Group(name=role)
            group.save()
        user, _created = User.objects.get_or_create(username='test')
        user.profile.username = user.username
        user.save()
        roles_to_groups(user, roles)
        self.client.force_authenticate(user)
        Aquifer(aquifer_id=1).save()

    def test_patch(self):
        url = reverse('aquifer-retrieve-update', kwargs={'aquifer_id': 1})
        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_shapefile(self):

        filepath = 'aquifers/fixtures/shp/shapefile.zip'
        with open(filepath, 'rb') as fh:
            url = reverse('aquifer-save-geometry', kwargs={'aquifer_id': 1})

            response = self.client.post(
                url,
                {'geometry': fh}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAquifersSpatial(APITestCase):

    def test_geodjango(self):
        # Currently we're re-directing to a static file.
        url = reverse('aquifer-geojson')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
