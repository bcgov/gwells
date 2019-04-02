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
import logging

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from django.db.models import Max

from gwells.db_comments import db_actions

logger = logging.getLogger(__name__)


def post_migration_callback(sender, **kwargs):
    # Dynamic comments from models
    db_actions.create_db_comments_from_models(db_actions.get_all_model_classes('wells.models'))

    # NOTE: This is a temporary measure to reduce issues surrounding the well_tag_number sequece being
    # incorrect after replication wells. This should be removed once we switch over to gwells for creating
    # wells.
    from wells.models import Well
    from django.db import connection

    result = Well.objects.all().aggregate(Max('well_tag_number'))
    if result['well_tag_number__max']:
        with connection.cursor() as cursor:
            sql = "alter sequence well_well_tag_number_seq restart with {}".format(
                result['well_tag_number__max'] + 1)
            logger.info('altering well_well_tag_number_seq: {}'.format(sql))
            cursor.execute(sql)


class WellsConfig(AppConfig):
    name = 'wells'

    def ready(self):
        post_migrate.connect(post_migration_callback, sender=self)
