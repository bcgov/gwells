import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from gwells.settings.base import get_env_variable


class Command(BaseCommand):
    help = 'Creates a default Admin user to manage administrative tasks'

    def handle(self, *args, **options):
        User = get_user_model()

        ADMIN_USER = get_env_variable('DJANGO_ADMIN_USER', None, strict=True)
        ADMIN_PASSWD = get_env_variable('DJANGO_ADMIN_PASSWORD', None, strict=True)

        if not ADMIN_USER or not ADMIN_PASSWD:
            raise CommandError('Please set DJANGO_ADMIN_USER and DJANGO_ADMIN_PASSWORD')

        elif ADMIN_USER and ADMIN_PASSWD and not User.objects.filter(username=ADMIN_USER).exists():
            user = User.objects.create_superuser(ADMIN_USER, 'gwells@gov.bc.ca', ADMIN_PASSWD)
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully created Admin user "%s"' % user.username))

        elif User.objects.filter(username=ADMIN_USER).exists():
            self.stdout.write(self.style.SUCCESS('Admin user already exists (username: "%s").' % ADMIN_USER))
