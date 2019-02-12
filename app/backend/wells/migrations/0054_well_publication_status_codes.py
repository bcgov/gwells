from django.db import migrations, models
from gwells.codes import CodeFixture
import os


def code_fixture():
    fixture = '0054_well_publication_status_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0053_auto_20190118_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='WellPublicationStatusCode',
            fields=[
                ('create_user', models.CharField(max_length=60)),
                ('create_date', models.DateTimeField()),
                ('update_user', models.CharField(max_length=60)),
                ('update_date', models.DateTimeField()),
                ('well_publication_status_code', models.CharField(editable=False, max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('display_order', models.PositiveIntegerField()),
                ('effective_date', models.DateTimeField()),
                ('expiry_date', models.DateTimeField(default='infinity')),
            ],
            options={
                'db_table': 'well_publication_status_code',
                'ordering': ['display_order', 'well_publication_status_code'],
            },
        ),
        migrations.RunPython(code_fixture().load_fixture, reverse_code=code_fixture().unload_fixture)
    ]
