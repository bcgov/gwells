# Generated by Django 2.1.7 on 2019-03-09 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0004_auto_20190308_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wellactivitycode',
            name='update_user',
            field=models.CharField(default='DATALOAD_USER', max_length=60),
        ),
    ]
