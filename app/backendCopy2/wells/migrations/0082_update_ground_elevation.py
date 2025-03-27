from django.db import migrations


# This can be deleted when doing next squash of migrations because it's a one time update
def update_well_ground_elevation_method_codes(apps, schema_editor):
    ground_method_code = apps.get_model('wells', 'GroundElevationMethodCode')
    well = apps.get_model('wells', 'well')

    unknown_method = ground_method_code.objects.get_or_create(
        pk='UNKNOWN',
        create_user='ETL_USER',
        create_date='2017-07-01T08:00:00Z',
        update_user='ETL_USER',
        update_date='2017-07-01T08:00:00Z',
        description='Unknown',
        display_order=90,
        effective_date='2018-05-25T07:00:00Z',
        expiry_date='9999-12-31T23:59:59Z'
    )
    # Set all ground elevation methods that are null to UNKNOWN
    well.objects.filter(ground_elevation_method__isnull=True).update(
        ground_elevation_method_id=unknown_method[0])


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0081_update_well_disinfect_values'),
    ]

    operations = [
        migrations.RunPython(update_well_ground_elevation_method_codes, reverse),
    ]

