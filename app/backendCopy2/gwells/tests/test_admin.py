from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.urls import reverse
from urllib.parse import urlparse
from urllib.parse import parse_qsl
from http import HTTPStatus


class AdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='admin')

    def setUp(self):
        pass

    def test_unauthorized_user_admin_view(self):
        # setup
        username = 'notadmin'
        password = 'notadmin'
        email = 'notadmin@example.com'
        self.user = User.objects.create_user(username=username, password=password, email=email)

        self.client.login(username=username, password=password)

        # test
        response = self.client.get(reverse('site_admin'))
        self.assertNotEqual(response.status_code, HTTPStatus.OK)
