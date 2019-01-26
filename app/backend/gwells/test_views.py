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
import logging
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.core import serializers
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from gwells.search import Search
from gwells.views import *
from gwells.forms import *
from gwells.models import Survey


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

    def test_site_admin_ok(self):
        group_name = 'admin'
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(
            username=username, password=password, email=email)
        admin_group = Group.objects.get(name=group_name)
        admin_group.user_set.add(self.user)
        self.client.login(username=username, password=password)

        self.ok('site_admin')

        self.client.logout()
        self.user.delete()

    def test_site_admin_has_add_survey(self):
        group_name = 'admin'
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(
            username=username, password=password, email=email)
        admin_group = Group.objects.get(name=group_name)
        admin_group.user_set.add(self.user)
        self.client.login(username=username, password=password)

        response = self.client.get(reverse('site_admin'))
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'id="add-survey"')

        self.client.logout()
        self.user.delete()

    def test_survey_detail_ok(self):
        group_name = 'admin'
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(
            username=username, password=password, email=email)
        admin_group = Group.objects.get(name=group_name)
        admin_group.user_set.add(self.user)
        self.client.login(username=username, password=password)

        surveys = Survey.objects.all()
        self.assertEqual(surveys.count(), 1)
        url = reverse('survey', kwargs={
                      'pk': "495a9927-5a13-490e-bf1d-08bf2048b098"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.client.logout()
        self.user.delete()
