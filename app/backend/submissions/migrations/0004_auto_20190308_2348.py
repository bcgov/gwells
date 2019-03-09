import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0003_fix_spelling_20190212_0631'),
    ]

    operations = [
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
    ]
