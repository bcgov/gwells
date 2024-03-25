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
import json
from unittest.mock import patch

from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import GEOSGeometry

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from gwells.settings import REST_FRAMEWORK
from gwells.models import ProvinceStateCode, Profile
from registries.models import (
    ApplicationStatusCode,
    Organization,
    Person,
    RegistriesApplication,
    Register,
    ActivityCode,
    SubactivityCode,
    ProofOfAgeCode)
from registries.views import PersonListView, PersonDetailView
from gwells.roles import (roles_to_groups, REGISTRIES_VIEWER_ROLE, REGISTRIES_EDIT_ROLE)

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
        # Prepare roles in DB ahead of test, to reduce amount of logging during tests.
        roles = [REGISTRIES_EDIT_ROLE, REGISTRIES_VIEWER_ROLE]
        for role in roles:
            group = Group(name=role)
            group.save()

        self.user, created = User.objects.get_or_create(username='testuser')
        self.user.profile.username = self.user.username
        self.user.save()
        roles_to_groups(self.user, roles)
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
        # Get activityCode
        self.activity_drill = ActivityCode.objects.get(registries_activity_code="DRILL")
        # Create new registrations
        # Create registered driller 1
        self.driller = Person.objects.create(
            first_name='Wendy', surname="Well")
        self.registration = Register.objects.create(
            person=self.driller,
            registries_activity=self.activity_drill,
            registration_no="F12345",
        )
        # Get subactivities
        self.subactivity = SubactivityCode.objects.get(registries_subactivity_code='WATER')
        self.subactivity = SubactivityCode.objects.get(registries_subactivity_code='GEOTECH')
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
        self.proof_of_age = ProofOfAgeCode.objects.create(
            code="TESTING",
            description="Testing",
            display_order="1")

        # Application
        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            proof_of_age=self.proof_of_age,
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
                      kwargs={'application_guid': self.app.application_guid, 'version': 'v1'})
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
                      kwargs={'application_guid': self.app.application_guid, 'version': 'v1'})
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
                      kwargs={'application_guid': self.app.application_guid, 'version': 'v1'})
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
            'street_address': '501 Belleville St',
            'city': 'Victoria',
            'province_state': 'BC'
        }

    @patch('registries.serializers.geocode_bc_location')
    def test_create_organization(self, mock_geocode_bc_location):
        """
        Create a new organization object.
        """
        mock_geocode_bc_location.return_value = None
        url = reverse('organization-list', kwargs={'version': 'v1'})
        count_before = Organization.objects.count()

        response = self.client.post(url, self.initial_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), count_before + 1)

    @patch('registries.serializers.geocode_bc_location')
    def test_list_organization(self, mock_geocode_bc_location):
        mock_geocode_bc_location.return_value = None
        url = reverse('organization-list', kwargs={'version': 'v1'})
        new_object = self.client.post(url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(created_guid), 36)
        self.assertContains(response, created_guid)

    @patch('registries.serializers.geocode_bc_location')
    def test_retrieve_organization(self, mock_geocode_bc_location):
        mock_geocode_bc_location.return_value = None
        create_url = reverse('organization-list', kwargs={'version': 'v1'})
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        retrieve_url = reverse('organization-detail',
                               kwargs={'org_guid': created_guid, 'version': 'v1'})
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.initial_data['name'])
        self.assertEqual(response.data['city'], self.initial_data['city'])

    @patch('registries.serializers.geocode_bc_location')
    def test_patch_organization(self, mock_geocode_bc_location):
        mock_geocode_bc_location.return_value = None
        new_data = {
            'city': 'Duncan'
        }

        create_url = reverse('organization-list', kwargs={'version': 'v1'})
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        object_url = reverse('organization-detail',
                             kwargs={'org_guid': created_guid, 'version': 'v1'})

        # Apply a new city name with PATCH method
        self.client.patch(object_url, new_data, format='json')

        response = self.client.get(object_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.initial_data['name'])
        self.assertEqual(response.data['city'], new_data['city'])

    @patch('registries.serializers.geocode_bc_location')
    def test_put_organization(self, mock_geocode_bc_location):
        mock_geocode_bc_location.return_value = None
        new_data = {
            'name': 'Betty\'s Drilling',
            'city': 'Duncan',
            'province_state': 'BC'
        }

        create_url = reverse('organization-list', kwargs={'version': 'v1'})
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        object_url = reverse('organization-detail',
                             kwargs={'org_guid': created_guid, 'version': 'v1'})

        # Apply a new city name with PATCH method
        self.client.put(object_url, new_data, format='json')

        response = self.client.get(object_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])
        self.assertEqual(response.data['city'], new_data['city'])

    @patch('registries.serializers.geocode_bc_location')
    def test_delete_organization(self, mock_geocode_bc_location):
        mock_geocode_bc_location.return_value = None
        # setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        create_url = reverse('organization-list', kwargs={'version': 'v1'})
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        retrieve_url = reverse('organization-detail',
                               kwargs={'org_guid': created_guid, 'version': 'v1'})
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

    @patch('registries.serializers.geocode_bc_location')
    def test_organization_audit_fields(self, mock_geocode_bc_location):
        """
        Test that AuditModel fields (create_user, create_date etc.)
        are updated when Organization objects are created.
        """
        mock_geocode_bc_location.return_value = None
        create_url = reverse('organization-list', kwargs={'version': 'v1'})
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['org_guid']

        retrieve_url = reverse('organization-detail',
                               kwargs={'org_guid': created_guid, 'version': 'v1'})
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # TODO: When authentication is enforced, this line will need to change
        self.assertEqual(response.data['create_user'], self.user.username)

    @patch('registries.serializers.geocode_bc_location')
    def test_create_org_not_authenticated(self, mock_geocode_bc_location):
        """
        Ensure that users who are not authenticated cannot create Organization objects
        """
        mock_geocode_bc_location.return_value = None
        self.client.force_authenticate(user=None)
        url = reverse('organization-list', kwargs={'version': 'v1'})
        data = {'name': 'Big Time Drilling Co'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('registries.serializers.geocode_bc_location')
    def test_unsafe_methods_by_unauthorized_users(self, mock_geocode_bc_location):
        """
        Ensure that users who are not authenticated cannot perform "unsafe" actions
        like UPDATE, PUT, DELETE on an object that is already in database
        """
        mock_geocode_bc_location.return_value = None

        self.client.force_authenticate(user=None)
        org_object = Organization.objects.create(
            name='Big Time Drilling Co', province_state=self.province)
        object_url = reverse('organization-detail',
                             kwargs={'org_guid': org_object.org_guid, 'version': 'v1'})

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
    
    @patch('registries.serializers.geocode_bc_location')
    def test_create_org_no_geom(self, mock_geocode_bc_location):
        """
        When a new Organization is created without an address, the
        geom attribute is not populated
        """
  
        # Note: we use a mock version of mock_geocode_bc_location(..) just in
        # case the create org implementation makes a call to it.  We don't
        # want this test to depend on a remote API.
        mock_geocode_bc_location.return_value = None

        # Create an organization with an initial address
        org_data = {
            "name": "test", 
            "province_state": "BC", 
            "street_address": None
        }
        url = reverse('organization-list', kwargs={'version': 'v1'})        
        response = self.client.post(url, org_data, format='json')

        # check that the response includes the geographic coordinates
        self.assertEquals(response.data.get("longitude"), None)
        self.assertEquals(response.data.get("latitude"), None)

        organization = Organization.objects.get(
            org_guid=response.data['org_guid'])
  
        # check that the organization was created and that is has a value
        # in the geom attribute
        self.assertTrue(organization != None)
        self.assertTrue(organization.geom == None)

    def test_create_update_org_populates_geom_1(self):
        """
        When a new Organization is created with an address in BC, a geometry
        should be automatically populated with the geocoded value.
        When that organization is updated with a different address, the
        geometry should be automatically updated too.
        """
    
        with patch('registries.serializers.geocode_bc_location') as mock_geocode_bc_location_1:

          #create an organization with an initial address
          mock_lon_1 = -124.2
          mock_lat_1 = 50.1
          mock_geocode_bc_location_1.return_value = \
              GEOSGeometry(f'POINT({mock_lon_1} {mock_lat_1})', srid=4326)

          url_1 = reverse('organization-list', kwargs={'version': 'v1'})        
          response_1 = self.client.post(url_1, self.initial_data, format='json')

          # check that the mock geocode function was used instead of the 
          # real version
          mock_geocode_bc_location_1.assert_called_once()

          # check that the response includes the geographic coordinates
          self.assertEquals(response_1.data.get("longitude"), mock_lon_1)
          self.assertEquals(response_1.data.get("latitude"), mock_lat_1)

          organization = Organization.objects.get(
              org_guid=response_1.data['org_guid'])
    
          # check that the organization was created and that is has a value
          # in the geom attribute
          self.assertTrue(organization != None)
          self.assertTrue(organization.geom != None)

        with patch('registries.serializers.geocode_bc_location') as mock_geocode_bc_location_2:

          # update the organization with a new address
          mock_lon_2 = -123.9
          mock_lat_2 = 51.3
          mock_geocode_bc_location_2.return_value = \
              GEOSGeometry(f'POINT({mock_lon_2} {mock_lat_2})', srid=4326)
          
          url_2 = reverse('organization-detail',
              kwargs={'org_guid': response_1.data['org_guid'], 'version': 'v1'})
          response_2 = self.client.patch(url_2, {"street_address": "101 NewAddress Ave."}, format='json')
          
          updated_org = Organization.objects.get(
              org_guid=response_1.data['org_guid'])

          # check that the response includes new geographic coordinates
          self.assertEquals(response_2.data.get("longitude"), mock_lon_2)
          self.assertEquals(response_2.data.get("latitude"), mock_lat_2)

          # check that the updated organization has updated geometry
          self.assertEquals(updated_org.latitude, mock_lat_2)
          self.assertEquals(updated_org.longitude, mock_lon_2)

    def test_create_update_org_populates_geom_2(self):
        """
        When a new Organization is created with an address in BC, a geometry
        should be automatically populated with the geocoded value.
        When that organization is updated with an incomplete address (no city), 
        the geometry should be reset to None
        """
    
        with patch('registries.serializers.geocode_bc_location') as mock_geocode_bc_location_1:

          #create an organization with an initial address
          mock_lon_1 = -124.6
          mock_lat_1 = 50.8
          mock_geocode_bc_location_1.return_value = \
              GEOSGeometry(f'POINT({mock_lon_1} {mock_lat_1})', srid=4326)

          url_1 = reverse('organization-list', kwargs={'version': 'v1'})        
          resp_1 = self.client.post(url_1, self.initial_data, format='json')

          # check that the mock geocode function was used instead of the 
          # real version
          mock_geocode_bc_location_1.assert_called_once()

          # check that the response includes the geographic coordinates
          self.assertEquals(resp_1.data.get("longitude"), mock_lon_1)
          self.assertEquals(resp_1.data.get("latitude"), mock_lat_1)

          organization = Organization.objects.get(
              org_guid=resp_1.data['org_guid'])
    
          # check that the organization was created and that is has a value
          # in the geom attribute
          self.assertTrue(organization != None)
          self.assertTrue(organization.geom != None)

        with patch('registries.serializers.geocode_bc_location') as mock_geocode_bc_location_2:

          # update the organization to unset the 'city'.  
          # Note: use a mock version of the mock_geocode_bc_location(...) function 
          # just in case the the update causes a call to that function 
          # (it may not, but we just want to be sure this test 
          # doesn't depend on a remote API call).
          mock_geocode_bc_location_2.return_value = None
          
          url_2 = reverse('organization-detail',
              kwargs={'org_guid': resp_1.data['org_guid'], 'version': 'v1'})
          resp_2 = self.client.patch(url_2, {"street_address": ""}, format='json')

          updated_organization = Organization.objects.get(
              org_guid=resp_1.data['org_guid'])
         
          # check that the response shows that the lat/lon have been cleared
          self.assertEquals(resp_2.data.get("longitude"), None)
          self.assertEquals(resp_2.data.get("latitude"), None)

          # check that the updated organization has no geometry
          self.assertEquals(updated_organization.latitude, None)
          self.assertEquals(updated_organization.longitude, None)
          self.assertEquals(updated_organization.geom, None)

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
        url = reverse('person-list', kwargs={'version': 'v1'})
        data = {'first_name': 'Bobby', 'surname': 'Driller'}
        count_before = Person.objects.count()

        response = self.client.post(url, data, format='json')
        created_guid = response.data.get('person_guid')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['first_name'], Person.objects.get(
            person_guid=created_guid).first_name)
        self.assertEqual(data['surname'], Person.objects.get(
            person_guid=created_guid).surname)
        self.assertEqual(Person.objects.count(), count_before + 1)

    def test_list_people(self):
        url = reverse('person-list', kwargs={'version': 'v1'})
        new_object = self.client.post(url, self.initial_data, format='json')
        created_guid = new_object.data['person_guid']

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(created_guid), 36)
        self.assertContains(response, created_guid)

    def test_list_people_within_bbox(self):
        """
        Tests that the "within" parameter causes the backend to limit results to
        within the specified GeoJSON geometry
        """
        
        surname_of_person_in_victoria = "One"

        #register one person and their organization
        activity = ActivityCode.objects.get(registries_activity_code="DRILL")
        person_1 = Person.objects.create(
            first_name='Person', surname=surname_of_person_in_victoria)
        org_1 = Organization.objects.create(
            name="Victoria Drilling Company",
            province_state=self.prov,
            geom=GEOSGeometry('POINT(-123.35948 48.4268161)', srid=4326) #near Victoria, BC
        )
        Register.objects.create(
            person=person_1,
            organization=org_1,
            registries_activity=activity,
            registration_no="F54321",
        )

        #register another person and their organization
        person_2 = Person.objects.create(
            first_name='Person', surname="Two")
        org_2 = Organization.objects.create(
            name="Kelowna Drilling Company",
            province_state=self.prov,
            geom=GEOSGeometry('POINT(-119.47901 49.882042)', srid=4326) #near Kelowna, BC
        )
        Register.objects.create(
            person=person_2,
            organization=org_2,
            registries_activity=activity,
            registration_no="F62232",
        )
        


        # Search for drillers near Victoria.  expect one result.
        url = reverse('person-list', kwargs={'version': 'v1'})
        search_params = {
          'sw_long': -123.40253945033623,
          'sw_lat': 48.40057269436966,
          'ne_long': -123.26195857741126,
          'ne_lat': 48.47868009861898              
          }
        response = self.client.get(url, search_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get("results")
        self.assertEqual(len(results), 1)

        surname = results[0].get("surname")
        self.assertEqual(surname, surname_of_person_in_victoria)

    def test_list_people_filtered_by_subactivity(self):
        """
        Tests that the "subactivities" query string param causes search results to 
        be limited to people registered only for those subactivities
        """
        
        proof_of_age = ProofOfAgeCode.objects.create(
            code="TESTING",
            description="Testing",
            display_order="1")

        #register one person and their organization
        activity = ActivityCode.objects.get(registries_activity_code="DRILL")
        person_1 = Person.objects.create(
            first_name='Person', surname="One")
        org_1 = Organization.objects.create(
            name="Drilling Company A",
            province_state=self.prov
        )
        registration_1 = Register.objects.create(
            person=person_1,
            organization=org_1,
            registries_activity=activity,
            registration_no="F54321",
        )
        RegistriesApplication.objects.create(
            registration=registration_1,
            proof_of_age=proof_of_age,
            subactivity=SubactivityCode.objects.get(registries_subactivity_code='WATER')
        )

        #register another person and their organization
        person_2 = Person.objects.create(
            first_name='Person', surname="Two")
        org_2 = Organization.objects.create(
            name="Drilling Company B",
            province_state=self.prov
        )
        registration_2 = Register.objects.create(
            person=person_2,
            organization=org_2,
            registries_activity=activity,
            registration_no="F62232",
        )
        RegistriesApplication.objects.create(
            registration=registration_2,
            proof_of_age=proof_of_age,
            subactivity=SubactivityCode.objects.get(registries_subactivity_code='GEOTECH')
        )
        

        # Search for drillers with subactivity 'GEOTECH'
        url = reverse('person-list', kwargs={'version': 'v1'})
        search_params = {
          'subactivities': "GEOTECH"    
          }
        response = self.client.get(url, search_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get("results")
        self.assertEqual(len(results), 1)


        subactivity = results[0].get("registrations")[0].get("applications")[0].get("subactivity")
        self.assertEqual(subactivity.get("registries_subactivity_code"), "GEOTECH")        
        

    def test_list_people_includes_org_coords(self):
        """
        Tests that latitude and longitude attributes are included in 
        each embedded Organization 
        (Person -> Registration -> Organization -> [latitude and longitude])
        """
        # Create registered driller linked to an organization
        activity = ActivityCode.objects.get(registries_activity_code="DRILL")
        driller = Person.objects.create(
            first_name='Debbie', surname="Driller")
        org = Organization.objects.create(
            name="Big Time Drilling Company",
            province_state=self.prov
        )
        Register.objects.create(
            person=driller,
            organization=org,
            registries_activity=activity,
            registration_no="F54321",
        )

        # list all people
        url = reverse('person-list', kwargs={'version': 'v1'})
        response = self.client.get(url, format='json')

        # Check that the Organization embedded under the Person has latitude 
        # and longitude attributes (although the values for both are None)
        results = response.data.get("results")            
        registrations = results[0].get("registrations")
        registered_org = registrations[0].get("organization")

        self.assertTrue("latitude" in registered_org)
        self.assertTrue("longitude" in registered_org)
        self.assertTrue(registered_org["latitude"] == None)
        self.assertTrue(registered_org["longitude"] == None)


    def test_retrieve_person(self):
        create_url = reverse('person-list', kwargs={'version': 'v1'})
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['person_guid']

        retrieve_url = reverse(
            'person-detail', kwargs={'person_guid': created_guid, 'version': 'v1'})
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

        create_url = reverse('person-list', kwargs={'version': 'v1'})
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['person_guid']

        object_url = reverse(
            'person-detail', kwargs={'person_guid': created_guid, 'version': 'v1'})

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

        create_url = reverse('person-list', kwargs={'version': 'v1'})
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['person_guid']

        object_url = reverse(
            'person-detail', kwargs={'person_guid': created_guid, 'version': 'v1'})

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

        create_url = reverse('person-list', kwargs={'version': 'v1'})
        new_object = self.client.post(
            create_url, self.initial_data, format='json')
        created_guid = new_object.data['person_guid']

        retrieve_url = reverse(
            'person-detail', kwargs={'person_guid': created_guid, 'version': 'v1'})
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
        post_url = reverse('person-list', kwargs={'version': 'v1'})
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
        post_url = reverse('person-list', kwargs={'version': 'v1'})
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
        url = reverse('person-list', kwargs={'version': 'v1'})
        data = {'first_name': 'Bobby', 'surname': 'Driller'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_wrong_role(self):
        user, created = User.objects.get_or_create(username='test_viewer')
        if created:
            Profile.objects.get_or_create(user=user)

        roles_to_groups(user, [REGISTRIES_VIEWER_ROLE, ])
        self.client.force_authenticate(user=user)
        url = reverse('person-list', kwargs={'version': 'v1'})
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
            'person-detail', kwargs={'person_guid': person_object.person_guid, 'version': 'v1'})

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
        self.activity_drill = ActivityCode.objects.get(registries_activity_code="DRILL")
        self.activity_pump = ActivityCode.objects.get(registries_activity_code="PUMP")
        self.subactivity_pump = SubactivityCode.objects.get(registries_subactivity_code='PUMPINST')
        self.proof_of_age = ProofOfAgeCode.objects.create(
            code="TESTING",
            description="Testing",
            display_order="1")
        # Create registered driller 1
        self.driller = Person.objects.create(
            first_name='Wendy', surname="Well")
        self.registration = Register.objects.create(
            person=self.driller,
            registries_activity=self.activity_drill,
            registration_no="F12345",
        )
        self.subactivity = SubactivityCode.objects.get(registries_subactivity_code='WATER')

        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            proof_of_age=self.proof_of_age,
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
            proof_of_age=self.proof_of_age,
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
            proof_of_age=self.proof_of_age,
            subactivity=self.subactivity)

        # create a company with no registered driller
        self.company_with_no_driller = Organization.objects.create(
            name="Big Time Drilling Company",
            province_state=self.province)

        # driller approved for one activity, removed for another
        self.partially_approved_driller = Person.objects.create(
            first_name="Billy", surname="Partially Approved"
        )
        self.partially_approved_drill_registration = Register.objects.create(
            person=self.partially_approved_driller,
            registries_activity=self.activity_drill,
            registration_no="P9999999"
        )
        self.partially_approved_drill_app = RegistriesApplication.objects.create(
            registration=self.partially_approved_drill_registration,
            proof_of_age=self.proof_of_age,
            current_status=self.status_inactive,
            subactivity=self.subactivity
        )
        self.partially_approved_pump_registration = Register.objects.create(
            person=self.partially_approved_driller,
            registries_activity=self.activity_pump,
            registration_no="P9999991"
        )
        self.partially_approved_drill_app = RegistriesApplication.objects.create(
            registration=self.partially_approved_pump_registration,
            proof_of_age=self.proof_of_age,
            current_status=self.status_active,
            subactivity=self.subactivity_pump
        )

    def test_user_cannot_see_unregistered_person_in_list(self):
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?activity=DRILL'
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['results']), 2)
        self.assertContains(response, 'Wendy')
        self.assertContains(response, 'Debbie')

        # Johnny is in database but is not registered, so make sure he's not in the publicly available list.
        self.assertNotContains(response, 'Johnny')
        self.assertNotContains(response, self.unregistered_driller.person_guid)
        self.assertNotContains(response, self.partially_approved_driller.person_guid)

    def test_user_cannot_retrieve_unregistered_person(self):
        """ unauthorized request to person detail view. Note: now always returns 401 if not staff. """

        # setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        url = reverse(
            'person-detail', kwargs={'person_guid': self.unregistered_driller.person_guid, 'version': 'v1'})
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
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?activity=DRILL&search=' + self.driller.first_name
        response = self.client.get(url, format='json')

        self.assertContains(response, self.driller.first_name)
        self.assertContains(response, self.driller.person_guid)
        self.assertNotContains(response, self.driller2.first_name)
        self.assertNotContains(response, 'Johnny')
        self.assertNotContains(response, self.driller2.person_guid)
        self.assertNotContains(response, self.unregistered_driller.person_guid)
        self.assertNotContains(response, self.partially_approved_driller.person_guid)

    def test_search_for_registration_number(self):
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?activity=DRILL&search=' + \
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
                      kwargs={'org_guid': self.company_with_no_driller.org_guid, 'version': 'v1'})
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
        url = reverse('person-list', kwargs={'version': 'v1'})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # teardown
        logger.setLevel(previous_level)


