"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from django.contrib import admin
from wells.models import (
    DecommissionMaterialCode,
    DecommissionMethodCode,
    WaterQualityCharacteristic,
    WaterQualityColour,
    FilterPackMaterialSizeCode,
    FilterPackMaterialCode,
    Well,
    WellAttachment,
    WellLicence
)
from gwells.models.lithology import (
    LithologyColourCode, LithologyHardnessCode,
    LithologyMaterialCode, LithologyMoistureCode,
)

# Register your models here.

admin.site.register(WaterQualityCharacteristic)
admin.site.register(WaterQualityColour)
admin.site.register(DecommissionMaterialCode)
admin.site.register(DecommissionMethodCode)
admin.site.register(LithologyColourCode)
admin.site.register(LithologyHardnessCode)
admin.site.register(LithologyMaterialCode)
admin.site.register(LithologyMoistureCode)
admin.site.register(FilterPackMaterialSizeCode)
admin.site.register(FilterPackMaterialCode)
admin.site.register(Well)
admin.site.register(WellAttachment)
admin.site.register(WellLicence)
