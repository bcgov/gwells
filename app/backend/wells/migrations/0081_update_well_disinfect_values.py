from django.db import migrations


# This can be deleted when doing next squash of migrations because it's a one time update
def migrate_well_disinfected(apps, schema_editor):
    well = apps.get_model('wells', 'well')
    code = apps.get_model('wells', 'welldisinfectedcode')

    disinfected = code.objects.filter(well_disinfected_code='Disinfected').first()
    not_disinfected = code.objects.filter(well_disinfected_code='Not Disinfected').first()
    unknown = code.objects.filter(well_disinfected_code='Unknown').first()

    well.objects.filter(well_disinfected=True).update(
        well_disinfected_status=disinfected)

    well.objects.filter(well_disinfected=False).update(
        well_disinfected_status=not_disinfected)

    well.objects.filter(well_disinfected__isnull=True).update(
        well_disinfected_status=unknown)


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0080_add_well_disinfect_status'),
    ]

    operations = [
        migrations.RunPython(migrate_well_disinfected, reverse),
    ]
