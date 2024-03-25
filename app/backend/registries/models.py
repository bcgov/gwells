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
import logging
import reversion
from reversion.models import Version

from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation

from gwells.models import AuditModel, ProvinceStateCode, CodeTableModel, BasicCodeTableModel

User = get_user_model()
logger = logging.getLogger(__name__)


@reversion.register()
class ActivityCode(CodeTableModel):
    """
    Restricted Activity related to drilling wells and installing well pumps.
    """
    registries_activity_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('code for valid activities that a registered individual can carry out, i.e. PUMP,'
                    ' DRILL'))
    description = models.CharField(
        max_length=100,
        db_comment=('Descriptions of valid activities that a registered individual can carry out, i.e. Pump '
                    'Installer, Well Driller.'))

    class Meta:
        db_table = 'registries_activity_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Activity codes'

    db_table_comment = ('Describes the registered individual\'s allowable activity on a well; i.e. Well'
                        ' Driller, or Pump Installer.')

    def __str__(self):
        return self.description


@reversion.register()
class SubactivityCode(CodeTableModel):
    """
    Restricted Activity Subtype related to drilling wells and installing well pumps.
    """
    registries_subactivity_code = models.CharField(
        primary_key=True,
        max_length=10,
        editable=False,
        db_comment=('Code for valid sub activities that a registered individual can carry out under each'
                    ' type of activity. E.g. GEOTECH, GEOXCHG'))
    registries_activity = models.ForeignKey(
        ActivityCode,
        db_column='registries_activity_code',
        on_delete=models.PROTECT,
        db_comment=('Code for valid activities that a registered individual can carry out, i.e. PUMP,'
                    ' DRILL'))
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'registries_subactivity_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Subactivity codes'

    db_table_comment = ('Describes valid sub activities that a registered individual can carry out under'
                        ' each type of activity. E.g. Water Well Driller, Geoexchange Driller.')

    def __str__(self):
        return self.description


@reversion.register()
class CertifyingAuthorityCode(BasicCodeTableModel):
    cert_auth_code = models.CharField(
        primary_key=True,
        max_length=50,
        editable=False,
        verbose_name="Certifying Authority Name")
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'registries_certifying_authority_code'
        ordering = ['cert_auth_code']
        verbose_name_plural = 'Certifying Authorities'

    db_table_comment = 'Placeholder table comment.'

    def __str__(self):
        return self.cert_auth_code


@reversion.register()
class AccreditedCertificateCode(BasicCodeTableModel):
    acc_cert_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Accredited Certificate UUID",
        db_comment='Unique surrogate identifier for the registries_accredited_certificate_code')
    cert_auth = models.ForeignKey(
        CertifyingAuthorityCode,
        db_column='cert_auth_code',
        on_delete=models.PROTECT)
    registries_activity = models.ForeignKey(
        ActivityCode,
        db_column='registries_activity_code',
        on_delete=models.PROTECT,
        db_comment=('Code for valid activities that a registered individual can carry out, i.e. PUMP,'
                    ' DRILL'))
    name = models.CharField(max_length=100, editable=False,
                            verbose_name="Certificate Name",
                            db_comment=('Certifications that are recognized by British Columbia for the '
                                        'purposes of registering an individual as a well pump installer or '
                                        'well driller. These certifications determine what type of well the '
                                        'individual is allowed to construct/alter/decomission. Individuals '
                                        'that were registered prior to 2006 did not have to provide a '
                                        'certification and as such they have been Grand-parented in which '
                                        'means they can construct/alter/decomission any type of well. E.g. '
                                        'Geoexchange Driller Certificate, Ground Water Pump Technician '
                                        'Certificate, Grand-parent.'))
    description = models.CharField(
        max_length=100, blank=True, null=True,
        db_comment=('Descriptions of valid activities that a registered individual can carry out, i.e. '
                    'Pump Installer, Well Driller.'))

    class Meta:
        db_table = 'registries_accredited_certificate_code'
        ordering = ['registries_activity', 'cert_auth']
        verbose_name_plural = 'Accredited Certificates'

    db_table_comment = ('Describes the valid qualifications or certificates (prescribed qualifications) as'
                        ' issued by the certifying authority; used to register a well driller or well pump'
                        ' installer. Individuals registered prior to 2006 may have qualified under the'
                        ' grandparenting provision. E.g., Water Well Driller Certificate issued by BC to'
                        ' register an applicant as a Well Driller.')

    def __str__(self):
        return '%s %s %s' % (self.cert_auth, self.registries_activity, self.name)


