from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

class CreateGroupsTest(TestCase):
    """ tests manage.py creategroups command """

    def test_groups_created_output(self):
        out = StringIO()
        call_command('creategroups', stdout=out)
        self.assertIn('Group gwells_administrator created', out.getvalue())
        self.assertIn('Group registries_statutory_authority created', out.getvalue())
        self.assertIn('Group registries_adjudicator created', out.getvalue())
        self.assertIn('Group registries_staff_viewer created', out.getvalue())

    def test_groups_already_created(self):
        out = StringIO()
        call_command('creategroups', stdout=None)
        # running a second time to simulate trying to create groups that already exist
        call_command('creategroups', stdout=out)
        self.assertIn('Group gwells_administrator exists', out.getvalue())
        self.assertIn('Group registries_statutory_authority exists', out.getvalue())
        self.assertIn('Group registries_adjudicator exists', out.getvalue())
        self.assertIn('Group registries_staff_viewer exists', out.getvalue())
