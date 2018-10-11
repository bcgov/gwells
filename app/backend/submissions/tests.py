from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from gwells.roles import roles_to_groups, WELLS_EDIT_ROLE, WELLS_VIEWER_ROLE


class TestPermissionsNotAuthenticated(APITestCase):

    def test_no_authenticated_attemps_submit(self):
        # As an unauthenticated user, I should not be authorised to submit anything.
        url = reverse('submissions-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPermissionsNoRights(APITestCase):

    def setUp(self):
        user, created = User.objects.get_or_create(username='no_rights')
        roles_to_groups(user, [])
        self.client.force_authenticate(user)

    def test_no_rights_attempts_submit(self):
        # As a user with no rights, I should not be able to make a submission.
        url = reverse('submissions-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPermissionsViewRights(APITestCase):

    def setUp(self):
        user, created = User.objects.get_or_create(username='view_rights')
        roles_to_groups(user, [WELLS_VIEWER_ROLE, ])
        self.client.force_authenticate(user)

    def test_view_rights_attempts_submit(self):
        # As a user with view rights, I should not be able to make a submission.
        url = reverse('submissions-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPermissionsEditRights(APITestCase):

    fixtures = ['gwells-codetables.json', ]

    def setUp(self):
        user, created = User.objects.get_or_create(username='edit_rights')
        roles_to_groups(user, [WELLS_EDIT_ROLE, ])
        self.client.force_authenticate(user)

    def test_edit_rights_attempts_submit(self):
        url = reverse('CON')
        # As a user with edit rights, I should be able to make a submission.
        data = {
            'owner_full_name': 'molly',
            'owner_mailing_address': 'somewhere',
            'owner_city': 'somewhere',
            'owner_province_state': 'BC',
            'well_activity_type': 'CON',
            'casing_set': []
        }
        response = self.client.post(url, data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
