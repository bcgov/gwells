# Generated by Django 2.2.1 on 2019-05-09 16:02
import logging

from django.db import migrations
from django.db.models import Q


logger = logging.getLogger(__name__)


def update_record(related_record, parent_record):
    if not related_record.update_user:
        related_record.update_user = parent_record.update_user
    if not related_record.create_user:
        related_record.create_user = parent_record.create_user


def fix_idir(apps, schema_editor):
    LithologyDescription = apps.get_model('wells', 'LithologyDescription')
    Casing = apps.get_model('wells', 'Casing')
    Screen = apps.get_model('wells', 'Screen')
    LinerPerforation = apps.get_model('wells', 'LinerPerforation')
    DecommissionDescription = apps.get_model('wells', 'DecommissionDescription')

    models = [LithologyDescription, Casing, Screen, LinerPerforation, DecommissionDescription]

    for model in models:
        logger.info('Fixing bad idir info on {}'.format(model))
        well_count = 0
        submission_count = 0
        for related_record in model.objects.filter(Q(update_user='') | Q(create_user='')):
            if related_record.activity_submission:
                update_record(related_record, related_record.activity_submission)
                submission_count += 1
            elif related_record.well:
                update_record(related_record, related_record.well)
                well_count += 1
            related_record.save()
        logger.info('{} well linked records updated'.format(well_count))
        logger.info('{} submission linked records updated'.format(submission_count))


def reverse(apps, schema_editor):
    # There's no going back!
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0079_auto_20190506_1959'),
    ]

    operations = [
        migrations.RunPython(fix_idir, reverse),
    ]