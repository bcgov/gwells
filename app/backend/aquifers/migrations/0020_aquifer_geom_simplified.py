# Generated by Django 2.1.8 on 2019-04-07 19:46

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0019_remove_waterrightslicence_well'),
    ]

    operations = [
        migrations.AddField(
            model_name='aquifer',
            name='geom_simplified',
            field=django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326),
        ),
    ]
