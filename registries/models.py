import uuid
import datetime
from django.db import models
from gwells.models import AuditModel, ProvinceState

# Create your models here.
class Person(AuditModel):
    person_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
    	verbose_name="Person UUID, hidden from users")
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    class Meta:
        db_table = 'registries_person'
        ordering = ['first_name', 'surname']        
        verbose_name_plural = 'Persons'

    def __str__(self):
        return '%s %s' % (self.first_name, self.surname)

class Organization(AuditModel):
    org_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
    	verbose_name="Organization UUID, hidden from users")

    name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Town/City')
    province_state = models.ForeignKey(ProvinceState, db_column='province_state_guid', on_delete=models.CASCADE, null=True, verbose_name='Province/State')
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Postal Code')

    main_tel = models.CharField(blank=True, null=True,max_length=15,verbose_name="Company main telephone number")
    fax_tel = models.CharField(blank=True, null=True,max_length=15,verbose_name="Facsimile telephone number")
    website_url = models.URLField(blank=True, null=True,verbose_name="Orgnization's Website")
    certificate_authority = models.BooleanField(default=False, verbose_name='Certifying Authority for Registries Activities', choices=((False, 'No'), (True, 'Yes')))

    class Meta:
        db_table = 'registries_organization'
        ordering = ['name']                
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name

class ContactAt(AuditModel):
    contact_at_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
    	verbose_name="Contact At UUID, hidden from users")
    person = models.ForeignKey(Person, db_column='person_guid', on_delete=models.CASCADE, null=True, 
    	verbose_name="Person Reference")
    org = models.ForeignKey(Organization, db_column='org_guid', on_delete=models.CASCADE, null=True, 
    	verbose_name="Company Reference")

    contact_tel = models.CharField(blank=True, null=True,max_length=15,verbose_name="Contact telephone number")
    contact_email = models.EmailField(blank=True, null=True,verbose_name="Email adddress")

    # TODO - GW Replace defaults with save() method, see
    # ../../gwells/models/AuditModel.py and 
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True,default=datetime.date.today)

    class Meta:
        db_table = 'registries_contact_at'
        verbose_name_plural = 'Person contact details for a given Company'

    def __str__(self):
        return '%s : %s %s at %s' % (self.contact_at_guid
            ,self.person.first_name
            ,self.person.surname
            ,self.org.name)

class ActivityCode(AuditModel):
    """
    Restricted Activity related to drilling wells and installing well pumps.
    """
    registries_activity_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'registries_activity_code'
        ordering = ['sort_order', 'description']
        verbose_name_plural = 'Possible types of restricted activity, related to well drilling and pump installing'

    def __str__(self):
        return self.description

