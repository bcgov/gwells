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

    def test_authorized_user_admin_view(self):
        # setup
        group_name = 'admin'
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(username=username, password=password, email=email)
        admin_group = Group.objects.get(name=group_name)
        admin_group.user_set.add(self.user)
        self.client.login(username=username, password=password)

        # test
        response = self.client.get(reverse('site_admin'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # teardown
        self.client.logout()
        self.user.delete()
        admin_group.user_set.remove(self.user)
