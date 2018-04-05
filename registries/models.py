import uuid
import datetime
from django.db import models
from gwells.models import AuditModel, ProvinceStateCode

class ActivityCode(AuditModel):
    """
    Restricted Activity related to drilling wells and installing well pumps.
    """
    registries_activity_code = models.CharField(primary_key=True, max_length=10, editable=False)
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

class SubactivityCode(AuditModel):
    """
    Restricted Activity Subtype related to drilling wells and installing well pumps.
    """
    registries_subactivity_code = models.CharField(primary_key=True, max_length=10, editable=False)
    registries_activity = models.ForeignKey(ActivityCode, db_column='registries_activity_code',
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


class CertifyingAuthorityCode(AuditModel):
    cert_auth_code = models.CharField(primary_key=True, max_length=50, editable=False,
        verbose_name="Certifying Authority Name")
    description = models.CharField(max_length=100, blank=True, null=True)

    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_certifying_authority_code'
        ordering = ['cert_auth_code']
        verbose_name_plural = 'Certifying Authorities'

    def __str__(self):
        return self.name

class AccreditedCertficateCode(AuditModel):
    acc_cert_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Accredited Certficate UUID")
    cert_auth = models.ForeignKey(CertifyingAuthorityCode, db_column='cert_auth_code',
        on_delete=models.PROTECT)
    registries_activity = models.ForeignKey(ActivityCode, db_column='registries_activity_code',
        on_delete=models.PROTECT)
    name = models.CharField(max_length=100, editable=False, verbose_name="Certificate Name")
    description = models.CharField(max_length=100, blank=True, null=True)

    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_accredited_certificate_code'
        ordering = ['registries_activity','cert_auth']
        verbose_name_plural = 'Accredited Certficates'

    def __str__(self):
        return '%s %s %s' % (self.cert_auth, self.registries_activity, self.name)


class Organization(AuditModel):
    org_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
    	verbose_name="Organization UUID")
    name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Town/City')
    province_state = models.ForeignKey(ProvinceStateCode, db_column='province_state_code',
        on_delete=models.PROTECT, verbose_name='Province/State', related_name="companies")
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Postal Code')
    main_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name="Telephone number")
    fax_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name="Fax number")
    website_url = models.URLField(blank=True, null=True, verbose_name="Website")
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_organization'
        ordering = ['name']
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name


# Create your models here.
class Person(AuditModel):
    person_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
    	verbose_name="Person UUID")
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    # Works With Org...  (should be a xref table)
    organization = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.PROTECT,
        related_name="People")

    class Meta:
        db_table = 'registries_person'
        ordering = ['first_name', 'surname']
        verbose_name_plural = 'People'

    def __str__(self):
        return '%s %s' % (self.first_name, self.surname)


class ContactInfo(AuditModel):
    contact_detail_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
    	verbose_name="Contact At UUID")
    person = models.ForeignKey(Person, db_column='person_guid', on_delete=models.PROTECT,
    	verbose_name="Person Reference", related_name="contact_info")
    contact_tel = models.CharField(blank=True, null=True, max_length=15,
        verbose_name="Contact telephone number")
    contact_email = models.EmailField(blank=True, null=True,verbose_name="Email adddress")
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
    registries_well_class_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_well_class_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Well Classes'

    def __str__(self):
        return self.description


class Qualification(AuditModel):
    """
    Qualification of Well Class for a given Activity/SubActivity.
    """
    registries_well_qualification_guid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False, verbose_name="Qualification / Well Class UUID")
    well_class = models.ForeignKey(WellClassCode, db_column='registries_well_class_code',
        on_delete=models.PROTECT,related_name="Qualification")
    subactivity = models.ForeignKey(SubactivityCode, db_column='registries_subactivity_code',
        on_delete=models.PROTECT,related_name="Qualification")
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_well_qualification'
        ordering = ['subactivity', 'display_order']
        verbose_name_plural = 'Qualification codes'

    def __str__(self):
        return '%s %s' % (self.subactivity, self.well_class)


class RegistriesStatusCode(AuditModel):
    """
    Status of the Register Entry
    """
    registries_status_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_status_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Registry Status Codes'

    def __str__(self):
        return self.description

class RegistriesRemovalReason(AuditModel):
    """
    Possible Reasons for Removal from either of the Registers
    """
    registries_removal_reason_code = models.CharField(primary_key=True, max_length=10, editable=False)
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

