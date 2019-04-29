from __future__ import unicode_literals

from django.db import migrations
import json
from io import open
import os

from wells import data_migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0074_auto_20190429_2148'),
    ]

    operations = [
        migrations.RunPython(
            data_migrations.load_lithology_significance_codes, reverse_code=data_migrations.unload_lithology_significance_codes),
    ]
