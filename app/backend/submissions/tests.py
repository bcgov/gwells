import logging
from http import HTTPStatus

import datetime
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.utils.dateparse import parse_datetime

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from gwells.settings import REST_FRAMEWORK
from gwells.roles import roles_to_groups, WELLS_SUBMISSION_ROLE, WELLS_SUBMISSION_VIEWER_ROLE,\
    WELLS_EDIT_ROLE, WELLS_VIEWER_ROLE
from submissions.serializers import (WellSubmissionListSerializer, WellConstructionSubmissionSerializer,
                                     WellAlterationSubmissionSerializer, WellDecommissionSubmissionSerializer)
from wells.models import (
    ActivitySubmission,
    ActivitySubmissionLinerPerforation,
    Casing,
    CasingCode,
    CasingMaterialCode,
    DevelopmentMethodCode,
    DrillingMethodCode,
    LinerPerforation,
    LithologyDescription,
    Screen,
    Well,
    WellStatusCode,
    AquiferParameters
)
from submissions.models import (
    WellActivityCode,
    WELL_ACTIVITY_CODE_STAFF_EDIT, WELL_ACTIVITY_CODE_LEGACY, WELL_ACTIVITY_CODE_ALTERATION, \
      WELL_ACTIVITY_CODE_CONSTRUCTION)
from gwells.models import DATALOAD_USER


logger = logging.getLogger(__name__)


class TestPermissionsNotAuthenticated(APITestCase):

    def test_not_authenticated_attemps_submit(self):
        # As an unauthenticated user, I should not be authorised to get a submission list.
        url = reverse('submissions-list', kwargs={'version': 'v1'})
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPermissionsNoRights(APITestCase):

    def setUp(self):
        user, created = User.objects.get_or_create(username='no_rights')
        roles_to_groups(user, [])
        self.client.force_authenticate(user)

    def test_no_rights_attempts_list(self):
        # As a user with no rights, I should not be able get a list of submissions.
        url = reverse('submissions-list', kwargs={'version': 'v1'})
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestSubmissionsBase(APITestCase):
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
        self.user = user
        roles_to_groups(user, roles)
        self.casing_code_surface = CasingCode.objects.get(code='SURFACE')
        self.casing_material_code_other = CasingMaterialCode.objects.get(
            code='OTHER')
        self.client.force_authenticate(user)


