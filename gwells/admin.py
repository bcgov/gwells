from django.contrib import admin
from .models import ProvinceState, LandDistrict, WellYieldUnit, WellActivityType, WellClass, WellSubclass, IntendedWaterUse, DrillingCompany, Driller, GroundElevationMethod, DrillingMethod
from .models import SurficialMaterial, BedrockMaterial, BedrockMaterialDescriptor, LithologyStructure, LithologyWeathering, LithologyColour, LithologyHardness, LithologyMoisture
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
admin.site.register(GroundElevationMethod)
admin.site.register(DrillingMethod)
admin.site.register(SurficialMaterial)
admin.site.register(BedrockMaterial)
admin.site.register(BedrockMaterialDescriptor)
admin.site.register(LithologyStructure)
admin.site.register(LithologyWeathering)
admin.site.register(LithologyColour)
admin.site.register(LithologyHardness)
admin.site.register(LithologyMoisture)
