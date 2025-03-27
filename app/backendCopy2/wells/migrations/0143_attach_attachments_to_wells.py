from django.db import migrations, models

from django.db.models import Count

def populate_wells_with_attachment_table(apps, schema_editor):
    Well = apps.get_model('wells', 'Well')
    WellAttachment = apps.get_model('wells', 'WellAttachment')

    # Batch processing: Set a limit for fetching wells without attachments
    batch_size = 100
    offset = 0

    while True:
        well_tag_numbers_without_attachment = (
            Well.objects
            .annotate(attachment_count=Count('wellattachment'))
            .filter(attachment_count=0)
            .values_list('well_tag_number', flat=True)[offset:offset + batch_size]
        )

        if not well_tag_numbers_without_attachment:
            break

        well_attachments_to_create = []

        # Iterate through each tag number and create WellAttachment instances
        for tag_number in well_tag_numbers_without_attachment:
            well_instance = Well.objects.get(well_tag_number=tag_number)
            well_attachment_instance = WellAttachment(well_tag_number=well_instance)
            well_attachments_to_create.append(well_attachment_instance)

        # Bulk create for the current batch
        WellAttachment.objects.bulk_create(well_attachments_to_create)

        # Move to the next batch
        offset += batch_size

  
class Migration(migrations.Migration):
  
  dependencies = [
    ('wells', '0142_auto_20231109_2145'),
  ]
  operations = [
    migrations.RunPython(populate_wells_with_attachment_table),
  ]
