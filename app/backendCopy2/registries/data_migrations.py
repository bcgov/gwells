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
from django.utils import timezone
from gwells.codes import CodeFixture
from registries.models import Organization
from registries.serializers import OrganizationAdminSerializer

def insert_remove_reasons(apps, schema_editor):
    data = {
        'FAILTM': {
            'description': 'Fails to maintain a requirement for registration',
            'display_order': 1
        },
        'NLACT': {
            'description': 'No longer actively working in Canada',
            'display_order': 2
        },
        'NMEET': {
            'description': 'Fails to meet a requirement for registration',
            'display_order': 3
        }
    }
    RegistriesRemovalReason = apps.get_model('registries', 'RegistriesRemovalReason')

    for (key, value) in data.items():
        RegistriesRemovalReason.objects.update_or_create(code=key, defaults=value)


def revert_remove_reasons(apps, schema_editor):
    # We don't need to do anything on revert
    pass


def activity_codes():
    fixture = 'migrations/activity_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)
    return CodeFixture(fixture_path)


def load_activity_codes(apps, schema_editor):
    return activity_codes().update_or_create_fixture(apps, schema_editor)


def unload_activity_codes(apps, schema_editor):
    return activity_codes().unload_fixture(apps, schema_editor)


def subactivity_codes():
    fixture = 'migrations/subactivity_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)
    return CodeFixture(fixture_path)


def load_subactivity_codes(apps, schema_editor):
    ActivityCode = apps.get_model('registries', 'ActivityCode')
    codes = subactivity_codes()
    for item in codes.fixture:
        # Turns strings into models
        item['fields']['registries_activity'] = ActivityCode.objects.get(pk=item['fields']['registries_activity'])
    return codes.update_or_create_fixture(apps, schema_editor)


def unload_subactivity_codes(apps, schema_editor):
    return subactivity_codes().unload_fixture(apps, schema_editor)

def populate_empty_geometries(apps, schema_editor):
    """
    Populate the geom field for all Organizations that meet the following
    criteria:
    1. 'geom' is currently null
    2. Either 'street_address' and 'city' are not null, or just 'city' is not null
    3. 'province_state' is BC
    4. The Organization's database record isn't expired
    The 'geom' field is populated by executing a no-change update 
    on the organization serializer.  This triggers the serializer to 
    attempt to populate the geometry by geocoding the street address
    and/or city.
    """
    orgs_to_update = \
        Organization.objects.filter(
            geom__isnull=True, 
            city__isnull=False,
            province_state__exact="BC",
            expiry_date__gt=timezone.now()
            )
    for org in orgs_to_update:
        serializer = OrganizationAdminSerializer(org)
        validated_data = {
            "city": org.city #no change
        }
        serializer.update(org, validated_data)