@reversion.register()
class Organization(AuditModel):
    org_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Organization UUID")
    name = models.CharField(
        max_length=200,
        db_comment='Company\'s Doing Business As name.')
    street_address = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Street Address',
        db_comment='Street address used for mailing address for the company.')
    city = models.CharField(
        max_length=50, null=True,
        blank=True, verbose_name='Town/City',
        db_comment='City used for mailing address for the company.')
    province_state = models.ForeignKey(
        ProvinceStateCode,
        db_column='province_state_code',
        on_delete=models.PROTECT,
        verbose_name='Province/State',
        related_name='companies',
        db_comment='Province or state used for the mailing address for the company')
    postal_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name='Postal Code',
        db_comment='Postal code used for mailing address for the company')
    main_tel = models.CharField(
        null=True, blank=True, max_length=15, verbose_name='Telephone number',
        db_comment='Telephone number used to contact the company')
    fax_tel = models.CharField(
        null=True, blank=True, max_length=15, verbose_name='Fax number',
        db_comment='Fax number used to contact the company')
    website_url = models.URLField(
        null=True, blank=True, verbose_name='Website',
        db_comment='The web address associated with the company')
    effective_date = models.DateTimeField(
        default=timezone.now, null=False,
        db_comment='The date the the organization record became available for use.')
    expiry_date = models.DateTimeField(
        default=timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone()), null=False,
        db_comment=('The date that the organization record was soft deleted (expired) by the staff.'
                    ' Common reasons for deleting the record would be to remove duplicates, and'
                    ' erroneous entries there by making these organizations unavailable for use.'))
    email = models.EmailField(
        blank=True, null=True, verbose_name="Email adddress",
        db_comment=('The email address for a company, this is different from the email for the individual '
                    'who is a registered driller or pump installer.'))
    geom = models.PointField(
        blank=True, null=True, 
        srid=4326,
        db_comment='Geo-referenced location of the address')
    regional_areas = models.ManyToManyField(
        'RegionalArea',
        related_name='organizations',
        blank=True,
        db_comment='The regional areas where the organization operates.')

    history = GenericRelation(Version)

    class Meta:
        db_table = 'registries_organization'
        ordering = ['name']
        verbose_name_plural = 'Organizations'

    db_table_comment = 'Placeholder table comment.'

    def __str__(self):
        return self.name

    @property
    def org_verbose_name(self):
        prov = self.province_state.province_state_code

        # display either "City, Province" or just "Province"
        location = '{}, {}'.format(
            self.city, prov) if (self.city is not None and len(self.city) is not 0) else prov

        return '{} ({})'.format(self.name, location)

    @property
    def mailing_address(self):
        address = [
            self.street_address,
            self.city,
            self.province_state_id,
            self.postal_code,
        ]
        return ", ".join([part for part in address if part])

    @property
    def latitude(self):
        if self.geom:
            return self.geom.y
        else:
            return None

    @property
    def longitude(self):
        if self.geom:
            return self.geom.x
        else:
            return None


