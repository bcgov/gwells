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

from .AuditModel import AuditModel
from .ProvinceStateCode import ProvinceStateCode
from .WellClassCode import WellClassCode
from .WellSubclassCode import WellSubclassCode
from .WellStatusCode import WellStatusCode
from .IntendedWaterUseCode import IntendedWaterUseCode
from .LicencedStatusCode import LicencedStatusCode
from .LandDistrictCode import LandDistrictCode
from .DrillingCompany import DrillingCompany
from .DrillingMethodCode import DrillingMethodCode
from .GroundElevationMethodCode import GroundElevationMethodCode
from .SurfaceSealMaterialCode import SurfaceSealMaterialCode
from .SurfaceSealMethodCode import SurfaceSealMethodCode
from .LinerMaterialCode import LinerMaterialCode
from .ScreenIntakeMethodCode import ScreenIntakeMethodCode
from .ScreenTypeCode import ScreenTypeCode
from .ScreenMaterialCode import ScreenMaterialCode
from .ScreenOpeningCode import ScreenOpeningCode
from .ScreenBottomCode import ScreenBottomCode
from .FilterPackMaterialCode import FilterPackMaterialCode
from .FilterPackMaterialSizeCode import FilterPackMaterialSizeCode
from .DevelopmentMethodCode import DevelopmentMethodCode
from .WaterQualityCharacteristic import WaterQualityCharacteristic
from .WellYieldUnitCode import WellYieldUnitCode
from .ObsWellStatusCode import ObsWellStatusCode
from .BCGS_Numbers import BCGS_Numbers
from .DecommissionMethodCode import DecommissionMethodCode