class Register(AuditModel):
    PENDING = 'P'

    register_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Register UUID")
    registries_activity = models.ForeignKey(ActivityCode, db_column='registries_activity_code',
        on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="registrations")
    status = models.ForeignKey(RegistriesStatusCode, db_column='registries_status_code',
        on_delete=models.PROTECT, default=PENDING, verbose_name="Register Entry Status")
    registration_no = models.CharField(max_length=15,blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    register_removal_reason = models.ForeignKey(RegistriesRemovalReason,
        db_column='registries_removal_reason_code',
        on_delete=models.PROTECT, blank=True, null=True, verbose_name="Removal Reason")
    register_removal_date = models.DateField(blank=True,
        null=True, verbose_name="Date of Removal from Register")

    class Meta:
        db_table = 'registries_register'
        verbose_name_plural = 'Registrations'

    def __str__(self):
        return '%s - %s' % (
            self.person,
            self.registries_activity
        )

class RegistriesApplication(AuditModel):
    """
    Application from a well driller or pump installer to be on the GWELLS Register.
    """
    application_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Register Application UUID")
    registration = models.ForeignKey(Register, db_column='register_guid', on_delete=models.PROTECT,
        verbose_name="Person Reference", related_name='applications')
    subactivity = models.ForeignKey(SubactivityCode, db_column='registries_subactivity_code',
        on_delete=models.PROTECT,related_name="applications")
    file_no = models.CharField(max_length=25, blank=True, null=True, verbose_name='ORCS File # reference.')
    over19_ind = models.BooleanField(default=True)
    registrar_notes = models.CharField(max_length=255, blank=True, null=True,
        verbose_name='Registrar notes, for internal use only.')
    reason_denied = models.CharField(max_length=255, blank=True, null=True,
        verbose_name='Free form text explaining reason for denial.')

    # TODO Support multiple certificates
    primary_certificate = models.ForeignKey(AccreditedCertficateCode, blank=True, null=True,
        db_column='acc_cert_guid', on_delete=models.PROTECT, verbose_name="Certificate")
    primary_certificate_no = models.CharField(max_length=50)

    class Meta:
        db_table = 'registries_application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return '%s : %s' % (
            self.registration,
            self.file_no)


class ApplicationStatusCode(AuditModel):
    """
    Status of Applications for the Well Driller and Pump Installer Registries
    """
    registries_application_status_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_application_status_code'
        ordering = ['display_order', 'description']
        verbose_name_plural = 'Application Status Codes'

    def __str__(self):
        return self.description


class RegistriesApplicationStatus(AuditModel):
    """
    Status of a specific Application for the Well Driller and Pump Installer Registries, at a point in time
    """
    application_status_guid = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False, verbose_name="Register Application Status UUID")
    application = models.ForeignKey(RegistriesApplication, db_column='application_guid',
        on_delete=models.PROTECT, verbose_name="Application Reference", related_name="status_set")
    status = models.ForeignKey(ApplicationStatusCode, db_column='registries_application_status_code', on_delete=models.PROTECT, verbose_name="Application Status Code Reference")
    notified_date = models.DateField(blank=True, null=True, default=datetime.date.today)
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'registries_application_status'
        ordering = ['application', 'effective_date']
        verbose_name_plural = 'Application status'

    def __str__(self):
        return '%s - %s - %s (exp %s)' % (
            self.application,
            self.status.description,
            self.effective_date,
            self.expired_date)
