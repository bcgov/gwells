# Generated by Django 2.2.1 on 2019-05-09 19:30

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0081_update_well_disinfect_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitysubmission',
            name='surface_seal_thickness',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Surface Seal Thickness'),
        ),
    ]
