# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-03 01:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registries', '0004_auto_20180202_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitycode',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
