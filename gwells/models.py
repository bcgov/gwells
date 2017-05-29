import datetime
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
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_activity_type'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class ClassOfWell(models.Model):
    """
    Class of Well type.
    """
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_class_of_well'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class SubclassOfWell(models.Model):
    """
    Subclass of Well type.
    """
    class_of_well = models.ForeignKey(ClassOfWell, db_column='gwells_class_of_well_id', on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_subclass_of_well'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class WellUse(models.Model):
    """
    Usage of Wells (water supply).
    """
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_use'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class DrillingCompany(models.Model):
    """
    Companies who perform drilling.
    """
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
    drilling_company = models.ForeignKey(DrillingCompany, db_column='gwells_drilling_company_id', on_delete=models.CASCADE, verbose_name='Drilling Company')
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'gwells_driller'

    def __str__(self):
        return '%s %s - %s' % (self.first_name, self.surname, self.registration_number)



class WellActivity(TimeStampedModel):
    """
    Activity information on a Well.
    """
    well_activity_type = models.ForeignKey(WellActivityType, db_column='gwells_well_activity_type_id', on_delete=models.CASCADE, verbose_name='Type of Work')
    class_of_well = models.ForeignKey(ClassOfWell, db_column='gwells_class_of_well_id', on_delete=models.CASCADE, verbose_name='Class of Well')
    subclass_of_well = models.ForeignKey(SubclassOfWell, db_column='gwells_subclass_of_well_id', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Subclass of Well')
    well_use = models.ForeignKey(WellUse, db_column='gwells_well_use_id', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Water Supply Well Intended Water Use')
    driller_responsible = models.ForeignKey(Driller, db_column='gwells_driller_responsible_id', on_delete=models.CASCADE, verbose_name='Person Responsible for Drilling')
    driller_name = models.CharField(max_length=200, blank=True, verbose_name='Name of Person Who Did the Work')
    consultant_name = models.CharField(max_length=200, blank=True, verbose_name='Consultant Name')
    consultant_company = models.CharField(max_length=200, blank=True, verbose_name='Consultant Company')
    activity_start_date = models.DateField(verbose_name='Start Date of Work')
    activity_end_date = models.DateField(verbose_name='End Date of Work')

    street_address = models.CharField(max_length=100, blank=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, verbose_name='Town/City')
    legal_lot = models.CharField(max_length=10, blank=True, verbose_name='Lot')
    legal_plan = models.CharField(max_length=20, blank=True, verbose_name='Plan')
    legal_district_lot = models.CharField(max_length=20, blank=True, verbose_name='District Lot')
    legal_block = models.CharField(max_length=10, blank=True, verbose_name='Block')
    legal_section = models.CharField(max_length=10, blank=True, verbose_name='Section')
    legal_township = models.CharField(max_length=20, blank=True, verbose_name='Township')
    legal_range = models.CharField(max_length=10, blank=True, verbose_name='Range')
    legal_land_district = models.ForeignKey(LandDistrict, db_column='gwells_legal_land_district_id', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(blank=True, null=True, verbose_name='PID')
    well_location_description = models.CharField(max_length=500, blank=True)

    identification_plate_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    well_tag_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    diameter = models.CharField(max_length=9, blank=True)  #want to be integer in future
    #diameter_unit
    total_depth_drilled = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    #depth_unit
    finished_well_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    #depth_unit
    well_yield = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    well_yield_unit = models.ForeignKey(WellYieldUnit, db_column='gwells_well_yield_unit_id', on_delete=models.CASCADE, blank=True, null=True)
    
    effective_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    tracker = FieldTracker()
    
    #def get_absolute_url(self):
    #    return reverse('well_activity_detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'gwells_well_activity'

    def __str__(self):
        return '%d %s %s' % (self.well_tag_number, self.well_activity_type.code, self.street_address)



class WellOwner(TimeStampedModel):
    """
    Well owner information.
    """
    well_activity = models.ForeignKey(WellActivity, db_column='gwells_well_activity_id', on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    mailing_address = models.CharField(max_length=100, verbose_name='Mailing Address')
    
    city = models.CharField(max_length=100, verbose_name='Town/City')
    province_state = models.ForeignKey(ProvinceState, db_column='gwells_province_state_id', on_delete=models.CASCADE, blank=True, verbose_name='Province')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')

    effective_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    tracker = FieldTracker()

    class Meta:
        db_table = 'gwells_well_owner'

    def __str__(self):
        return '%s %s' % (self.full_name, self.street_address)





