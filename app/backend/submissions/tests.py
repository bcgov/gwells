from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from gwells.roles import roles_to_groups, WELLS_EDIT_ROLE, WELLS_VIEWER_ROLE
from submissions.serializers import (WellSubmissionListSerializer, WellConstructionSubmissionSerializer,
                                     WellAlterationSubmissionSerializer, WellDecommissionSubmissionSerializer)


class TestPermissionsNotAuthenticated(APITestCase):

    def test_no_authenticated_attemps_submit(self):
        # As an unauthenticated user, I should not be authorised to get a submission list.
        url = reverse('submissions-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPermissionsNoRights(APITestCase):

    def setUp(self):
        user, created = User.objects.get_or_create(username='no_rights')
        roles_to_groups(user, [])
        self.client.force_authenticate(user)

    def test_no_rights_attempts_list(self):
        # As a user with no rights, I should not be able get a list of submissions.
        url = reverse('submissions-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPermissionsViewRights(APITestCase):

    def setUp(self):
        user, created = User.objects.get_or_create(username='view_rights')
        roles_to_groups(user, [WELLS_VIEWER_ROLE, ])
        self.client.force_authenticate(user)

    def test_view_rights_attempts_get_submission_list(self):
        # As a user with view rights, I should not be able to get a submission list.
        url = reverse('submissions-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_rights_attempts_construction_submission(self):
        # As a user with view rights, I should not be able to create a construction submission.
        url = reverse('CON')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_rights_attempts_alteration_submission(self):
        # As a user with view rights, I should not be able to create an alteration submission.
        url = reverse('ALT')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_rights_attempts_alteration_submission(self):
        # As a user with view rights, I should not be able to create a decommission submission.
        url = reverse('DEC')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPermissionsSubmissionRights(APITestCase):

    fixtures = ['gwells-codetables.json', ]

    def setUp(self):
        user, created = User.objects.get_or_create(username='edit_rights')
        roles_to_groups(user, [WELLS_EDIT_ROLE, ])
        self.client.force_authenticate(user)

    def test_edit_rights_attempts_construction_submition(self):
        url = reverse('CON')
        # As a user with edit rights, I should be able to make a construction submission.
        data = {
            'owner_full_name': 'molly',
            'owner_mailing_address': 'somewhere',
            'owner_city': 'somewhere',
            'owner_province_state': 'BC',
            'casing_set': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_rights_attempts_alteration_submition(self):
        url = reverse('ALT')
        # As a user with edit rights, I should be able to make an alteration submission.
        data = {
            'owner_full_name': 'molly',
            'owner_mailing_address': 'somewhere',
            'owner_city': 'somewhere',
            'owner_province_state': 'BC',
            'casing_set': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_rights_attempts_decommission_submition(self):
        url = reverse('DEC')
        # As a user with edit rights, I should be able to make a decommission submission.
        data = {
            'owner_full_name': 'molly',
            'owner_mailing_address': 'somewhere',
            'owner_city': 'somewhere',
            'owner_province_state': 'BC',
            'casing_set': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
