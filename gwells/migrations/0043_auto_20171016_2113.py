# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-16 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0042_auto_20171016_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='well',
            name='alteration_date',
            field=models.DateField(null=True, verbose_name='Alteration Date'),
        ),
        migrations.AddField(
            model_name='well',
            name='construction_date',
            field=models.DateField(null=True, verbose_name='Construction Date'),
        ),
        migrations.AddField(
            model_name='well',
            name='decommission_date',
            field=models.DateField(null=True, verbose_name='Decommission Date'),
        ),
    ]
