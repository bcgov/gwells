from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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
        user, _created = User.objects.get_or_create(username='test')
        roles_to_groups(user, [AQUIFERS_EDIT_ROLE])
        self.client.force_authenticate(user)
        Aquifer(aquifer_id=1).save()

    def test_patch(self):
        url = reverse('aquifer-retrieve-update', kwargs={'aquifer_id': 1})
        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
