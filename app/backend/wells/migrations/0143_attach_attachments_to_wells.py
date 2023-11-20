from django.db import migrations, models

def populate_wells_with_attachment_table(apps, schema_editor):
    Well = apps.get_model('wells', 'Well')
    WellAttachment = apps.get_model('wells', 'WellAttachment')

    # Get all well tag numbers that don't have an entry in WellAttachment
    well_tag_numbers_without_attachment = Well.objects.exclude(wellattachment__isnull=False).values_list('well_tag_number', flat=True)

    well_attachments_to_create = []
    
    # Iterate through each tag number and create WellAttachment instances
    for tag_number in well_tag_numbers_without_attachment:
        well_instance = Well.objects.get(well_tag_number=tag_number)
        well_attachment_instance = WellAttachment(well_tag_number=well_instance)
        well_attachments_to_create.append(well_attachment_instance)

    WellAttachment.objects.bulk_create(well_attachments_to_create)

  
class Migration(migrations.Migration):
  
  dependencies = [
    ('wells', '0142_auto_20231109_2145'),
  ]
  operations = [
    migrations.RunPython(populate_wells_with_attachment_table),
  ]
