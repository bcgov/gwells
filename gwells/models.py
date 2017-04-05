import datetime
from django.db import models
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

    def __str__(self):
        return self.code



class LandDistrict(models.Model):
    """
    Lookup of Land Districts.
    """
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_land_district'

    def __str__(self):
        return self.code



class WellYieldUnit(models.Model):
    """
    Units of Well Yield.
    """
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_yield_unit'

    def __str__(self):
        return self.code



class WellOwner(TimeStampedModel):
    """
    Well owner information.
    """
    full_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=100)
    
    city = models.CharField(max_length=100)
    province_state_id = models.ForeignKey(ProvinceState, db_column='gwells_province_state_id', on_delete=models.CASCADE, blank=True)
    tracker = FieldTracker()
    
    class Meta:
        db_table = 'gwells_well_owner'

    def __str__(self):
        return '%s %s' % (self.full_name, self.street_address)

	

class Well(TimeStampedModel):
    """
    Well information.
    """
    well_owner_id = models.ForeignKey(WellOwner, db_column='gwells_well_owner_id', on_delete=models.CASCADE, blank=True, null=True)
    street_address = models.CharField(max_length=100, blank=True)
    site_area = models.CharField(max_length=50, blank=True)
    lot_number = models.CharField(max_length=10, blank=True)
    legal_plan = models.CharField(max_length=20, blank=True)
    legal_district_lot = models.CharField(max_length=20, blank=True)
    land_district_id = models.ForeignKey(LandDistrict, db_column='gwells_land_district_id', on_delete=models.CASCADE, blank=True, null=True)
    pid = models.PositiveIntegerField(blank=True, null=True)
    identification_plate_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    well_tag_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    diameter = models.CharField(max_length=9, blank=True)  #want to be integer in future
    #diameter_unit
    well_drilled_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    #depth_unit
    finished_well_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    #depth_unit
    well_yield = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    well_yield_unit_id = models.ForeignKey(WellYieldUnit, db_column='gwells_well_yield_unit_id', on_delete=models.CASCADE, blank=True, null=True)
    tracker = FieldTracker()
    
    def __str__(self):
        return '%d %s' % (self.well_tag_number, self.street_address)




