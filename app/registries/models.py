"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import uuid
import datetime
import logging
import reversion
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from reversion.models import Version
from gwells.models import AuditModel, ProvinceStateCode

User = get_user_model()
logger = logging.getLogger(__name__)


@reversion.register()
class ActivityCode(AuditModel):
    """
    Restricted Activity related to drilling wells and installing well pumps.
    """
    registries_activity_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_activity_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Activity codes'

    def __str__(self):
        return self.description


@reversion.register()
class SubactivityCode(AuditModel):
    """
    Restricted Activity Subtype related to drilling wells and installing well pumps.
    """
    registries_subactivity_code = models.CharField(
        primary_key=True,
        max_length=10,
        editable=False)
    registries_activity = models.ForeignKey(
        ActivityCode,
        db_column='registries_activity_code',
        on_delete=models.PROTECT)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_subactivity_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Subactivity codes'

    def __str__(self):
        return self.description


@reversion.register()
class CertifyingAuthorityCode(AuditModel):
    cert_auth_code = models.CharField(
        primary_key=True,
        max_length=50,
        editable=False,
        verbose_name="Certifying Authority Name")
    description = models.CharField(max_length=100, blank=True, null=True)

    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_certifying_authority_code'
        ordering = ['cert_auth_code']
        verbose_name_plural = 'Certifying Authorities'

    def __str__(self):
        return self.cert_auth_code


@reversion.register()
class AccreditedCertificateCode(AuditModel):
    acc_cert_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Accredited Certificate UUID")
    cert_auth = models.ForeignKey(
        CertifyingAuthorityCode,
        db_column='cert_auth_code',
        on_delete=models.PROTECT)
    registries_activity = models.ForeignKey(
        ActivityCode,
        db_column='registries_activity_code',
        on_delete=models.PROTECT)
    name = models.CharField(max_length=100, editable=False,
                            verbose_name="Certificate Name")
    description = models.CharField(max_length=100, blank=True, null=True)

    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_accredited_certificate_code'
        ordering = ['registries_activity', 'cert_auth']
        verbose_name_plural = 'Accredited Certificates'

    def __str__(self):
        return '%s %s %s' % (self.cert_auth, self.registries_activity, self.name)


@reversion.register()
class Organization(AuditModel):
    org_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Organization UUID")
    name = models.CharField(max_length=200)
    street_address = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, null=True,
                            blank=True, verbose_name='Town/City')
    province_state = models.ForeignKey(
        ProvinceStateCode,
        db_column='province_state_code',
        on_delete=models.PROTECT,
        verbose_name='Province/State',
        related_name="companies")
    postal_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name='Postal Code')
    main_tel = models.CharField(
        null=True, blank=True, max_length=15, verbose_name="Telephone number")
    fax_tel = models.CharField(
        null=True, blank=True, max_length=15, verbose_name="Fax number")
    website_url = models.URLField(
        null=True, blank=True, verbose_name="Website")
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)
    email = models.EmailField(
        blank=True, null=True, verbose_name="Email adddress")

    history = GenericRelation(Version)

    class Meta:
        db_table = 'registries_organization'
        ordering = ['name']
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name

    @property
    def org_verbose_name(self):
        prov = self.province_state.province_state_code

        # display either "City, Province" or just "Province"
        location = '{}, {}'.format(
            self.city, prov) if (self.city is not None and len(self.city) is not 0) else prov

        return '{} ({})'.format(self.name, location)


@reversion.register()
class Person(AuditModel):
    person_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Person UUID")
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    # As per D.A. - temporary fields to hold compliance-related details
    well_driller_orcs_no = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name='ORCS File # reference (in context of Well Driller).')
    pump_installer_orcs_no = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name='ORCS File # reference (in context of Pump Installer).')

    # contact information
    contact_tel = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        verbose_name="Contact telephone number")
    contact_cell = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        verbose_name="Contact cell number")
    contact_email = models.EmailField(
        blank=True, null=True, verbose_name="Email address")

    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    history = GenericRelation(Version)

    class Meta:
        db_table = 'registries_person'
        ordering = ['first_name', 'surname']
        verbose_name_plural = 'People'

    def __str__(self):
        return '%s %s' % (self.first_name, self.surname)

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.surname)


