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
        db_table = 'registry_person'
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
    province_state = models.ForeignKey(ProvinceState, db_column='province_state_guid', on_delete=models.CASCADE, verbose_name='Province/State')
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Postal Code')

    main_tel = models.CharField(blank=True, null=True,max_length=12,verbose_name="Company main telephone number")
    fax_tel = models.CharField(blank=True, null=True,max_length=12,verbose_name="Facsimile telephone number")
    website_url = models.URLField(blank=True, null=True,verbose_name="Orgnization's Website")
    certificate_authority = models.BooleanField(default=False, verbose_name='Certifying Authority for Registry Activities', choices=((False, 'No'), (True, 'Yes')))

    class Meta:
        db_table = 'registry_organization'
        ordering = ['name']                
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name

class ContactAt(AuditModel):
    contact_at_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
    	verbose_name="Contact At UUID, hidden from users")
    person = models.ForeignKey(Person, db_column='person_guid', on_delete=models.CASCADE, blank=True, null=True, 
    	verbose_name="Person Reference")
    org = models.ForeignKey(Organization, db_column='org_guid', on_delete=models.CASCADE, blank=True, null=True, 
    	verbose_name="Company Reference")

    tel = models.CharField(blank=True, null=True,max_length=12,verbose_name="Contact telephone number")
    email_address = models.EmailField(blank=True, null=True,verbose_name="Email adddress")

    # TODO - GW Replace defaults with save() method, see
    # ../../gwells/models/AuditModel.py and 
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True,default=datetime.date.today)

    class Meta:
        db_table = 'registry_contact_at'
        verbose_name_plural = 'Person contact details for a given Company'

    def __str__(self):
        return '%s : %s %s at %s' % (self.contact_at_guid
            ,self.person.first_name
            ,self.person.surname
            ,self.org.name)


class ActivityType(AuditModel):
    """
    Restricted Activity related to drilling wells and installing well pumps.
    """
    registry_activity_type_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    subcode = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('code', 'subcode')
        db_table = 'registry_activity_type'
        ordering = ['sort_order', 'code','description']

    def __str__(self):
        return self.description


class QualificationType(AuditModel):
    """
    Type of well for which the activity is qualified.
    """
    registry_qualification_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registry_activity_type = models.ForeignKey(ActivityType, null=True, db_column='registry_activity_type_guid', on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'registry_qualification'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return '%s (%s - %s)' % (self.description
            ,self.registry_activity_type.code
            ,self.registry_activity_type.description
            )

class RegistryApplication(AuditModel):

    application_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Registry Application UUID, hidden from users")
    person = models.ForeignKey(Person, db_column='person_guid', on_delete=models.CASCADE, verbose_name="Person Reference")
    file_no = models.CharField(max_length=25, blank=True, null=True, verbose_name='ORCS File # reference.')
    over19_ind = models.BooleanField(default=True)
    registrar_notes = models.CharField(max_length=255, blank=True, null=True, verbose_name='Registrar Notes, for internal use only.')
    reason_denied   = models.CharField(max_length=255, blank=True, null=True, verbose_name='Free form text explaining reason for denial.')

    class Meta:
        db_table = 'registry_application'
        verbose_name_plural = 'Applications for Driller or Pump Installer'

    def __str__(self):
        return '%s : %s %s (%s)' % (self.application_guid
            ,self.person.first_name
            ,self.person.surname
            ,self.file_no)


# TODO - GW for the one-off application where a secondary Certificate is attached
class ClassificationAppliedFor(AuditModel):
    classification_applied_for_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="UUID of the Registry Classification being applied for, hidden from users")
    registry_application = models.ForeignKey(RegistryApplication, db_column='application_guid', on_delete=models.CASCADE, verbose_name="Application Reference")
    registry_activity_type = models.ForeignKey(ActivityType, null=True, db_column='registry_activity_type_guid', on_delete=models.CASCADE)

    primary_certificate_authority = models.ForeignKey(Organization, db_column='org_guid', on_delete=models.CASCADE, limit_choices_to={'certificate_authority': True}
        ,verbose_name="Certifying Organization")
    primary_certificate_no = models.CharField(max_length=50)

    class Meta:
        db_table = 'registry_classification_applied_for'
        verbose_name_plural = 'Registry Classification being applied for'

    def __str__(self):
        return '%s : %s %s %s %s (%s)' % (self.classification_applied_for_guid
            ,self.registry_application.application_guid
            ,self.registry_application.person.surname            
            ,self.registry_application.person.surname
            ,self.registry_activity_type.description
            ,self.registry_application.file_no)


