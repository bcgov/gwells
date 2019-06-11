from django.db import migrations


# This can be deleted when doing next squash of migrations because it's a one time update
def migrate_well_orientation_status(apps, schema_editor):
    well = apps.get_model('wells', 'well')
    code = apps.get_model('wells', 'wellorientationcode')

    vertical = code.objects.filter(well_orientation_code='VERTICAL').first()
    horizontal = code.objects.filter(well_orientation_code='HORIZONTAL').first()

    well.objects.filter(well_orientation=True).update(
        well_orientation_status=vertical)

    well.objects.filter(well_orientation=False).update(
        well_orientation_status=horizontal)


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0098_auto_20190606_1833'),
    ]

    operations = [
        migrations.RunPython(migrate_well_orientation_status, reverse),
    ]
