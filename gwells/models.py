import datetime
import uuid
from django.db import models
from  django.utils import timezone
from model_utils.models import TimeStampedModel
from model_utils import FieldTracker




class ProvinceState(models.Model):
    """
    Lookup of Provinces/States.
    Used to specify valid provinces or states for the address of the owner of a well.
    It provides for a standard commonly understood code and description for provinces and states.
    Some examples include: BC, AB, W
    """
    province_state_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_province_state'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class LandDistrict(models.Model):
    """
    Lookup of Land Districts.
    """
    land_district_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_land_district'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name



class WellYieldUnit(models.Model):
    """
    Units of Well Yield.
    """
    well_yield_unit_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_yield_unit'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class WellActivityType(models.Model):
    """
    Types of Well Activity.
    """
    well_activity_type_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_activity_type'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class WellClass(models.Model):
    """
    Class of Well type.
    """
    well_class_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_class'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class WellSubclass(models.Model):
    """
    Subclass of Well type.
    """
    well_subclass_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well_class = models.ForeignKey(WellClass, db_column='well_class_guid', on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_subclass'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class IntendedWaterUse(models.Model):
    """
    Usage of Wells (water supply).
    """
    intended_water_use_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_intended_water_use'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class DrillingCompany(models.Model):
    """
    Companies who perform drilling.
    """
    drilling_company_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    is_hidden = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'gwells_drilling_company'
        verbose_name_plural = 'Drilling Companies'

    def __str__(self):
        return self.name



class Driller(models.Model):
    """
    People responsible for drilling.
    """
    driller_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drilling_company = models.ForeignKey(DrillingCompany, db_column='drilling_company_guid', on_delete=models.CASCADE, verbose_name='Drilling Company')
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'gwells_driller'

    def __str__(self):
        return '%s %s - %s' % (self.first_name, self.surname, self.registration_number)



class Well(TimeStampedModel):
    """
    Well information.
    """
    well_tag_number = models.AutoField(primary_key=True)
    well_guid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    well_class = models.ForeignKey(WellClass, db_column='well_class_guid', on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclass, db_column='well_subclass_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUse, db_column='intended_water_use_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Water Supply Well Intended Water Use')

    owner_full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    owner_mailing_address = models.CharField(max_length=100, verbose_name='Mailing Address')  
    owner_city = models.CharField(max_length=100, verbose_name='Town/City')
    owner_province_state = models.ForeignKey(ProvinceState, db_column='province_state_guid', on_delete=models.CASCADE, blank=True, verbose_name='Province')
    owner_postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')

    street_address = models.CharField(max_length=100, blank=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, verbose_name='Town/City')
    legal_lot = models.CharField(max_length=10, blank=True, verbose_name='Lot')
    legal_plan = models.CharField(max_length=20, blank=True, verbose_name='Plan')
    legal_district_lot = models.CharField(max_length=20, blank=True, verbose_name='District Lot')
    legal_block = models.CharField(max_length=10, blank=True, verbose_name='Block')
    legal_section = models.CharField(max_length=10, blank=True, verbose_name='Section')
    legal_township = models.CharField(max_length=20, blank=True, verbose_name='Township')
    legal_range = models.CharField(max_length=10, blank=True, verbose_name='Range')
    legal_land_district = models.ForeignKey(LandDistrict, db_column='legal_land_district_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(blank=True, null=True, verbose_name='PID')
    well_location_description = models.CharField(max_length=500, blank=True, verbose_name='Well Location Description')

    identification_plate_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    diameter = models.CharField(max_length=9, blank=True)  #want to be integer in future
    #diameter_unit
    total_depth_drilled = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    #depth_unit
    finished_well_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    #depth_unit
    well_yield = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    well_yield_unit = models.ForeignKey(WellYieldUnit, db_column='well_yield_unit_guid', on_delete=models.CASCADE, blank=True, null=True)
    
    tracker = FieldTracker()
    
    class Meta:
        db_table = 'gwells_well'

    def __str__(self):
        return '%d %s' % (self.well_tag_number, self.street_address)



class ActivitySubmission(TimeStampedModel):
    """
    Activity information on a Well submitted by a user.
    """
    filing_number = models.AutoField(primary_key=True)
    activity_submission_guid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    well_activity_type = models.ForeignKey(WellActivityType, db_column='well_activity_type_guid', on_delete=models.CASCADE, verbose_name='Type of Work')
    well_class = models.ForeignKey(WellClass, db_column='well_class_guid', on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclass, db_column='well_subclass_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUse, db_column='intended_water_use_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Water Supply Well Intended Water Use')
    driller_responsible = models.ForeignKey(Driller, db_column='driller_responsible_guid', on_delete=models.CASCADE, verbose_name='Person Responsible for Drilling')
    driller_name = models.CharField(max_length=200, blank=True, verbose_name='Name of Person Who Did the Work')
    consultant_name = models.CharField(max_length=200, blank=True, verbose_name='Consultant Name')
    consultant_company = models.CharField(max_length=200, blank=True, verbose_name='Consultant Company')
    work_start_date = models.DateField(verbose_name='Work Start Date')
    work_end_date = models.DateField(verbose_name='Work End Date')

    owner_full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    owner_mailing_address = models.CharField(max_length=100, verbose_name='Mailing Address')  
    owner_city = models.CharField(max_length=100, verbose_name='Town/City')
    owner_province_state = models.ForeignKey(ProvinceState, db_column='province_state_guid', on_delete=models.CASCADE, verbose_name='Province')
    owner_postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')

    street_address = models.CharField(max_length=100, blank=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, verbose_name='Town/City')
    legal_lot = models.CharField(max_length=10, blank=True, verbose_name='Lot')
    legal_plan = models.CharField(max_length=20, blank=True, verbose_name='Plan')
    legal_district_lot = models.CharField(max_length=20, blank=True, verbose_name='District Lot')
    legal_block = models.CharField(max_length=10, blank=True, verbose_name='Block')
    legal_section = models.CharField(max_length=10, blank=True, verbose_name='Section')
    legal_township = models.CharField(max_length=20, blank=True, verbose_name='Township')
    legal_range = models.CharField(max_length=10, blank=True, verbose_name='Range')
    legal_land_district = models.ForeignKey(LandDistrict, db_column='legal_land_district_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(blank=True, null=True, verbose_name='PID')
    well_location_description = models.CharField(max_length=500, blank=True, verbose_name='Well Location Description')

    identification_plate_number = models.PositiveIntegerField(unique=True, blank=True, null=True, verbose_name='Identification Plate Number')
    diameter = models.CharField(max_length=9, blank=True)  #want to be integer in future
    #diameter_unit
    total_depth_drilled = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    #depth_unit
    finished_well_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    #depth_unit
    well_yield = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    well_yield_unit = models.ForeignKey(WellYieldUnit, db_column='well_yield_unit_guid', on_delete=models.CASCADE, blank=True, null=True)
    
    tracker = FieldTracker()

    def createWell(self):
        w = Well(well_class = self.well_class)
        w.well_subclass = self.well_subclass
        w.intended_water_use = self.intended_water_use
        w.owner_full_name = self.owner_full_name
        w.owner_mailing_address = self.owner_mailing_address
        w.owner_city = self.owner_city
        w.owner_province_state = self.owner_province_state
        w.owner_postal_code = self.owner_postal_code
    
        w.street_address = self.street_address
        w.city = self.city
        w.legal_lot = self.legal_lot
        w.legal_plan = self.legal_plan
        w.legal_district_lot = self.legal_district_lot
        w.legal_block = self.legal_block
        w.legal_section = self.legal_section
        w.legal_township = self.legal_township
        w.legal_range = self.legal_range
        w.legal_land_district = self.legal_land_district
        w.legal_pid = self.legal_pid
        w.well_location_description = self.well_location_description

        w.identification_plate_number = self.identification_plate_number
        #TODO

        return w;

    class Meta:
        db_table = 'gwells_activity_submission'

    def __str__(self):
        return '%d %s %s' % (self.well_tag_number, self.well_activity_type.code, self.street_address)



class LtsaOwner(TimeStampedModel):
    """
    Well owner information.
    """
    lsts_owner_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(Well, db_column='well_guid', on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    mailing_address = models.CharField(max_length=100, verbose_name='Mailing Address')
    
    city = models.CharField(max_length=100, verbose_name='Town/City')
    province_state = models.ForeignKey(ProvinceState, db_column='province_state_guid', on_delete=models.CASCADE, verbose_name='Province')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')

    tracker = FieldTracker()

    class Meta:
        db_table = 'gwells_ltsa_owner'

    def __str__(self):
        return '%s %s' % (self.full_name, self.mailing_address)





