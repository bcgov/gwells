# Generated by Django 2.2.18 on 2021-03-25 19:51

from django.db import migrations


"""
This delete statement deletes all well_subclass_code records where the well class code is null and the well subclass code is one of
'BOREHOLE', 'DOMESTIC', 'TEST_PIT'
"""
DELETE_INVALID_DUPLICATE_SUBCLASSES_SQL = """DELETE FROM well_subclass_code
WHERE well_class_code IS NULL
AND well_subclass_code in ('BOREHOLE', 'DOMESTIC', 'TEST_PIT');
"""


class Migration(migrations.Migration):
    """
        Why: delete invalid subclass codes where well class code is null (these are duplicates)
        Traceability: JIRA Ticket WATER-1634
        Clarification:
            -- These are bad
            well_subclass_code, well_class_code
            BOREHOLE          , NULL
            DOMESTIC          , NULL
            TEST_PIT          , NULL

            -- These are the good ones
            well_subclass_code, well_class_code
            BOREHOLE          , GEOTECH
            DOMESTIC          , WATR_SPPLY
            TEST_PIT          , GEOTECH

            -- This is the total of mixed up subclasses
            well_subclass_code, well_class_code
            BOREHOLE          , NULL
            DOMESTIC          , NULL
            TEST_PIT          , NULL
            BOREHOLE          , GEOTECH
            DOMESTIC          , WATR_SPPLY
            TEST_PIT          , GEOTECH

        Verification:
            Steve ran this query to ensure these NULL'ed subclasses aren't in use in production
            and this resulted in 0 rows
                select count as wells_using_bad_subclasses
                from well w
                where w.well_subclass_guid in
                (select wsc.well_subclass_guid from well_subclass_code wsc
                where wsc.well_class_code is NULL
                and wsc.well_subclass_code in (‘BOREHOLE’, ‘DOMESTIC’, ‘TEST_PIT’)
                );

        We're safe to delete these errand code table rows
    """

    dependencies = [
        ('wells', '0126_alter_well_submission_transmissivity_water_1444'),
    ]

    operations = [
        migrations.RunSQL(DELETE_INVALID_DUPLICATE_SUBCLASSES_SQL)
    ]
