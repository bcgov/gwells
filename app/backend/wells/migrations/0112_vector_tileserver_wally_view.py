
from django.db import migrations

CREATE_WALLY_WELLS_VIEW_SQL = """
    CREATE VIEW postgis_ftw.wally_well_view AS
        SELECT
            well_tag_number,
            geom
        FROM well;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0111_vector_tileserver_wells_view_20200430_1941'),
        ('gwells', '0007_create_postgis_ftw_schema_20200501_2146'),
    ]

    operations = [
        migrations.RunSQL(
            CREATE_WALLY_WELLS_VIEW_SQL,
        ),
    ]
