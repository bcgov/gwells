from django.db import migrations

UPDATE_WELL_CLASS_DESCRIPTION = f"""
    UPDATE well_class_code
    SET description = 'Closed Loop Geoexchange'
    WHERE well_class_code = 'CLS_LP_GEO';
"""

class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0150_remove_well_export_columns'),
    ]

    operations = [
        migrations.RunSQL(UPDATE_WELL_CLASS_DESCRIPTION)
    ]
