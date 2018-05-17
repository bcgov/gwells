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

from gwells.models import *
from django.test import TestCase
from gwells.search import Search
from django.contrib.auth.models import Group

class SearchTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        prov = ProvinceStateCode.objects.create(display_order=1)
        prov.save()

        well_class = WellClassCode.objects.create(display_order=1)
        well_class.save()

        w = Well.objects.create(well_class=well_class, owner_province_state=prov)
        w.identification_plate_number = 123
        w.street_address = '123 Main St.'
        w.legal_plan = '7789'
        w.owner_full_name = 'John Smith'
        w.latitude = 48.413551
        w.longitude = -123.359973
        w.save()

        w2 = Well.objects.create(well_class=well_class, owner_province_state=prov)
        w2.identification_plate_number = 3456332
        w2.street_address = '555 Government Street'
        w2.legal_district_lot = '789'
        w2.owner_full_name = 'Jane Doe'
        w2.latitude = 48.416088
        w2.longitude = -123.362910
        w2.save()

        w3 = Well.objects.create(well_class=well_class, owner_province_state=prov)
        w3.identification_plate_number = 1
        w3.street_address = '200 Main Street'
        w3.legal_pid = 54321
        w3.owner_full_name = 'Joe Smith'
        w3.latitude = 48.415571
        w3.longitude = -123.364190
        w3.save()

        Group.objects.create(name='admin')

    def test_well_search_well_number(self):
        wells = Search.well_search('1', '', '', '')
        self.assertEqual(wells.count(), 2)


    def test_well_search_address(self):
        wells = Search.well_search('', 'gov', '', '')
        self.assertEqual(wells.count(), 1)


    def test_well_search_legal(self):
        wells = Search.well_search('', '', '78', '')
        self.assertEqual(wells.count(), 2)

    def test_well_search_owner(self):
        wells = Search.well_search('', '', '', 'smi')
        self.assertEqual(wells.count(), 2)


    def test_well_search_well_number_owner(self):
        wells = Search.well_search('123', '', '', 'john')
        self.assertEqual(wells.count(), 1)


    def test_well_search_params_named_positional(self):
        named = Search.well_search(addr='gov')
        positional = Search.well_search('', 'gov', '', '')
        self.assertEqual(named.count(), positional.count())


    def test_well_search_empty_string_params(self):
        wells = Search.well_search('', '', '', '')
        self.assertIsNone(wells)


    def test_well_search_none_params(self):
        wells = Search.well_search(None, None, None, None)
        self.assertIsNone(wells)


    def test_well_search_gps(self):
        """ Check that a bounding box can be specified as search criteria """
        lat_long_box = {'start_corner': '48.418466095707046,-123.36755990982056', 'end_corner': '48.41493417062313,-123.36180925369264'}
        wells = Search.well_search('', '', '', '', lat_long_box)
        self.assertEqual(wells.count(), 2)


    def test_well_search_gps_street(self):
        """ Check that a street address and bounding box can be specified as search criteria """
        lat_long_box = {'start_corner': '48.418466095707046,-123.36755990982056', 'end_corner': '48.41493417062313,-123.36180925369264'}
        wells = Search.well_search('', 'government', '', '', lat_long_box)
        self.assertEqual(wells.count(), 1)
