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

    fixtures = ['views_test_case']

    well_tag_number = 123

    @classmethod
    def setUpTestData(cls):
        pass

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
        self.ok('registry-legacy')

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

    def test_auth_enforced_no_access(self):
        response = self.client.get(reverse('logout_view')) #logout
        response = self.client.get(reverse('activity_submission_create'))
        print('response.url: ', response.url)
        self.assertNotEqual(response.url, '/gwells/submission/create') #not passed through to create form
        self.assertEqual(response.url, '/openid/openid/KeyCloak?next=/gwells/submission/create') #redirected to login

#    def test_activity_submission_list_ok(self):
#        self.ok('activity_submission_list')

#    def test_activity_submission_create_ok(self):
#        self.ok('activity_submission_create')
