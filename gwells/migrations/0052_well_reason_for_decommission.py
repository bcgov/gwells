# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-29 23:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0051_auto_20171129_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='well',
            name='reason_for_decommission',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Reason for Decomission'),
        ),
    ]
