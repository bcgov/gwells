import uuid
import logging
import os
from django.urls import reverse
from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from gwells.models.ProvinceStateCode import ProvinceStateCode
from django.contrib.auth.models import User
from registries.models import Organization, Person, RegistriesApplication, Register, RegistriesStatusCode, ActivityCode
from registries.views import PersonListView, PersonDetailView
from django.contrib.auth.models import Group

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
        """
        Set up authenticated test cases.
        """

        self.user = User.objects.create_user('testuser', 'test@example.com', 'douglas')
        self.user.is_staff = True
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
            province_state_code = 'BC',
            description = 'British Columbia',
            display_order = 1
        )

        self.org = Organization.objects.create(
            name='Frankie and Betty Well Drilling Co.',
            city='Victoria',
            province_state = self.province
        )

    def test_organization_was_created(self):
        org = Organization.objects.get(name='Frankie and Betty Well Drilling Co.')
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


# Django REST Framework tests

class APIOrganizationTests(AuthenticatedAPITestCase):
    """
    Tests for requests to the Organization resource endpoint

    Includes tests for create, list, update (patch and put), and delete
    """

    def test_create_organization(self):
        """
        Create a new organization object.
        """

        # create a ProvinceStateCode object
        province = ProvinceStateCode.objects.create(
            province_state_code = 'BC',
            description = 'British Columbia',
            display_order = 1
        )

        initial_data = {
            'name': 'Bobby\'s Drilling',
            'city': 'Victoria',
            'province_state': province.province_state_code
        }

        url = reverse('organization-list')
        count_before = Organization.objects.count()

        response = self.client.post(url, initial_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), count_before + 1)

    def test_list_organization(self):
        initial_data = {
            'name': 'Bobby\'s Drilling',
            'city': 'Victoria'
        }
        url = reverse('organization-list')
        new_object = self.client.post(url, initial_data, format='json')
        created_guid = new_object.data['org_guid']

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(created_guid), 36)
        self.assertContains(response, created_guid)

    def test_retrieve_organization(self):
        initial_data = {
            'name': 'Bobby\'s Drilling',
            'city': 'Victoria'
        }

        create_url = reverse('organization-list')
        new_object = self.client.post(create_url, initial_data, format='json')
        created_guid = new_object.data['org_guid']

        retrieve_url = reverse('organization-detail', kwargs={'org_guid': created_guid})
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], initial_data['name'])
        self.assertEqual(response.data['city'], initial_data['city'])

    def test_patch_organization(self):
        initial_data = {
            'name': 'Bobby\'s Drilling',
            'city': 'Victoria'
        }
        new_data = {
            'city': 'Duncan'
        }

        create_url = reverse('organization-list')
        new_object = self.client.post(create_url, initial_data, format='json')
        created_guid = new_object.data['org_guid']

        object_url = reverse('organization-detail', kwargs={'org_guid': created_guid})

        # Apply a new city name with PATCH method
        self.client.patch(object_url, new_data, format='json')

        response = self.client.get(object_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], initial_data['name'])
        self.assertEqual(response.data['city'], new_data['city'])

    def test_put_organization(self):
        initial_data = {
            'name': 'Bobby\'s Drilling',
            'city': 'Victoria'
        }
        new_data = {
            'name': 'Betty\'s Drilling',
            'city': 'Duncan'
        }

        create_url = reverse('organization-list')
        new_object = self.client.post(create_url, initial_data, format='json')
        created_guid = new_object.data['org_guid']

        object_url = reverse('organization-detail', kwargs={'org_guid': created_guid})

        # Apply a new city name with PATCH method
        self.client.put(object_url, new_data, format='json')

        response = self.client.get(object_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])
        self.assertEqual(response.data['city'], new_data['city'])

    def test_delete_organization(self):
        #setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        initial_data = {
            'name': 'Bobby\'s Drilling',
            'city': 'Victoria'
        }

        create_url = reverse('organization-list')
        new_object = self.client.post(create_url, initial_data, format='json')
        created_guid = new_object.data['org_guid']

        retrieve_url = reverse('organization-detail', kwargs={'org_guid': created_guid})
        retrieve_response = self.client.get(retrieve_url, format='json')

        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.data['name'], initial_data['name'])
        self.assertEqual(retrieve_response.data['city'], initial_data['city'])

        delete_response = self.client.delete(retrieve_url, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        get_after_delete_response = self.client.get(retrieve_url, format='json')
        self.assertEqual(get_after_delete_response.status_code, status.HTTP_404_NOT_FOUND)

        #teardown
        logger.setLevel(previous_level)

    def test_organization_audit_fields(self):
        """
        Test that AuditModel fields (create_user, create_date etc.)
        are updated when Organization objects are created.
        """
        initial_data = {
            'name': 'Bobby\'s Drilling',
            'city': 'Victoria'
        }

        create_url = reverse('organization-list')
        new_object = self.client.post(create_url, initial_data, format='json')
        created_guid = new_object.data['org_guid']

        retrieve_url = reverse('organization-detail', kwargs={'org_guid': created_guid})
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
        org_object = Organization.objects.create(name='Big Time Drilling Co')
        object_url = reverse('organization-detail', kwargs={'org_guid':org_object.org_guid})

        update_response = self.client.patch(object_url, {'name':'Small Time Drilling Company'}, format='json')
        put_response = self.client.put(
            object_url,
            {
                'org_guid':org_object.org_guid,
                'name':'Small Time Drilling Company',
            },
            format='json'
        )
        delete_response = self.client.delete(object_url, format='json')

        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)


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
        super().setUp()

    def test_create_person(self):
        url = reverse('person-list')
        data = {'first_name': 'Bobby', 'surname': 'Driller'}
        count_before = Person.objects.count()

        response = self.client.post(url, data, format='json')
        created_guid = response.data['person_guid']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['first_name'], Person.objects.get(person_guid=created_guid).first_name)
        self.assertEqual(data['surname'], Person.objects.get(person_guid=created_guid).surname)
        self.assertEqual(Person.objects.count(), count_before + 1)

    def test_list_people(self):
        initial_data = {
            'first_name': 'Bobby',
            'surname': 'Driller'
        }
        url = reverse('person-list')
        new_object = self.client.post(url, initial_data, format='json')
        created_guid = new_object.data['person_guid']

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(created_guid), 36)
        self.assertContains(response, created_guid)

    def test_retrieve_person(self):
        initial_data = {
            'first_name': 'Bobby',
            'surname': 'Driller'
        }

        create_url = reverse('person-list')
        new_object = self.client.post(create_url, initial_data, format='json')
        created_guid = new_object.data['person_guid']

        retrieve_url = reverse('person-detail', kwargs={'person_guid': created_guid})
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], initial_data['first_name'])
        self.assertEqual(response.data['surname'], initial_data['surname'])

    def test_patch_person(self):
        initial_data = {
            'first_name': 'Bobby',
            'surname': 'Driller'
        }
        new_data = {
            'surname': 'Wells'
        }

        create_url = reverse('person-list')
        new_object = self.client.post(create_url, initial_data, format='json')
        created_guid = new_object.data['person_guid']

        object_url = reverse('person-detail', kwargs={'person_guid': created_guid})

        # Apply a new city name with PATCH method
        self.client.patch(object_url, new_data, format='json')

        response = self.client.get(object_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], initial_data['first_name'])
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
        new_object = self.client.post(create_url, initial_data, format='json')
        created_guid = new_object.data['person_guid']

        object_url = reverse('person-detail', kwargs={'person_guid': created_guid})

        # Apply a new name with PATCH method
        self.client.put(object_url, new_data, format='json')

        response = self.client.get(object_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], new_data['first_name'])
        self.assertEqual(response.data['surname'], new_data['surname'])

    def test_delete_person(self):
        #setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        initial_data = {
            'first_name': 'Bobby',
            'surname': 'Driller'
        }

        create_url = reverse('person-list')
        new_object = self.client.post(create_url, initial_data, format='json')
        created_guid = new_object.data['person_guid']

        retrieve_url = reverse('person-detail', kwargs={'person_guid': created_guid})
        retrieve_response = self.client.get(retrieve_url, format='json')

        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.data['first_name'], initial_data['first_name'])
        self.assertEqual(retrieve_response.data['surname'], initial_data['surname'])

        delete_response = self.client.delete(retrieve_url, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        get_after_delete_response = self.client.get(retrieve_url, format='json')
        self.assertEqual(get_after_delete_response.status_code, status.HTTP_404_NOT_FOUND)

        #teardown
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

    def test_create_person_not_authenticated(self):
        """
        Ensure that users who are not authenticated cannot create Person objects
        """
        self.client.force_authenticate(user=None)
        url = reverse('person-list')
        data = {'first_name': 'Bobby', 'surname': 'Driller'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unsafe_methods_by_unauthorized_users(self):
        """
        Ensure that users who are not authenticated cannot perform "unsafe" actions
        like UPDATE, PUT, DELETE on an object that is already in database
        """
        self.client.force_authenticate(user=None)
        person_object = Person.objects.create(first_name='Bobby', surname='Driller')
        object_url = reverse('person-detail', kwargs={'person_guid':person_object.person_guid})

        update_response = self.client.patch(object_url, {'first_name':'Billy'}, format='json')
        put_response = self.client.put(
            object_url,
            {
                'person_guid':person_object.person_guid,
                'first_name':'Betty',
                'surname':'McDrillerson'
            },
            format='json'
        )
        delete_response = self.client.delete(object_url, format='json')

        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

class APIFilteringPaginationTests(APITestCase):
    """
    Tests of the filtering, searching and pagination systems.
    Filtering tests include filtering out results if user is anonymous.
    """

    def setUp(self):
        self.status_active = RegistriesStatusCode.objects.create(code="ACTIVE", description="active", display_order="1")
        self.status_inactive = RegistriesStatusCode.objects.create(code="INACTIVE", description="inactive", display_order="2")
        self.activity_drill = ActivityCode.objects.create(code="DRILL", description="driller", display_order="1")
        self.activity_pump = ActivityCode.objects.create(code="PUMP", description="pump installer", display_order="2")

        # Create registered driller 1
        self.driller = Person.objects.create(first_name='Wendy', surname="Well")
        self.app = RegistriesApplication.objects.create(person=self.driller)
        self.registration = Register.objects.create(
            status=self.status_active,
            registries_application=self.app,
            registries_activity=self.activity_drill,
            registration_no="F12345",
        )

        # Create registered driller 2
        self.driller2 = Person.objects.create(first_name='Debbie', surname="Driller")
        self.app2 = RegistriesApplication.objects.create(person=self.driller2)
        self.registration2 = Register.objects.create(
            status=self.status_active,
            registries_application=self.app2,
            registries_activity=self.activity_drill,
            registration_no="F54321",
        )

        # Create unregistered driller
        self.unregistered_driller = Person.objects.create(first_name="Johnny", surname="Unregistered")

        # Create inactive driller
        self.inactive_driller = Person.objects.create(first_name="Billy", surname="Retired")
        self.retired_app = RegistriesApplication.objects.create(person=self.inactive_driller)
        self.retired_registration = Register.objects.create(
            status=self.status_inactive,
            registries_application=self.retired_app,
            registries_activity=self.activity_drill,
            registration_no="R55555"
        )

        # create a company with no registered driller
        self.company_with_no_driller = Organization.objects.create(name="Big Time Drilling Company")

    def test_user_cannot_see_unregistered_person_in_list(self):
        url = reverse('person-list')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 2)
        self.assertContains(response, 'Wendy')
        self.assertContains(response, 'Debbie')
        self.assertNotContains(response, 'Johnny')
        self.assertNotContains(response, self.unregistered_driller.person_guid)

    def test_user_cannot_retrieve_unregistered_person(self):
        #setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        url = reverse('person-detail', kwargs={'person_guid':self.unregistered_driller.person_guid})
        response = self.client.get(url, format='json')
        person = Person.objects.get(person_guid=self.unregistered_driller.person_guid)

        self.assertEqual(person.first_name, 'Johnny')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        #teardown
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
        url = reverse('person-list') + '?search=' + self.registration2.registration_no
        response = self.client.get(url, format='json')

        self.assertContains(response, self.driller2.first_name)
        self.assertContains(response, self.driller2.person_guid)
        self.assertNotContains(response, self.driller.first_name)
        self.assertNotContains(response, 'Johnny')
        self.assertNotContains(response, self.driller.person_guid)
        self.assertNotContains(response, self.unregistered_driller.person_guid)

    def test_anon_user_cannot_see_unregistered_organization(self):
        #setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        self.client.force_authenticate(user=None)
        url = reverse('organization-detail', kwargs={'org_guid':self.company_with_no_driller.org_guid})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        #teardown
        logger.setLevel(previous_level)

# class FixtureOrganizationTests(AuthenticatedAPITestCase):
#     """
#     Tests for the API organization resource endpoint using fake data fixtures
#     """
#     fixtures = ['registries/fixtures/registries.json']

#     def test_duplicated_entries(self):
#         # use anonymous user for this test. Anonymous user filtering is more complex
#         self.client.force_authenticate(user=None)
#         url = reverse('organization-list') + '?limit=100'
#         response = self.client.get(url, format='json')

#         company_set = set()
#         for item in response.data['results']:
#             company_set.add(item['org_guid'])
#         self.assertEqual(len(company_set), len(response.data['results']))

#     def test_duplicated_entries_admin(self):
#         # using test user
#         url = reverse('organization-list') + '?limit=100'
#         response = self.client.get(url, format='json')

#         # add the list of org_guids in the results to a set. A set will not contain duplicates
#         # so if the set has fewer items than the list, then the list has duplicates.
#         company_set = set()
#         for item in response.data['results']:
#             company_set.add(item['org_guid'])
#         self.assertEqual(len(company_set), len(response.data['results']))

#     def test_pagination_max_page_size(self):
#         # using test user
#         url = reverse('organization-list') + '?limit=500'
#         response = self.client.get(url, format='json')

#         # assert that we have enough records to hit the limit
#         # note: this will cause a test failure if we don't have enough records in the database
#         self.assertGreater(response.data['count'], len(response.data['results']))

#         # max_limit comes from class APILimitOffsetPagination in views.py
#         self.assertEqual(len(response.data['results']), 100)


# class FixturePersonTests(AuthenticatedAPITestCase):
#     """
#     Tests for the API Person resource endpoint using fake data fixtures
#     """
#     fixtures = ['registries/fixtures/registries.json']

#     def test_duplicated_person_entries_anon_user(self):
#         # use anonymous user
#         self.client.force_authenticate(user=None)
#         url = reverse('person-list') + '?limit=100'
#         response = self.client.get(url, format='json')

#         person_set = set()
#         for item in response.data['results']:
#             person_set.add(item['person_guid'])
#         self.assertEqual(len(person_set), len(response.data['results']))

#     def test_duplicated_person_entries_admin_user(self):
#         # use test user
#         url = reverse('person-list') + '?limit=100'
#         response = self.client.get(url, format='json')

#         person_set = set()
#         for item in response.data['results']:
#             person_set.add(item['person_guid'])
#         self.assertEqual(len(person_set), len(response.data['results']))

#     def test_fields_returned(self):
#         self.client.force_authenticate(user=None)
#         url = reverse('person-list')
#         response = self.client.get(url, format='json')

#         for item in response.data['results']:
#             fields = [
#             'person_guid',
#             'first_name',
#             'surname',
#             'organization_name',
#             'street_address',
#             'province_state',
#             'city',
#             'contact_tel',
#             'contact_email',
#             'activity',
#             'status',
#             'registration_no',
#             ]

#             wrong_fields = [
#                 'created_user',
#                 'created_date',
#                 'asdf',
#                 'companies',
#                 'applications'
#             ]

#             for field in fields:
#                 self.assertEqual(field in item, True)

#             for wrong_field in wrong_fields:
#                 self.assertEqual(wrong_field in item, False)

#             for key in item.keys():
#                 self.assertEqual(key in fields, True)

#     def test_search_response(self):
#         url = reverse('person-list')
#         response = self.client.get(url, format='json', search='ann')

#         # looking for errors (misconfigured search, filters etc)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_filter_response_city(self):
#         url = reverse('person-list') + '?city=Atlin'
#         response = self.client.get(url, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 1)

#     def test_filter_response_status(self):
#         url = reverse('person-list') + '?status=ACTIVE'
#         response = self.client.get(url, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_filter_response_status_with_invalid_code(self):
#         url = reverse('person-list') + '?status=NOT_A_REAL_STATUS'
#         response = self.client.get(url, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_filter_response_province(self):
#         url = reverse('person-list') + '?prov=BC'
#         response = self.client.get(url, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_filter_response_province_and_city(self):
#         url = reverse('person-list') + '?prov=BC&city=Atlin'
#         response = self.client.get(url, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_filter_response_city_invalid_province(self):
#         url = reverse('person-list') + '?prov=ZZ&city=Atlin'
#         response = self.client.get(url, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 0)

#     def test_filter_response_city_invalid_province_status(self):
#         url = reverse('person-list') + '?prov=ZZ&city=Atlin&status=ACTIVE'
#         response = self.client.get(url, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 0)

#     def test_filter_response_city_province_status_activity(self):
#         url = reverse('person-list') + '?prov=BC&city=Atlin&status=ACTIVE&activity=DRILL'
#         response = self.client.get(url, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_filter_response_invalid_activity(self):
#         url = reverse('person-list') + '?prov=BC&city=Atlin&status=ACTIVE&activity=asdf'
#         response = self.client.get(url, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 0)

#     def test_cities_search(self):
#         url = reverse('person-list') + '?city=Atlin,Cedarvale'
#         response = self.client.get(url, format='json')

#         self.assertEqual(len(response.data['results']), 2)

#     def test_cities_search_with_spaces(self):
#         url = reverse('person-list') + '?city=Atlin,Cedarvale,Lake Windermere'
#         response = self.client.get(url, format='json')

#         self.assertEqual(len(response.data['results']), 3)
