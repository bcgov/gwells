# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-20 20:28
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):
    engine = settings.DATABASES.get('default').get('engine')
    atomic = engine == 'django.db.backends.postgresql' or engine == 'django.contrib.gis.db.backends.postgis'

    dependencies = [
        ('wells', '0012_load_water_quality_codes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='linermaterialcode',
            old_name='liner_material_code',
            new_name='code',
        ),
        migrations.AlterField(
            model_name='linermaterialcode',
            name='code',
            field=models.CharField(db_column='liner_material_code', editable=False, max_length=10, primary_key=True, serialize=False),
        )
    ]