@reversion.register()
class Person(AuditModel):
    person_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Person UUID")
    first_name = models.CharField(
        max_length=100,
        db_comment=('Legal first name of the well driller or well pump installer who has applied and/or is '
                    'registered with the province.'))
    surname = models.CharField(
        max_length=100,
        db_comment=('Legal last name of the well driller or well pump installer who has applied and/or is '
                    'registered with the province.'))

    # As per D.A. - temporary fields to hold compliance-related details
    well_driller_orcs_no = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name='ORCS File # reference (in context of Well Driller).',
        db_comment=('Well driller\'s unique filing number used in the BC government Operational Records '
                    'Classification Systems (ORCS) filing system. Each person has an ORCS number when a file '
                    'is started with their correspondence, usually with the application for being '
                    'registered. E.g. 3800-25/PUMP DRI W. The standard format for this number is '
                    '3800-25/DRI {first 4 characters of last name} {initial of first name}.'))
    pump_installer_orcs_no = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name='ORCS File # reference (in context of Pump Installer).',
        db_comment=('Well pump installer\'s unique filing number used in the BC government Operational '
                    'Records Classification Systems (ORCS) filing system. Each person has an ORCS number '
                    'when a file is started with their correspondence, usually with the application for '
                    'being registered. Each person can have a unique ORCS number as a well pump installer '
                    'and as a well driller. E.g. 3800-25/PUMP PRIC W. The standard format for this number '
                    'is 3800-25/PUMP {first 4 characters of last name} {initial of first name}.'))
    # contact information
    contact_tel = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        verbose_name='Contact telephone number',
        db_comment=('Land line area code and 7 digit phone number provided by the well driller or well pump '
                    'installer where they can be contacted.'))
    contact_cell = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        verbose_name='Contact cell number',
        db_comment=('Cell phone area code and 7 digit number provided by the well driller or well pump '
                    'installer where they can be contacted.'))
    contact_email = models.EmailField(
        blank=True, null=True, verbose_name='Email address',
        db_comment='Email address for the well driller or well pump installer.')

    effective_date = models.DateTimeField(
        default=timezone.now, null=False,
        db_comment='The date when the registries person record became available for use.')
    expiry_date = models.DateTimeField(
        default=timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone()), null=False,
        db_comment='The date and time after which the record is no longer valid and should not be used.')

    history = GenericRelation(Version)

    class Meta:
        db_table = 'registries_person'
        ordering = ['first_name', 'surname']
        verbose_name_plural = 'People'

    db_table_comment = 'Placeholder table comment.'

    def __str__(self):
        return '%s %s' % (self.first_name, self.surname)

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.surname)


class WellClassCode(CodeTableModel):
    """
    Class of Wells, classifying the type of wells and activities/subactivies permitted
    """
    registries_well_class_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('Code for the type of well that a driller is allowed to construct, alter, or'
                    ' decommission based on the driller\'s classification e.g. CLOS, DEWAT, GEO'))
    description = models.CharField(
        max_length=100,
        db_comment=('Description for the registries_class_of_well_code that a driller is allowed to '
                    'construct/alter/decommission based on the driller\'s classification e.g. Closed loop '
                    'geoexchange well, Dewatering well, Geotechnical well.'))

    class Meta:
        db_table = 'registries_well_class_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Well Classes'

    db_table_comment = 'Placeholder table comment.'

    def __str__(self):
        return self.registries_well_class_code


@reversion.register()
class Qualification(CodeTableModel):
    """
    Qualification of Well Class for a given Activity/SubActivity.
    """
    registries_well_qualification_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Qualification / Well Class UUID',
        db_comment='The unique identifier for each record.')
    well_class = models.ForeignKey(
        WellClassCode,
        db_column='registries_well_class_code',
        on_delete=models.PROTECT,
        db_comment=('Code for the type of well that a driller is allowed to construct, alter, or'
                    ' decommission based on the driller\'s classification e.g. CLOS, DEWAT, GEO'))
    subactivity = models.ForeignKey(
        SubactivityCode,
        db_column='registries_subactivity_code',
        on_delete=models.PROTECT,
        related_name="qualification_set")

    class Meta:
        db_table = 'registries_well_qualification'
        ordering = ['subactivity', 'display_order']
        verbose_name_plural = 'Qualification codes'

    db_table_comment = ('A cross reference table maintaining the list of valid combinations of'
                        ' registries_subactivity_code and registries_well_class_code.')

    def __str__(self):
        return self.well_class.registries_well_class_code


@reversion.register()
class RegistriesRemovalReason(CodeTableModel):
    """
    Possible Reasons for Removal from either of the Registers
    """
    code = models.CharField(
        primary_key=True, max_length=10, editable=False, db_column='registries_removal_reason_code',
        db_comment=('Reason why a well driller or well pump installer was removed from the registry '
                    'i.e. NMEET, FAILTM, NLACT'))
    description = models.CharField(
        max_length=100,
        db_comment='Description of code e.g. NMEET = Fails to meet a requirement for registration.')

    class Meta:
        db_table = 'registries_removal_reason_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Registry Removal Reasons'

    db_table_comment = ('Describes reasons why a well driller or well pump installer was removed from the'
                        ' registry i.e.No longer actively working in Canada, Fails to maintain a requirement'
                        ' for registration, Fails to meet a requirement for registration.')

    def __str__(self):
        return self.description


