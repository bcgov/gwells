# Generated by Django 2.2.1 on 2019-05-25 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0024_waterrightslicence'),
        ('wells', '0083_remove_well_licence'),
    ]

    operations = [
        migrations.AddField(
            model_name='well',
            name='licences',
            field=models.ManyToManyField(to='aquifers.WaterRightsLicence'),
        ),
    ]
