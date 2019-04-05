from __future__ import unicode_literals
from django.db import migrations
import os

from wells import data_migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0058_auto_20190213_2128'),
    ]

    operations = [
        migrations.RunPython(
            data_migrations.load_other_code_values,
            reverse_code=data_migrations.unload_other_code_values),
    ]