class TestConstruction(TestSubmissionsBase):

    def test_submission_liner_perforation(self):
        # Test that on construction submission, liner perforation for submission is created.
        data = {
            'linerperforation_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        response = self.client.post(reverse('CON', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the liner info on the submission
        liner = ActivitySubmissionLinerPerforation.objects.get(
            activity_submission__well__well_tag_number=response.data['well'])
        # We expect a liner has been created for the submission.
        self.assertIsNotNone(liner)

    def test_well_liner_perforation(self):
        # Test that on construction submission, liner perforation for well is created.
        data = {
            'linerperforation_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        response = self.client.post(reverse('CON', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the liner info on the submission
        liner = LinerPerforation.objects.get(
            well__well_tag_number=response.data['well'])
        # We expect a liner has been created for the well.
        self.assertIsNotNone(liner)

    def test_lithology_submission_create_user_update_user(self):
        """
        Test that when creating a construction submission, the lithology records on the submissions have
        the create user and update user set correctly.
        """
        # Data for the construction submission.
        data = {
            'lithologydescription_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an construction submissions.
        response = self.client.post(reverse('CON', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the submission back.
        submission = ActivitySubmission.objects.get(well__well_tag_number=response.data['well'])
        # Get the resultant lithology record
        lithology = submission.lithologydescription_set.all()[0]
        self.assertEqual(lithology.create_user, self.user.username)
        self.assertEqual(lithology.update_user, self.user.username)

    def test_lithology_well_create_user_update_user(self):
        """
        Test that the well created by a construction submission, has lithology records with the
        create user and update user set correctly.
        """
        # Data for the construction submission.
        data = {
            'lithologydescription_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an construction submissions.
        response = self.client.post(reverse('CON', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the well back.
        well = Well.objects.get(well_tag_number=response.data['well'])
        # Get the resultant lithology record
        lithology = well.lithologydescription_set.all()[0]
        self.assertEqual(lithology.create_user, self.user.username)
        self.assertEqual(lithology.update_user, self.user.username)

    def test_screens_well_create_user_update_user(self):
        """
        Test that the well created by a construction submission, has screen records with the
        create user and update user set correctly.
        """
        # Data for the construction submission.
        data = {
            'screen_set': [
                {
                    'start': 0,
                    'end': 10,
                    'assembly_type': 'SCREEN'
                }
            ]
        }
        # Post an construction submissions.
        response = self.client.post(reverse('CON', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the well back.
        well = Well.objects.get(well_tag_number=response.data['well'])
        # Get the resultant lithology record
        screen = well.screen_set.all()[0]
        self.assertEqual(screen.create_user, self.user.username)
        self.assertEqual(screen.update_user, self.user.username)

    def test_casings_well_create_user_update_user(self):
        """
        Test that the well created by a construction submission, has casing records with the
        create user and update user set correctly.
        """
        # Data for the construction submission.
        data = {
            'casing_set': [
                {
                    'start': 0,
                    'end': 10,
                    'diameter': 10
                }
            ]
        }
        # Post an construction submissions.
        response = self.client.post(reverse('CON', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the well back.
        well = Well.objects.get(well_tag_number=response.data['well'])
        # Get the resultant lithology record
        casing = well.casing_set.all()[0]
        self.assertEqual(casing.create_user, self.user.username)
        self.assertEqual(casing.update_user, self.user.username)

    def test_aquifer_parameters_well_create_user_update_user(self):
        """
        Test that the well created by a construction submission, has aquifer parameters records with the
        create user and update user set correctly.
        """
        # Data for the construction submission.
        data = {
            'aquifer_parameters_set': [
                {
                    'storativity': 0.25,
                    'testing_comments': 'Test comment for aquifer parameters.'
                }
            ]
        }
        # Post an construction submissions.
        response = self.client.post(reverse('CON', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the well back.
        well = Well.objects.get(well_tag_number=response.data['well'])
        # Get the resultant lithology record
        aquifer_parameters = well.aquifer_parameters_set.all()[0]
        self.assertEqual(aquifer_parameters.create_user, self.user.username)
        self.assertEqual(aquifer_parameters.update_user, self.user.username)

    def test_perforations_create_user_update_user(self):
        """
        Test that the well created by a construction submission, has perforation records with the
        create user and update user set correctly.
        """
        # Data for the construction submission.
        data = {
            'linerperforation_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an construction submissions.
        response = self.client.post(reverse('CON', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the well back.
        well = Well.objects.get(well_tag_number=response.data['well'])
        # Get the resultant lithology record
        perforation = well.linerperforation_set.all()[0]
        self.assertEqual(perforation.create_user, self.user.username)
        self.assertEqual(perforation.update_user, self.user.username)


class TestEdit(TestSubmissionsBase):

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
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
        Screen.objects.create(well=well, start=0, end=10)
        # Screen HAS to be sent!
        data = {
            'well': well.well_tag_number,
            'screen_set': [
                {'start': 0, 'end': 10, 'assembly_type': 'SCREEN'},
                {'start': 10, 'end': 20, 'assembly_type': 'SCREEN'},
            ]
        }
        # Post an edit
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(well.screen_set.all().count(), 2)

    def test_casings_persist_on_legacy(self):
        well = Well.objects.create(create_user='A', update_user='B')
        Screen.objects.create(well=well, start=0, end=10)
        Screen.objects.create(well=well, start=10, end=20)
        data = {
            'well': well.well_tag_number
        }
        # Post an edit
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        legacy_submission = ActivitySubmission.objects.get(
            well=well,
            well_activity_type=WellActivityCode.types.legacy())
        self.assertEqual(legacy_submission.screen_set.all().count(), 2)

    def test_water_quality_submission(self):
        """ Check that water quality on a staff edit is reflected on the well """
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        data = {
            'well': well.well_tag_number,
            'water_quality_characteristics': ['CLOUDY', 'FRESH', 'GAS']
        }
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(well.water_quality_characteristics.count(), 3)

    def test_casing_submission(self):
        """ Test that if a legacy well does not have a casing drive shoe, it doesn't cause problems """
        # We create a pre-existing "legacy well"
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        # We attached a casing to the well, a casing the is missing a drive_shoe, which is a "required"
        # field.
        Casing.objects.create(
            well=well, start=0, end=10, diameter=6.63, casing_code=self.casing_code_surface,
            casing_material=self.casing_material_code_other, drive_shoe_status=None, wall_thickness=0.22,
            create_user='Blah', update_user='Blah')
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
                    'drive_shoe_status': 'Installed',
                    'wall_thickness': '0.220'
                }
            ],
            'decommission_description_set': []
        }
        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_end_greater_than_zero_on_legacy(self):
        """ Test that if a legacy well does not have correct lithology info, it doesn't cause problems """
        # We create a pre-existing "legacy well"
        well = Well.objects.create(create_user='Blah', update_user='Blah')
        # We attached lithology to the well, that's should fail validation.
        LithologyDescription.objects.create(
            start=0,
            end=0,
            well=well,
            create_user='Blah',
            update_user='Blah')
        # Doing a valid edit, updating the lithology information, should be fine.
        data = {
            'well': well.well_tag_number,
            'latitude': 48.639643,
            'longitude': -123.55975,
            'lithologydescription_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_edit_with_bad_lithology_in_old_well_returns_bad_request(self):
        """ Test that if a legacy well does not have correct lithology info, that it doesn't fail
        on generating the legacy record, but does give us a bad request response. """
        # We create a pre-existing "legacy well"
        well = Well.objects.create(create_user='Blah', update_user='Blah')
        # We attached lithology to the well, that should fail validation.
        LithologyDescription.objects.create(
            well=well, start=117, end=None, create_user='Blah', update_user='Blah')
        # Doing an edit, without passing in the correct validation, should fail!
        data = {
            'well': well.well_tag_number
        }
        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_staff_edit_with_bad_lithology_in_old_well_but_edit_good_returns_ok(self):
        """ Test that if a legacy well does not have correct lithology info, but we submit
        good data on an edit, that everything works fine."""
        # We create a pre-existing "legacy well"
        well = Well.objects.create(create_user='Blah', update_user='Blah')
        # We attached lithology to the well, that should fail validation.
        LithologyDescription.objects.create(
            well=well, start=117, end=None, create_user='Blah', update_user='Blah')
        # Doing a valid edit, updating the lithology information, should be fine.
        data = {
            'well': well.well_tag_number,
            'lithologydescription_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_edit_with_bad_lithology_in_old_well_but_edit_saves_new_data(self):
        """ Test that if a legacy well does not have correct lithology info, but we submit
        good data on an edit, that everything works fine."""
        # We create a pre-existing "legacy well"
        well = Well.objects.create(create_user='Blah', update_user='Blah')
        # We attached lithology to the well, that should fail validation.
        LithologyDescription.objects.create(
            well=well, start=117, end=None, update_user='Blah', create_user='Blah')
        # Doing a valid edit, updating the lithology information, should be fine.
        data = {
            'well': well.well_tag_number,
            'lithologydescription_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        lithology = well.lithologydescription_set.all()
        self.assertAlmostEqual(lithology[0].start, 0)
        self.assertAlmostEqual(lithology[0].end, 10)

    def test_no_city_on_legacy(self):
        """ Test that the legacy record creates ok, even with missing legacy data.

            NOTE: a missing owner_city is a common legacy data issue.
            This test used to assert that a missing city would stop the staff edit
            request, but requiring a valid owner_city (when it wasn't required before)
            caused too many issues for users.  This test is kept in place to ensure
            that legacy data won't cause validation errors, but a new test will (hopefully)
            be written to prevent new wells from being created without required information.
        """
        well = Well.objects.create(
            create_user='Blah', update_user='Blah', owner_city=' ')
        data = {
            'well': well.well_tag_number
        }

        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['owner_city'] = 'Somewhere'
        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_construction_dates(self):
        """ Check that altering the constructions dates on a staff edit is reflected on the well """
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        data = {
            'well': well.well_tag_number,
            'construction_start_date': '1999-05-05',
            'construction_end_date': '1999-06-06'
        }
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(well.construction_start_date, datetime.date(1999, 5, 5))
        self.assertEqual(well.construction_end_date, datetime.date(1999, 6, 6))

    def test_update_alteration_dates(self):
        """ Check that altering the alteration dates on a staff edit is reflected on the well """
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        data = {
            'well': well.well_tag_number,
            'alteration_start_date': '1999-05-05',
            'alteration_end_date': '1999-06-06'
        }
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(well.alteration_start_date, datetime.date(1999, 5, 5))
        self.assertEqual(well.alteration_end_date, datetime.date(1999, 6, 6))

    def test_update_decommission_dates(self):
        """ Check that altering the decommission dates on a staff edit is reflected on the well """
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        data = {
            'well': well.well_tag_number,
            'decommission_start_date': '1999-05-05',
            'decommission_end_date': '1999-06-06'
        }
        response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(well.decommission_start_date, datetime.date(1999, 5, 5))
        self.assertEqual(well.decommission_end_date, datetime.date(1999, 6, 6))

    def test_lithology_submission_create_user_update_user(self):
        """ Check that the lithology has the correct create_user and update user after editing. """
        """
        Test that when creating a construction submission, the lithology records on the submissions have
        the create user and update user set correctly.
        """
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        # Data for the edit submission.
        data = {
            'well': well.well_tag_number,
            'lithologydescription_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an edit submissions.
        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the submission back.
        submission = ActivitySubmission.objects.get(
            well__well_tag_number=response.data['well'],
            well_activity_type=WELL_ACTIVITY_CODE_STAFF_EDIT)
        # Get the resultant lithology record
        lithology = submission.lithologydescription_set.all()[0]
        self.assertEqual(lithology.create_user, self.user.username)
        self.assertEqual(lithology.update_user, self.user.username)

    def test_lithology_well_create_user_update_user(self):
        """ Check that the lithology on the resultant well has the correct create_user and udpate_user after
        editing"""
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        # Data for the edit submission.
        data = {
            'well': well.well_tag_number,
            'lithologydescription_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an edit submissions.
        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the well back.
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        # Get the resultant lithology record
        lithology = well.lithologydescription_set.all()[0]
        self.assertEqual(lithology.create_user, self.user.username)
        self.assertEqual(lithology.update_user, self.user.username)

    def test_edit_submission_liner_perforation(self):
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        # Data for the edit submission.
        data = {
            'well': well.well_tag_number,
            'linerperforation_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an edit submissions.
        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the submission back.
        liner = ActivitySubmissionLinerPerforation.objects.get(
            activity_submission__well__well_tag_number=well.well_tag_number,
            activity_submission__well_activity_type=WELL_ACTIVITY_CODE_STAFF_EDIT
        )
        # We expect a liner has been created for the submission.
        self.assertIsNotNone(liner)

    def test_edit_legacy_submission_liner_perforation(self):
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        LinerPerforation.objects.create(well=well, start=0, end=10)
        # Data for the edit submission.
        data = {
            'well': well.well_tag_number,
            'linerperforation_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an edit submissions.
        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the submission back.
        liner = ActivitySubmissionLinerPerforation.objects.get(
            activity_submission__well__well_tag_number=well.well_tag_number,
            activity_submission__well_activity_type=WELL_ACTIVITY_CODE_LEGACY
        )
        # We expect a liner has been created for the submission.
        self.assertIsNotNone(liner)

    def test_edit_well_liner_perforation(self):
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        # Data for the edit submission.
        data = {
            'well': well.well_tag_number,
            'linerperforation_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an edit submissions.
        response = response = self.client.post(reverse('STAFF_EDIT', kwargs={'version': 'v1'}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the submission back.
        liner = LinerPerforation.objects.get(
            well__well_tag_number=well.well_tag_number
        )
        # We expect a liner has been created for the submission.
        self.assertIsNotNone(liner)


class TestAlteration(TestSubmissionsBase):

    def test_alteration_submission_liner_perforation(self):
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        # Data for the edit submission.
        data = {
            'well': well.well_tag_number,
            'linerperforation_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an edit submissions.
        response = self.client.post(reverse('ALT', kwargs={'version': 'v1'}), data, format='json')
        # Get the submission back.
        liner = ActivitySubmissionLinerPerforation.objects.get(
            activity_submission__well__well_tag_number=well.well_tag_number,
            activity_submission__well_activity_type=WELL_ACTIVITY_CODE_ALTERATION
        )
        # We expect a liner has been created for the submission.
        self.assertIsNotNone(liner)

    def test_alteration_legacy_submission_liner_perforation(self):
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        LinerPerforation.objects.create(well=well, start=0, end=10)
        # Data for the edit submission.
        data = {
            'well': well.well_tag_number,
            'linerperforation_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an edit submissions.
        response = self.client.post(reverse('ALT', kwargs={'version': 'v1'}), data, format='json')
        # Get the submission back.
        liner = ActivitySubmissionLinerPerforation.objects.get(
            activity_submission__well__well_tag_number=well.well_tag_number,
            activity_submission__well_activity_type=WELL_ACTIVITY_CODE_LEGACY
        )
        # We expect a liner has been created for the submission.
        self.assertIsNotNone(liner)

    def test_alteration_well_liner_perforation(self):
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        # Data for the edit submission.
        data = {
            'well': well.well_tag_number,
            'linerperforation_set': [
                {
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an edit submissions.
        response = self.client.post(reverse('ALT', kwargs={'version': 'v1'}), data, format='json')
        # Get the submission back.
        liner = LinerPerforation.objects.get(
            well__well_tag_number=well.well_tag_number
        )
        # We expect a liner has been created for the submission.
        self.assertIsNotNone(liner)

    def test_comments_propagated_with_alteration_1(self):
        """
        Tests that the 'comments' and 'internal_comments' submitted with 
        an alteration report are concatenated onto pre-existing values
        from the well record.                  
        In this test, comments from a previous construction report
        are included in the following alteration report.
        """
        # submit a construction report
        construction_data = {
            'comments': "original comments",
            'internal_comments': "original internal comments"
        }
        construction_response = self.client.post(
            reverse(WELL_ACTIVITY_CODE_CONSTRUCTION, kwargs={'version': 'v1'}), construction_data, format='json')

        well_tag_number = construction_response.data['well']

        # submit an alteration report
        alteration_data = {
            'well': well_tag_number,
            'comments': 'alteration comments',
            'internal_comments': 'alteration internal comments'
        }
        alteration_response = self.client.post(
            reverse(WELL_ACTIVITY_CODE_ALTERATION, kwargs={'version': 'v1'}), alteration_data, format='json')
        self.assertEqual(alteration_response.status_code,
                         status.HTTP_201_CREATED)

        # confirm that the 'comments' and 'internal comments' in the alteration submission
        # are the concatenation of the values from the construction submission with the
        # newly submitted values
        alteration = ActivitySubmission.objects.get(
            filing_number=alteration_response.data['filing_number'])

        self.assertTrue(alteration.comments.startswith(
            construction_data.get("comments")))
        self.assertTrue(alteration.comments.endswith(
            alteration_data.get("comments")))
        self.assertTrue(alteration.internal_comments.startswith(
            construction_data.get("internal_comments")))
        self.assertTrue(alteration.internal_comments.endswith(
            alteration_data.get("internal_comments")))

    def test_comments_propagated_with_alteration_2(self):
        """
        Tests that the 'comments' and 'internal_comments' submitted with 
        an alteration report are concatenated onto pre-existing values
        from the well record.        
        """
        well = Well.objects.create(
            create_user=self.user.username,
            update_user=self.user.username,
            comments="original comments",
            internal_comments="original internal comments"
        )
        well_tag_number = well.well_tag_number

        # submit an alteration report
        alteration_data = {
            'well': well_tag_number,
            'comments': 'alteration comments',
            'internal_comments': 'alteration internal comments'
        }
        alteration_response = self.client.post(
            reverse(WELL_ACTIVITY_CODE_ALTERATION, kwargs={'version': 'v1'}), alteration_data, format='json')
        self.assertEqual(alteration_response.status_code,
                         status.HTTP_201_CREATED)

        # confirm that the 'comments' and 'internal comments' in the alteration submission
        # are the concatenation of the values from the construction submission with the
        # newly submitted values
        alteration = ActivitySubmission.objects.get(
            filing_number=alteration_response.data['filing_number'])

        self.assertTrue(alteration.comments.startswith(
            "original comments"))
        self.assertTrue(alteration.comments.endswith(
            alteration_data.get("comments")))
        self.assertTrue(alteration.internal_comments.startswith(
            "original internal comments"))
        self.assertTrue(alteration.internal_comments.endswith(
            alteration_data.get("internal_comments")))            

    def test_comments_propagated_with_alteration_3(self):
        """
        Tests that the 'comments' and 'internal_comments' submitted with 
        an alteration report are concatenated onto pre-existing values
        from the well record.        
        In this test, there is an original well record and two alteration 
        reports.  Comments from the original record should be copied to the first
        alteration report, and comments from both the original record and the first
        alteration report should be present in the second report.
        """
        well = Well.objects.create(
            create_user=self.user.username,
            update_user=self.user.username,
            comments="original comments",
            internal_comments="original internal comments"
        )
        well_tag_number = well.well_tag_number

        # submit alteration report #1
        alteration_data_1 = {
            'well': well_tag_number,
            'comments': 'alteration comments 1',
            'internal_comments': 'alteration internal comments 1'
        }
        alteration_response_1 = self.client.post(
            reverse(WELL_ACTIVITY_CODE_ALTERATION, kwargs={'version': 'v1'}), alteration_data_1, format='json')
        self.assertEqual(alteration_response_1.status_code,
                         status.HTTP_201_CREATED)

        # confirm that the comments in the first alteration report are correct
        alteration_1 = ActivitySubmission.objects.get(
            filing_number=alteration_response_1.data['filing_number'])

        self.assertTrue(alteration_1.comments.startswith(
            "original comments"))
        self.assertTrue(alteration_1.comments.endswith(
            alteration_data_1.get("comments")))
        self.assertTrue(alteration_1.internal_comments.startswith(
            "original internal comments"))
        self.assertTrue(alteration_1.internal_comments.endswith(
            alteration_data_1.get("internal_comments")))   

        # submit alteration report #2
        alteration_data_2 = {
            'well': well_tag_number,
            'comments': 'alteration comments 2',
            'internal_comments': 'alteration internal comments 2'
        }
        alteration_response_2 = self.client.post(
            reverse(WELL_ACTIVITY_CODE_ALTERATION, kwargs={'version': 'v1'}), alteration_data_2, format='json')
        self.assertEqual(alteration_response_2.status_code,
                         status.HTTP_201_CREATED)
 
        # confirm that the comments in the second alteration report are correct
        alteration_2 = ActivitySubmission.objects.get(
            filing_number=alteration_response_2.data['filing_number'])

        self.assertTrue(alteration_2.comments.startswith(
            alteration_1.comments))
        self.assertTrue(alteration_2.comments.endswith(
            alteration_data_2.get("comments")))
        self.assertTrue(alteration_2.internal_comments.startswith(
            alteration_1.internal_comments))
        self.assertTrue(alteration_2.internal_comments.endswith(
            alteration_data_2.get("internal_comments")))   

    def test_no_comments_propagated_with_alteration_of_unknown_well(self):
        """
        Tests that an alteration report with no well_tag_number
        will succeed, and the alteration comments will be saved 
        exactly as they appeared in the request.
        """
        # submit an alteration report
        alteration_data = {
            'comments': 'alteration comments',
            'internal_comments': 'alteration internal comments'
        }
        alteration_response = self.client.post(
            reverse(WELL_ACTIVITY_CODE_ALTERATION, kwargs={'version': 'v1'}), alteration_data, format='json')
        self.assertEqual(alteration_response.status_code,
                         status.HTTP_201_CREATED)

        # confirm that the 'comments' and 'internal comments' in the alteration submission
        # are the concatenation of the values from the construction submission with the
        # newly submitted values
        alteration = ActivitySubmission.objects.get(
            filing_number=alteration_response.data['filing_number'])

        self.assertEquals(alteration.comments, alteration_data.get("comments"))
        self.assertEquals(alteration.internal_comments, alteration_data.get("internal_comments"))
        

    def test_comments_propagated_with_decommission(self):
        """
        Tests that the 'comments' and 'internal_comments' submitted with 
        a decommission report are concatenated onto pre-existing values
        from an earlier submission (or from the well record if no previous
        submission exists).        
        In this test, comments from a previous staff edit
        are included in the following decommission report.
        """
        well = Well.objects.create(
            create_user=self.user.username,
            update_user=self.user.username,
            comments="original comments",
            internal_comments="original internal comments"
        )
        well_tag_number = well.well_tag_number

        # submit a staff edit
        staff_edit_data = {
            'well': well_tag_number,
            'comments': "staff edit comments",
            'internal_comments': "staff edit internal comments"
        }
        staff_edit_response = self.client.post(
            reverse(WELL_ACTIVITY_CODE_STAFF_EDIT, kwargs={'version': 'v1'}), staff_edit_data, format='json')

        # submit a decommission report
        decommission_data = {
            'well': well_tag_number,
            'comments': 'decommission comments',
            'internal_comments': 'decommission internal comments'
        }
        decommission_response = self.client.post(
            reverse(WELL_ACTIVITY_CODE_ALTERATION, kwargs={'version': 'v1'}), decommission_data, format='json')
        self.assertEqual(decommission_response.status_code,
                         status.HTTP_201_CREATED)

        # confirm that the 'comments' and 'internal comments' in the alteration submission
        # are the concatenation of the values from the construction submission with the
        # newly submitted values
        decommission = ActivitySubmission.objects.get(
            filing_number=decommission_response.data['filing_number'])

        self.assertTrue(decommission.comments.startswith(
            staff_edit_data.get("comments")))
        self.assertTrue(decommission.comments.endswith(
            decommission_data.get("comments")))
        self.assertTrue(decommission.internal_comments.startswith(
            staff_edit_data.get("internal_comments")))
        self.assertTrue(decommission.internal_comments.endswith(
            decommission_data.get("internal_comments")))

    def test_comments_not_propagated_with_staff_edit(self):
        """
        Tests that the 'comments' and 'internal_comments' included with 
        a STAFF_EDIT submission are saved "as is", and not concatenated
        with any previous comments (as happens with alteration and decommission
        submissions)
        """
        # submit a construction report
        construction_data = {
            'comments': "original comments",
            'internal_comments': "original internal comments"
        }
        construction_response = self.client.post(
            reverse(WELL_ACTIVITY_CODE_CONSTRUCTION, kwargs={'version': 'v1'}), construction_data, format='json')

        well_tag_number = construction_response.data['well']

        # submit a staff edit
        staff_edit_data = {
            'well': well_tag_number,
            'comments': "staff edit comments",
            'internal_comments': "staff edit internal comments"
        }
        staff_edit_response = self.client.post(
            reverse(WELL_ACTIVITY_CODE_STAFF_EDIT, kwargs={'version': 'v1'}), staff_edit_data, format='json')
        self.assertEqual(staff_edit_response.status_code,
                         status.HTTP_201_CREATED)

        # confirm that the 'comments' and 'internal comments' in the
        # staff edit submission match the submitted values
        staff_edit = ActivitySubmission.objects.get(
            well=well_tag_number,
            well_activity_type=WELL_ACTIVITY_CODE_STAFF_EDIT)

        self.assertEquals(staff_edit.comments,
                          staff_edit_data.get("comments"))
        self.assertEquals(staff_edit.internal_comments,
                          staff_edit_data.get("internal_comments"))

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
        url = reverse('submissions-list', kwargs={'version': 'v1'})
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_rights_attempts_construction_submission(self):
        # As a user with view rights, I should not be able to create a construction submission.
        url = reverse('CON', kwargs={'version': 'v1'})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_rights_attempts_alteration_submission(self):
        # As a user with view rights, I should not be able to create an alteration submission.
        url = reverse('ALT', kwargs={'version': 'v1'})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_rights_attempts_alteration_submission(self):
        # As a user with view rights, I should not be able to create a decommission submission.
        url = reverse('DEC', kwargs={'version': 'v1'})
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
        url = reverse('submissions-list', kwargs={'version': 'v1'})
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_submission_rights_attempts_construction_submission(self):
        url = reverse('CON', kwargs={'version': 'v1'})
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
        url = reverse('ALT', kwargs={'version': 'v1'})
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
        url = reverse('DEC', kwargs={'version': 'v1'})
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
        url = reverse('CON', kwargs={'version': 'v1'})
        data = {}
        response = self.client.post(url, data, format='json')
        well = Well.objects.get(well_tag_number=response.data['well'])
        self.assertEqual(well.create_user, self.user.username)

    def test_update_user_populated_on_submission(self):
        # Upon creation of a submission, the update user must be the same as the created_by user.
        url = reverse('CON', kwargs={'version': 'v1'})
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
        url = reverse('ALT', kwargs={'version': 'v1'})
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
        url = reverse('CON', kwargs={'version': 'v1'})
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
        url = reverse('CON', kwargs={'version': 'v1'})
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
        url = reverse('ALT', kwargs={'version': 'v1'})
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
        url = reverse('ALT', kwargs={'version': 'v1'})
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
        self.assertEqual(well.create_user, DATALOAD_USER)
        # The legacy submission should show dataload user as the create_user and update_user.
        self.assertEqual(legacy.create_user, DATALOAD_USER)
        self.assertEqual(legacy.update_user, DATALOAD_USER)
        # The alteration should show the current user as the create_user and update_user.
        self.assertEqual(alteration.create_user, self.user.username)
        self.assertEqual(alteration.update_user, self.user.username)

    def test_decommission_create_user_update_user(self):
        """
        Test that the well created by a construction submission, has perforation records with the
        create user and update user set correctly.
        """
        well = Well.objects.create(create_user=self.user.username, update_user=self.user.username)
        # Data for the construction submission.
        data = {
            'well': well.well_tag_number,
            'decommission_description_set': [
                {
                    'material': 'BENTONITE_CHIPS',
                    'start': 0,
                    'end': 10
                }
            ]
        }
        # Post an construction submissions.
        response = self.client.post(reverse('DEC', kwargs={'version': 'v1'}), data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            # Useful for debugging failing tests.
            logger.warn(response)
        # Get the well back.
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        # Get the resultant lithology record
        decommission = well.decommission_description_set.all()[0]
        self.assertEqual(decommission.create_user, self.user.username)
        self.assertEqual(decommission.update_user, self.user.username)
