# Generated by Django 2.1.7 on 2019-03-11 18:20

import django.contrib.gis.db.models.fields
from django.db import migrations
from aquifers.models import Aquifer as NewAquifer


def add_shapefile(apps, schema_editor):
    Aquifer = apps.get_model('aquifers', 'Aquifer')
    aquifers = Aquifer.objects.all()
    aquifer = aquifers[0]
    NewAquifer.load_shapefile(aquifer, "aquifers/fixtures/shp/aquifer1193.zip")
    aquifer.save()
    aquifer = aquifers[1]
    NewAquifer.load_shapefile(aquifer, "aquifers/fixtures/shp/aquiferagate.zip")
    aquifer.save()


def remove_shapefile(apps, schema_editor):
    pass  # column is deleted, don't worry about it.


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0011_auto_20190309_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='aquifer',
            name='geom',
            field=django.contrib.gis.db.models.fields.PolygonField(
                null=True, srid=3005),
        ),
        # migrations.RunPython(
        #     add_shapefile,
        #     reverse_code=remove_shapefile
        # ),
    ]