@reversion.register(follow=('organization',))
class Register(AuditModel):

    register_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Register UUID',
        db_comment='Unique identifier for the registries_register record.')
    registries_activity = models.ForeignKey(
        ActivityCode,
        db_column='registries_activity_code',
        on_delete=models.PROTECT,
        db_comment=('Code for valid activities that a registered individual can carry out, i.e. PUMP,'
                    ' DRILL'))
    person = models.ForeignKey(Person, db_column='person_guid',
                               on_delete=models.PROTECT, related_name="registrations")
    organization = models.ForeignKey(
        Organization, blank=True,
        db_column='organization_guid',
        null=True, on_delete=models.PROTECT,
        related_name="registrations")
    registration_no = models.CharField(
        max_length=15, blank=True, null=True,
        db_comment=('Unique number assigned to the well driller or well pump installer upon registration. '
                    'Format used: certification type yymmddsequence where sequence is two digits starting '
                    'with 01 for the first person registered in alphabetical order for that day, and '
                    'certification type would be \'WD\' well driller and \'WPI\' for well pump installer. '
                    'E.g. WD 18031001'))

    history = GenericRelation(Version)

    class Meta:
        db_table = 'registries_register'
        verbose_name_plural = 'Registrations'

    db_table_comment = 'Placeholder table comment.'

    def __str__(self):
        return '%s - %s' % (
            self.person,
            self.registries_activity
        )


class ApplicationStatusCodeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()


@reversion.register()
class ApplicationStatusCode(CodeTableModel):
    """
    Status of Applications for the Well Driller and Pump Installer Registries
    """
    code = models.CharField(
        primary_key=True, max_length=10, editable=False, db_column='registries_application_status_code',
        db_comment=('Code for the status of the application for registration of a well driller or well pump '
                    'installer. i.e. A, I, NA, P'))
    description = models.CharField(
        max_length=100,
        db_comment=('Description of the status of the application for registration of a well driller or well '
                    'pump installer. i.e. Registered, Incomplete, Not Approved, Pending'))

    objects = ApplicationStatusCodeManager()

    class Meta:
        db_table = 'registries_application_status_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Application Status Codes'

    db_table_comment = ('Describes the statuses that the application for well driller or well pump installer'
                        ' registration goes through, i.e., Pending, Incomplete, Not Approved, Registered')

    def __str__(self):
        return self.description


