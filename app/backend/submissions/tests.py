import logging
from http import HTTPStatus

from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.utils.dateparse import parse_datetime

from rest_framework.test import APITestCase
from rest_framework import status

from gwells.roles import roles_to_groups, WELLS_SUBMISSION_ROLE, WELLS_SUBMISSION_VIEWER_ROLE,\
    WELLS_EDIT_ROLE, WELLS_VIEWER_ROLE
from submissions.serializers import (WellSubmissionListSerializer, WellConstructionSubmissionSerializer,
                                     WellAlterationSubmissionSerializer, WellDecommissionSubmissionSerializer)
from wells.models import ActivitySubmission, Well, WellStatusCode, WellActivityCode, Casing, CasingCode,\
    CasingMaterialCode, LithologyDescription, DevelopmentMethodCode, DrillingMethodCode, Screen
from gwells.models import DATALOAD_USER


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


class TestEdit(APITestCase):
    fixtures = ['wellsearch-codetables']

    def setUp(self):
        roles = [WELLS_EDIT_ROLE, WELLS_VIEWER_ROLE,
                 WELLS_SUBMISSION_ROLE, WELLS_SUBMISSION_VIEWER_ROLE]
        for role in roles:
            group = Group(name=role)
            group.save()
        user, created = User.objects.get_or_create(username='edit_user')
        user.profile.username = 'edit_user'
        user.save()
        roles_to_groups(user, roles)
        self.casing_code_surface = CasingCode.objects.get(code='SURFACE')
        self.casing_material_code_other = CasingMaterialCode.objects.get(
            code='OTHER')
        self.client.force_authenticate(user)

    def test_drilling_methods_persist_on_well(self):
        # Create a well with some codes.
        codes = sorted(('AUGER', 'AIR_ROTARY'))
        well = Well.objects.create(create_user='A', update_user='B')
        for code in codes:
            well.drilling_methods.add(
                DrillingMethodCode.objects.get(drilling_method_code=code))
        # Data for the edit - NO drilling method specified.
        data = {
            'well': well.well_tag_number,
        }
        # Post an edit.
        self.client.post(reverse('STAFF_EDIT'), data, format='json')
        # We expect the rendered well to contain the drilling methods.
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        saved_well_codes = sorted(
            [item.drilling_method_code for item in well.drilling_methods.all()])
        self.assertListEqual(codes, saved_well_codes)

    def test_drilling_methods_persist_on_legacy(self):
        # Create a well with some codes.
        codes = sorted(('AUGER', 'AIR_ROTARY'))
        well = Well.objects.create(create_user='A', update_user='B')
        for code in codes:
            well.drilling_methods.add(
                DrillingMethodCode.objects.get(drilling_method_code=code))
        data = {
            'well': well.well_tag_number
        }
        # Post an edit
        self.client.post(reverse('STAFF_EDIT'), data, format='json')
        # We expect the legacy record to contain the drilling methods.
        legacy_submission = ActivitySubmission.objects.get(
            well=well,
            well_activity_type=WellActivityCode.types.legacy())
        saved_well_codes = [
            item.drilling_method_code for item in legacy_submission.drilling_methods.all()]
        saved_well_codes = sorted(saved_well_codes)
        self.assertListEqual(codes, saved_well_codes)

    def test_development_methods_persist_on_well(self):
        # Create a well with some codes.
        codes = sorted(('AIR_LIFT', 'BAIL'))
        well = Well.objects.create(create_user='A', update_user='B')
        for code in codes:
            well.development_methods.add(
                DevelopmentMethodCode.objects.get(development_method_code=code))
        data = {
            'well': well.well_tag_number
        }
        # Post an edit
        self.client.post(reverse('STAFF_EDIT'), data, format='json')
        # We expect the well record to contain the development methods.
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        saved_well_codes = [
            item.development_method_code for item in well.development_methods.all()]
        saved_well_codes = sorted(saved_well_codes)
        self.assertListEqual(codes, saved_well_codes)

    def test_development_methods_persist_on_legacy(self):
        # Create a well with some codes.
        codes = sorted(('AIR_LIFT', 'BAIL'))
        well = Well.objects.create(create_user='A', update_user='B')
        for code in codes:
            well.development_methods.add(
                DevelopmentMethodCode.objects.get(development_method_code=code))
        data = {
            'well': well.well_tag_number
        }
        # Post an edit
        self.client.post(reverse('STAFF_EDIT'), data, format='json')
        # We expect the legacy record to contain the development methods.
        legacy_submission = ActivitySubmission.objects.get(
            well=well,
            well_activity_type=WellActivityCode.types.legacy())
        saved_well_codes = [
            item.development_method_code for item in legacy_submission.development_methods.all()]
        saved_well_codes = sorted(saved_well_codes)
        self.assertListEqual(codes, saved_well_codes)

    def test_screen_details_persist_on_well(self):
        well = Well.objects.create(create_user='A', update_user='B')
        screen = Screen.objects.create(well=well, start=0, end=10)
        screen = Screen.objects.create(well=well, start=10, end=20)
        # Screen HAS to be sent!
        data = {
            'well': well.well_tag_number,
            'screen_set': [
                {'start': item.start, 'end': item.end} for item in well.screen_set.all()
            ]
        }
        # Post an edit
        self.client.post(reverse('STAFF_EDIT'), data, format='json')
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(well.screen_set.all().count(), 2)

    def test_casings_persist_on_legacy(self):
        well = Well.objects.create(create_user='A', update_user='B')
        screen = Screen.objects.create(well=well, start=0, end=10)
        screen = Screen.objects.create(well=well, start=10, end=20)
        data = {
            'well': well.well_tag_number
        }
        # Post an edit
        self.client.post(reverse('STAFF_EDIT'), data, format='json')
        legacy_submission = ActivitySubmission.objects.get(
            well=well,
            well_activity_type=WellActivityCode.types.legacy())
        self.assertEqual(legacy_submission.screen_set.all().count(), 2)

    def test_water_quality_submission(self):
        """ Check that water quality on a staff edit is reflected on the well """
        well = Well.objects.create()
        data = {
            'well': well.well_tag_number,
            'water_quality_characteristics': ['CLOUDY', 'FRESH', 'GAS']
        }
        self.client.post(reverse('STAFF_EDIT'), data, format='json')
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(well.water_quality_characteristics.count(), 3)

    def test_casing_submission(self):
        """ Test that if a legacy well does not have a casing drive shoe, it doesn't cause problems """
        # We create a pre-existing "legacy well"
        well = Well.objects.create()
        # We attached a casing to the well, a casing the is missing a drive_shoe, which is a "required"
        # field.
        Casing.objects.create(
            well=well, start=0, end=10, diameter=6.63, casing_code=self.casing_code_surface,
            casing_material=self.casing_material_code_other, drive_shoe=None, wall_thickness=0.22)
        # Test for bug relating to edit submission with casing set. Our new casing has a drive shoe, which
        # is correct, so we should be able to submit this record just fine.
        data = {
            'well': well.well_tag_number,
            'owner_tel': '',
            'linerperforation_set': [],
            'latitude': 48.639643,
            'longitude': -123.55975,
            'casing_set': [
                {
                    'start': '0',
                    'end': '10',
                    'diameter': '6.630',
                    'casing_code': 'SURFACE',
                    'casing_material': 'OTHER',
                    'drive_shoe': True,
                    'wall_thickness': '0.220'
                }
            ],
            'decommission_description_set': []
        }
        response = self.client.post(reverse('STAFF_EDIT'), data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.data)

    def test_lithology_to_greater_than_zero_on_legacy(self):
        """ Test that if a legacy well does not have correct lithology info, it doesn't cause problems """
        # We create a pre-existing "legacy well"
        well = Well.objects.create(create_user='Blah', update_user='Blah')
        # We attached lithology to the well, that's should fail validation.
        lithology = LithologyDescription.objects.create(
            lithology_from=0,
            lithology_to=0,
            well=well)
        # Doing a valid edit, updating the lithology information, should be fine.
        data = {
            'well': well.well_tag_number,
            'latitude': 48.639643,
            'longitude': -123.55975,
            'lithologydescription_set': [
                {
                    'lithology_from': 0,
                    'lithology_to': 10
                }
            ]
        }
        response = self.client.post(reverse('STAFF_EDIT'), data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.data)

    def test_staff_edit_with_bad_lithology_in_old_well_returns_bad_request(self):
        """ Test that if a legacy well does not have correct lithology info, that it doesn't fail
        on generating the legacy record, but does give us a bad request response. """
        # We create a pre-existing "legacy well"
        well = Well.objects.create(create_user='Blah', update_user='Blah')
        # We attached lithology to the well, that should fail validation.
        LithologyDescription.objects.create(
            well=well, lithology_from=117, lithology_to=None)
        # Doing an edit, without passing in the correct validation, should fail!
        data = {
            'well': well.well_tag_number
        }
        response = self.client.post(reverse('STAFF_EDIT'), data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, response.data)

    def test_staff_edit_with_bad_lithology_in_old_well_but_edit_good_returns_ok(self):
        """ Test that if a legacy well does not have correct lithology info, but we submit
        good data on an edit, that everything works fine."""
        # We create a pre-existing "legacy well"
        well = Well.objects.create(create_user='Blah', update_user='Blah')
        # We attached lithology to the well, that should fail validation.
        LithologyDescription.objects.create(
            well=well, lithology_from=117, lithology_to=None)
        # Doing a valid edit, updating the lithology information, should be fine.
        data = {
            'well': well.well_tag_number,
            'lithologydescription_set': [
                {
                    'lithology_from': 0,
                    'lithology_to': 10
                }
            ]
        }
        response = self.client.post(reverse('STAFF_EDIT'), data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.data)

    def test_staff_edit_with_bad_lithology_in_old_well_but_edit_saves_new_data(self):
        """ Test that if a legacy well does not have correct lithology info, but we submit
        good data on an edit, that everything works fine."""
        # We create a pre-existing "legacy well"
        well = Well.objects.create(create_user='Blah', update_user='Blah')
        # We attached lithology to the well, that should fail validation.
        LithologyDescription.objects.create(
            well=well, lithology_from=117, lithology_to=None)
        # Doing a valid edit, updating the lithology information, should be fine.
        data = {
            'well': well.well_tag_number,
            'lithologydescription_set': [
                {
                    'lithology_from': 0,
                    'lithology_to': 10
                }
            ]
        }
        self.client.post(reverse('STAFF_EDIT'), data, format='json')
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        lithology = well.lithologydescription_set.all()
        self.assertAlmostEqual(lithology[0].lithology_from, 0)
        self.assertAlmostEqual(lithology[0].lithology_to, 10)

    def test_no_city_on_legacy(self):
        """ Test that the legacy record creates ok, but we get a bad request response if we have bad
        data.
        """
        well = Well.objects.create(
            create_user='Blah', update_user='Blah', owner_city=' ')
        data = {
            'well': well.well_tag_number
        }
        response = self.client.post(reverse('STAFF_EDIT'), data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, response.data)
        data['owner_city'] = 'Somewhere'
        response = self.client.post(reverse('STAFF_EDIT'), data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.data)


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

    fixtures = ['gwells-codetables.json', 'wellsearch-codetables.json']

    def setUp(self):
        roles = [WELLS_SUBMISSION_ROLE, ]
        for role in roles:
            group = Group(name=role)
            group.save()
        user, created = User.objects.get_or_create(
            username='submission_rights')
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
    fixtures = ['wellsearch-codetables']

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
        submission = ActivitySubmission.objects.get(
            filing_number=response.data['filing_number'])
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
            'well': well.well_tag_number
        }
        response = self.client.post(url, data, format='json')

        # Test the result.
        well = Well.objects.get(well_tag_number=response.data['well'])
        self.assertEqual(well.create_user, 'A',
                         'Original well user should remain the same')
        self.assertEqual(well.update_user, self.user.username)
        submission = ActivitySubmission.objects.get(
            well=well,
            well_activity_type=WellActivityCode.types.legacy())
        self.assertEqual(
            submission.create_user, 'A', 'The legacy record create user should be same as the well')
        self.assertEqual(submission.update_user, 'B')

    def test_post_external_override_of_audit_information(self):
        url = reverse('CON')
        data = {
            'create_user': 'BAD CREATE USER',
            'update_user': 'BAD UPDATE USER',
            'update_date': '1999-05-05',
            'create_date': '1999-05-05'
        }
        response = self.client.post(url, data, format='json')
        submission = ActivitySubmission.objects.get(
            filing_number=response.data['filing_number'])
        self.assertNotEqual(submission.create_user, data['create_user'])
        self.assertNotEqual(submission.update_user, data['update_user'])
        self.assertNotEqual(submission.well.create_user, data['create_user'])
        self.assertNotEqual(submission.well.update_user, data['update_user'])
        self.assertNotEqual(submission.create_date.year, 1999)
        self.assertNotEqual(submission.update_date.year, 1999)

    def test_well_create_date_matches_construction(self):
        # Make sure that the well create_date matches up with the construction date on a new well.
        url = reverse('CON')
        data = {
        }
        response = self.client.post(url, data, format='json')
        submission = ActivitySubmission.objects.get(
            filing_number=response.data['filing_number'])
        self.assertEqual(
            submission.create_date,
            submission.well.create_date,
            'Create date for well and construction matches')
        self.assertEqual(
            submission.update_date,
            submission.well.update_date,
            'Update date for well and construction matches')

    def test_legacy_submission_create_and_update_date_matches_old_well(self):
        # Make sure that a legacy record, contains the original well audit information.
        original_create_date = parse_datetime('1999-09-09T10:10:10Z')
        original_update_date = parse_datetime('2000-01-01T10:10:10Z')
        well = Well.objects.create(
            create_user='A', update_user='B',
            create_date=original_create_date, update_date=original_update_date)

        # Alteration submission.
        url = reverse('ALT')
        data = {
            'well': well.well_tag_number
        }
        response = self.client.post(url, data, format='json')
        alteration = ActivitySubmission.objects.get(
            filing_number=response.data['filing_number'])

        # Check that well create_date remains the same
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(well.create_date, original_create_date)
        # Check that legacy records matches with old well info
        submission = ActivitySubmission.objects.get(
            well=well,
            well_activity_type=WellActivityCode.types.legacy())
        self.assertEqual(
            submission.create_date, original_create_date, 'Legacy create date should matche well')
        self.assertEqual(
            submission.update_date, original_update_date, 'Legacy update date should match well')
        self.assertEqual(
            well.create_date, original_create_date, 'Well create date should be unchanged')
        self.assertEqual(
            well.update_date, alteration.update_date, 'Well update date should match alteration')

    def test_bad_audit_info_on_well_no_failure(self):
        # If the original well doesn't have audit info, we don't want that to cause a failure.
        well = Well.objects.create()

        # Alteration submission.
        url = reverse('ALT')
        data = {
            'well': well.well_tag_number
        }
        response = self.client.post(url, data, format='json')
        # If we don't get aa 200 OK here, just go ahead and fail right now!
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        # Load resultant well.
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        # Load resultant legacy submission.
        legacy = ActivitySubmission.objects.get(
            well=well,
            well_activity_type=WellActivityCode.types.legacy())
        # Load resultant alteration.
        alteration = ActivitySubmission.objects.get(
            well=well,
            well_activity_type=WellActivityCode.types.alteration())
        # The well should now show the logged in user as having updated.
        self.assertEqual(well.update_user, self.user.username)
        # The well should now show dataload user as the create_user.
        self.assertEquals(well.create_user, DATALOAD_USER)
        # The legacy submission should show dataload user as the create_user and update_user.
        self.assertEquals(legacy.create_user, DATALOAD_USER)
        self.assertEquals(legacy.update_user, DATALOAD_USER)
        # The alteration should show the current user as the create_user and update_user.
        self.assertEquals(alteration.create_user, self.user.username)
        self.assertEquals(alteration.update_user, self.user.username)
