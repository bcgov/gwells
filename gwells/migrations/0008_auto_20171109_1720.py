# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-09 17:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0007_auto_20171108_2153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='developmentmethod',
            old_name='code',
            new_name='development_method_code',
        ),
    ]
