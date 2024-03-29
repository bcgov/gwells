# Generated by Django 2.2.28 on 2023-08-11 18:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0140_auto_20230727_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitysubmission',
            name='drinking_water_protection_area_ind',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False, verbose_name='Drinking Water Protection Area'),
        ),
        migrations.AddField(
            model_name='fieldsprovided',
            name='drinking_water_protection_area_ind',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='well',
            name='drinking_water_protection_area_ind',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False, verbose_name='Drinking Water Protection Area'),
        )
    ]
