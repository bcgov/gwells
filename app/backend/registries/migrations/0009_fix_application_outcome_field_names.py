# Generated migration to fix corrupted field names in RegistriesApplication model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registries', '0008_organization_regional_areas'),
    ]

    operations = [
        # Rename mispelt columns in the database to match the intended field names
        migrations.RunSQL(
            sql='ALTER TABLE registries_application RENAME COLUMN "application_otimezone.utcome_date" TO application_outcome_date;',
            reverse_sql='ALTER TABLE registries_application RENAME COLUMN application_outcome_date TO "application_otimezone.utcome_date";'
        ),
        migrations.RunSQL(
            sql='ALTER TABLE registries_application RENAME COLUMN "application_otimezone.utcome_notification_date" TO application_outcome_notification_date;',
            reverse_sql='ALTER TABLE registries_application RENAME COLUMN application_outcome_notification_date TO "application_otimezone.utcome_notification_date";'
        ),
        # Update the field definitions in the Django ORM to match the renamed columns
        migrations.AlterField(
            model_name='registriesapplication',
            name='application_outcome_date',
            field=models.DateField(blank=True, null=True, db_comment='Date that the comptroller decided if the application for registration of a well driller or well pump installer was approved or denied.'),
        ),
        migrations.AlterField(
            model_name='registriesapplication',
            name='application_outcome_notification_date',
            field=models.DateField(blank=True, null=True, db_comment='Date that the individual was notified of the outcome of their application for registration for well driller or well pump installer.'),
        ),
    ]
