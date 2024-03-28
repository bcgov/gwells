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
import reversion
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.reverse import reverse

from aquifers.models import Aquifer, AquiferDemand, AquiferMaterial, AquiferProductivity, AquiferResource, AquiferResourceSection, AquiferSubtype, AquiferVulnerabilityCode, QualityConcern, WaterUse
from gwells.settings import REST_FRAMEWORK
from gwells.roles import roles_to_groups, AQUIFERS_EDIT_ROLE, AQUIFERS_VIEWER_ROLE

from aquifers.models.vertical_aquifer_extents import VerticalAquiferExtent, VerticalAquiferExtentsHistory
from aquifers.change_history import get_aquifer_history_diff, get_vertical_aquifer_extents_history
from aquifers.data_migrations import aquifer_vulnerability_codes
from dateutil.parser import parse
from wells.models import Well

from aquifers.serializers_v2 import AquiferDetailSerializerV2


# Create your tests here.


class TestAquiferMappingYearDynamicMaxValueValidator(APITestCase):
    dummy_geom = GEOSGeometry(
        'MULTIPOLYGON(((-5.86333200   8.14347501,   -6.70445600   7.47862301,   -3.44929601   6.28074401,   -3.08375301   3.08165901,   -1.71378401   3.10939901,   -5.86333200   8.14347501)))')
    dummy_aquifer = {'create_user': 'TEST_GWELLS', 'update_user': 'TEST_GWELLS', 'geom': dummy_geom, 'geom_simplified': dummy_geom, 'mapping_year': None }

    def test_create_proper_dated_mapping_year_aquifer(self):
        aquifer = Aquifer.objects.create(**TestAquiferMappingYearDynamicMaxValueValidator.dummy_aquifer)
        aquifer.mapping_year = timezone.now().year
        aquifer.area = 124.5
        aquifer.full_clean()

    def test_create_postdated_mapping_year_aquifer(self):
        with self.assertRaises(ValidationError):
            aquifer = Aquifer.objects.create(**TestAquiferMappingYearDynamicMaxValueValidator.dummy_aquifer)
            aquifer.mapping_year = timezone.now().year + 1
            aquifer.area = 124.5
            aquifer.full_clean()


