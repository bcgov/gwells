# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-15 21:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0027_auto_20171115_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productiondata',
            name='well_id',
        ),
        migrations.AddField(
            model_name='productiondata',
            name='well_guid',
            field=models.ForeignKey(blank=True, db_column='well_guid', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.Well'),
        ),
    ]
