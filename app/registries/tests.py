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
import uuid
import logging
import os

from django.urls import reverse
from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from gwells.models import ProvinceStateCode, Profile
from registries.models import (
    ApplicationStatusCode,
    Organization,
    Person,
    RegistriesApplication,
    Register,
    ActivityCode,
    SubactivityCode)
from registries.views import PersonListView, PersonDetailView
from gwells.roles import (roles_to_groups, GWELLS_ROLE_GROUPS, GWELLS_ROLES,
                          REGISTRIES_ADJUDICATOR_ROLE, ADMIN_ROLE, REGISTRIES_AUTHORITY_ROLE,
                          REGISTRIES_VIEWER_ROLE)

# Note: see postman/newman for more API tests.
# Postman API tests include making requests with incomplete data, missing required fields etc.
# They are located at {base-dir}/api-tests/

# Base classes


class AuthenticatedAPITestCase(APITestCase):
    """
    Creates a user before each test and forces authentication with that user.
    Extends APITestCase from Django REST Framework.
    Not intended for regular Django TestCase (for DRF tests only)
    """

    def setUp(self):
        self.user, created = User.objects.get_or_create(username='testuser')
        if created:
            Profile.objects.get_or_create(user=self.user)
        self.user.is_staff = True
        self.user.profile.is_gwells_admin = True
        self.user.save()
        self.user.profile.save()

        roles_to_groups(self.user, ['gwells_admin'])
        self.client.force_authenticate(self.user)


# Django unit tests

class OrganizationTests(TestCase):
    """
    Tests for the Organization model

    Simple test that we can create objects from models.py for the Organization model
    Tests for views.py and other modules are in Django REST Framework tests
    """

    def setUp(self):
        # Create a ProvinceStateCode object for our Organization's foreign key field
        self.province = ProvinceStateCode.objects.create(
            province_state_code='BC',
            description='British Columbia',
            display_order=1
        )

        self.org = Organization.objects.create(
            name='Frankie and Betty Well Drilling Co.',
            city='Victoria',
            province_state=self.province
        )

    def test_organization_was_created(self):
        org = Organization.objects.get(
            name='Frankie and Betty Well Drilling Co.')
        self.assertEqual(org.city, 'Victoria')
        self.assertEqual(org.province_state, self.province)


class PersonTests(TestCase):
    """
    Tests for Person model
    """

    def setUp(self):
        Person.objects.create(
            first_name='Bobby',
            surname='Driller'
        )

    def test_person_was_created(self):
        person = Person.objects.get(first_name='Bobby')
        self.assertEqual(person.first_name, 'Bobby')


class RegistriesApplicationTestBase(AuthenticatedAPITestCase):
    """
    Base class for RegistriesApplication
    """

    def setUp(self):
        super().setUp()
        # Crate activityCode
        self.activity_drill = ActivityCode.objects.create(
            registries_activity_code="DRILL",
            description="driller",
            display_order="1")
        # Create new registrations
        # Create registered driller 1
        self.driller = Person.objects.create(
            first_name='Wendy', surname="Well")
        self.registration = Register.objects.create(
            person=self.driller,
            registries_activity=self.activity_drill,
            registration_no="F12345",
        )
        # Create subactivities
        self.subactivity = SubactivityCode.objects.create(
            registries_activity=self.activity_drill,
            registries_subactivity_code='WATER',
            description='water',
            display_order=1)
        self.subactivity = SubactivityCode.objects.create(
            registries_activity=self.activity_drill,
            registries_subactivity_code='GEOTECH',
            description='geotech',
            display_order=1)
        # Create application status
        self.application_status_active = ApplicationStatusCode.objects.create(
            code='A',
            description='Active',
            display_order=1
        )
        self.application_status_pending = ApplicationStatusCode.objects.create(
            code='P',
            description='Pending',
            display_order=1
        )
        # Application
        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            subactivity=self.subactivity)


