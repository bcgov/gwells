# Generated by Django 2.2.12 on 2020-05-01 21:46

from django.db import migrations


CREATE_POSTGIS_FTW_SCHEMA = """
    CREATE SCHEMA IF NOT EXISTS postgis_ftw
"""


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0006_related_name_set_20200302_1752'),
    ]

    operations = [
        migrations.RunSQL(
            CREATE_POSTGIS_FTW_SCHEMA,
        ),
    ]
