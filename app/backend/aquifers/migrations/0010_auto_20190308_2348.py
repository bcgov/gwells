import datetime
from django.db import migrations, models
from django.db.models import F
from django.utils.timezone import utc
import django.utils.timezone


def update_fields(apps, schema_editor):
    app_config = apps.get_app_config('aquifers')
    app_models = app_config.get_models()
    for model in app_models:
        if hasattr(model, 'update_user'):
            try:
                model.objects.filter(update_user__isnull=True).update(update_user=F('create_user'))
            except AttributeError:
                print("skipping")


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0009_auto_20190108_1925'),
    ]

    operations = [
        migrations.RunPython(update_fields),
        migrations.AlterField(
            model_name='aquifer',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquifer',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquiferdemand',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquiferdemand',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquiferdemand',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='aquiferdemand',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquifermaterial',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquifermaterial',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquifermaterial',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='aquifermaterial',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquiferproductivity',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquiferproductivity',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquiferproductivity',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='aquiferproductivity',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquifersubtype',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquifersubtype',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquifersubtype',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='aquifersubtype',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquifervulnerabilitycode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquifervulnerabilitycode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aquifervulnerabilitycode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='aquifervulnerabilitycode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='qualityconcern',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='qualityconcern',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='qualityconcern',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='qualityconcern',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='wateruse',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='wateruse',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='wateruse',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='wateruse',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
