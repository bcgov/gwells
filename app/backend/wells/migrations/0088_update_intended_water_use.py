from django.db import migrations
from django.db.models import Q

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

    unknown = intended_water_use.objects.get_or_create(
        pk='UNK',
        create_user='ETL_USER',
        create_date='2017-07-01T08:00:00Z',
        update_user='ETL_USER',
        update_date='2017-07-01T08:00:00Z',
        description='Unknown Well Use',
        display_order=100,
        effective_date='2018-05-25T07:00:00Z',
        expiry_date='9999-12-31T23:59:59Z'
    )

    # Update all wells with well class of null or unknown and intended water use of below values to water supply
    well.objects\
        .filter(Q(well_class__isnull=True) | Q(well_class='UNK'))\
        .filter(Q(intended_water_use='DOM') | Q(intended_water_use='COM') |
                Q(intended_water_use='DWS') | Q(intended_water_use='IRR'))\
        .update(well_class='WATR_SPPLY')

    # Set all wells intended water use to Not Applicable where well class is not equal to Water Supply System
    well.objects.exclude(well_class='WATR_SPPLY').update(
        intended_water_use=not_applicable[0])

    # update all water supply class wells that have null intended water use to use unknown
    well.objects.filter(well_class='WATR_SPPLY').filter(intended_water_use__isnull=True).update(
        intended_water_use=unknown[0])


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0087_merge_20190514_1806'),
    ]

    operations = [
        migrations.RunPython(update_intended_water_use_code, reverse),
    ]

