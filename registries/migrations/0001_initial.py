# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-04 23:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gwells', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityCode',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('registries_activity_code', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'registries_activity_code',
                'verbose_name_plural': 'Activity codes',
                'ordering': ['display_order', 'description'],
            },
        ),
        migrations.CreateModel(
            name='ApplicationStatusCode',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('registries_application_status_code', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'registries_application_status_code',
                'verbose_name_plural': 'Application Status Codes',
                'ordering': ['display_order', 'description'],
            },
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('contact_detail_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Contact At UUID')),
                ('contact_tel', models.CharField(blank=True, max_length=15, null=True, verbose_name='Contact telephone number')),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email adddress')),
                ('effective_date', models.DateField(default=datetime.date.today)),
                ('expired_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
            ],
            options={
                'db_table': 'registries_contact_detail',
                'verbose_name_plural': 'Contact Information',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('org_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Organization UUID')),
                ('name', models.CharField(max_length=200)),
                ('street_address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='Town/City')),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Postal Code')),
                ('main_tel', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telephone number')),
                ('fax_tel', models.CharField(blank=True, max_length=15, null=True, verbose_name='Fax number')),
                ('website_url', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('certificate_authority', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False, verbose_name='Certifying Authority for Registries Activities')),
                ('province_state', models.ForeignKey(db_column='province_state_code', on_delete=django.db.models.deletion.PROTECT, related_name='companies', to='gwells.ProvinceStateCode', verbose_name='Province/State')),
            ],
            options={
                'db_table': 'registries_organization',
                'verbose_name_plural': 'Organizations',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('person_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Person UUID')),
                ('first_name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='People', to='registries.Organization')),
            ],
            options={
                'db_table': 'registries_person',
                'verbose_name_plural': 'People',
                'ordering': ['first_name', 'surname'],
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('registries_well_qualification_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Qualification / Well Class UUID')),
                ('display_order', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'registries_well_qualification',
                'verbose_name_plural': 'Qualification codes',
                'ordering': ['subactivity', 'display_order'],
            },
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('register_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Register UUID')),
                ('registration_no', models.CharField(blank=True, max_length=15, null=True)),
                ('registration_date', models.DateField(blank=True, null=True)),
                ('register_removal_date', models.DateField(blank=True, null=True, verbose_name='Date of Removal from Register')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='registrations', to='registries.Person')),
            ],
            options={
                'db_table': 'registries_register',
                'verbose_name_plural': 'Registrations',
            },
        ),
        migrations.CreateModel(
            name='RegistriesApplication',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('application_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Register Application UUID')),
                ('file_no', models.CharField(blank=True, max_length=25, null=True, verbose_name='ORCS File # reference.')),
                ('over19_ind', models.BooleanField(default=True)),
                ('registrar_notes', models.CharField(blank=True, max_length=255, null=True, verbose_name='Registrar notes, for internal use only.')),
                ('reason_denied', models.CharField(blank=True, max_length=255, null=True, verbose_name='Free form text explaining reason for denial.')),
                ('primary_certificate_no', models.CharField(max_length=50)),
                ('primary_certificate_authority', models.ForeignKey(blank=True, db_column='certifying_org_guid', null=True, on_delete=django.db.models.deletion.PROTECT, to='registries.Organization', verbose_name='Certifying Organization')),
                ('registration', models.ForeignKey(db_column='register_guid', on_delete=django.db.models.deletion.PROTECT, related_name='applications', to='registries.Register', verbose_name='Person Reference')),
            ],
            options={
                'db_table': 'registries_application',
                'verbose_name_plural': 'Applications',
            },
        ),
        migrations.CreateModel(
            name='RegistriesApplicationStatus',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('application_status_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Register Application Status UUID')),
                ('notified_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('effective_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('expired_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('application', models.ForeignKey(db_column='application_guid', on_delete=django.db.models.deletion.PROTECT, related_name='status_set', to='registries.RegistriesApplication', verbose_name='Application Reference')),
                ('status', models.ForeignKey(db_column='registries_application_status_code', on_delete=django.db.models.deletion.PROTECT, to='registries.ApplicationStatusCode', verbose_name='Application Status Code Reference')),
            ],
            options={
                'db_table': 'registries_application_status',
                'verbose_name_plural': 'Application status',
                'ordering': ['application', 'effective_date'],
            },
        ),
        migrations.CreateModel(
            name='RegistriesRemovalReason',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('registries_removal_reason_code', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'registries_removal_reason_code',
                'verbose_name_plural': 'Registry Removal Reasons',
                'ordering': ['display_order', 'description'],
            },
        ),
        migrations.CreateModel(
            name='RegistriesStatusCode',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('registries_status_code', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'registries_status_code',
                'verbose_name_plural': 'Registry Status Codes',
                'ordering': ['display_order', 'description'],
            },
        ),
        migrations.CreateModel(
            name='SubactivityCode',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('registries_subactivity_code', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.PositiveIntegerField()),
                ('registries_activity', models.ForeignKey(db_column='registries_activity_code', on_delete=django.db.models.deletion.PROTECT, to='registries.ActivityCode')),
            ],
            options={
                'db_table': 'registries_subactivity_code',
                'verbose_name_plural': 'Subactivity codes',
                'ordering': ['display_order', 'description'],
            },
        ),
        migrations.CreateModel(
            name='WellClassCode',
            fields=[
                ('create_user', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=30, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('registries_well_class_code', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'registries_well_class_code',
                'verbose_name_plural': 'Well Classes',
                'ordering': ['display_order', 'description'],
            },
        ),
        migrations.AddField(
            model_name='registriesapplication',
            name='subactivity',
            field=models.ForeignKey(db_column='registries_subactivity_code', on_delete=django.db.models.deletion.PROTECT, related_name='applications', to='registries.SubactivityCode'),
        ),
        migrations.AddField(
            model_name='register',
            name='register_removal_reason',
            field=models.ForeignKey(blank=True, db_column='registries_removal_reason_code', null=True, on_delete=django.db.models.deletion.PROTECT, to='registries.RegistriesRemovalReason', verbose_name='Removal Reason'),
        ),
        migrations.AddField(
            model_name='register',
            name='registries_activity',
            field=models.ForeignKey(db_column='registries_activity_code', on_delete=django.db.models.deletion.PROTECT, to='registries.ActivityCode'),
        ),
        migrations.AddField(
            model_name='register',
            name='status',
            field=models.ForeignKey(db_column='registries_status_code', default='P', on_delete=django.db.models.deletion.PROTECT, to='registries.RegistriesStatusCode', verbose_name='Register Entry Status'),
        ),
        migrations.AddField(
            model_name='qualification',
            name='subactivity',
            field=models.ForeignKey(db_column='registries_subactivity_code', on_delete=django.db.models.deletion.PROTECT, related_name='Qualification', to='registries.SubactivityCode'),
        ),
        migrations.AddField(
            model_name='qualification',
            name='well_class',
            field=models.ForeignKey(db_column='registries_well_class_code', on_delete=django.db.models.deletion.PROTECT, related_name='Qualification', to='registries.WellClassCode'),
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='person',
            field=models.ForeignKey(db_column='person_guid', on_delete=django.db.models.deletion.PROTECT, related_name='contact_info', to='registries.Person', verbose_name='Person Reference'),
        ),
    ]
