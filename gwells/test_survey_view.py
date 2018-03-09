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
from gwells.models import Survey
from gwells.views.admin import SurveyView
import logging
from django.core import serializers
from django.conf import settings
from django.test import RequestFactory
from django.http import QueryDict
import json
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from urllib.parse import urlparse
from urllib.parse import parse_qsl

class SurveyViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='admin')

    def setUp(self):
        pass

class SurveyViewGenericTestCase(TestCase):
    def test_with_unauthenticated_user(self):

        response = self.client.post(reverse('survey'))

        self.assertEqual(response.status_code, 302)
        url_components = urlparse(response.url)
        self.assertEqual(url_components.path, reverse('admin:login'))

        query=parse_qsl(url_components.query)
        self.assertEqual(len(query), 1)

        arg_tuple = query[0];
        self.assertEqual(len(arg_tuple), 2)
        self.assertEqual(arg_tuple[0], 'next')
        self.assertEqual(arg_tuple[1], reverse('survey'))

class SurveyViesPutTestCase(SurveyViewTestCase):

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='admin')

    def setUp(self):
        pass

    def test_put(self):
        if settings.ENABLE_DATA_ENTRY:

            fixture_file = '/'.join([settings.FIXTURES_DIRS[0], 'survey_get_fixture.json'])

            group_name = 'admin'
            username = 'admin'
            password = 'admin'
            email = 'admin@admin.com'
            self.user = User.objects.create_user(username=username, password=password, email=email)
            admin_group = Group.objects.get(name=group_name)
            admin_group.user_set.add(self.user)
            self.client.login(username=username,password=password)

            with open(fixture_file) as fixture:
                fixture = list(serializers.deserialize('json', fixture))
                self.assertEqual(1, len(fixture)) #make sure the fixture hasn't changed
                survey = fixture[0]

                factory = RequestFactory()

                data = {'survey_introduction_text':survey.object.survey_introduction_text,
                        'survey_page':survey.object.survey_page,
                        '_method':'put'}

                response = self.client.post(reverse('survey'), data)

                self.assertEqual(response.status_code, HTTPStatus.FOUND) #302 from redirect
                self.assertEqual(response.url, reverse('site_admin'))

                self.assertEqual(1, Survey.objects.all().count())
                self.assertEqual(survey.object.survey_introduction_text, Survey.objects.all()[0].survey_introduction_text)

            self.client.logout()
            self.user.delete()
        else:
            pass



class SurveyViewPostTestCase(SurveyViewTestCase):
    fixtures = ['survey_get_fixture']

    def test_post(self):
        if settings.ENABLE_DATA_ENTRY:

            #setup
            group_name = 'admin'
            username = 'admin'
            password = 'admin'
            email = 'admin@admin.com'
            self.user = User.objects.create_user(username=username, password=password, email=email)
            admin_group = Group.objects.get(name=group_name)
            admin_group.user_set.add(self.user)
            self.client.login(username=username,password=password)

            #test
            new_survey_introduction_text = 'new survey introduction text'
            new_survey_page = 'r'
            new_survey_link = 'newlink.ca'

            data = {'form-number':0,
                    'form-0-survey_guid':'495a9927-5a13-490e-bf1d-08bf2048b098',
                    'form-0-survey_introduction_text':new_survey_introduction_text,
                    'form-0-survey_page':new_survey_page,
                    'form-0-survey_link':new_survey_link,
                    '_method':'post'}

            response = self.client.post(reverse('survey'), data)

            self.assertEqual(response.status_code, HTTPStatus.FOUND) #302 from redirect
            self.assertEqual(1, Survey.objects.all().count())

            survey = Survey.objects.all()[0]
            self.assertEqual(str(survey.survey_guid), '495a9927-5a13-490e-bf1d-08bf2048b098')
            self.assertEqual(survey.survey_introduction_text, new_survey_introduction_text)
            self.assertEqual(survey.survey_page, new_survey_page)
            self.assertEqual(survey.survey_link, new_survey_link)

            #teardown
            self.client.logout()
            self.user.delete()
        else:
            pass

class SurveyViewDeleteTestCase(SurveyViewTestCase):
    fixtures = ['survey_get_fixture']

    def test_delete(self):
        if settings.ENABLE_DATA_ENTRY:
            #setup
            group_name = 'admin'
            username = 'admin'
            password = 'admin'
            email = 'admin@admin.com'
            self.user = User.objects.create_user(username=username, password=password, email=email)
            admin_group = Group.objects.get(name=group_name)
            admin_group.user_set.add(self.user)
            self.client.login(username=username,password=password)

            #test
            self.assertEqual(1, Survey.objects.all().count()) #validate that setup complete correctly --fixture
            data = {'form-number':0,
                    'form-0-survey_guid':'495a9927-5a13-490e-bf1d-08bf2048b098',
                    '_method':'delete'}

            response = self.client.post(reverse('survey'), data)

            self.assertEqual(response.status_code, HTTPStatus.FOUND) #302 from redirect
            self.assertEqual(response.url, reverse('site_admin'))

            self.assertEqual(0, Survey.objects.all().count())

            #teardown
            self.client.logout()
            self.user.delete()
        else:
            pass

class SurveyViewNoMethodTestCase(SurveyViewTestCase):
    def test_nomethod(self):
        if settings.ENABLE_DATA_ENTRY:
            #setup
            group_name = 'admin'
            username = 'admin'
            password = 'admin'
            email = 'admin@admin.com'
            self.user = User.objects.create_user(username=username, password=password, email=email)
            admin_group = Group.objects.get(name=group_name)
            admin_group.user_set.add(self.user)
            self.client.login(username=username,password=password)

            logger = logging.getLogger('django.request')
            previous_level = logger.getEffectiveLevel()
            logger.setLevel(logging.ERROR)

            #test
            data = {}

            response = self.client.post(reverse('survey'), data)

            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

            #teardown
            self.client.logout()
            self.user.delete()
            logger.setLevel(previous_level)

        else:
            pass

class SurveyViewInvalidMethodTestCase(SurveyViewTestCase):
    fixtures = ['survey_get_fixture']

    def test_invalid_method(self):
        if settings.ENABLE_DATA_ENTRY:
            self.assertEqual(1, Survey.objects.all().count()) #validate that setup complete correctly --fixture

            data = {'form-number':0,
                    'form-0-survey_guid':'495a9927-5a13-490e-bf1d-08bf2048b098',
                    '_method':'foo'}

            #setup
            logger = logging.getLogger('django.request')
            previous_level = logger.getEffectiveLevel()
            logger.setLevel(logging.ERROR)

            response = self.client.post(reverse('survey'), data) #defaults to get

            self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

            #teardown
            logger.setLevel(previous_level)
        else:
            pass
