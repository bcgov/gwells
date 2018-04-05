"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from gwells.settings import get_env_variable


class Command(BaseCommand):
    help = 'Creates a test user to assist with API testing'

    def handle(self, *args, **options):
        User = get_user_model()

        TEST_USER = get_env_variable('GWELLS_API_TEST_USER')
        TEST_PASSWD = get_env_variable('GWELLS_API_TEST_PASSWORD')

        if not User.objects.filter(username=TEST_USER).exists():
            user = User.objects.create_user(TEST_USER, 'test@example.com', TEST_PASSWD)
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully created test user "%s"' % user.username))

        elif User.objects.filter(username=TEST_USER).exists():
            self.stdout.write(self.style.SUCCESS('Test user already exists (username: "%s").' % TEST_USER))
