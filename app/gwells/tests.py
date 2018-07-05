from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from gwells.roles import (
    roles_to_groups,
    ADMIN_ROLE,
    AUTHORITY_ROLE,
    ADJUDICATOR_ROLE,
    VIEWER_ROLE,
    ADMIN_GROUP_NAME,
    AUTHORITY_GROUP_NAME,
    ADJUDICATOR_GROUP_NAME,
    VIEWER_GROUP_NAME)
from django.contrib.auth.models import User
from gwells.models import Profile


class GwellsRoleGroupsTests(TestCase):
    """
    Tests GWELLS "SSO role"-based groups
    """

    def setUp(self):
        """
        Set up user for each test case
        """
        self.test_user, _ = User.objects.get_or_create(
            username='Test_User', email='example@example.com', password='123456789')
        self.test_profile, _ = Profile.objects.get_or_create(
            user=self.test_user)

    def test_groups_created(self):
        roles = [ADMIN_ROLE, AUTHORITY_ROLE, ADJUDICATOR_ROLE, VIEWER_ROLE]
        roles_to_groups(self.test_user, roles)

        self.assertEquals(self.test_user.groups.filter(
            name=ADMIN_GROUP_NAME).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=AUTHORITY_GROUP_NAME).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=ADJUDICATOR_GROUP_NAME).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=VIEWER_GROUP_NAME).exists(), True)

    def test_user_removed_from_groups(self):
        """ Test that a user is removed from a group when their role is updated """
        roles = [ADMIN_ROLE, AUTHORITY_ROLE]
        roles_to_groups(self.test_user, roles)

        self.assertEquals(self.test_user.groups.filter(
            name=ADMIN_GROUP_NAME).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=AUTHORITY_GROUP_NAME).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=ADJUDICATOR_GROUP_NAME).exists(), False)
        self.assertEquals(self.test_user.groups.filter(
            name=VIEWER_GROUP_NAME).exists(), False)

        roles = [ADJUDICATOR_ROLE, VIEWER_ROLE]
        roles_to_groups(self.test_user, roles)

        self.assertEquals(self.test_user.groups.filter(
            name=ADMIN_GROUP_NAME).exists(), False)
        self.assertEquals(self.test_user.groups.filter(
            name=AUTHORITY_GROUP_NAME).exists(), False)
        self.assertEquals(self.test_user.groups.filter(
            name=ADJUDICATOR_GROUP_NAME).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=VIEWER_GROUP_NAME).exists(), True)
