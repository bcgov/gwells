import datetime
from django.db import models
from model_utils.models import TimeStampedModel
from model_utils import FieldTracker



class ProvinceState(models.Model):
    """
    Lookup of Provinces/States.
    """
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    sort_order = models.IntegerField()
    
    class Meta:
        db_table = 'gwells_province_state'

    def __str__(self):
        return self.code



class WellYieldUnit(models.Model):
    """
    Units of Well Yield.
    """
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    sort_order = models.IntegerField()
    
    class Meta:
        db_table = 'gwells_well_yield_unit'

    def __str__(self):
        return self.code



class WellOwner(TimeStampedModel):
    """
    Well owner information.
    """
    given_name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100)
    address_line = models.CharField(max_length=100)
    
    city = models.CharField(max_length=100)
    province_state_id = models.ForeignKey(ProvinceState, db_column='gwells_province_state_id', on_delete=models.CASCADE, blank=True)
    tracker = FieldTracker()
    
    class Meta:
        db_table = 'gwells_well_owner'

    def __str__(self):
        return self.given_name + self.surname + address_line

	

class Well(TimeStampedModel):
    """
    Well information.
    """
    well_owner_id = models.ForeignKey(WellOwner, db_column='gwells_well_owner_id', on_delete=models.CASCADE)
    address_line = models.CharField(max_length=100, blank=True)
    site_area = models.CharField(max_length=50, blank=True)
    lot_number = models.CharField(max_length=10, blank=True)
    legal_plan = models.CharField(max_length=20, blank=True)
    legal_district_lot = models.IntegerField(blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)
    identification_plate_number = models.IntegerField(unique=True, blank=True, null=True)
    diameter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)  #currently text
    #diameter_unit
    well_drilled_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    #depth_unit
    #final_well_depth = models.DecimalField(max_digits=7, decimal_places=2)
    #depth_unit
    well_yield = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    well_yield_unit_id = models.ForeignKey(WellYieldUnit, db_column='gwells_well_yield_unit_id', on_delete=models.CASCADE, blank=True)
    tracker = FieldTracker()
    
    def __str__(self):
        return self.address_line + self.identification_plate_number