class TestPublicSearch(TestCase):

    def setUp(self):
        super().setUp()
        self.activity_drill = ActivityCode.objects.get(registries_activity_code="DRILL")
        self.status_pending = ApplicationStatusCode.objects.create(
            code="P",
            description="Pending",
            display_order="2")
        self.status_approved = ApplicationStatusCode.objects.create(
            code="A",
            description="Approved",
            display_order="3")
        self.proof_of_age = ProofOfAgeCode.objects.create(
            code="TESTING",
            description="Testing",
            display_order="1")

        # Get subactivities
        self.subactivity = SubactivityCode.objects.get(registries_subactivity_code='WATER')
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
            proof_of_age=self.proof_of_age,
            current_status=self.status_approved,
            subactivity=self.subactivity)
        RegistriesApplication.objects.create(
            registration=self.registration,
            proof_of_age=self.proof_of_age,
            current_status=self.status_pending,
            subactivity=self.subactivity)
        RegistriesApplication.objects.create(
            registration=self.registration,
            proof_of_age=self.proof_of_age,
            current_status=self.status_approved,
            removal_date='2018-01-01',
            subactivity=self.subactivity)

    def test_search_only_returns_approved(self):
        # Test that when searching, only the active applications are returned.
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status=Removed'
        response = self.client.get(url, format='json')
        # We expect no pending records to have been returned.
        self.assertNotContains(response, 'Pending')
        # We expect only one Approved record, as the other record has a removal_date.
        # The word approved appears twice. Once in the current_status and once in the display status.
        self.assertContains(response, 'Approved', 2)


