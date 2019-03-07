from django.db import migrations, models
from django.db.models import F


def update_fields(apps, schema_editor):
    app_config = apps.get_app_config('submissions')
    app_models = app_config.get_models()
    for model in app_models:
        if hasattr(model, 'update_user'):
            try:
                model.objects.filter(update_user__isnull=True).update(update_user=F('create_user'))
            except AttributeError:
                print("skipping")


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0004_auto_20190307_0123'),
    ]

    operations = [
        migrations.RunPython(update_fields),
        migrations.AlterField(
            model_name='wellactivitycode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
    ]
