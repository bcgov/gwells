from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from registries.models import Organization, Person

# Note: see postman/newman for more API tests.

class OrganizationTests(APITestCase):
    """
    Tests for the Organization resource endpoint
    """

    def test_create_organization(self):
        """
        Create a new organization object.
        """
        initial_data = {
            'name': 'Bobby\'s Drilling',
            'city': 'Victoria'
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

        retrieve_url = reverse('organization-detail', kwargs={'org_guid': created_guid})

        # Apply a new city name with PATCH method
        self.client.patch(retrieve_url, new_data, format='json')

        response = self.client.get(retrieve_url, format='json')

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

        retrieve_url = reverse('organization-detail', kwargs={'org_guid': created_guid})

        # Apply a new city name with PATCH method
        self.client.put(retrieve_url, new_data, format='json')
        
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])
        self.assertEqual(response.data['city'], new_data['city'])

    def test_delete_organization(self):
        pass


class PersonTests(APITestCase):
    """
    Tests for Person resource endpoint
    """

    created_guid = None

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
        url = reverse('person-list')
        count = Person.objects.count()
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), count)

    def test_retrieve_person(self):
        pass

    def test_patch_person(self):
        pass

    def test_put_person(self):
        pass

    def test_delete_person(self):
        pass
