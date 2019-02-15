from __future__ import unicode_literals
from django.db import migrations
import os
from gwells.codes import CodeFixture


def code_fixture():
    fixture = '0059_other_code_values.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0058_auto_20190213_2128'),
    ]

    operations = [
        migrations.RunPython(code_fixture().load_fixture, reverse_code=code_fixture().unload_fixture),
    ]
