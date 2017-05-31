from django.contrib import admin
from .models import ProvinceState, LandDistrict, WellYieldUnit, WellActivityType, WellClass, WellSubclass, IntendedWaterUse, DrillingCompany, Driller
# Register your models here.
admin.site.register(ProvinceState)
admin.site.register(LandDistrict)
admin.site.register(WellYieldUnit)
admin.site.register(WellActivityType)
admin.site.register(WellClass)
admin.site.register(WellSubclass)
admin.site.register(IntendedWaterUse)
admin.site.register(DrillingCompany)
admin.site.register(Driller)
