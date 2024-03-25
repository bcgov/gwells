
from django.db import migrations

UPDATE_GWELLS_WELLS_VIEW_SQL = """
    DROP VIEW postgis_ftw.gwells_well_view;
    CREATE VIEW postgis_ftw.gwells_well_view AS
        SELECT
            well_tag_number,
            aquifer_id,
            artesian_conditions AS artesian,
            COALESCE
              (hydraulic_conductivity::text, transmissivity::text, storativity::text)
              IS NOT NULL 
              as has_hydraulic_info,
            street_address,
            identification_plate_number,
            observation_well_number,
            obs_well_status_code AS observation_well_status_code,
            ems,
            well_publication_status_code = 'Published' AS is_published,
            geom,
            EXISTS (
                SELECT 1
                FROM aquifer_parameters
                WHERE aquifer_parameters.well_tag_number = well.well_tag_number
            ) as has_aquifer_parameters
        FROM well
        WHERE geom IS NOT NULL;
        GRANT SELECT ON postgis_ftw.gwells_well_view TO ftw_reader;
"""

class Migration(migrations.Migration):
    """
    This migration adds the field 'has_aquifer_parameters' to the gwells_well_view
    under the postgis_ftw schema in the gwells database. The purpose of this field
    is to check whether there is existing pump test/aquifer parameter data for a well, and then display
    a different well icon on the well search map if this data exists.
    """
    dependencies = [
        ('wells', '0145_auto_20231127_2105'),
    ]

    operations = [
        migrations.RunSQL(
          UPDATE_GWELLS_WELLS_VIEW_SQL
        )
    ]
