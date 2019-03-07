from django.db import migrations, models
from django.db.models import F


def update_fields(apps, schema_editor):
    app_models = apps.all_models['aquifers']
    for model in app_models:
        if hasattr(model, 'update_user'):
            try:
                model.objects.filter(update_user__isnull=True).update(update_user=F('create_user'))
            except AttributeError:
                print("skipping")


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0010_auto_20190307_0123'),
    ]

    operations = [
        migrations.RunPython(update_fields),
        migrations.AlterField(
            model_name='aquifer',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='aquiferdemand',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='aquifermaterial',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='aquiferproductivity',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='aquifersubtype',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='aquifervulnerabilitycode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='qualityconcern',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
        migrations.AlterField(
            model_name='wateruse',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
    ]