class SubactivityCode(AuditModel):
    """
    Restricted Activity Subtype related to drilling wells and installing well pumps.
    """
    registries_subactivity_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registries_activity = models.ForeignKey(ActivityCode, null=True, db_column='registries_activity_guid', on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'registries_subactivity_code'
        ordering = ['sort_order', 'description']
        verbose_name_plural = 'Possible subtypes of restricted activity, under a given Activity'

    def __str__(self):
        return self.description


class Qualificationcode(AuditModel):
    """
    Type of well for which the activity is qualified.
    """
    registries_qualification_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registries_subactivity = models.ForeignKey(SubactivityCode, null=True, db_column='registries_subactivity_guid', on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'registries_qualification_code'
        ordering = ['sort_order', 'description']
        verbose_name_plural = 'Possible qualifications, under a given Activity and Subactivity'

    def __str__(self):
        return '%s (%s)' % (self.description
            ,self.registry_subactivity.description
            )

class RegistriesApplication(AuditModel):
    """
    Application from a well driller or pump installer to be on the GWELLS Register.
    """
    application_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Register Application UUID, hidden from users")
    person = models.ForeignKey(Person, db_column='person_guid', on_delete=models.CASCADE, verbose_name="Person Reference")
    file_no = models.CharField(max_length=25, blank=True, null=True, verbose_name='ORCS File # reference.')
    over19_ind = models.BooleanField(default=True)
    registrar_notes = models.CharField(max_length=255, blank=True, null=True, verbose_name='Registrar Notes, for internal use only.')
    reason_denied   = models.CharField(max_length=255, blank=True, null=True, verbose_name='Free form text explaining reason for denial.')

    class Meta:
        db_table = 'registries_application'
        verbose_name_plural = 'Applications for Driller or Pump Installer'

    def __str__(self):
        return '%s : %s %s (%s)' % (self.application_guid
            ,self.person.first_name
            ,self.person.surname
            ,self.file_no)

# TODO - GW A related model/table for the one-off application where a secondary certificate(s) are attached
class ClassificationAppliedFor(AuditModel):
    classification_applied_for_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="UUID of the Registries Classification being applied for, hidden from users")
    registries_application = models.ForeignKey(RegistriesApplication, db_column='application_guid', on_delete=models.CASCADE, verbose_name="Application Reference")
    registries_subactivity = models.ForeignKey(SubactivityCode, null=True, db_column='registries_subactivity_guid', on_delete=models.CASCADE)

    primary_certificate_authority = models.ForeignKey(Organization, null=True, db_column='certifying_org_guid', on_delete=models.CASCADE, limit_choices_to={'certificate_authority': True}
        ,verbose_name="Certifying Organization")
    primary_certificate_no = models.CharField(max_length=50)

    class Meta:
        db_table = 'registries_classification_applied_for'
        verbose_name_plural = 'Registries Classification being applied for'

    def __str__(self):
        return '%s : %s %s %s %s (%s)' % (self.classification_applied_for_guid
            ,self.registries_application.person.first_name            
            ,self.registries_application.person.surname
            ,self.registries_subactivity.description
            ,self.registries_application.file_no)

class RegistriesStatusCode(AuditModel):
    """
    Status of the Register Entry
    """
    registries_status_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'registries_status_code'
        ordering = ['sort_order', 'description']
        verbose_name_plural = 'Possible Status Codes of Register Entries'

    def __str__(self):
        return self.description

class RegistriesRemovalReason(AuditModel):
    """
    Possible Reasons for Removal from either of the Registers
    """
    registries_removal_reason_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'registries_removal_reason_code'
        ordering = ['sort_order', 'description']
        verbose_name_plural = 'Possible reasons for removal from either of the Registers'

    def __str__(self):
        return self.description

class Register(AuditModel):

    register_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Register UUID, hidden from users")
    # TODO - GW constraint to ensure that DRILL/PUMP ActivityCode of this entry is consistent with the Application
    registries_activity = models.ForeignKey(ActivityCode, db_column='registries_activity_guid', on_delete=models.CASCADE, blank=True)
    registries_application = models.ForeignKey(RegistriesApplication, db_column='application_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Application Reference")

    registration_no = models.CharField(max_length=15,blank=True, null=True)    
    status = models.ForeignKey(RegistriesStatusCode, db_column='registries_status_guid', on_delete=models.CASCADE, verbose_name="Register Entry Status")
    registration_date = models.DateField(blank=True, null=True)

    register_removal_reason = models.ForeignKey(RegistriesRemovalReason, db_column='registries_removal_reason_guid', on_delete=models.CASCADE, blank=True, null=True,verbose_name="Removal Reason")
    register_removal_date  = models.DateField(blank=True, null=True,verbose_name="Date of Removal from Register")

    class Meta:
        db_table = 'registries_register'
        verbose_name_plural = 'Register of Drillers and Pump Installers'

    def __str__(self):
        return '%s : %s %s %s %s %s %s %s' % (self.register_guid
            ,self.registries_activity.description
            ,self.registration_no
            ,self.registries_application.file_no
            ,self.status
            ,self.registration_date
            ,self.registries_application.person.first_name
            ,self.registries_application.person.surname
            )


class ApplicationStatusCode(AuditModel):
    """
    Status of Applications for the Well Driller and Pump Installer Registries
    """
    registries_application_status_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'registries_application_status_code'
        ordering = ['sort_order', 'description']
        verbose_name_plural = 'Possible statuses of Applications'

    def __str__(self):
        return self.description

class RegistriesApplicationStatus(AuditModel):
    """
    Status of a specific Application for the Well Driller and Pump Installer Registries, at a point in time
    """    
    application_status_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Register Application Status UUID, hidden from users")
    application = models.ForeignKey(RegistriesApplication, db_column='application_guid', on_delete=models.CASCADE, verbose_name="Application Reference")    
    status = models.ForeignKey(ApplicationStatusCode, db_column='registries_application_status_guid', on_delete=models.CASCADE, verbose_name="Application Status Code Reference")

    notified_date = models.DateField(blank=True, null=True,default=datetime.date.today)

    # TODO - GW Replace defaults with save() method, see
    # ../../gwells/models/AuditModel.py and 
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True,default=datetime.date.today)

    class Meta:
        db_table = 'registries_application_status'
        ordering = ['application', 'effective_date']        
        verbose_name_plural = 'Status for a given Application'

    def __str__(self):
        return '%s : %s %s %s %s %s %s %s' % (self.application_status_guid
            ,self.application.file_no
            ,self.status.description
            ,self.effective_date
            ,self.expired_date
            )
