import logging

from django.db import migrations, models
from django.db.models import F


logger = logging.getLogger(__name__)


def update_fields(apps, schema_editor):
    app_config = apps.get_app_config('submissions')
    app_models = app_config.get_models()
    for model in app_models:
        if hasattr(model, 'update_user'):
            try:
                model.objects.filter(update_user__isnull=True).update(update_user=F('create_user'))
            except AttributeError:
                logger.error("skipping")


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0004_auto_20190308_2348'),
    ]

    operations = [
        migrations.RunPython(update_fields),
        migrations.AlterField(
            model_name='wellactivitycode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
    ]
