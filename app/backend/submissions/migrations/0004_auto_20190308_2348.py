import datetime
from django.db import migrations, models
from django.db.models import F
from django.utils.timezone import utc
import django.utils.timezone


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
        ('submissions', '0003_fix_spelling_20190212_0631'),
    ]

    operations = [
        migrations.RunPython(update_fields),
        migrations.AlterField(
            model_name='wellactivitycode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='wellactivitycode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='wellactivitycode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='wellactivitycode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='wellactivitycode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
    ]