@reversion.register()
class ProofOfAgeCode(CodeTableModel):
    """
    List of documents that can be used to indentify (the age) of an application
    """
    code = models.CharField(
        primary_key=True, max_length=15, editable=False, db_column='registries_proof_of_age_code',
        db_comment=('List of valid options for what documentation the ministry staff reviewed to verify the '
                    'applicants age to be over 19. I.e. Drivers, Birth, Passport.'))
    description = models.CharField(
        max_length=100,
        db_comment=('Descriptions of the valid options for documentation that the ministry staff reviewed '
                    'to verify the applicants age to be over 19, i.e. Drivers Licence, Birth Certificate, '
                    'Passport.'))

    class Meta:
        db_table = 'registries_proof_of_age_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'ProofOfAgeCodes'

    db_table_comment = ('Describes options for what documentation the ministry staff reviewed to verify the'
                        ' applicants age to be over 19. i.e., Drivers, Birth, Passport.')

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
        verbose_name='Register Application UUID',
        db_comment='Unique identifier for the registries_application record.')
    registration = models.ForeignKey(
        Register,
        db_column='register_guid',
        on_delete=models.PROTECT,
        verbose_name='Person Reference',
        related_name='applications',
        db_comment='Unique identifier for the registries_register record.')
    subactivity = models.ForeignKey(
        SubactivityCode,
        db_column='registries_subactivity_code',
        on_delete=models.PROTECT,
        related_name="applications")
    file_no = models.CharField(
        max_length=25, blank=True, null=True, verbose_name='ORCS File # reference.',
        db_comment=('Operational Records Classification Systems (ORCS) number. Information schedules used '
                    'to classify, file, retrieve and dispose of operational records. This number is '
                    'assigned on creation of a file.'))
    proof_of_age = models.ForeignKey(
        ProofOfAgeCode,
        db_column='registries_proof_of_age_code',
        on_delete=models.PROTECT,
        verbose_name="Proof of age.",
        null=False
    )
    registrar_notes = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Registrar notes, for internal use only.',
        db_comment='Internal notes documenting communication between an applicant and the province.')
    reason_denied = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Free form text explaining reason for denial.',
        db_comment=('The reason the Comptroller did not approve an individuals application for well driller '
                    'or well pump installer, for example not meeting the requirements of the application. '
                    'A brief internal note.'))

    # TODO Support multiple certificates
    primary_certificate = models.ForeignKey(
        AccreditedCertificateCode,
        blank=True,
        null=True,
        db_column='acc_cert_guid',
        on_delete=models.PROTECT,
        verbose_name="Certificate")
    primary_certificate_no = models.CharField(
        max_length=50,
        db_comment='Unique number assigned to the certificate by the certifying organization.')

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
        blank=True, null=True,
        db_comment=('Date that the province received an application for registration of a well driller or '
                    'well pump installer.'))
    application_outcome_date = models.DateField(
        blank=True, null=True,
        db_comment=('Date that the comptroller decided if the application for registration of a well '
                    'driller or well pump installer was approved or denied.'))
    application_outcome_notification_date = models.DateField(
        blank=True, null=True,
        db_comment=('Date that the individual was notified of the outcome of their application for '
                    'registration for well driller or well pump installer.'))
    # The "removal_date" refers to the date on which a classification is "removed" from the register.
    # Removing a classification may result in a person being removed from the public register as a whole,
    # only if there are no other Approved classification.
    removal_date = models.DateField(
        blank=True, null=True,
        db_comment='Date that a registered individual was removed from the register.'
    )
    removal_reason = models.ForeignKey(
        RegistriesRemovalReason,
        db_column='registries_removal_reason_code',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='Removal Reason')

    history = GenericRelation(Version)

    class Meta:
        db_table = 'registries_application'
        verbose_name_plural = 'Applications'
        ordering = ['primary_certificate_no']

    db_table_comment = 'Placeholder table comment.'

    def __str__(self):
        return '%s : %s' % (
            self.registration,
            self.file_no)


class Register_Note(AuditModel):
    register_note_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Register Node UUID')
    registration = models.ForeignKey(
        Register,
        db_column='register_guid',
        on_delete=models.PROTECT,
        verbose_name="Register Reference",
        related_name='notes',
        db_comment='Unique identifier for the registries_register record.')
    notes = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name='Registrar notes, for internal use only.')

    class Meta:
        db_table = 'registries_register_note'
        verbose_name_plural = 'Registrar Notes'

    db_table_comment = 'Placeholder table comment.'

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
    note = models.TextField(
        max_length=2000,
        db_comment='Internal note used for the purposes of conducting business with the company.')

    class Meta:
        db_table = 'registries_organization_note'

    db_table_comment = 'Placeholder table comment.'

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
    note = models.TextField(
        max_length=2000,
        db_comment='Internal note used for the purposes of conducting business with an applicant.')

    class Meta:
        db_table = 'registries_person_note'

    db_table_comment = 'Placeholder table comment.'

    def __str__(self):
        return self.note[:20] + ('...' if len(self.note) > 20 else '')


"""
Tue Apr 10 10:15:34 2018 Expose DB Views to Django
"""

# TODO: This appears to be unused. Remove?
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


class RegionalArea(AuditModel):
    regional_area_guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Regional Area UUID")

    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        db_comment='Regional Area Administrative Name')
    
    geom = models.PolygonField(
        srid=4326, 
        null=False,
        blank=False,
        db_comment='Regional Area polygon.'
    )

    class Meta:
        db_table = 'regional_area'
        ordering = ['name']
        verbose_name_plural = 'Regional Areas'

    db_table_comment = 'Regional Areas in BC used to locate drillers and pump installers.'

    def __str__(self):
        return self.name
