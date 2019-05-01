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
