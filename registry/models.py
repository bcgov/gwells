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
        db_table = 'gwells_person'
        ordering = ['first_name', 'surname']        
        verbose_name_plural = 'Persons'

    def __str__(self):
        return '%s %s' % (self.first_name, self.surname)

class Organization(AuditModel):
    org_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
    	verbose_name="Organization UUID, hidden from users")

    name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=100, blank=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, verbose_name='Town/City')
    province_state = models.ForeignKey(ProvinceState, db_column='province_state_guid', on_delete=models.CASCADE, verbose_name='Province/State')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')

    main_tel = models.CharField(blank=True, null=True,max_length=12,verbose_name="Company main telephone number")
    fax_tel = models.CharField(blank=True, null=True,max_length=12,verbose_name="Facsimile telephone number")
    website_url = models.URLField

    class Meta:
        db_table = 'gwells_organization'
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

    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True,default=datetime.date.today)


    class Meta:
        db_table = 'gwells_contact_at'
        verbose_name_plural = 'Person contact details for a given Company'

    def __str__(self):
        return '%s : %s %s at %s' % (self.contact_at_guid
            ,self.person.first_name
            ,self.person.surname
            ,self.org.name)


class RegistryApplicationType(AuditModel):
    """
    Type of applications to Driller / Pump Installer Registries.
    """
    registry_appl_type_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    subcode = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('code', 'subcode')
        db_table = 'gwells_registry_appl_type'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description


class RegistryQualifiedFor(AuditModel):
    """
    Subclass of Well type.
    """
    registry_qual_for_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registry_appl_type = models.ForeignKey(RegistryApplicationType, null=True, db_column='registry_appl_type_guid', on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'gwells_registry_qualified_for'
        ordering = ['sort_order', 'description']

    def validate_unique(self, exclude=None):
        qs = Room.objects.filter(name=self.code)
        if qs.filter(wregistry_appl_type__subcode=self.registry_appl_type__subcode).exists():
            raise ValidationError('Qualified-For Well must be unique per Registry Application Type')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(RegistryQualifiedFor, self).save(*args, **kwargs)

    def __str__(self):
        return '%s (%s - %s)' % (self.description
            ,self.registry_appl_type.code
            ,self.registry_appl_type.description
            )

class Application(AuditModel):

    appl_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Application UUID, hidden from users")
    person = models.ForeignKey(Person, db_column='person_guid', on_delete=models.CASCADE, verbose_name="Person Reference")
    file_no = models.CharField(max_length=25, blank=True, null=True, verbose_name='ORCS File # reference.')
    over19_ind = models.BooleanField(default=True)
    registrar_notes = models.CharField(max_length=255, blank=True, null=True, verbose_name='Registrar Notes, for internal use only.')
    reason_denied   = models.CharField(max_length=255, blank=True, null=True, verbose_name='Free form text explaining reason for denial.')

    class Meta:
        db_table = 'gwells_registry_application'
        verbose_name_plural = 'Applications for Driller or Pump Installer'

    def __str__(self):
        return '%s : %s %s (%s)' % (self.appl_guid
            ,self.person.first_name
            ,self.person.surname
            ,self.file_no)


class QualificationAppliedFor(AuditModel):

    qual_appl_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Qualification XREF UUID, hidden from users")
    application = models.ForeignKey(Person, db_column='appl_guid', on_delete=models.CASCADE, verbose_name="Application Reference")
    qualification = models.ForeignKey(RegistryQualifiedFor, db_column='registry_qual_for_guid', on_delete=models.CASCADE, verbose_name="Qualification being applied for")

    class Meta:
        db_table = 'gwells_registry_qual_applied'
        verbose_name_plural = 'Application Qualification being applied for'

    def __str__(self):
        return '%s : %s %s %s (%s)' % (self.qual_appl_guid
            ,self.application.person.first_name
            ,self.application.person.surname
            ,self.qualification.description
            ,self.application.file_no)


