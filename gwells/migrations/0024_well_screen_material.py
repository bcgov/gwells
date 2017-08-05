# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-04 23:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0023_auto_20170803_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='well',
            name='screen_material',
            field=models.ForeignKey(blank=True, db_column='screen_material_guid', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.ScreenMaterial', verbose_name='Screen Material'),
        ),
    ]
