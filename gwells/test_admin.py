from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.urls import reverse

class AdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
	    Group.objects.create(name='admin')

    def setUp(self):
        pass

    def test_authenticated_user(self):
        group_name = 'admin'
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(username=username, password=password, email=email)
        admin_group = Group.objects.get(name=group_name)
        admin_group.user_set.add(self.user)
        self.client.login(username=username,password=password)

        response = self.client.get(reverse('search'))

        self.assertContains(response, 'id="ribbon-admin"')

    def test_unauthenticated_user(self):

        response = self.client.get(reverse('search'))

        self.assertNotContains(response, 'id="ribbon-admin"')

    def test_unauthorized_user(self):
        username = 'admin'
        password = 'admin'
        email = 'admin@admin.com'
        self.user = User.objects.create_user(username=username, password=password, email=email)

        response = self.client.get(reverse('search'))

        self.assertNotContains(response, 'id="ribbon-admin"')
