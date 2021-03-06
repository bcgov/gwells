# Generated by Django 2.2.18 on 2021-03-31 16:01

from django.db import migrations

"""
NOTES: This ticket contains 3 migrations, just to keep things as clear as possible.
The first migration updates the views to either return null for the column well.surface_seal_length being removed
or to exclude it completely for version 2 related export and databc
2 of 3
"""

"""
This sql finds all well.surface_seal_depth = null and well.surface_seal_length not null and > 0 and assigns
    the value of well.surface_seal_length to well.surface_seal_depth.
We update the auditing rows affected with the ticket name and the date/time the migration was run!
"""
UPDATE_SURFACE_SEAL_DEPTH_SQL = """
update well
set update_user = 'WATER-1687',
    update_date = now(),
    surface_seal_depth = surface_seal_length
where surface_seal_depth is null
  and (surface_seal_length is not null and surface_seal_length > 0);
"""


class Migration(migrations.Migration):
    """
    JIRA Ticket WATER-1687
        Description:
        This ticket requires us to remove the well.surface_seal_length column.
        In order to achieve this we have several housekeeping measures to account for.
        Overall this ticket requires us to remove a column after we've assigned some of the
            data to the surface_seal_depth column, and removed our uses of this column;
            unless shared data such as export or databc, in which case we just keep
            the column but nullify the output (only v1)
        Testing:
        This ticket was tested locally, ensuring that we have some fixture data to work with
    """

    dependencies = [
        ('wells', '0129_alter_well_export_views_water_1687'),
    ]

    operations = [
        migrations.RunSQL(UPDATE_SURFACE_SEAL_DEPTH_SQL)
    ]
