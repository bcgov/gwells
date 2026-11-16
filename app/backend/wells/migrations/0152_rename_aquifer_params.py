from django.db import migrations, models

CREATE_EXPORT_AQUIFER_PARAMETERS_VIEW_V1_SQL = """
DROP VIEW IF EXISTS export_aquifer_parameters_v1_view;
CREATE OR REPLACE view export_aquifer_parameters_v1_view as
SELECT
  ap.well_tag_number,
  ap.testing_number,
  ap.start_date_pumping_test,
  tt.description AS pumping_test_description,
  ap.test_duration AS test_duration_min,
  be.description AS boundary_effect,
  ap.storativity,
  ap.transmissivity AS "transmissivity_m^2/day",
  ap.hydraulic_conductivity AS "hydraulic_conductivity_m/day",
  ap.specific_yield,
  ap.specific_capacity AS "specific_capacity_L/s/m",
  am.description AS analysis_method,
  ap.comments
FROM
  aquifer_parameters AS ap
LEFT JOIN
  pumping_test_description_code AS tt ON ap.pumping_test_description_code = tt.pumping_test_description_code
LEFT JOIN
  boundary_effect_code AS be ON ap.boundary_effect_code = be.boundary_effect_code
LEFT JOIN
  analysis_method_code AS am ON ap.analysis_method_code = am.analysis_method_code
INNER JOIN
  well ON ap.well_tag_number = well.well_tag_number
WHERE
  well.well_publication_status_code = 'Published' OR well.well_publication_status_code IS NULL
ORDER BY
  ap.testing_number;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0150_remove_well_export_columns'),
    ]

    operations = [
        migrations.RunSQL(CREATE_EXPORT_AQUIFER_PARAMETERS_VIEW_V1_SQL),
    ]
