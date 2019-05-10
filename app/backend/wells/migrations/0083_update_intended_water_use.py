from django.db import migrations


# This can be deleted when doing next squash of migrations because it's a one time update
def update_intended_water_use_code(apps, schema_editor):
    intended_water_use = apps.get_model('wells', 'IntendedWaterUseCode')
    well = apps.get_model('wells', 'well')

    not_applicable = intended_water_use.objects.get_or_create(
        pk='N/A',
        create_user='ETL_USER',
        create_date='2017-07-01T08:00:00Z',
        update_user='ETL_USER',
        update_date='2017-07-01T08:00:00Z',
        description='Not Applicable',
        display_order=110,
        effective_date='2018-05-25T07:00:00Z',
        expiry_date='9999-12-31T23:59:59Z'
    )

    # Set all wells intended water use to Not Applicable where well class is not equal to Water Supply System
    well.objects.exclude(well_class='DWS').update(
        intended_water_use=not_applicable[0])

    well.objects.filter(well_class='DWS').filter().update(
        intended_water_use=not_applicable[0])


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0081_update_well_disinfect_values'),
    ]

    operations = [
        migrations.RunPython(update_well_ground_elevation_method_codes, reverse),
    ]

