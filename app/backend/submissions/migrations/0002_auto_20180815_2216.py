# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-15 22:16
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):
    atomic = settings.DATABASES.get('default').get('engine') == 'django.db.backends.postgresql'

    dependencies = [
        ('submissions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wellactivitycode',
            old_name='well_activity_type_code',
            new_name='code',
        ),
        migrations.AlterField(
            model_name='wellactivitycode',
            name='code',
            field=models.CharField(db_column='well_activity_type_code', editable=False, max_length=10, primary_key=True, serialize=False),
        )
    ]
