from django.test import TestCase
from django.core.urlresolvers import reverse
from http import HTTPStatus
from django.contrib.auth.models import Group


class SurveyRenderTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='admin')

    def setUp(self):
        pass


class WellTestCase(SurveyRenderTestCase):
    fixtures = ['well_detail_fixture', 'survey_well_fixture']

    def test_well(self):
        url = reverse('well_detail', kwargs={'pk': '123'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        survey_id = ' id="survey:'
        self.assertContains(response, survey_id, count=1)  # one and only one survey included
        survey_id = survey_id + '495a9927-5a13-490e-bf1d-08bf2048b098'
        self.assertContains(response, survey_id)  # the right survey included


class DisabledSurveyTestCase(SurveyRenderTestCase):
    fixtures = ['well_detail_fixture', 'survey_well_disabled_survey_fixture']

    def test_disabled_survey(self):
        url = reverse('well_detail', kwargs={'pk': '123'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        survey_id = 'id="survey:'
        self.assertContains(response, survey_id, count=0)  # one and only one survey included


class RegistryTestCase(SurveyRenderTestCase):
    fixtures = ['survey_registry_fixture']

    def test_registry(self):
        url = reverse('registry-legacy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        survey_id = 'id="survey:'
        self.assertContains(response, survey_id, count=1)  # one and only one survey included
        survey_id = survey_id + '495a9927-5a13-490e-bf1d-08bf2048b098'
        self.assertContains(response, survey_id)  # the right survey included


class SearchTestCase(SurveyRenderTestCase):
    fixtures = ['survey_search_fixture']

    def test_search(self):
        url = reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        survey_id = 'id="survey:'
        self.assertContains(response, survey_id, count=1)  # one and only one survey included
        survey_id = survey_id + '495a9927-5a13-490e-bf1d-08bf2048b098'
        self.assertContains(response, survey_id)  # the right survey included


class NoSurveysTestCase(SurveyRenderTestCase):
    fixtures = ['well_detail_fixture']

    def test_no_surveys(self):
        url = reverse('well_detail', kwargs={'pk': '123'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        survey_id = 'id="survey:'
        self.assertContains(response, survey_id, count=0)


class MultipleSurveysTestCase(SurveyRenderTestCase):
    fixtures = ['well_detail_fixture', 'survey_well_fixture1', 'survey_well_fixture2']

    def test_multiple_surveys(self):
        url = reverse('well_detail', kwargs={'pk': '123'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        survey_id = 'id="survey:'
        self.assertContains(response, survey_id, count=2)  # 2 surveys included
        survey_id1 = survey_id + '495a9927-5a13-490e-bf1d-08bf2048b098'
        self.assertContains(response, survey_id1)  # the first survey is included
        survey_id2 = survey_id + '6ec24102-129d-44ea-ad3d-67c2517e3fb9'
        self.assertContains(response, survey_id2)  # the second survey is included
