import logging

from django.db import migrations, models
from django.db.models import F


logger = logging.getLogger(__name__)


def update_fields(apps, schema_editor):
    app_config = apps.get_app_config('registries')
    app_models = app_config.get_models()
    for model in app_models:
        if hasattr(model, 'update_user'):
            try:
                model.objects.filter(update_user__isnull=True).update(update_user=F('create_user'))
            except AttributeError:
                logger.error("skipping")


class Migration(migrations.Migration):

    dependencies = [
        ('registries', '0014_auto_20190308_2348'),
    ]

    operations = [
        migrations.RunPython(update_fields),
        migrations.AlterField(
            model_name='accreditedcertificatecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='activitycode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='applicationstatuscode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='certifyingauthoritycode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='organization',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='organizationnote',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='person',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='personnote',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='proofofagecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='register',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='register_note',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='registriesapplication',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='registriesremovalreason',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='subactivitycode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='wellclasscode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
    ]
