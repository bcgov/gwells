import logging

from django.db import migrations, models
from django.db.models import F

from aquifers import data_migrations


logger = logging.getLogger(__name__)


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0010_auto_20190308_2348'),
    ]

    operations = [
        migrations.RunPython(
            data_migrations.update_user_fields,
            reverse_code=data_migrations.reverse_update_user_fields
        ),
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