class RegistriesApplicationNoStatusTest(RegistriesApplicationTestBase):

    def test_update_application_status_to_active(self):
        """ Test that an application created without a status can be updated to Active
        """
        data = {
            'current_status': {
                'code': 'A'
            }
        }

        url = reverse('application-detail',
                      kwargs={'application_guid': self.app.application_guid})
        response = self.client.patch(url, data, format='json')
        updated_application = RegistriesApplication.objects.get(
            application_guid=self.app.application_guid)
        self.assertEqual(
            updated_application.current_status.code, 'A')


class RegistriesApplicationWithStatusActiveTest(RegistriesApplicationTestBase):

    def setUp(self):
        super().setUp()

    def test_update_application_status_to_active(self):
        """ Test that an application created with a Pending status can be updated to Active
        """
        data = {
            'current_status': {
                'code': 'A'
            }
        }

        url = reverse('application-detail',
                      kwargs={'application_guid': self.app.application_guid})
        response = self.client.patch(url, data, format='json')
        updated_application = RegistriesApplication.objects.get(
            application_guid=self.app.application_guid)
        self.assertEqual(
            updated_application.current_status.code, 'A')


class RegistriesApplicationStatusSubactivityTest(RegistriesApplicationTestBase):

    def test_update_application_subactivity(self):
        """ Test that an application created with water as a subactivity can be changed to geotech
        """
        data = {'subactivity': 'GEOTECH'}

        url = reverse('application-detail',
                      kwargs={'application_guid': self.app.application_guid})
        response = self.client.patch(url, data, format='json')
        updated_application = RegistriesApplication.objects.get(
            application_guid=self.app.application_guid)
        self.assertEqual(
            updated_application.subactivity.registries_subactivity_code, 'GEOTECH')


