# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-08 21:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0006_auto_20171107_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitysubmission',
            name='water_quality_characteristics',
            field=models.ManyToManyField(blank=True, db_table='gwells_activity_submission_water_quality', to='gwells.WaterQualityCharacteristic', verbose_name='Obvious Water Quality Characteristics'),
        ),
    ]
