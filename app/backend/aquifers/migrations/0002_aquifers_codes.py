# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-21 17:02
from __future__ import unicode_literals

from django.db import migrations
import json
from io import open
import os
from gwells.codes import CodeFixture


def aquifers_codes():
    fixture = '0002_aquifers_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(aquifers_codes().load_fixture, reverse_code=aquifers_codes().unload_fixture),
    ]
