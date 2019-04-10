from django.db import migrations, models
import django.db.models.deletion
import os

from wells import data_migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0061_auto_20190215_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='AquiferLithologyCode',
            fields=[
                ('create_user', models.CharField(max_length=60)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=60, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('aquifer_lithology_code', models.CharField(db_column='aquifer_lithology_code', max_length=100, primary_key=True,
                                          serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.PositiveIntegerField()),
                ('effective_date', models.DateTimeField(blank=True, null=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Aquifer Lithology Codes',
                'db_table': 'aquifer_lithology_code',
                'ordering': ['display_order', 'aquifer_lithology_code'],
            },
        ),
        migrations.RunPython(
            data_migrations.load_aquifer_lithology_code_values,
            reverse_code=data_migrations.unload_aquifer_lithology_code_values),
        migrations.AddField(
            model_name='activitysubmission',
            name='aquifer_lithology',
            field=models.ForeignKey(blank=True, db_column='aquifer_lithology_code', null=True,
                                    on_delete=django.db.models.deletion.CASCADE, to='wells.AquiferLithologyCode',
                                    verbose_name='Aquifer Lithology'),
        ),
        migrations.AddField(
            model_name='well',
            name='aquifer_lithology',
            field=models.ForeignKey(blank=True, db_column='aquifer_lithology_code', null=True,
                                    on_delete=django.db.models.deletion.CASCADE, to='wells.AquiferLithologyCode',
                                    verbose_name='Aquifer Lithology'),
        ),
    ]
