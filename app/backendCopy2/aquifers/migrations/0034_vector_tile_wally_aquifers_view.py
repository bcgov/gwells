
from django.db import migrations

CREATE_WALLY_AQUIFER_VIEW_SQL = """
    CREATE VIEW postgis_ftw.wally_aquifer_view AS
        SELECT
            aquifer_id,
            geom
        FROM aquifer;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0033_vector_tile_aquifers_view_20200430_1941'),
        ('gwells', '0007_create_postgis_ftw_schema_20200501_2146'),
    ]

    operations = [
        migrations.RunSQL(
            CREATE_WALLY_AQUIFER_VIEW_SQL,
        ),
    ]