class TestPostNotAuthenticated(APITestCase):
    def test_not_authenticated_attempts_patch(self):
        url = reverse('aquifer-retrieve-update-v1', kwargs={'aquifer_id': 1})
        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAquifersEditRole(APITestCase):
    def setUp(self):
        roles = [AQUIFERS_EDIT_ROLE]
        for role in roles:
            group = Group(name=role)
            group.save()
        user, _created = User.objects.get_or_create(username='test')
        user.profile.username = user.username
        user.save()
        roles_to_groups(user, roles)
        self.client.force_authenticate(user)
        Aquifer(aquifer_id=1).save()

    def test_patch(self):
        url = reverse('aquifer-retrieve-update-v1', kwargs={'aquifer_id': 1})
        response = self.client.patch(url, {'resources': [{
            'url': '',
        }]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_shapefile(self):

        filepath = 'aquifers/fixtures/shp/shapefile.zip'
        with open(filepath, 'rb') as fh:
            url = reverse('aquifer-save-geometry', kwargs={'aquifer_id': 1, 'version': 'v1'})

            response = self.client.post(
                url,
                {'geometry': fh}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_export_csv(self):
        url = reverse('aquifers-list-csv-v1')
        response = self.client.get(
            url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAquifersSpatial(APITestCase):

    def test_geodjango(self):
        # Currently we're re-directing to a static file.
        url = reverse('aquifer-geojson-v1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_geodjango_bounds(self):
        # Currently we're re-directing to a static file.
        url = reverse('aquifer-geojson-v1')
        response = self.client.get(
            url,
            {
                'realtime': 'true', 'sw_lat': 49, 'sw_long': -125, 'ne_lat': 49, 'ne_long': -124
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestAquiferHistoryDiff(TestCase):
    def setUp(self):
        # Set up test data here
        self.aquifer_demand_code = AquiferDemand.objects.create(
            code='Z',
            description='Low',
            display_order=1
        )
        self.water_use = WaterUse.objects.create(
            code='Z',
            description='Municipal',
            display_order=1
        )
        self.aquifer_productivity_code = AquiferProductivity.objects.create(
            code='Z',
            description='Moderate',
            display_order=1
        )
        self.quality_concern_code = QualityConcern.objects.create(
            code='Z',
            description='Low',
            display_order=1
        )
        self.aquifer_material_code = AquiferMaterial.objects.create(
            code='Z',
            description='Bedrock',
            display_order=1
        )
        self.aquifer_subtype_code = AquiferSubtype.objects.create(
            code='Za',
            description='6a',
            display_order=1
        )
        self.aquifer_vulnerability_code = AquiferVulnerabilityCode.objects.create(
            code='Z',
            description='Moderate',
            display_order=1
        )

        self.aquifer = Aquifer.objects.create(
            aquifer_id=303,
            aquifer_name='Test Aquifer',
            location_description='Test Description',
            area=3.5,
            litho_stratographic_unit='Cenozoic, Tertiary, Miocene and/or Pliocene Epochs',
            mapping_year=2017,
            notes='TestNotes',
            demand=self.aquifer_demand_code,
            known_water_use=self.water_use,
            material=self.aquifer_material_code,
            productivity=self.aquifer_productivity_code,
            quality_concern=self.quality_concern_code,
            subtype=self.aquifer_subtype_code,
            vulnerability=self.aquifer_vulnerability_code,
            geom='0106000020BD0B00000100000001030000000100000006000000FB6591A3052432413E2A8975A7B31D41090C44ACDC273241C45A56B278B21D411AA46EC6F728324150C702C1BBA11D411A0A643CA22732410100ADA5658E1D4133B184D563203241FCF2C2DF13961D41FB6591A3052432413E2A8975A7B31D41',
            geom_simplified='0106000020E61000000100000001030000000100000006000000A4522AFEADD95EC07D7F8003B3AE4840A4522A36D1D85EC07731580B92AE4840A5522A5E9AD85EC07274404E53AD4840A4522A8EF1D85EC06A25DB5BEAAB4840A4522AFE8EDA5EC02320B7448FAC4840A4522AFEADD95EC07D7F8003B3AE4840',
            effective_date=parse('2024-03-19 23:26:25.117394+00'),
            expiry_date=parse('9999-03-19 23:26:25.117394+00'),
            retire_date=parse('9999-03-19 23:26:25.117394+00')
        )
        
        with reversion.create_revision():
            self.aquifer.save()

        with reversion.create_revision():
            self.aquifer.aquifer_name = 'Updated Aquifer Name'
            self.aquifer.save()

        with reversion.create_revision():
            self.aquifer.location_description = 'Updated Location Description'
            self.aquifer.save()

    def test_get_aquifer_history_diff(self):
        # Test the get_aquifer_history_diff function
        history = get_aquifer_history_diff(self.aquifer)
        # Add assertions to check the output of the function
        self.assertIsNotNone(history)
        self.assertEqual(len(history), 3)

class TestVerticalAquiferHistoryDiffTest(TestCase):
    def setUp(self):
        # Foreign keys for vertical aquifer
        self.well = Well.objects.create(
            well_tag_number=304
        )
        self.aquifer = Aquifer.objects.create(
            aquifer_id=303,
            aquifer_name='Test Aquifer',
            location_description='Test Description',
            area=3.5,
            litho_stratographic_unit='Cenozoic, Tertiary, Miocene and/or Pliocene Epochs',
            mapping_year=2017,
            notes='TestNotes',
            geom='0106000020BD0B00000100000001030000000100000006000000FB6591A3052432413E2A8975A7B31D41090C44ACDC273241C45A56B278B21D411AA46EC6F728324150C702C1BBA11D411A0A643CA22732410100ADA5658E1D4133B184D563203241FCF2C2DF13961D41FB6591A3052432413E2A8975A7B31D41',
            geom_simplified='0106000020E61000000100000001030000000100000006000000A4522AFEADD95EC07D7F8003B3AE4840A4522A36D1D85EC07731580B92AE4840A5522A5E9AD85EC07274404E53AD4840A4522A8EF1D85EC06A25DB5BEAAB4840A4522AFE8EDA5EC02320B7448FAC4840A4522AFEADD95EC07D7F8003B3AE4840',
            effective_date=parse('2024-03-19 23:26:25.117394+00'),
            expiry_date=parse('9999-03-19 23:26:25.117394+00'),
            retire_date=parse('9999-03-19 23:26:25.117394+00')
        )

        # Create the vertical aquifer for testing
        self.vertical_aquifer = VerticalAquiferExtent.objects.create(
            id=302,
            aquifer_id=303,
            well=self.well,
            geom='0101000020E6100000EC866D8B32D95EC0A72215C616AE4840',
            start=1.0,
            end=144.00,
        )

        # Register two changes to the aquifer in the vertical aquifer history table
        self.vertical_aquifer_history = VerticalAquiferExtentsHistory.objects.create(
            id=1,
            aquifer_id=303,
            well_tag_number=304,
            geom='0101000020E6100000EC866D8B32D95EC0A72215C616AE4840',
            start=2.0,
            end=144.00,
        )
        self.vertical_aquifer_history = VerticalAquiferExtentsHistory.objects.create(
            id=2,
            aquifer_id=303,
            well_tag_number=304,
            geom='0101000020E6100000EC866D8B32D95EC0A72215C616AE4840',
            start=2.0,
            end=146.00,
        )
        
    def test_get_vertical_aquifer_extents_history(self):
        history = get_vertical_aquifer_extents_history(self.vertical_aquifer)
        self.assertIsNotNone(history)
        self.assertEqual(len(history), 2)

class TestAquiferDetailSerializerV2(TestCase):
    def setUp(self):
        self.aquifer = Aquifer.objects.create(
            aquifer_id=303,
            aquifer_name='Test Aquifer',
            location_description='Test Description',
            area=3.5,
            litho_stratographic_unit='Cenozoic, Tertiary, Miocene and/or Pliocene Epochs',
            mapping_year=2017,
            notes='TestNotes',
            geom='0106000020BD0B00000100000001030000000100000006000000FB6591A3052432413E2A8975A7B31D41090C44ACDC273241C45A56B278B21D411AA46EC6F728324150C702C1BBA11D411A0A643CA22732410100ADA5658E1D4133B184D563203241FCF2C2DF13961D41FB6591A3052432413E2A8975A7B31D41',
            geom_simplified='0106000020E61000000100000001030000000100000006000000A4522AFEADD95EC07D7F8003B3AE4840A4522A36D1D85EC07731580B92AE4840A5522A5E9AD85EC07274404E53AD4840A4522A8EF1D85EC06A25DB5BEAAB4840A4522AFE8EDA5EC02320B7448FAC4840A4522AFEADD95EC07D7F8003B3AE4840',
            effective_date=parse('2024-03-19 23:26:25.117394+00'),
            expiry_date=parse('9999-03-19 23:26:25.117394+00'),
            retire_date=parse('9999-03-19 23:26:25.117394+00')
        )
        self.aquifer_resource_section = AquiferResourceSection.objects.create(code='Z')
        self.aquifer_resource = AquiferResource.objects.create(
            name='Resource 1',
            url='http://example.com',
            section=self.aquifer_resource_section,
            aquifer=self.aquifer
        )
        self.client = APIClient()

    def test_create_aquifer_with_resources(self):
        data = {
            'aquifer_id': 304,
            'aquifer_name': 'New Aquifer',
            'resources': [
                {
                    'url': 'http://example.com',
                    'name': 'New Resource',
                    'section_code': self.aquifer_resource_section.code
                }
            ]
        }
        serializer = AquiferDetailSerializerV2(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        aquifer = serializer.save()
        self.assertEqual(aquifer.aquifer_name, 'New Aquifer')
        self.assertEqual(aquifer.resources.count(), 1)
        self.assertEqual(aquifer.resources.first().url, 'http://example.com')


    def test_update_aquifer_with_resources(self):
        data = {
            'aquifer_id': 303,
            'aquifer_name': 'Updated Aquifer',
            'resources': [
                {
                    'id': self.aquifer_resource.id,
                    'url': 'http://updatedresource.com',
                    'name': 'Updated Resource',
                    'section_code': self.aquifer_resource_section.code
                }
            ]
        }
        serializer = AquiferDetailSerializerV2(instance=self.aquifer, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_aquifer = serializer.save()
        self.assertEqual(updated_aquifer.aquifer_id, 303)
        self.assertEqual(updated_aquifer.aquifer_name, 'Updated Aquifer')
        self.assertEqual(updated_aquifer.resources.count(), 1)
        self.assertEqual(updated_aquifer.resources.first().url, 'http://updatedresource.com')


    def test_invalid_data(self):
        data = {
            'aquifer_id': 303,
            'aquifer_name': 'Test Aquifer',
            'resources': [
                {
                    'url': 'http://example.com',
                    'name': 'Resource 1',
                    'section_id': 1,
                }
            ]
        }
        serializer = AquiferDetailSerializerV2(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('resources', serializer.errors)

    def test_create_aquifer_without_resources(self):
        data = {
            'aquifer_id': 305,
            'aquifer_name': 'Aquifer Without Resources',
        }
        serializer = AquiferDetailSerializerV2(data=data)
        self.assertTrue(serializer.is_valid())
        aquifer = serializer.save()
        self.assertEqual(aquifer.aquifer_name, 'Aquifer Without Resources')
        self.assertEqual(aquifer.resources.count(), 0)