from model_utils import FieldTracker

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class Well(AuditModel):
    """
    Well information.
    """
    well_guid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    well_tag_number = models.AutoField(primary_key=True, verbose_name='Well Tag Number')
    identification_plate_number = models.PositiveIntegerField(unique=True, blank=True, null=True, verbose_name="Well Identification Plate Number")

    owner_full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    owner_mailing_address = models.CharField(max_length=100, verbose_name='Mailing Address')
    owner_city = models.CharField(max_length=100, verbose_name='Town/City')
    owner_province_state = models.ForeignKey(ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, blank=True, verbose_name='Province')
    owner_postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')

    well_class = models.ForeignKey(WellClassCode, null=True, db_column='well_class_code', on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclassCode, db_column='well_subclass_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUseCode, db_column='intended_water_use_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Intended Water Use')
    well_status = models.ForeignKey(WellStatusCode, db_column='well_status_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Well Status')
    licenced_status = models.ForeignKey(LicencedStatusCode, db_column='licenced_status_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Licenced Status')

    street_address = models.CharField(max_length=100, blank=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, verbose_name='Town/City')
    legal_lot = models.CharField(max_length=10, blank=True, verbose_name='Lot')
    legal_plan = models.CharField(max_length=20, blank=True, verbose_name='Plan')
    legal_district_lot = models.CharField(max_length=20, blank=True, verbose_name='District Lot')
    legal_block = models.CharField(max_length=10, blank=True, verbose_name='Block')
    legal_section = models.CharField(max_length=10, blank=True, verbose_name='Section')
    legal_township = models.CharField(max_length=20, blank=True, verbose_name='Township')
    legal_range = models.CharField(max_length=10, blank=True, verbose_name='Range')
    land_district = models.ForeignKey(LandDistrictCode, db_column='land_district_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Land District')
    legal_pid = models.CharField(max_length=9, blank=True, null=True, verbose_name='Property Identification Description (PID)')
    well_location_description = models.CharField(max_length=500, blank=True, verbose_name='Description of Well Location')

    construction_start_date = models.DateTimeField(null=True, verbose_name="Construction Start Date")
    construction_end_date = models.DateTimeField(null=True, verbose_name="Construction Date")

    alteration_start_date = models.DateTimeField(null=True, verbose_name="Alteration Start Date")
    alteration_end_date = models.DateTimeField(null=True, verbose_name="Alteration Date")

    decommission_start_date = models.DateTimeField(null=True, verbose_name="Decommission Start Date")
    decommission_end_date = models.DateTimeField(null=True, verbose_name="Decommission Date")

    drilling_company = models.ForeignKey(DrillingCompany, db_column='drilling_company_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Drilling Company')

    well_identification_plate_attached = models.CharField(max_length=500, blank=True, null=True, verbose_name='Well Identification Plate Is Attached')

    latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, verbose_name='Latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Longitude')
    ground_elevation = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethodCode, db_column='ground_elevation_method_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Elevation Determined By')
    drilling_method = models.ForeignKey(DrillingMethodCode, db_column='drilling_method_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Drilling Method')
    other_drilling_method = models.CharField(max_length=50, blank=True, null=True, verbose_name='Specify Other Drilling Method')
    well_orientation = models.BooleanField(default=True, verbose_name='Orientation of Well', choices=((True, 'vertical'), (False, 'horizontal')))

    surface_seal_material = models.ForeignKey(SurfaceSealMaterialCode, db_column='surface_seal_material_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Surface Seal Material')
    surface_seal_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Length')
    surface_seal_thickness = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Thickness')
    surface_seal_method = models.ForeignKey(SurfaceSealMethodCode, db_column='surface_seal_method_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Surface Seal Installation Method')
    backfill_type = models.CharField(max_length=250, blank=True, null=True, verbose_name="Backfill Material Above Surface Seal")
    backfill_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')

    liner_material = models.ForeignKey(LinerMaterialCode, db_column='liner_material_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Liner Material')
    liner_diameter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner Diameter', validators=[MinValueValidator(Decimal('0.00'))])
    liner_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Liner Thickness', validators=[MinValueValidator(Decimal('0.00'))])
    liner_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner From', validators=[MinValueValidator(Decimal('0.00'))])
    liner_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner To', validators=[MinValueValidator(Decimal('0.01'))])

    screen_intake_method = models.ForeignKey(ScreenIntakeMethodCode, db_column='screen_intake_method_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Intake Method')
    screen_type = models.ForeignKey(ScreenTypeCode, db_column='screen_type_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Type')
    screen_material = models.ForeignKey(ScreenMaterialCode, db_column='screen_material_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Material')
    other_screen_material = models.CharField(max_length=50, blank=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpeningCode, db_column='screen_opening_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Opening')
    screen_bottom = models.ForeignKey(ScreenBottomCode, db_column='screen_bottom_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Bottom')
    other_screen_bottom = models.CharField(max_length=50, blank=True, verbose_name='Specify Other Screen Bottom')

    filter_pack_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Filter Pack From', validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Filter Pack To', validators=[MinValueValidator(Decimal('0.01'))])
    filter_pack_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Filter Pack Thickness', validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_material = models.ForeignKey(FilterPackMaterialCode, db_column='filter_pack_material_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Filter Pack Material')
    filter_pack_material_size = models.ForeignKey(FilterPackMaterialSizeCode, db_column='filter_pack_material_size_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Filter Pack Material Size')

    development_method = models.ForeignKey(DevelopmentMethodCode, db_column='development_method_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Developed By')
    development_hours = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name='Development Total Duration', validators=[MinValueValidator(Decimal('0.00'))])
    development_notes = models.CharField(max_length=255, blank=True, verbose_name='Development Notes')

    water_quality_characteristics = models.ManyToManyField(WaterQualityCharacteristic, db_table='well_water_quality', blank=True, verbose_name='Obvious Water Quality Characteristics')
    water_quality_colour = models.CharField(max_length=60, blank=True, verbose_name='Water Quality Colour')
    water_quality_odour = models.CharField(max_length=60, blank=True, verbose_name='Water Quality Odour')

    total_depth_drilled = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Total Depth Drilled')
    finished_well_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Finished Well Depth')
    final_casing_stick_up = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, verbose_name='Final Casing Stick Up')
    bedrock_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Depth to Bedrock')
    water_supply_system_name = models.CharField(max_length=80, blank=True, null=True, verbose_name='Water Supply System Name')
    water_supply_system_well_name = models.CharField(max_length=80, blank=True, null=True, verbose_name='Water Supply System Well Name')
    static_water_level = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Static Water Level (BTOC)')
    well_yield = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, verbose_name='Estimated Well Yield')
    artesian_flow = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Flow')
    artesian_pressure = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure')
    well_cap_type = models.CharField(max_length=40, blank=True, null=True, verbose_name='Well Cap')
    well_disinfected = models.BooleanField(default=False, verbose_name='Well Disinfected', choices=((False, 'No'), (True, 'Yes')))

    comments = models.CharField(max_length=3000, blank=True, null=True)
    alternative_specs_submitted = models.BooleanField(default=False, verbose_name='Alternative specs submitted (if required)', choices=((False, 'No'), (True, 'Yes')))

    well_yield_unit = models.ForeignKey(WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True)
    diameter = models.CharField(max_length=9, blank=True)  #want to be integer in future

    observation_well_number = models.CharField(max_length=3, blank=True, null=True, verbose_name="Observation Well Number")

    observation_well_status = models.ForeignKey(ObsWellStatusCode, db_column='obs_well_status_code', blank=True, null="True", verbose_name="Observation Well Status")

    ems = models.CharField(max_length=10, blank=True, null=True, verbose_name="Environmental Monitoring System (EMS) ID")

    utm_zone_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Zone")
    utm_northing = models.IntegerField(blank=True, null=True, verbose_name="UTM Northing")
    utm_easting = models.IntegerField(blank=True, null=True, verbose_name="UTM Easting")
    utm_accuracy_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Location Accuracy Code")
    bcgs_id = models.ForeignKey(BCGS_Numbers, db_column='bcgs_id', on_delete=models.CASCADE, blank=True, null=True, verbose_name="BCGS Mapsheet Number")

    decommission_reason = models.CharField(max_length=250, blank=True, null=True, verbose_name="Reason for Decommission")
    decommission_method = models.ForeignKey(DecommissionMethodCode, db_column='decommission_method_code', blank=True, null="True", verbose_name="Method of Decommission")
    sealant_material = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sealant Material")
    backfill_material = models.CharField(max_length=100, blank=True, null=True, verbose_name="Backfill Material")
    decommission_details = models.CharField(max_length=250, blank=True, null=True, verbose_name="Decommission Details")

    tracker = FieldTracker()

    class Meta:
        db_table = 'well'

    def __str__(self):
        if self.well_tag_number:
            return '%d %s' % (self.well_tag_number, self.street_address)
        else:
            return 'No well tag number %s' % (self.street_address)

    # Custom JSON serialisation for Wells. Expand as needed.
    def as_dict(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "guid": self.well_guid,
            "identification_plate_number": self.identification_plate_number,
            "street_address": self.street_address,
            "well_tag_number": self.well_tag_number
        }
