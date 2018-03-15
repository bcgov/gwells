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

from gwells.forms import *
from django.test import TestCase
from django.core.urlresolvers import reverse
from http import HTTPStatus
from gwells.models import *
from gwells.search import Search
from gwells.views import *
import logging
from django.core import serializers
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

#TODO split tests into one file per view

class ViewsTestCase(TestCase):
    fixtures = ['well_detail_fixture',  'survey_get_fixture']

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='admin')

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
        #setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        initial_url = reverse('well_detail', kwargs={'pk':'1'})
        url = initial_url[:-2]
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        #teardown
        logger.setLevel(previous_level)

    def test_well_detail_ok(self):
        wells = Search.well_search(123, '', '', '')
        self.assertEqual(wells.count(), 1)

        url = reverse('well_detail', kwargs={'pk':123})
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

    def test_404_not_ok(self):
        #setup
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        #look for clearly erroneous well_tag_number
        url = reverse('well_detail', kwargs={'pk':999999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        #teardown
        logger.setLevel(previous_level)

    def test_site_admin_ok(self):
        group_name = 'admin'
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(username=username, password=password, email=email)
        admin_group = Group.objects.get(name=group_name)
        admin_group.user_set.add(self.user)
        self.client.login(username=username,password=password)

        self.ok('site_admin')

        self.client.logout()
        self.user.delete()

    def test_site_admin_has_add_survey(self):
        group_name = 'admin'
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(username=username, password=password, email=email)
        admin_group = Group.objects.get(name=group_name)
        admin_group.user_set.add(self.user)
        self.client.login(username=username,password=password)

        response = self.client.get(reverse('site_admin'))
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains( response, 'id="add-survey"')

        self.client.logout()
        self.user.delete()

    def test_survey_detail_ok(self):
        group_name = 'admin'
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(username=username, password=password, email=email)
        admin_group = Group.objects.get(name=group_name)
        admin_group.user_set.add(self.user)
        self.client.login(username=username,password=password)

        surveys = Survey.objects.all()
        self.assertEqual(surveys.count(), 1)
        url = reverse('survey', kwargs={'pk':"495a9927-5a13-490e-bf1d-08bf2048b098"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.client.logout()
        self.user.delete()
