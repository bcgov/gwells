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

    def test_authenticated_user_navbar(self):
        group_name = 'admin'
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(username=username, password=password, email=email)
        admin_group = Group.objects.get(name=group_name)
        admin_group.user_set.add(self.user)
        self.client.login(username=username, password=password)

        response = self.client.get(reverse('search'))

        self.assertContains(response, 'name="show.admin" content="true"')

        self.client.logout()
        self.user.delete()

    def test_unauthenticated_user_navbar(self):

        response = self.client.get(reverse('search'))

        self.assertContains(response, 'name="show.admin" content="false"')

    def test_unauthorized_user_navbar(self):
        # setup
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(username=username, password=password, email=email)
        self.client.login(username=username, password=password)

        # test
        response = self.client.get(reverse('search'))
        self.assertContains(response, 'name="show.admin" content="false"')

        # teardown
        self.client.logout()
        self.user.delete()

    def test_unauthenticated_user_admin_view(self):

        response = self.client.get(reverse('site_admin'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        url_components = urlparse(response.url)
        self.assertEqual(url_components.path, reverse('admin:login'))

        query = parse_qsl(url_components.query)
        self.assertEqual(len(query), 1)

        arg_tuple = query[0]
        self.assertEqual(len(arg_tuple), 2)
        self.assertEqual(arg_tuple[0], 'next')
        self.assertEqual(arg_tuple[1], reverse('site_admin'))

    def test_unauthorized_user_admin_view(self):
        # setup
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(username=username, password=password, email=email)
        self.client.login(username=username, password=password)

        # test
        # default django behaviour is to redirect to login.
        # TODO: provide a 403
        response = self.client.get(reverse('site_admin'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        url_components = urlparse(response.url)
        self.assertEqual(url_components.path, reverse('admin:login'))

        query = parse_qsl(url_components.query)
        self.assertEqual(len(query), 1)

        arg_tuple = query[0]
        self.assertEqual(len(arg_tuple), 2)
        self.assertEqual(arg_tuple[0], 'next')
        self.assertEqual(arg_tuple[1], reverse('site_admin'))

        # teardown
        self.client.logout()
        self.user.delete()

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


class AdminTestCaseForMissingConfiguration(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_page_loads_when_app_is_not_configured_with_admin_group(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'name="show.admin" content="false"')
