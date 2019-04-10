from django.db import migrations, models
from gwells.codes import CodeFixture
import os

from wells import data_migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0053_auto_20190118_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='WellPublicationStatusCode',
            fields=[
                ('create_user', models.CharField(max_length=60)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=60, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('well_publication_status_code', models.CharField(editable=False, max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('display_order', models.PositiveIntegerField()),
                ('effective_date', models.DateTimeField()),
                ('expiry_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'well_publication_status_code',
                'ordering': ['display_order', 'well_publication_status_code'],
            },
        ),
        migrations.RunPython(data_migrations.load_well_publication_status, reverse_code=data_migrations.unload_well_publication_status)
    ]