"""
class DrillerRegister(models.Model):
     Consolidated view of Driller Register
     registration_no = models.CharField(max_length=15,blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    status_code = models.CharField(max_length=10)
    register_removal_date  = models.DateField(blank=True, null=True,verbose_name="Date of Removal from Register")
    register_removal_reason = models.DateField(blank=True, null=True)
    activity_code = models.CharField(max_length=10, unique=True)
    #
    file_no = models.CharField(max_length=25, blank=True, null=True, verbose_name='ORCS File # reference.')
    over19_ind = models.BooleanField(default=True)
    registrar_notes = models.CharField(max_length=255, blank=True, null=True, verbose_name='Registrar Notes, for internal use only.')
    reason_denied   = models.CharField(max_length=255, blank=True, null=True, verbose_name='Free form text explaining reason for denial.')
    #
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    #
    contact_tel = models.CharField(blank=True, null=True,max_length=15,verbose_name="Contact telephone number")
    contact_email = models.EmailField(blank=True, null=True,verbose_name="Email adddress")
    #
    org_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Town/City')
    prov_state_code = models.CharField(max_length=10, unique=True)
    prov_state_desc = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Postal Code')
    #
    main_tel = models.CharField(blank=True, null=True,max_length=15,verbose_name="Company main telephone number")
    fax_tel = models.CharField(blank=True, null=True,max_length=15,verbose_name="Facsimile telephone number")
    website_url = models.URLField(blank=True, null=True,verbose_name="Orgnization's Website")
    #
    register_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Register UUID")
    reg_create_user = models.CharField(max_length=30)
    reg_create_date = models.DateTimeField(blank=True, null=True)
    reg_update_user = models.CharField(max_length=30, null=True)
    reg_update_date = models.DateTimeField(blank=True, null=True)
    #
    registration_status_guid = models.ForeignKey(RegistriesStatusCode, db_column='registries_status_guid', on_delete=models.DO_NOTHING, verbose_name="Register Entry Status")
    status_create_user = models.CharField(max_length=30)
    status_create_date = models.DateTimeField(blank=True, null=True)
    status_update_user = models.CharField(max_length=30, null=True)
    status_update_date = models.DateTimeField(blank=True, null=True)
    #
    application_guid = models.ForeignKey(RegistriesApplication, db_column='application_guid', on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="Application Reference")
    appl_create_user = models.CharField(max_length=30)
    appl_create_date = models.DateTimeField(blank=True, null=True)
    appl_update_user = models.CharField(max_length=30, null=True)
    appl_update_date = models.DateTimeField(blank=True, null=True)
    #
    registries_removal_reason_guid = models.ForeignKey(RegistriesRemovalReason, db_column='registries_removal_reason_guid', on_delete=models.DO_NOTHING, blank=True, null=True,verbose_name="Removal Reason")
    removal_create_user = models.CharField(max_length=30)
    removal_create_date = models.DateTimeField(blank=True, null=True)
    removal_update_user = models.CharField(max_length=30, null=True)
    removal_update_date = models.DateTimeField(blank=True, null=True)

    registries_activity_guid = models.ForeignKey(ActivityCode, db_column='registries_activity_guid', on_delete=models.DO_NOTHING, blank=True)
    act_create_user = models.CharField(max_length=30)
    act_create_date = models.DateTimeField(blank=True, null=True)
    act_update_user = models.CharField(max_length=30, null=True)
    act_update_date = models.DateTimeField(blank=True, null=True)

    person_guid = models.UUIDField(editable=False,
        verbose_name="Person UUID, hidden from users")
    per_create_user = models.CharField(max_length=30)
    per_create_date = models.DateTimeField(blank=True, null=True)
    per_update_user = models.CharField(max_length=30, null=True)
    per_update_date = models.DateTimeField(blank=True, null=True)

    contact_at_guid = models.UUIDField(editable=False,
        verbose_name="ContactAt UUID, hidden from users")
    contact_effective_date = models.DateTimeField(blank=True, null=True)
    contact_expired_date = models.DateTimeField(blank=True, null=True)
    contact_create_user = models.CharField(max_length=30)
    contact_create_date = models.DateTimeField(blank=True, null=True)
    contact_update_user = models.CharField(max_length=30, null=True)
    contact_update_date = models.DateTimeField(blank=True, null=True)

    org_guid = models.UUIDField(editable=False,
        verbose_name="Organization UUID, hidden from users")
    org_create_user = models.CharField(max_length=30)
    org_create_date = models.DateTimeField(blank=True, null=True)
    org_update_user = models.CharField(max_length=30, null=True)
    org_update_date = models.DateTimeField(blank=True, null=True)

    prov_guid = models.UUIDField(editable=False,
        verbose_name="ProvinceStateCode UUID, hidden from users")
    prov_create_user = models.CharField(max_length=30)
    prov_create_date = models.DateTimeField(blank=True, null=True)
    prov_update_user = models.CharField(max_length=30, null=True)
    prov_update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registries_driller_register'

        ordering = ['display_order', 'description']
        verbose_name_plural = 'Possible statuses of Applications'

    def __str__(self):
        return self.registration_no
"""
