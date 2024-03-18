from django.db import migrations
import csv
import zipfile
import os

def import_well_data(apps, schema_editor):
    Well = apps.get_model('wells', 'Well')
    well_count = Well.objects.count()
    dev_threshold = 500
    
    if well_count < dev_threshold:
        print("Skipping qaqc data migration as it seems to be a non-production environment.")
        return

    process_wells(Well, get_well_data())

def get_well_data():
    migration_dir = os.path.dirname(__file__)
    with zipfile.ZipFile(os.path.join(migration_dir, '../fixtures/qaqc_well_data.zip'), 'r') as zip_file:
        csv_filename = zip_file.namelist()[0]
        with zip_file.open(csv_filename, 'r') as csvfile:
            return csv.DictReader(csvfile.read().decode('utf-8').splitlines())

def process_wells(Well, reader):
    batch_size = 1000  # Adjust batch size if there are memory issues
    wells_to_update = []
    count = 0

    for row in reader:
        try:
            well_instance = Well.objects.get(well_tag_number=row['well_tag_number'])
            update_well_attributes(well_instance, row)
            wells_to_update.append(well_instance)
            count += 1

            # Process in batches of batch_size
            if count % batch_size == 0:
                Well.objects.bulk_update(wells_to_update, ['geocode_distance', 'distance_to_pid', 'score_address', 
                                                           'score_city', 'cross_referenced', 'cross_referenced_date', 
                                                           'cross_referenced_by', 'natural_resource_region'])
                wells_to_update = []  # Reset the list after updating

        except Well.DoesNotExist:
            print(f"Well with tag number {row['well_tag_number']} not found.")
        except ValueError as e:
            print(f"Error processing well {row['well_tag_number']}: {e}")

    # Update any remaining wells in the list
    if wells_to_update:
        Well.objects.bulk_update(wells_to_update, ['geocode_distance', 'distance_to_pid', 'score_address',
                                                   'score_city', 'cross_referenced', 'cross_referenced_date',
                                                   'cross_referenced', 'natural_resource_region'])

def update_well_attributes(well, row):
    fields_to_update = ['distance_geocode', 'distance_to_matching_pid', 'score_address', 'score_city']
    for field in fields_to_update:
        setattr(well, 'geocode_distance' if field == 'distance_geocode' else field, 
                float(row[field]) if row[field] else None)

    well.cross_referenced = row['xref_ind'] == 'True'
    if well.cross_referenced:
        well.cross_referenced_date = well.update_date
        well.cross_referenced_by = well.update_user
    well.natural_resource_region = row['nr_region_name'] if row['nr_region_name'] else None

class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0147_auto_20240105_qaqc'),
    ]

    operations = [
        migrations.RunPython(import_well_data, reverse_code=migrations.RunPython.noop),
    ]
