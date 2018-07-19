from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from gwells.roles import (
    roles_to_groups,
    ADMIN_ROLE,
    REGISTRIES_AUTHORITY_ROLE,
    REGISTRIES_ADJUDICATOR_ROLE,
    REGISTRIES_VIEWER_ROLE,
)
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
        roles = [ADMIN_ROLE, REGISTRIES_AUTHORITY_ROLE,
                 REGISTRIES_ADJUDICATOR_ROLE, REGISTRIES_VIEWER_ROLE]
        roles_to_groups(self.test_user, roles)

        self.assertEquals(self.test_user.groups.filter(
            name=ADMIN_ROLE).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=REGISTRIES_AUTHORITY_ROLE).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=REGISTRIES_ADJUDICATOR_ROLE).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=REGISTRIES_VIEWER_ROLE).exists(), True)

    def test_user_removed_from_groups(self):
        """ Test that a user is removed from a group when their role is updated """
        roles = [ADMIN_ROLE, REGISTRIES_AUTHORITY_ROLE]
        roles_to_groups(self.test_user, roles)

        self.assertEquals(self.test_user.groups.filter(
            name=ADMIN_ROLE).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=REGISTRIES_AUTHORITY_ROLE).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=REGISTRIES_ADJUDICATOR_ROLE).exists(), False)
        self.assertEquals(self.test_user.groups.filter(
            name=REGISTRIES_VIEWER_ROLE).exists(), False)

        roles = [REGISTRIES_ADJUDICATOR_ROLE, REGISTRIES_VIEWER_ROLE]
        roles_to_groups(self.test_user, roles)

        self.assertEquals(self.test_user.groups.filter(
            name=ADMIN_ROLE).exists(), False)
        self.assertEquals(self.test_user.groups.filter(
            name=REGISTRIES_AUTHORITY_ROLE).exists(), False)
        self.assertEquals(self.test_user.groups.filter(
            name=REGISTRIES_ADJUDICATOR_ROLE).exists(), True)
        self.assertEquals(self.test_user.groups.filter(
            name=REGISTRIES_VIEWER_ROLE).exists(), True)