# deprecated - to be removed
class ContactInfo(AuditModel):
    contact_detail_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Contact At UUID")
    person = models.ForeignKey(
        Person,
        db_column='person_guid',
        on_delete=models.PROTECT,
        verbose_name="Person Reference",
        related_name="contact_info")
    contact_tel = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        verbose_name="Contact telephone number")
    contact_cell = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        verbose_name="Contact cell number")

    contact_email = models.EmailField(
        blank=True, null=True, verbose_name="Email adddress")
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_contact_detail'
        verbose_name_plural = 'Contact Information'

    def __str__(self):
        return '%s - %s, %s' % (
            self.person,
            self.contact_tel,
            self.contact_email)


class WellClassCode(AuditModel):
    """
    Class of Wells, classifying the type of wells and activities/subactivies permitted
    """
    registries_well_class_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_well_class_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Well Classes'

    def __str__(self):
        return self.registries_well_class_code


@reversion.register()
class Qualification(AuditModel):
    """
    Qualification of Well Class for a given Activity/SubActivity.
    """
    registries_well_qualification_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Qualification / Well Class UUID")
    well_class = models.ForeignKey(
        WellClassCode,
        db_column='registries_well_class_code',
        on_delete=models.PROTECT)
    subactivity = models.ForeignKey(
        SubactivityCode,
        db_column='registries_subactivity_code',
        on_delete=models.PROTECT,
        related_name="qualification_set")
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_well_qualification'
        ordering = ['subactivity', 'display_order']
        verbose_name_plural = 'Qualification codes'

    def __str__(self):
        return self.well_class.registries_well_class_code


