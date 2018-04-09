import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from gwells.settings.base import get_env_variable


class Command(BaseCommand):
    help = 'Creates a test user to assist with API testing'

    def handle(self, *args, **options):
        User = get_user_model()

        TEST_USER = get_env_variable('GWELLS_API_TEST_USER', None, strict=True)
        TEST_PASSWD = get_env_variable('GWELLS_API_TEST_PASSWORD', None, strict=True)

        if not TEST_USER or not TEST_PASSWD:
            raise CommandError('Please set GWELLS_API_TEST_USER and GWELLS_API_TEST_PASSWORD')

        elif TEST_USER and TEST_PASSWD and not User.objects.filter(username=TEST_USER).exists():
            user = User.objects.create_user(TEST_USER, 'test@example.com', TEST_PASSWD)
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully created test user "%s"' % user.username))

        elif User.objects.filter(username=TEST_USER).exists():
            self.stdout.write(self.style.SUCCESS('Test user already exists (username: "%s").' % TEST_USER))
