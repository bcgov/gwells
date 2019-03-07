from django.db import migrations, models
from django.db.models import F


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
        ('gwells', '0004_auto_20190307_0123'),
    ]

    operations = [
        migrations.RunPython(update_fields),
        migrations.AlterField(
            model_name='bedrockmaterialcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='bedrockmaterialdescriptorcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologycolourcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologydescriptioncode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologyhardnesscode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologymaterialcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologymoisturecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='lithologystructurecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='provincestatecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screenassemblytypecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screenbottomcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screenintakemethodcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screenmaterialcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screenopeningcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='screentypecode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='surficialmaterialcode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='survey',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
    ]
