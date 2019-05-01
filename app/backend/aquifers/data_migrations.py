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
import datetime
import os
import json
import logging
from django.utils.timezone import utc

from django.db.models import F
from django.db.models import Q

from gwells.codes import CodeFixture
from gwells.models import DATALOAD_USER

logger = logging.getLogger(__name__)


def aquifers_codes():
    fixture = 'migrations/aquifers_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_aquifer_codes(apps, schema_editor):
    return aquifers_codes().load_fixture(apps, schema_editor)


def unload_aquifer_codes(apps, schema_editor):
    return aquifers_codes().unload_fixture(apps, schema_editor)


def aquifer_vulnerability_codes():
    fixture = 'migrations/aquifer_vulnerability_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_aquifer_vulnerability_codes(apps, schema_editor):
    return aquifer_vulnerability_codes().load_fixture(apps, schema_editor)


def unload_aquifer_vulnerability_codes(apps, schema_editor):
    return aquifer_vulnerability_codes().unload_fixture(apps, schema_editor)


def alter_aquifer_sequence(apps, schema):
    schema.execute("alter sequence aquifer_aquifer_id_seq restart with 2000")


def revert_aquifer_sequence(apps, schema):
    # It's no big deal if we don't go back
    pass


def aquifer_resource_sections():
    fixture = 'migrations/aquifer_resource_sections.json'
    fixture_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), fixture)
    return CodeFixture(fixture_path)


def load_aquifer_resource_sections(apps, schema_editor):
    return aquifer_resource_sections().load_fixture(apps, schema_editor)


def unload_aquifer_resource_sections(apps, schema_editor):
    return aquifer_resource_sections().unload_fixture(apps, schema_editor)


def generate_aquifer_resource_reverse(apps, schema_editor):
    AquiferResource = apps.get_model('aquifers', 'AquiferResource')
    AquiferResource.objects.filter(
        url='https://onlinelibrary.wiley.com/doi/abs/10.1002/hyp.7724').delete()


def generate_aquifer_resource(apps, schema_editor):
    AquiferResource = apps.get_model('aquifers', 'AquiferResource')
    Aquifer = apps.get_model('aquifers', 'Aquifer')
    for aquifer in Aquifer.objects.all():
        AquiferResource.objects.create(
            aquifer=aquifer,
            section_id='I',
            url='https://onlinelibrary.wiley.com/doi/abs/10.1002/hyp.7724',
            name=('Evaluating the use of a gridded climate surface for modelling groundwater recharge in a '
                  'semi-arid region'),
        )


def update_user_fields(apps, schema_editor):
    app_config = apps.get_app_config('aquifers')
    app_models = app_config.get_models()
    for model in app_models:
        if hasattr(model, 'update_user'):
            try:
                model.objects.filter(update_user__isnull=True).update(
                    update_user=F('create_user'))
            except AttributeError:
                logger.error("skipping")


def reverse_update_user_fields(apps, schema_editor):
    pass


def update_aquifer_resource_fields(apps, schema_editor):
    AquiferResource = apps.get_model('aquifers', 'AquiferResource')
    AquiferResource.objects.filter(create_date__isnull=True).update(create_date=datetime.datetime.now(utc))
    AquiferResource.objects.filter(update_date__isnull=True).update(update_date=F('create_date'))
    AquiferResource.objects.filter(
        Q(create_user__isnull=True) | Q(create_user='')).update(create_user=DATALOAD_USER)
    AquiferResource.objects.filter(
        Q(update_user__isnull=True) | Q(update_user='')).update(update_user=F('create_user'))
