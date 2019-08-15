from django.db import migrations


# This can be deleted when doing next squash of migrations because it's a one time update
def migrate_drive_shoe(apps, schema_editor):
    casing = apps.get_model('wells', 'casing')
    code = apps.get_model('wells', 'driveshoecode')

    installed = code.objects.filter(drive_shoe_code='Installed').first()
    not_installed = code.objects.filter(drive_shoe_code='Not Installed').first()

    casing.objects.filter(drive_shoe=True).update(
        drive_shoe_status=installed)

    casing.objects.filter(drive_shoe=False).update(
        drive_shoe_status=not_installed)


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0095_auto_20190604_0515'),
    ]

    operations = [
        migrations.RunPython(migrate_drive_shoe, reverse),
    ]