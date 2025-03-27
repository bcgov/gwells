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
from gwells.codes import CodeFixture


def well_activity_code():
    fixture = 'migrations/well_activity_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)
    return CodeFixture(fixture_path)


def load_well_activity_codes(apps, schema_editor):
    return well_activity_code().load_fixture(apps, schema_editor)


def unload_well_activity_codes(apps, schema_editor):
    return well_activity_code().unload_fixture(apps, schema_editor)