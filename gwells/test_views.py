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

from .forms import *
from django.test import TestCase
from django.core.urlresolvers import reverse
from http import HTTPStatus
from .models import *
from .search import Search
from .views import *

#TODO split tests into one file per view

class ViewsTestCase(TestCase):

    well_tag_number = 123

    @classmethod
    def setUpTestData(cls):
        #setup
        prov = ProvinceState.objects.create(sort_order=1)
        prov.save()

        well_class = WellClass.objects.create(sort_order=1)
        well_class.save()

        w = Well.objects.create(well_class=well_class, owner_province_state=prov)
        w.identification_plate_number = 123
        w.well_tag_number = ViewsTestCase.well_tag_number
        w.street_address = '123 Main St.'
        w.legal_plan = '7789'
        w.owner_full_name = 'John Smith'
        w.latitude = 48.413551
        w.longitude = -123.359973
        w.save()

    def setUp(self):
        pass

    def ok(self, view):
        response = self.client.get(reverse(view))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def not_ok(self, view, status):
        response = self.client.get(reverse(view))
        self.assertEqual(response.status_code, status)

    def test_robots_view_ok(self):
        self.ok('robots')

    def test_home_view_ok(self):
        self.ok('home')

    def test_search_view_ok(self):
        self.ok('search')

    def test_search_view_with_no_params(self):
        url = reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_well_detail_no_well(self):
        initial_url = reverse('well_detail', kwargs={'pk':'1'})
        url = initial_url[:-2]
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_well_detail_ok(self):
        wells = Search.well_search(ViewsTestCase.well_tag_number, '', '', '')
        self.assertEqual(wells.count(), 1)

        url = reverse('well_detail', kwargs={'pk':ViewsTestCase.well_tag_number})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_registry_ok(self):
        self.ok('registry')

    def test_activity_activity_submission(self):
        self.ok('activity_submission_list')

    def test_health_ok(self):
        self.ok('health')

    def test_groundwater_information_ok(self):
        self.ok('groundwater_information')

    def test_map_well_search(self):
        self.ok('map_well_search')

    def test_500_not_ok(self):
        self.not_ok('test_500', HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_404_not_ok(self):
        self.not_ok('test_404', HTTPStatus.NOT_FOUND)

    def test_activity_submission_list_ok(self):
        self.ok('activity_submission_list')

    def test_activity_submission_create_ok(self):
        self.ok('activity_submission_create')
