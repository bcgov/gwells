# Generated by Django 2.2.18 on 2021-03-31 16:19

from django.db import migrations, models

"""
NOTES: This ticket contains 3 migrations, just to keep things as clear as possible.
The first migration updates the views to either return null for the column well.surface_seal_length being removed
or to exclude it completely for version 2 related export and databc
3 of 3
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
        This ticket was tested locally, ensuring that the column is removed from the database
    """
    dependencies = [
        ('wells', '0130_update_surface_seal_depth_water_1687'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='well',
            name='surface_seal_length'
        ),
    ]