class TestAuthenticatedSearch(AuthenticatedAPITestCase):

    def setUp(self):
        super().setUp()
        self.activity_drill = ActivityCode.objects.get(registries_activity_code="DRILL")
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
        self.proof_of_age = ProofOfAgeCode.objects.create(
            code="TESTING",
            description="Testing",
            display_order="1")

        # Get subactivities
        self.subactivity = SubactivityCode.objects.get(registries_subactivity_code='WATER')
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
            proof_of_age=self.proof_of_age,
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
            proof_of_age=self.proof_of_age,
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
            proof_of_age=self.proof_of_age,
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
            proof_of_age=self.proof_of_age,
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
            proof_of_age=self.proof_of_age,
            current_status=self.status_approved,
            removal_date='2018-01-01',
            subactivity=self.subactivity)
        self.app = RegistriesApplication.objects.create(
            registration=self.registration,
            proof_of_age=self.proof_of_age,
            current_status=self.status_approved,
            subactivity=self.subactivity)

    def test_search_all_no_registration(self):
        # We expect a person that has no registration whatsoever to show up when searching for all.
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL'
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_without_registration.surname)

    def test_search_all_no_application(self):
        # We expect a person that has a registration, but no application to show up when searching for all.
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL'
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_without_application.surname)

    def test_search_pending_no_registration(self):
        # We expect a person that has no registrations whatsoever to show up in any
        # pending search.
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_pending.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_without_registration.surname)

    def test_search_pending_no_application(self):
        # We expect a person that has a registration, but no application to show up when searching for all.
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_pending.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_without_application.surname)

    def test_search_pending_with_pending_application(self):
        # We expect a person that has a registration, and a pending application to show up when searching for
        # pending.
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_pending.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_pending.surname)

    def test_search_approved_does_not_return_pending_person(self):
        # Test that when we search for approved person, we don't get pending persons
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_approved.code)
        response = self.client.get(url, format='json')
        self.assertNotContains(response, self.person_pending.surname)
        self.assertNotContains(response, self.person_without_application.surname)
        self.assertNotContains(response, self.person_without_registration.surname)

    def test_search_approved_returns_approved_person(self):
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_approved.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_approved.surname)

    def test_search_approved_does_not_return_removed(self):
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_approved.code)
        response = self.client.get(url, format='json')
        self.assertNotContains(response, self.person_removed.surname)

    def test_search_for_removed_returns_removed(self):
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status=Removed'
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_removed.surname)

    def test_search_for_removed_does_not_return_approved(self):
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status=Removed'
        response = self.client.get(url, format='json')
        self.assertNotContains(response, self.person_approved.surname)

    def test_search_for_not_approved_returns_not_approved(self):
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_not_approved.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_not_approved.surname)

    def test_search_for_not_approved_does_not_return_removed(self):
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_not_approved.code)
        response = self.client.get(url, format='json')
        self.assertNotContains(response, self.person_removed.surname)

    def test_search_for_not_approved_returns_someone_with_approved_and_removed(self):
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status=Removed'
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_approved_and_removed.surname)

    def test_search_approved_returns_someone_with_approved_and_removed(self):
        url = reverse('person-list', kwargs={'version': 'v1'}) + '?search=&limit=10&activity=DRILL&status={}'.format(
            self.status_approved.code)
        response = self.client.get(url, format='json')
        self.assertContains(response, self.person_approved_and_removed.surname)

    def test_person_history_endpoint(self):
        url = reverse('person-history', kwargs={'person_guid': self.person_approved.person_guid, 'version': 'v1'})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
