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

class SurveyViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        #using fixtures
        pass

    def setUp(self):
        pass

class PutTestCase(SurveyViewTestCase):

    def test_put(self):
        fixture_file = '/'.join([settings.FIXTURES_DIRS[0], 'survey_get_fixture.json'])

        if settings.ENABLE_DATA_ENTRY:
            with open(fixture_file) as fixture:
                fixture = list(serializers.deserialize('json', fixture))

                self.assertEqual(1, len(fixture)) #make sure the fixture hasn't changed

                survey = fixture[0]

                factory = RequestFactory()

                data = {'survey_introduction_text':survey.object.survey_introduction_text,
                        'survey_page':survey.object.survey_page,
                        '_method':'put'}

                request = factory.post(reverse('survey'), data)
                request.PUT = request.POST #middleware usually takes care of this
                survey_view = SurveyView.as_view()
                response = survey_view(request)

                self.assertEqual(response.status_code, HTTPStatus.FOUND) #302 from redirect
                self.assertEqual(response.url, reverse('site_admin'))

                self.assertEqual(1, Survey.objects.all().count())
                self.assertEqual(survey.object.survey_introduction_text, Survey.objects.all()[0].survey_introduction_text)
        else:
            pass

class PostTestCase(SurveyViewTestCase):
    fixtures = ['survey_get_fixture']

    def test_post(self):
        if settings.ENABLE_DATA_ENTRY:
            new_survey_introduction_text = 'new survey introduction text'
            new_survey_page = 'r'
            new_survey_link = 'newlink.ca'

            data = {'form-number':0,
                    'form-0-survey_guid':'495a9927-5a13-490e-bf1d-08bf2048b098',
                    'form-0-survey_introduction_text':new_survey_introduction_text,
                    'form-0-survey_page':new_survey_page,
                    'form-0-survey_link':new_survey_link,
                    '_method':'post'}

            factory = RequestFactory()
            request = factory.post(reverse('survey'), data)

            survey_view = SurveyView.as_view()
            response = survey_view(request)

            self.assertEqual(response.status_code, HTTPStatus.FOUND) #302 from redirect
            self.assertEqual(1, Survey.objects.all().count())

            survey = Survey.objects.all()[0]
            self.assertEqual(str(survey.survey_guid), '495a9927-5a13-490e-bf1d-08bf2048b098')
            self.assertEqual(survey.survey_introduction_text, new_survey_introduction_text)
            self.assertEqual(survey.survey_page, new_survey_page)
            self.assertEqual(survey.survey_link, new_survey_link)
        else:
            pass

class DeleteTestCase(SurveyViewTestCase):
    fixtures = ['survey_get_fixture']

    def test_delete(self):
        if settings.ENABLE_DATA_ENTRY:
            self.assertEqual(1, Survey.objects.all().count()) #validate that setup complete correctly --fixture
            data = {'form-number':0,
                    'form-0-survey_guid':'495a9927-5a13-490e-bf1d-08bf2048b098',
                    '_method':'delete'}

            factory = RequestFactory()
            request = factory.post(reverse('survey'), data)

            survey_view = SurveyView.as_view()
            response = survey_view(request)

            self.assertEqual(response.status_code, HTTPStatus.FOUND) #302 from redirect
            self.assertEqual(response.url, reverse('site_admin'))

            self.assertEqual(0, Survey.objects.all().count())
        else:
            pass

class SurveyViewNoMethodTestCase(SurveyViewTestCase):
    def test_nomethod(self):
        if settings.ENABLE_DATA_ENTRY:
            data = {}

            factory = RequestFactory()
            request = factory.post(reverse('survey'), data) #defaults to get
            survey_view = SurveyView.as_view()
            response = survey_view(request)

            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
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

            factory = RequestFactory()
            request = factory.post(reverse('survey'), data) #defaults to get
            survey_view = SurveyView.as_view()

            response = survey_view(request)

            self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            pass
