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
from zipfile import ZipFile
import shutil

import django.contrib.gis.db.models.fields
from django.db import migrations, models
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from django.db import connection


def border_data(apps, schema_editor):
    # This border data sourced from iMapBC, specifically the "Province of BC - ABMS - Outlined" layer.
    # Shapefile inspected using:
    # ogrinfo -so gwells/migrations/ABMS_PROVINCE_SP/ABMS_PROV_polygon.shp ABMS_PROV_polygon
    # Model and mapping generated using:
    # python manage.py ogrinspect gwells/migrations/ABMS_PROVINCE_SP/ABMS_PROV_polygon.shp gwells.Border \
    #   --srid=4269 --mapping --multi
    Border = apps.get_model('gwells', 'Border')

    tmp_path = '/tmp/BCGW_ABMS_PROV-migrations/'

    zip_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'migrations/BCGW_ABMS_PROV.zip')
    with ZipFile(zip_path, 'r') as zipObj:
        zipObj.extractall(tmp_path)

    border_shp = os.path.join(tmp_path, 'ABMS_PROVINCE_SP/ABMS_PROV_polygon.shp')
    if not os.path.exists(border_shp):
        raise FileNotFoundError('file not found: {}'.format(border_shp))

    border_mapping = {
        'se_a_c_flg': 'SE_A_C_FLG',
        'obejctid': 'OBEJCTID',
        'shape': 'SHAPE',
        'length_m': 'LENGTH_M',
        'oic_number': 'OIC_NUMBER',
        'area_sqm': 'AREA_SQM',
        'upt_date': 'UPT_DATE',
        'upt_type': 'UPT_TYPE',
        'chng_org': 'CHNG_ORG',
        'aa_parent': 'AA_PARENT',
        'aa_type': 'AA_TYPE',
        'aa_id': 'AA_ID',
        'aa_name': 'AA_NAME',
        'abrvn': 'ABRVN',
        'bdy_type': 'BDY_TYPE',
        'oic_year': 'OIC_YEAR',
        'afctd_area': 'AFCTD_AREA',
        'geom': 'MULTIPOLYGON25D',
    }

    lm = LayerMapping(Border, border_shp, border_mapping, transform=False)
    lm.save(strict=True, verbose=True)

    # Now clean up
    shutil.rmtree(tmp_path)


def reverse_border_data(apps, schema_editor):
    pass
