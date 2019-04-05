import logging

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User, Group

from rest_framework.test import APITestCase
from rest_framework import status

from gwells.roles import roles_to_groups, WELLS_SUBMISSION_ROLE, WELLS_SUBMISSION_VIEWER_ROLE
from submissions.serializers import (WellSubmissionListSerializer, WellConstructionSubmissionSerializer,
                                     WellAlterationSubmissionSerializer, WellDecommissionSubmissionSerializer)
from wells.models import ActivitySubmission, Well, WellStatusCode


logger = logging.getLogger(__name__)


class TestPermissionsNotAuthenticated(APITestCase):

    def test_not_authenticated_attemps_submit(self):
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
        roles = [WELLS_SUBMISSION_VIEWER_ROLE, ]
        for role in roles:
            group = Group(name=role)
            group.save()
        user, created = User.objects.get_or_create(username='view_rights')
        roles_to_groups(user, roles)
        self.client.force_authenticate(user)

    def test_view_rights_attempts_get_submission_list(self):
        # As a user with view rights, I should be able to get a submission list.
        url = reverse('submissions-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    fixtures = ['gwells-codetables.json', 'wellsearch-codetables.json' ]

    def setUp(self):
        roles = [WELLS_SUBMISSION_ROLE, ]
        for role in roles:
            group = Group(name=role)
            group.save()
        user, created = User.objects.get_or_create(username='submission_rights')
        user.profile.username = user.username
        user.save()
        roles_to_groups(user, roles)
        self.client.force_authenticate(user)

    def test_submission_rights_attempts_get_submission_list(self):
        # As a user with submission rights, I should not be able to get a submission list.
        url = reverse('submissions-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_submission_rights_attempts_construction_submission(self):
        url = reverse('CON')
        # As a user with submission rights, I should be able to make a construction submission.
        data = {
            'owner_full_name': 'molly',
            'owner_mailing_address': 'somewhere',
            'owner_city': 'somewhere',
            'owner_province_state': 'BC',
            'casing_set': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_submission_rights_attempts_alteration_submission(self):
        url = reverse('ALT')
        # As a user with submission rights, I should be able to make an alteration submission.
        data = {
            'owner_full_name': 'molly',
            'owner_mailing_address': 'somewhere',
            'owner_city': 'somewhere',
            'owner_province_state': 'BC',
            'casing_set': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_submission_rights_attempts_decommission_submission(self):
        url = reverse('DEC')
        # As a user with submission rights, I should be able to make a decommission submission.
        data = {
            'owner_full_name': 'molly',
            'owner_mailing_address': 'somewhere',
            'owner_city': 'somewhere',
            'owner_province_state': 'BC',
            'casing_set': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestAuditInformation(APITestCase):

    def setUp(self):
        roles = [WELLS_SUBMISSION_ROLE]
        for role in roles:
            group = Group(name=role)
            group.save()

        self.user, created = User.objects.get_or_create(username='testuser')
        self.user.profile.username = self.user.username
        self.user.save()
        roles_to_groups(self.user, roles)
        self.client.force_authenticate(self.user)

        for index, code in enumerate(('NEW', 'ALTERATION', 'CLOSURE', 'OTHER')):
            WellStatusCode.objects.create(well_status_code=code, display_order=index)

    def test_create_user_populated_on_well(self):
        # When a well is created as a result of a construction submission, the create_user on the
        # well must match that of the submission.
        url = reverse('CON')
        data = {
        }
        response = self.client.post(url, data, format='json')
        well = Well.objects.get(well_tag_number=response.data['well'])
        self.assertEqual(well.create_user, self.user.username)

    def test_update_user_populated_on_submission(self):
        # Upon creation of a submission, the update user must be the same as the created_by user.        
        url = reverse('CON')
        data = {
        }
        response = self.client.post(url, data, format='json')
        submission = ActivitySubmission.objects.get(filing_number=response.data['filing_number'])
        self.assertEqual(submission.update_user, self.user.username)

    def test_create_user_populated_on_legacy_submission(self):
        # The original well was created by user A, and at some point update by user B.
        # The activity submission, was then created by user C.
        # The resultant legacy record, should persist the fact that A created it, and B updated it.
        # The resultant well record, should reprensent the fact that A created it, and C updated it.
        # Original well.
        well = Well.objects.create(create_user='A', update_user='B')
        # Alteration submission.
        url = reverse('ALT')
        data = {
        }
        response = self.client.post(url, data, format='json')

        # Test the result.
        well = Well.objects.get(well_tag_number=response.data['well'])
        self.assertEqual(well.create_user, 'A')
        self.assserEqual(well.update_user, sel.user.username)
        submission = ActivitySubmission.objects.get(
            well_tag_number=well.well_tag_number,
            well_activity_type=WellActivityCode.types.legacy())
        self.assertEqual(submission.create_user, 'A')
        self.assertEqual(submission.update_user, 'B')