@reversion.register()
class RegistriesRemovalReason(AuditModel):
    """
    Possible Reasons for Removal from either of the Registers
    """
    code = models.CharField(
        primary_key=True, max_length=10, editable=False, db_column='registries_removal_reason_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_removal_reason_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Registry Removal Reasons'

    def __str__(self):
        return self.description


@reversion.register(follow=('organization'))
class Register(AuditModel):

    register_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Register UUID")
    registries_activity = models.ForeignKey(
        ActivityCode,
        db_column='registries_activity_code',
        on_delete=models.PROTECT)
    person = models.ForeignKey(Person, db_column='person_guid',
                               on_delete=models.PROTECT, related_name="registrations")
    organization = models.ForeignKey(
        Organization, blank=True,
        db_column='organization_guid',
        null=True, on_delete=models.PROTECT,
        related_name="registrations")
    registration_no = models.CharField(max_length=15, blank=True, null=True)

    history = GenericRelation(Version)

    class Meta:
        db_table = 'registries_register'
        verbose_name_plural = 'Registrations'

    def __str__(self):
        return '%s - %s' % (
            self.person,
            self.registries_activity
        )


class ApplicationStatusCodeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(expired_date__isnull=True)


@reversion.register()
class ApplicationStatusCode(AuditModel):
    """
    Status of Applications for the Well Driller and Pump Installer Registries
    """
    code = models.CharField(
        primary_key=True, max_length=10, editable=False, db_column='registries_application_status_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    objects = ApplicationStatusCodeManager()

    class Meta:
        db_table = 'registries_application_status_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Application Status Codes'

    def __str__(self):
        return self.description


@reversion.register()
class ProofOfAgeCode(AuditModel):
    """
    List of documents that can be used to indentify (the age) of an application
    """
    code = models.CharField(
        primary_key=True, max_length=10, editable=False, db_column='registries_proof_of_age_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_proof_of_age_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'ProofOfAgeCodes'

    def __str__(self):
        return self.code


@reversion.register(
    follow=(
        'proof_of_age',
        'subactivity',
        'current_status',
        'primary_certificate',
        'removal_reason'
    )
)
class RegistriesApplication(AuditModel):
    """
    Application from a well driller or pump installer to be on the GWELLS Register.
    """
    application_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Register Application UUID")
    registration = models.ForeignKey(
        Register,
        db_column='register_guid',
        on_delete=models.PROTECT,
        verbose_name="Person Reference",
        related_name='applications')
    subactivity = models.ForeignKey(
        SubactivityCode,
        db_column='registries_subactivity_code',
        on_delete=models.PROTECT,
        related_name="applications")
    file_no = models.CharField(
        max_length=25, blank=True, null=True, verbose_name='ORCS File # reference.')
    proof_of_age = models.ForeignKey(
        ProofOfAgeCode,
        db_column='registries_proof_of_age_code',
        on_delete=models.PROTECT,
        verbose_name="Proof of age.",
        null=True
    )
    registrar_notes = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Registrar notes, for internal use only.')
    reason_denied = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Free form text explaining reason for denial.')

    # TODO Support multiple certificates
    primary_certificate = models.ForeignKey(
        AccreditedCertificateCode,
        blank=True,
        null=True,
        db_column='acc_cert_guid',
        on_delete=models.PROTECT,
        verbose_name="Certificate")
    primary_certificate_no = models.CharField(max_length=50)

    @property
    def display_status(self):
        # When an application is removed, it's status remains "Active", and only the removal date is
        # populated. We spare the front-end from having to know about this, by generating a human
        # readable property on this level.
        status = None
        if self.removal_date:
            status = 'Removed'
        elif self.current_status:
            status = self.current_status.description
        return status

    # TODO Should probably force this to have a default value of Pending!
    # This field should really be called "Approval Outcome"
    current_status = models.ForeignKey(
        ApplicationStatusCode,
        blank=True,
        null=True,
        db_column='registries_application_status_code',
        on_delete=models.PROTECT,
        verbose_name="Application Status Code Reference")
    application_recieved_date = models.DateField(
        blank=True, null=True)
    application_outcome_date = models.DateField(
        blank=True, null=True)
    application_outcome_notification_date = models.DateField(
        blank=True, null=True)
    # The "removal_date" refers to the date on which a classification is "removed" from the register.
    # Removing a classification may result in a person being removed from the public register as a whole,
    # only if there are no other Approved classification.
    removal_date = models.DateField(
        blank=True, null=True
    )
    removal_reason = models.ForeignKey(
        RegistriesRemovalReason,
        db_column='registries_removal_reason_code',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Removal Reason")

    history = GenericRelation(Version)

    class Meta:
        db_table = 'registries_application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return '%s : %s' % (
            self.registration,
            self.file_no)


class Register_Note(AuditModel):
    register_note_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Register Node UUID")
    registration = models.ForeignKey(
        Register,
        db_column='register_guid',
        on_delete=models.PROTECT,
        verbose_name="Register Reference",
        related_name='notes')
    notes = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name='Registrar notes, for internal use only.')

    class Meta:
        db_table = 'registries_register_note'
        verbose_name_plural = 'Registrar Notes'

    def __str__(self):
        return '%s' % (
            self.notes
        )


class OrganizationNote(AuditModel):
    org_note_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Company note UUID")
    author = models.ForeignKey(
        User,
        db_column='user_guid',
        on_delete=models.PROTECT,
        verbose_name='Author reference')
    organization = models.ForeignKey(
        Organization,
        db_column='org_guid',
        on_delete=models.PROTECT,
        verbose_name="Company reference",
        related_name="notes")
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(max_length=2000)

    class Meta:
        db_table = 'registries_organization_note'

    def __str__(self):
        return self.note[:20] + ('...' if len(self.note) > 20 else '')


class PersonNote(AuditModel):
    person_note_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Person note UUID")
    author = models.ForeignKey(
        User,
        db_column='user_guid',
        on_delete=models.PROTECT,
        verbose_name='Author reference')
    person = models.ForeignKey(
        Person,
        db_column='person_guid',
        on_delete=models.PROTECT,
        verbose_name="Person reference",
        related_name="notes")
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(max_length=2000)

    class Meta:
        db_table = 'registries_person_note'

    def __str__(self):
        return self.note[:20] + ('...' if len(self.note) > 20 else '')


"""
Tue Apr 10 10:15:34 2018 Expose DB Views to Django
"""


class vw_well_class(models.Model):

    subactivity = models.CharField(
        primary_key=True,
        max_length=10,
        editable=False)
    activity_code = models.ForeignKey(
        ActivityCode,
        db_column='registries_activity_code',
        on_delete=models.PROTECT)
    class_desc = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'vw_well_class'
        verbose_name = "Registries Well Class"
        verbose_name_plural = "Registries Well Classes"
        managed = False

    def __str__(self):
        return '%s %s %s' % (self.subactivity, self.activity_code, self.well_class)
