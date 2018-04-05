# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-05 19:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registries', '0002_auto_20180405_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='person_set', to='registries.Organization'),
        ),
    ]
