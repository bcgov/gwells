from django.db import migrations, models
import django.db.models.deletion
from gwells.codes import CodeFixture
import os


def code_fixture():
    fixture = '0010_aquifer_lithology_codes.json'
    fixture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), fixture)

    return CodeFixture(fixture_path)


class Migration(migrations.Migration):

    dependencies = [
        ('aquifers', '0009_auto_20190108_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='AquiferLithologyCode',
            fields=[
                ('create_user', models.CharField(max_length=60)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=60, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(db_column='aquifer_lithology_code', max_length=100, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.PositiveIntegerField()),
                ('effective_date', models.DateTimeField(blank=True, null=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Aquifer Lithology Codes',
                'db_table': 'aquifer_lithology_code',
                'ordering': ['display_order', 'code'],
            },
        ),
        migrations.RunPython(code_fixture().load_fixture, reverse_code=code_fixture().unload_fixture),
    ]
