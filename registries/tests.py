import uuid
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from gwells.models.ProvinceStateCode import ProvinceStateCode
from gwells.models.User import User
from registries.models import Organization, Person
from registries.views import APIPersonListCreateView, APIPersonRetrieveUpdateDestroyView

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

        # Use djangorestframework-jwt to get a valid token for our user.
        # This could fail to work when Keycloak auth is implemented.
        # auth_url = reverse('get-token')
        # testuser_credentials = {
        #     'username': 'testuser',
        #     'password': 'douglas'
        # }

        # self.user = User.objects.create_user(
        #     testuser_credentials['username'],
        #     'test@example.com',
        #     testuser_credentials['password']
        # )

        # token = self.client.post(auth_url, testuser_credentials, format='json').data['token']

        # self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        
        self.user = User.objects.create_user('testuser', 'test@example.com', 'douglas')
        self.client.force_authenticate(self.user)


# Django unit tests

class OrganizationTests(TestCase):
    """
    Tests for the Organization model
    """

    def setUp(self):
        # Create a ProvinceStateCode object for our Organization's foreign key field
        province = ProvinceStateCode.objects.create(
            province_state_code = 'BC',
            description = 'British Columbia',
            display_order = 1
        )

        Organization.objects.create(
            name='Frankie and Betty Well Drilling Co.',
            city='Victoria',
            province_state = province
        )

    def test_organization_was_created(self):
        org = Organization.objects.get(name='Frankie and Betty Well Drilling Co.')
        self.assertEqual(org.city, 'Victoria')


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
            'province_state': province.province_state_guid
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

    # NOTE: Create object by put request is not implemented.
    # def test_create_person_by_put(self):
    #     view = APIPersonRetrieveUpdateDestroyView.as_view()
    #     new_guid = uuid.uuid4()
    #     print(new_guid)
    #     url = reverse('person-detail', kwargs={'person_guid': new_guid})
    #     data = self.initial_data
    #     data['person_guid'] = new_guid

    #     request = self.factory.put(url, data, format='json')
    #     request.user = self.user

    #     response = view(request)

    #     self.assertEqual(response.data['first_name'], self.initial_data['first_name'])
    #     self.assertEqual(Person.objects.get(person_guid=new_guid).first_name, self.initial_data['first_name'])

    def test_delete_person(self):
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

    def test_person_audit_fields(self):
        """
        Test that AuditModel fields (create_user, create_date etc.)
        are updated when Person objects are created.
        """
        view = APIPersonListCreateView.as_view()
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
