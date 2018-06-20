# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-08 19:34
from __future__ import unicode_literals

from django.db import migrations


def update_application_status(apps, schema_editor):
    RegistriesApplicationStatus = apps.get_model(
        'registries', 'RegistriesApplicationStatus')
    RegistriesApplication = apps.get_model(
        'registries', 'RegistriesApplication')
    for application in RegistriesApplication.objects.all():
        pending = RegistriesApplicationStatus\
            .objects.filter(application=application,
                            status__registries_application_status_code='P').first()
        if pending:
            application.current_status = pending.status
            application.application_recieved_date = pending.effective_date
        approved = RegistriesApplicationStatus\
            .objects.filter(application=application,
                            status__registries_application_status_code='A').first()
        if approved:
            application.current_status = approved.status
            application.application_outcome_date = approved.effective_date
            application.application_outcome_notification_date = approved.notified_date
        not_approved = RegistriesApplicationStatus\
            .objects.filter(application=application,
                            status__registries_application_status_code='NA').first()
        if not_approved:
            application.current_status = approved.status
            application.application_outcome_date = not_approved.effective_date
            application.application_outcome_notification_date = not_approved.notified_date

        incomplete = RegistriesApplicationStatus\
            .objects.filter(application=application,
                            status__registries_application_status_code='I').first()
        if incomplete:
            application.current_status = incomplete.status
            application.application_outcome_date = incomplete.effective_date
            application.application_outcome_notification_date = incomplete.notified_date
        application.save()


def revert(apps, schema_editor):
    RegistriesApplication = apps.get_model(
        'registries', 'RegistriesApplication')
    for application in RegistriesApplication.objects.all():
        application.current_status = None
        application.application_recieved_date = None
        application.application_outcome_date = None
        application.application_outcome_notification_date = None
        application.save()


class Migration(migrations.Migration):

    dependencies = [
        ('registries', '0005_auto_20180608_1930'),
    ]

    operations = [
        migrations.RunPython(update_application_status, revert)
    ]
