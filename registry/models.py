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
    email_address = models.EmailField(blank=True, null=True,verbose_name="Organization's generic inbox email adddress")

    class Meta:
        db_table = 'gwells_organization'
        ordering = ['name']                
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name

class ContactAt(AuditModel):
    contact_at_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
    	verbose_name="Contact At UUID, hidden from users")
    person_id = models.ForeignKey(Person, db_column='person_guid', on_delete=models.CASCADE, blank=True, null=True, 
    	verbose_name="Person Reference")
    org_id = models.ForeignKey(Organization, db_column='org_guid', on_delete=models.CASCADE, blank=True, null=True, 
    	verbose_name="Company Reference")

    cell_tel = models.CharField(blank=True, null=True,max_length=12,verbose_name="Cellular telephone number")
    office_tel = models.CharField(blank=True, null=True,max_length=12,verbose_name="Office telephone number")
    email_address = models.EmailField(blank=True, null=True,verbose_name="Email adddress")

    effective_date = models.DateField(default=datetime.date.today)
    expired_date = models.DateField(blank=True, null=True,default=datetime.date.today)


    class Meta:
        db_table = 'gwells_contact_at'
        verbose_name_plural = 'Person contact details for a given Company'

    def __str__(self):
        return self.contact_at_guid

        return '%s : %s %s at %s' % (self.contact_at_guid
            ,self.person_id.first_name
            ,self.person_id.surname
            ,self.org_id.name)

class Application(AuditModel):
    DRILLER_APPLICATION  = 'DRILL'
    PUMP_APPLICATION  = 'PUMP'
    APPL_TYPE_CHOICES = (
        (DRILLER_APPLICATION, 'Driller'),
        (PUMP_APPLICATION, 'Pump Installer')
        )

    appl_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="Application UUID, hidden from users")
    person_id = models.ForeignKey(Person, db_column='person_guid', on_delete=models.CASCADE, blank=True, null=True, 
        verbose_name="Person Reference")
    appl_type = models.CharField(max_length=4,
        choices=APPL_TYPE_CHOICES, default=DRILLER_APPLICATION,
        )
    over19_ind = models.BooleanField(default=True)
    registrar_notes = models.CharField(max_length=255, blank=True, null=True, verbose_name='Registrar Notes, for internal use only.')
    reason_denied   = models.CharField(max_length=255, blank=True, null=True, verbose_name='Free form text explaining reason for denial.')

    class Meta:
        db_table = 'gwells_application'
        verbose_name_plural = 'Applications for Driller or Pump Installer'

    def __str__(self):
        return '%s : %s %s, applying for %s' % (self.appl_guid
            ,self.person_id.first_name
            ,self.person_id.surname
            ,self.appl_type)
