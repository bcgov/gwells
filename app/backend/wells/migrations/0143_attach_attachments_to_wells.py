from django.db import migrations, models

def populate_wells_with_attachment_table(apps, schema_editor):
  A = apps.get_model('wells', 'Well')
  B = apps.get_model('wells', 'WellAttachment')

  for a_instance in A.objects.all():
    B.objects.create(well_tag_number=a_instance)
  
class Migration(migrations.Migration):
  
  dependencies = [
    ('wells', '0142_auto_20231109_2145'),
  ]
  operations = [
    migrations.RunPython(populate_wells_with_attachment_table),
  ]