# Django REST Framework tests
class APIOrganizationTests(AuthenticatedAPITestCase):
    """
    Tests for requests to the Organization resource endpoint

    Includes tests for create, list, update (patch and put), and delete
    """

    def setUp(self):
        super().setUp()
        self.province = ProvinceStateCode.objects.create(
            province_state_code='BC',
            description='British Columbia',
            display_order=1)

        self.initial_data = {
            'name': 'Bobby\'s Drilling',
            'city': 'Victoria',
            'province_state': 'BC'
        }

    def test_create_organization(self):
        """
        Create a new organization object.
        """

        url = reverse('organization-list')
        count_before = Organization.objects.count()

        response = self.client.post(url, self.initial_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), count_before + 1)

    def test_list_organization(self):
        url = reverse('organization-list')
        new_object = self.client.post(url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(created_guid), 36)
        self.assertContains(response, created_guid)

    def test_retrieve_organization(self):
        create_url = reverse('organization-list')
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        retrieve_url = reverse('organization-detail',
                               kwargs={'org_guid': created_guid})
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.initial_data['name'])
        self.assertEqual(response.data['city'], self.initial_data['city'])

    def test_patch_organization(self):
        new_data = {
            'city': 'Duncan'
        }

        create_url = reverse('organization-list')
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        object_url = reverse('organization-detail',
                             kwargs={'org_guid': created_guid})

        # Apply a new city name with PATCH method
        self.client.patch(object_url, new_data, format='json')

        response = self.client.get(object_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.initial_data['name'])
        self.assertEqual(response.data['city'], new_data['city'])

    def test_put_organization(self):
        new_data = {
            'name': 'Betty\'s Drilling',
            'city': 'Duncan',
            'province_state': 'BC'
        }

        create_url = reverse('organization-list')
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        object_url = reverse('organization-detail',
                             kwargs={'org_guid': created_guid})

        # Apply a new city name with PATCH method
        self.client.put(object_url, new_data, format='json')

        response = self.client.get(object_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])
        self.assertEqual(response.data['city'], new_data['city'])

    def test_delete_organization(self):
        # setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        create_url = reverse('organization-list')
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        retrieve_url = reverse('organization-detail',
                               kwargs={'org_guid': created_guid})
        retrieve_response = self.client.get(retrieve_url, format='json')

        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            retrieve_response.data['name'], self.initial_data['name'])
        self.assertEqual(
            retrieve_response.data['city'], self.initial_data['city'])

        delete_response = self.client.delete(retrieve_url, format='json')
        self.assertEqual(delete_response.status_code,
                         status.HTTP_204_NO_CONTENT)

        get_after_delete_response = self.client.get(
            retrieve_url, format='json')
        self.assertEqual(get_after_delete_response.status_code,
                         status.HTTP_404_NOT_FOUND)

        # teardown
        logger.setLevel(previous_level)

    def test_organization_audit_fields(self):
        """
        Test that AuditModel fields (create_user, create_date etc.)
        are updated when Organization objects are created.
        """

        create_url = reverse('organization-list')
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        retrieve_url = reverse('organization-detail',
                               kwargs={'org_guid': created_guid})
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # TODO: When authentication is enforced, this line will need to change
        self.assertEqual(response.data['create_user'], self.user.username)

    def test_create_org_not_authenticated(self):
        """
        Ensure that users who are not authenticated cannot create Organization objects
        """
        self.client.force_authenticate(user=None)
        url = reverse('organization-list')
        data = {'name': 'Big Time Drilling Co'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unsafe_methods_by_unauthorized_users(self):
        """
        Ensure that users who are not authenticated cannot perform "unsafe" actions
        like UPDATE, PUT, DELETE on an object that is already in database
        """
        self.client.force_authenticate(user=None)
        org_object = Organization.objects.create(
            name='Big Time Drilling Co', province_state=self.province)
        object_url = reverse('organization-detail',
                             kwargs={'org_guid': org_object.org_guid})

        update_response = self.client.patch(
            object_url, {'name': 'Small Time Drilling Company'}, format='json')
        put_response = self.client.put(
            object_url,
            {
                'org_guid': org_object.org_guid,
                'name': 'Small Time Drilling Company',
            },
            format='json'
        )
        delete_response = self.client.delete(object_url, format='json')

        self.assertEqual(update_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(put_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)


class APIPersonTests(AuthenticatedAPITestCase):
    """
    Tests for Person resource endpoint
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.initial_data = {
            'first_name': 'Bobby',
            'surname': 'Driller'
        }
        self.prov, _ = ProvinceStateCode.objects.get_or_create(
            province_state_code='BC', display_order=1)
        super().setUp()

    def test_create_person(self):
        url = reverse('person-list')
        data = {'first_name': 'Bobby', 'surname': 'Driller'}
        count_before = Person.objects.count()

        response = self.client.post(url, data, format='json')
        created_guid = response.data['person_guid']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['first_name'], Person.objects.get(
            person_guid=created_guid).first_name)
        self.assertEqual(data['surname'], Person.objects.get(
            person_guid=created_guid).surname)
        self.assertEqual(Person.objects.count(), count_before + 1)

    def test_list_people(self):
        url = reverse('person-list')
        new_object = self.client.post(url, self.initial_data, format='json')
        created_guid = new_object.data['person_guid']

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(created_guid), 36)
        self.assertContains(response, created_guid)

    def test_retrieve_person(self):
        create_url = reverse('person-list')
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['person_guid']

        retrieve_url = reverse(
            'person-detail', kwargs={'person_guid': created_guid})
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'],
                         self.initial_data['first_name'])
        self.assertEqual(response.data['surname'],
                         self.initial_data['surname'])

    def test_patch_person(self):
        new_data = {
            'surname': 'Wells'
        }

        create_url = reverse('person-list')
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['person_guid']

        object_url = reverse(
            'person-detail', kwargs={'person_guid': created_guid})

        # Apply a new city name with PATCH method
        self.client.patch(object_url, new_data, format='json')

        response = self.client.get(object_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'],
                         self.initial_data['first_name'])
        self.assertEqual(response.data['surname'], new_data['surname'])

    def test_update_person_by_put(self):
        initial_data = {
            'first_name': 'Bobby',
            'surname': 'Driller'
        }
        new_data = {
            'first_name': 'Betty',
            'surname': 'Wells'
        }

        create_url = reverse('person-list')
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['person_guid']

        object_url = reverse(
            'person-detail', kwargs={'person_guid': created_guid})

        # Apply a new name with PATCH method
        self.client.put(object_url, new_data, format='json')

        response = self.client.get(object_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], new_data['first_name'])
        self.assertEqual(response.data['surname'], new_data['surname'])

    def test_delete_person(self):
        # setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        initial_data = {
            'first_name': 'Bobby',
            'surname': 'Driller'
        }

        create_url = reverse('person-list')
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['person_guid']

        retrieve_url = reverse(
            'person-detail', kwargs={'person_guid': created_guid})
        retrieve_response = self.client.get(retrieve_url, format='json')

        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            retrieve_response.data['first_name'], self.initial_data['first_name'])
        self.assertEqual(
            retrieve_response.data['surname'], self.initial_data['surname'])

        delete_response = self.client.delete(retrieve_url, format='json')
        self.assertEqual(delete_response.status_code,
                         status.HTTP_204_NO_CONTENT)

        get_after_delete_response = self.client.get(
            retrieve_url, format='json')
        self.assertEqual(get_after_delete_response.status_code,
                         status.HTTP_404_NOT_FOUND)

        # teardown
        logger.setLevel(previous_level)

    def test_person_audit_fields(self):
        """
        Test that AuditModel fields (create_user, create_date etc.)
        are updated when Person objects are created.
        """
        view = PersonListView.as_view()
        post_url = reverse('person-list')
        request = self.factory.post(post_url, self.initial_data)
        request.user = self.user
        response = view(request)
        created_guid = response.data['person_guid']

        person = Person.objects.get(person_guid=created_guid)

        self.assertEqual(person.create_user, self.user.username)

    def test_person_history(self):
        """
        Test that a version history is created when Person objects are created.
        """
        call_command('createinitialrevisions')
        view = PersonListView.as_view()
        post_url = reverse('person-list')
        request = self.factory.post(post_url, self.initial_data)
        request.user = self.user
        response = view(request)
        created_guid = response.data['person_guid']

        person = Person.objects.get(person_guid=created_guid)

        self.assertEqual(person.history.count(), 1)

    def test_create_person_not_authenticated(self):
        """
        Ensure that users who are not authenticated cannot create Person objects
        """
        self.client.force_authenticate(user=None)
        url = reverse('person-list')
        data = {'first_name': 'Bobby', 'surname': 'Driller'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_wrong_role(self):
        user, created = User.objects.get_or_create(username='test_viewer')
        if created:
            Profile.objects.get_or_create(user=user)

        roles_to_groups(user, REGISTRIES_VIEWER_ROLE)
        self.client.force_authenticate(user=user)
        url = reverse('person-list')
        data = {'first_name': 'Bobby', 'surname': 'Driller'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unsafe_methods_by_unauthorized_users(self):
        """
        Ensure that users who are not authenticated cannot perform "unsafe" actions
        like UPDATE, PUT, DELETE on an object that is already in database
        """
        self.client.force_authenticate(user=None)
        person_object = Person.objects.create(
            first_name='Bobby', surname='Driller')
        object_url = reverse(
            'person-detail', kwargs={'person_guid': person_object.person_guid})

        update_response = self.client.patch(
            object_url, {'first_name': 'Billy'}, format='json')
        put_response = self.client.put(
            object_url,
            {
                'person_guid': person_object.person_guid,
                'first_name': 'Betty',
                'surname': 'McDrillerson'
            },
            format='json'
        )
        delete_response = self.client.delete(object_url, format='json')

        self.assertEqual(update_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(put_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)


class APIFilteringPaginationTests(APITestCase):
    """
    Tests of the filtering, searching and pagination systems.
    Filtering tests include filtering out results if user is anonymous.
    """

    def setUp(self):
        self.province = ProvinceStateCode.objects.create(
            province_state_code='BC',
            display_order=1)
        self.status_active = ApplicationStatusCode.objects.create(
            code="A",
            description="active",
            display_order="1")
        self.status_inactive = ApplicationStatusCode.objects.create(
            code="NA",
            description="inactive",
            display_order="2")
        self.activity_drill = ActivityCode.objects.create(
            registries_activity_code="DRILL",
            description="driller",
            display_order="1")
        self.activity_pump = ActivityCode.objects.create(
            registries_activity_code="PUMP",
            description="pump installer",
            display_order="2")

        # Create registered driller 1
        self.driller = Person.objects.create(
            first_name='Wendy', surname="Well")
        self.registration = Register.objects.create(
            person=self.driller,
            registries_activity=self.activity_drill,
            registration_no="F12345",
        )
        self.subactivity = SubactivityCode.objects.create(
            registries_activity=self.activity_drill,
            registries_subactivity_code='WAT',
            description='water',
            display_order=1)
        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            current_status=self.status_active,
            subactivity=self.subactivity)

        # Create registered driller 2
        self.driller2 = Person.objects.create(
            first_name='Debbie', surname="Driller")
        self.registration2 = Register.objects.create(
            person=self.driller2,
            registries_activity=self.activity_drill,
            registration_no="F54321",
        )

        self.app2 = RegistriesApplication.objects.create(
            registration=self.registration2,
            current_status=self.status_active,
            subactivity=self.subactivity)

        # Create unregistered driller
        self.unregistered_driller = Person.objects.create(
            first_name="Johnny", surname="Unregistered")

        # Create inactive driller
        self.inactive_driller = Person.objects.create(
            first_name="Billy", surname="Retired")
        self.retired_registration = Register.objects.create(
            person=self.inactive_driller,
            registries_activity=self.activity_drill,
            registration_no="R55555"
        )
        self.retired_app = RegistriesApplication.objects.create(
            registration=self.retired_registration,
            subactivity=self.subactivity)

        # create a company with no registered driller
        self.company_with_no_driller = Organization.objects.create(
            name="Big Time Drilling Company",
            province_state=self.province)

    def test_user_cannot_see_unregistered_person_in_list(self):
        url = reverse('person-list')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 2)
        self.assertContains(response, 'Wendy')
        self.assertContains(response, 'Debbie')

        # Johnny is in database but is not registered, so make sure he's not in the publicly available list.
        self.assertNotContains(response, 'Johnny')
        self.assertNotContains(response, self.unregistered_driller.person_guid)

    def test_user_cannot_retrieve_unregistered_person(self):
        """ unauthorized request to person detail view. Note: now always returns 401 if not staff. """

        # setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        url = reverse(
            'person-detail', kwargs={'person_guid': self.unregistered_driller.person_guid})
        response = self.client.get(url, format='json')

        # quick check to make sure the record actually exists
        person = Person.objects.get(
            person_guid=self.unregistered_driller.person_guid)
        self.assertEqual(person.first_name, 'Johnny')

        # now make sure API does not return the record if unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # teardown
        logger.setLevel(previous_level)

    def test_search_for_name(self):
        url = reverse('person-list') + '?search=' + self.driller.first_name
        response = self.client.get(url, format='json')

        self.assertContains(response, self.driller.first_name)
        self.assertContains(response, self.driller.person_guid)
        self.assertNotContains(response, self.driller2.first_name)
        self.assertNotContains(response, 'Johnny')
        self.assertNotContains(response, self.driller2.person_guid)
        self.assertNotContains(response, self.unregistered_driller.person_guid)

    def test_search_for_registration_number(self):
        url = reverse('person-list') + '?search=' + \
            self.registration2.registration_no
        response = self.client.get(url, format='json')

        self.assertContains(response, self.driller2.first_name)
        self.assertContains(response, self.driller2.person_guid)
        self.assertNotContains(response, self.driller.first_name)
        self.assertNotContains(response, 'Johnny')
        self.assertNotContains(response, self.driller.person_guid)
        self.assertNotContains(response, self.unregistered_driller.person_guid)

    def test_anon_user_cannot_see_unregistered_organization(self):
        # setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        self.client.force_authenticate(user=None)
        url = reverse('organization-detail',
                      kwargs={'org_guid': self.company_with_no_driller.org_guid})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # teardown
        logger.setLevel(previous_level)

    def test_anon_user_cannot_create_driller(self):
        # setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        self.client.force_authenticate(user=None)
        url = reverse('person-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # teardown
        logger.setLevel(previous_level)


class TestPublicSearch(TestCase):

    def setUp(self):
        super().setUp()
        self.activity_drill = ActivityCode.objects.create(
            registries_activity_code="DRILL",
            description="driller",
            display_order="1")
        self.status_pending = ApplicationStatusCode.objects.create(
            code="P",
            description="Pending",
            display_order="2")
        self.status_approved = ApplicationStatusCode.objects.create(
            code="A",
            description="Approved",
            display_order="3")
        # Create subactivities
        self.subactivity = SubactivityCode.objects.create(
            registries_activity=self.activity_drill,
            registries_subactivity_code='WATER',
            description='water',
            display_order=1)
        # Person with Pending, Removed and Approved
        # A person with a removed application
        self.person_removed = Person.objects.create(
            first_name='Wendy', surname="Schmoo")
        self.registration = Register.objects.create(
            person=self.person_removed,
            registries_activity=self.activity_drill,
            registration_no="F12345")
        RegistriesApplication.objects.create(
            registration=self.registration,
            current_status=self.status_approved,
            subactivity=self.subactivity)
        RegistriesApplication.objects.create(
            registration=self.registration,
            current_status=self.status_pending,
            subactivity=self.subactivity)
        RegistriesApplication.objects.create(
            registration=self.registration,
            current_status=self.status_approved,
            removal_date='2018-01-01',
            subactivity=self.subactivity)

    def test_search_only_returns_approved(self):
        # Test that when searching, only the active applications are returned.
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status=Removed'
        response = self.client.get(url, format='json')
        # We expect no pending records to have been returned.
        self.assertNotContains(response, 'Pending')
        # We expect only one Approved record, as the other record has a removal_date.
        # The word approved appears twice. Once in the current_status and once in the display status.
        self.assertContains(response, 'Approved', 2)


class TestAuthenticatedSearch(AuthenticatedAPITestCase):

    def setUp(self):
        super().setUp()
        self.activity_drill = ActivityCode.objects.create(
            registries_activity_code="DRILL",
            description="driller",
            display_order="1")
        self.status_pending = ApplicationStatusCode.objects.create(
            code="P",
            description="Pending",
            display_order="2")
        self.status_approved = ApplicationStatusCode.objects.create(
            code="A",
            description="Approved",
            display_order="3")
        self.status_not_approved = ApplicationStatusCode.objects.create(
            code="NA",
            description="Not Approved",
            display_order="4")
        # Create subactivities
        self.subactivity = SubactivityCode.objects.create(
            registries_activity=self.activity_drill,
            registries_subactivity_code='WATER',
            description='water',
            display_order=1)
        # A person with no registration associated
        self.person_without_registration = Person.objects.create(
            first_name='Wendy', surname="NoRegistration")
        # A person with a registration, but no application associated
        self.person_without_application = Person.objects.create(
            first_name='Wendy', surname="NoApplication")
        self.registration = Register.objects.create(
            person=self.person_without_application,
            registries_activity=self.activity_drill,
            registration_no="F12345")
        # A person with a registration, and an application, with status set to P
        self.person_pending = Person.objects.create(
            first_name='Wendy', surname="PersonPending")
        self.registration = Register.objects.create(
            person=self.person_pending,
            registries_activity=self.activity_drill,
            registration_no="F12345")
        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            current_status=self.status_pending,
            subactivity=self.subactivity)
        # A person with an approved application
        self.person_approved = Person.objects.create(
            first_name='Wendy', surname="PersonApproved")
        self.registration = Register.objects.create(
            person=self.person_approved,
            registries_activity=self.activity_drill,
            registration_no="F12345")
        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            current_status=self.status_approved,
            subactivity=self.subactivity)
        # A person with a removed application
        self.person_removed = Person.objects.create(
            first_name='Wendy', surname="PersonRemoved")
        self.registration = Register.objects.create(
            person=self.person_removed,
            registries_activity=self.activity_drill,
            registration_no="F12345")
        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            current_status=self.status_approved,
            removal_date='2018-01-01',
            subactivity=self.subactivity)
        # A person with a "not approved" state
        self.person_not_approved = Person.objects.create(
            first_name='Wendy', surname='NotApproved')
        self.registration = Register.objects.create(
            person=self.person_not_approved,
            registries_activity=self.activity_drill,
            registration_no="F12345")
        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            current_status=self.status_not_approved,
            subactivity=self.subactivity)
        # A person with an approved application, AND a removed application
        self.person_approved_and_removed = Person.objects.create(
            first_name='Wendy', surname="ApprovedAndRemoved")
        self.registration = Register.objects.create(
            person=self.person_approved_and_removed,
            registries_activity=self.activity_drill,
            registration_no="F12345")
        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            current_status=self.status_approved,
            removal_date='2018-01-01',
            subactivity=self.subactivity)
        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            current_status=self.status_approved,
            subactivity=self.subactivity)

    def test_search_all_no_registration(self):
        # We expect a person that has no registration whatsoever to show up when searching for all.
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL'
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_without_registration.surname)

    def test_search_all_no_application(self):
        # We expect a person that has a registration, but no application to show up when searching for all.
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL'
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_without_application.surname)

    def test_search_pending_no_registration(self):
        # We expect a person that has no registrations whatsoever to show up in any
        # pending search.
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_pending.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_without_registration.surname)

    def test_search_pending_no_application(self):
        # We expect a person that has a registration, but no application to show up when searching for all.
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_pending.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_without_application.surname)

    def test_search_pending_with_pending_application(self):
        # We expect a person that has a registration, and a pending application to show up when searching for
        # pending.
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_pending.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_pending.surname)

    def test_search_approved_does_not_return_pending_person(self):
        # Test that when we search for approved person, we don't get pending persons
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_approved.code)
        response = self.client.get(url, format='json')
        self.assertNotContains(response, self.person_pending.surname)
        self.assertNotContains(response, self.person_without_application.surname)
        self.assertNotContains(response, self.person_without_registration.surname)

    def test_search_approved_returns_approved_person(self):
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_approved.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_approved.surname)

    def test_search_approved_does_not_return_removed(self):
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_approved.code)
        response = self.client.get(url, format='json')
        self.assertNotContains(response, self.person_removed.surname)

    def test_search_for_removed_returns_removed(self):
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status=Removed'
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_removed.surname)

    def test_search_for_removed_does_not_return_approved(self):
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status=Removed'
        response = self.client.get(url, format='json')
        self.assertNotContains(response, self.person_approved.surname)

    def test_search_for_not_approved_returns_not_approved(self):
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_not_approved.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_not_approved.surname)

    def test_search_for_not_approved_does_not_return_removed(self):
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_not_approved.code)
        response = self.client.get(url, format='json')
        self.assertNotContains(response, self.person_removed.surname)

    def test_search_for_not_approved_returns_someone_with_approved_and_removed(self):
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status=Removed'
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_approved_and_removed.surname)

    def test_search_approved_returns_someone_with_approved_and_removed(self):
        url = reverse('person-list') + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_approved.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_approved_and_removed.surname)

    def test_person_history_endpoint(self):
        url = reverse('person-history', kwargs={'person_guid': self.person_approved.person_guid})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)