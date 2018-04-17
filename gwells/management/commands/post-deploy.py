from django.core import management
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates a test user to assist with API testing'

    def handle(self, *args, **options):
        management.call_command('createtestuser', verbosity=0, interactive=False)
        management.call_command('creategroups', verbosity=0, interactive=False)
