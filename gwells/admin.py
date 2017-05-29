from django.contrib import admin
from .models import ProvinceState, LandDistrict, WellYieldUnit, WellActivityType, ClassOfWell, SubclassOfWell, WellUse, DrillingCompany, Driller
# Register your models here.
admin.site.register(ProvinceState)
admin.site.register(LandDistrict)
admin.site.register(WellYieldUnit)
admin.site.register(WellActivityType)
admin.site.register(ClassOfWell)
admin.site.register(SubclassOfWell)
admin.site.register(WellUse)
admin.site.register(DrillingCompany)
admin.site.register(Driller)
