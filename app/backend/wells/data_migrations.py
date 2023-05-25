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
import json
import pytz
import logging

from django.utils import timezone
from django.db.models import F

from gwells.codes import CodeFixture


logger = logging.getLogger(__name__)


def casing_codes():
    """
    Generator that deserializes and provides casing objects.
    Doing it this way, instead of using fixtures, means we don't have to maintain the json, it will
    always work as it has access to the historic model.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(path, 'migrations/casing_codes.json'), 'r') as json_data:
        data = json.load(json_data)
        for item in data:
            yield item


def load_casing_codes_fixture(apps, schema_editor):
    CasingCode = apps.get_model('wells', 'CasingCode')
    for item in casing_codes():
        CasingCode.objects.create(**item)


def unload_casing_codes_fixture(apps, schema_editor):
    CasingCode = apps.get_model('wells', 'CasingCode')
    for item in casing_codes():
        CasingCode.objects.get(code=item.get('code')).delete()


def water_quality_codes():
    fixture = 'migrations/water_quality_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_water_quality_codes(apps, schema_editor):
    return water_quality_codes().load_fixture(apps, schema_editor)


def unload_water_quality_codes(apps, schema_editor):
    return water_quality_codes().unload_fixture(apps, schema_editor)


def change_code_description(apps, schema_editor):
    CasingCode = apps.get_model('wells', 'CasingCode')
    CasingMaterialCode = apps.get_model('wells', 'CasingMaterialCode')
    Casing = apps.get_model('wells', 'Casing')

    casing_code = CasingCode(code='STL_REM', description='Steel Removed', display_order=3)
    casing_code.save()

    casing_material = CasingMaterialCode.objects.filter(code='STL_PUL_OT').first()

    if casing_material:
        for casing in Casing.objects.filter(casing_material=casing_material):
            # Any case where we are overwriting a different casing_code can be ignored, as casing material
            # is an entirely new field, and this migration should thus only find records in test/dev.
            casing.casing_code = casing_code
            casing.casing_material = None
            casing.save()

        casing_material.delete()


def restore_code_description(apps, schema_editor):
    CasingCode = apps.get_model('wells', 'CasingCode')
    CasingMaterialCode = apps.get_model('wells', 'CasingMaterialCode')
    Casing = apps.get_model('wells', 'Casing')

    casing_code = CasingCode.objects.get(code='STL_REM')

    casing_material = CasingMaterialCode(code='STL_PUL_OT', description='Steel pulled out', display_order=20)
    casing_material.save()

    for casing in Casing.objects.filter(casing_code=casing_code):
        if casing.casing_material:
            raise DataError('Was not expecting to find casing code: {}'.format(casing.casing_code))
        casing.casing_material = casing_material
        casing.casing_code = None
        casing.save()

    casing_code.delete()


def decomission_material_codes():
    fixture = 'migrations/decom_mat_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_decomission_material_codes(apps, schema_editor):
    return decomission_material_codes().load_fixture(apps, schema_editor)


def unload_decomission_material_codes(apps, schema_editor):
    return decomission_material_codes().unload_fixture(apps, schema_editor)


DATA = {
    'A': '(10 m accuracy)  ICF cadastre and good location sketch',
    'B': '(20 m accuracy) Digitized from 1:5,000 mapping',
    'C': '(50 m accuracy) Digitized from 1:20,000 mapping',
    'D': '(100 m accuracy) Digitized from old Dept. of Lands, Forests and Water Resources maps',
    'E': '(200 m accuracy) Digitized from 1:50,000 maps',
    'F': '(1 m accuracy) CDGPS',
    'G': ('(unknown, accuracy based on parcel size) No ICF cadastre, poor or no location sketch; site ' +
          'located in center of primary parcel'),
    'H': '(10 m accuracy) Handheld GPS with accuracy of +/- 10 metres',
    'I': '(20 m accuracy) No ICF cadastre but good location sketch or good written description',
    'J': ('unknown, accuracy based on parcel size) ICF cadastre, poor or no location sketch, ' +
          'arbitrarily located in center of parcel'),
}


def load_coordinate_aquisition_data(apps, schema_editor):
    CoordinateAcquisitionCode = apps.get_model(
        'wells', 'CoordinateAcquisitionCode')
    for (key, value) in DATA.items():
        code = CoordinateAcquisitionCode()
        code.code = key
        code.create_user = "DATALOAD_USER"
        code.create_date = timezone.now()
        code.description = value
        code.effective_date = timezone.now()
        code.save()


def unload_coordinate_aquisition_data(apps, schema_editor):
    CoordinateAcquisitionCode = apps.get_model(
        'wells', 'CoordinateAcquisitionCode')
    for key in DATA:
        try:
            code = CoordinateAcquisitionCode.objects.get(code=key)
            code.delete()
        except:
            # We don't panic too much if this fails, the table is going to be dropped!
            logger.error('failed to delete {}'.format(key))


def lithology_moisture_code_fixture():
    fixture = 'migrations/lithology_moisture_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_lithology_moisture_codes(apps, schema_editor):
    return lithology_moisture_code_fixture().load_fixture(apps, schema_editor)


def unload_lithology_moisture_codes(apps, schema_editor):
    return lithology_moisture_code_fixture().unload_fixture(apps, schema_editor)


def well_disinfected_code_fixture():
    fixture = 'migrations/well_disinfected_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_well_disinfected_codes(apps, schema_editor):
    return well_disinfected_code_fixture().load_fixture(apps, schema_editor)


def unload_well_disinfected_codes(apps, schema_editor):
    return well_disinfected_code_fixture().unload_fixture(apps, schema_editor)


def well_orientation_code_fixture():
    fixture = 'migrations/well_orientation_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_well_orientation_codes(apps, schema_editor):
    return well_orientation_code_fixture().load_fixture(apps, schema_editor)


def unload_well_orientation_codes(apps, schema_editor):
    return well_orientation_code_fixture().unload_fixture(apps, schema_editor)


def boundary_effect_code_fixture():
    fixture = 'migrations/boundary_effect_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_boundary_effect_codes(apps, schema_editor):
    return boundary_effect_code_fixture().load_fixture(apps, schema_editor)


def unload_boundary_effect_codes(apps, schema_editor):
    return boundary_effect_code_fixture().unload_fixture(apps, schema_editor)


def drive_shoe_code_fixture():
    fixture = 'migrations/drive_shoe_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_drive_shoe_codes(apps, schema_editor):
    return drive_shoe_code_fixture().load_fixture(apps, schema_editor)


def unload_drive_shoe_codes(apps, schema_editor):
    return drive_shoe_code_fixture().unload_fixture(apps, schema_editor)


def filter_pack_code_fixture():
    fixture = 'migrations/filter_pack_code_fixtures.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_filter_pack_codes(apps, schema_editor):
    return filter_pack_code_fixture().load_fixture(apps, schema_editor)


def unload_filter_pack_codes(apps, schema_editor):
    return filter_pack_code_fixture().unload_fixture(apps, schema_editor)


def load_unspecified_coordinate_aquisition_code(apps, schema):
    CoordinateAcquisitionCode = apps.get_model('wells', 'CoordinateAcquisitionCode')
    CoordinateAcquisitionCode.objects.create(
        code='0',
        description='Not Specified',
        effective_date=timezone.now(),
        create_user='Django Migration')


def unload_unspecified_coordinate_aquisition_code(apps, schema):
    CoordinateAcquisitionCode = apps.get_model('wells', 'CoordinateAcquisitionCode')
    codes = CoordinateAcquisitionCode.objects.filter(code='0')
    for code in codes:
        code.delete()


def well_publication_status_code_fixture():
    fixture = 'migrations/well_publication_status_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_well_publication_status(apps, schema):
    return well_publication_status_code_fixture().load_fixture(apps, schema)


def unload_well_publication_status(apps, schema):
    return well_publication_status_code_fixture().unload_fixture(apps, schema)


def insert_unk_well_class_code(apps, schema_editor):
    data = {
        'UNK': {
            "description": "Unknown",
            "display_order": 19,
            "effective_date": "2019-02-12 01:00:00Z",
            "expiry_date": "9999-12-31T23:59:59.999999Z",
            "create_user": "ETL_USER",
            "create_date": "2019-02-12 01:00:00Z",
            "update_user": "ETL_USER",
            "update_date": "2019-02-12 01:00:00Z"
        },
    }
    WellClassCode = apps.get_model('wells', 'WellClassCode')

    for (key, value) in data.items():
        WellClassCode.objects.update_or_create(well_class_code=key, defaults=value)


def revert_unk_well_class_code(apps, schema_editor):
    # Deleting these could be dangerous (we don't want to cascade delete the submissions),
    # so we do nothing here.
    logger.warning('Not deleting WellClassCode records! That would be dangerous.')


def other_code_values_code_fixture():
    fixture = 'migrations/other_code_values.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_other_code_values(apps, schema):
    return other_code_values_code_fixture().load_fixture(apps, schema)


def unload_other_code_values(apps, schema):
    return other_code_values_code_fixture().unload_fixture(apps, schema)


def aquifer_lithology_code_fixture():
    fixture = 'migrations/aquifer_lithology_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


def load_aquifer_lithology_code_values(apps, schema):
    return aquifer_lithology_code_fixture().load_fixture(apps, schema)


def unload_aquifer_lithology_code_values(apps, schema):
    return aquifer_lithology_code_fixture().unload_fixture(apps, schema)


def update_update_user_fields(apps, schema_editor):
    app_config = apps.get_app_config('wells')
    app_models = app_config.get_models()
    for model in app_models:
        if hasattr(model, 'update_user'):
            try:
                model.objects.filter(update_user__isnull=True).update(update_user=F('create_user'))
            except AttributeError:
                logger.error("skipping")
