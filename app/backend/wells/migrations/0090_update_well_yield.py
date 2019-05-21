from django.db import migrations
from django.db.models import F


# This can be deleted when doing next squash of migrations because it's a one time update
def update_well_yield(apps, schema_editor):
    well = apps.get_model('wells', 'well')

    # Update GPH well yield to USGPM
    well.objects.filter(well_yield_unit='GPH').update(
        well_yield=(round(F('well_yield') * 0.0166667, 2)))

    # Update well yield code from GPH to USGPM
    # well.objects.filter(well_yield_unit='GPH').update(
    #     well_yield_unit='USGPM')

    # Update well yield code GPM to USGPM
    # well.objects.filter(well_yield_unit='GPM').update(
    #     well_yield_unit='USGPM')


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0089_auto_20190515_2359'),
    ]

    operations = [
        migrations.RunPython(update_well_yield, reverse),
    ]

