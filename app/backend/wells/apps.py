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

from gwells.db_comments import db_actions


logger = logging.getLogger(__name__)


def post_migration_callback(sender, **kwargs):
    # Dynamic comments from models
    logger.info('Running post_migration_callback for wells')
    db_actions.create_db_comments_from_models(db_actions.get_all_model_classes('wells.models'))


class WellsConfig(AppConfig):
    name = 'wells'

    def ready(self):
        post_migrate.connect(post_migration_callback, sender=self)
