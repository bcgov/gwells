import datetime
from django.db import migrations, models
from django.db.models import F
from django.utils.timezone import utc
import django.utils.timezone


def update_fields(apps, schema_editor):
    app_config = apps.get_app_config('gwells')
    app_models = app_config.get_models()
    for model in app_models:
        if hasattr(model, 'update_user'):
            try:
                model.objects.filter(update_user__isnull=True).update(update_user=F('create_user'))
            except AttributeError:
                print("skipping")


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0003_border'),
    ]

    operations = [
        migrations.RunPython(update_fields),
        migrations.AlterField(
            model_name='bedrockmaterialcode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bedrockmaterialcode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bedrockmaterialcode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='bedrockmaterialcode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bedrockmaterialcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='bedrockmaterialdescriptorcode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bedrockmaterialdescriptorcode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bedrockmaterialdescriptorcode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='bedrockmaterialdescriptorcode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bedrockmaterialdescriptorcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologycolourcode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologycolourcode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologycolourcode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lithologycolourcode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologycolourcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologydescriptioncode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologydescriptioncode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologydescriptioncode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lithologydescriptioncode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologydescriptioncode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologyhardnesscode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologyhardnesscode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologyhardnesscode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lithologyhardnesscode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologyhardnesscode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologymaterialcode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologymaterialcode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologymaterialcode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lithologymaterialcode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologymaterialcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologymoisturecode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologymoisturecode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologymoisturecode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lithologymoisturecode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologymoisturecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologystructurecode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologystructurecode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologystructurecode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lithologystructurecode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lithologystructurecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='onlinesurvey',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='provincestatecode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='provincestatecode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='provincestatecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screenassemblytypecode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenassemblytypecode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenassemblytypecode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='screenassemblytypecode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenassemblytypecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screenbottomcode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenbottomcode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenbottomcode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='screenbottomcode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenbottomcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screenintakemethodcode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenintakemethodcode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenintakemethodcode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='screenintakemethodcode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenintakemethodcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screenmaterialcode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenmaterialcode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenmaterialcode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='screenmaterialcode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenmaterialcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screenopeningcode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenopeningcode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenopeningcode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='screenopeningcode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screenopeningcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screentypecode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screentypecode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screentypecode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='screentypecode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='screentypecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='surficialmaterialcode',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='surficialmaterialcode',
            name='effective_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='surficialmaterialcode',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='surficialmaterialcode',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='surficialmaterialcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='survey',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='survey',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='survey',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
    ]
