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
    def __str__(self):
        return self.code



class WellYieldUnit(models.Model):
    """
    Units of Well Yield.
    """
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    sort_order = models.IntegerField()
    def __str__(self):
        return self.code



class WellOwner(TimeStampedModel):
    """
    Well owner information.
    """
    given_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province_state_id = models.ForeignKey(ProvinceState, on_delete=models.CASCADE)
    def __str__(self):
        return self.given_name + self.surname + street_number + street_name
    tracker = FieldTracker()

	

class Well(TimeStampedModel):
    """
    Well information.
    """
    well_owner_id = models.ForeignKey(WellOwner, on_delete=models.CASCADE)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=100)
    site_area = models.CharField(max_length=50)
    lot_number = models.CharField(max_length=10)
    legal_plan = models.CharField(max_length=20)
    legal_district_lot = models.IntegerField()
    pid = models.IntegerField()
    identification_plate_number = models.IntegerField()
    diameter = models.DecimalField(max_digits=7, decimal_places=2)  #currently text
    #diameter_unit
    depth = models.DecimalField(max_digits=7, decimal_places=2)
    #depth_unit
    well_yield = models.DecimalField(max_digits=8, decimal_places=3)
    well_yield_unit_id = models.ForeignKey(WellYieldUnit, on_delete=models.CASCADE)
    def __str__(self):
        return self.street_number + self.street_name + self.identification_plate_number
    tracker = FieldTracker()




