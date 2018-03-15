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
from .Well import Well
from .WellActivityCode import WellActivityCode
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
from .Driller import Driller

from model_utils import FieldTracker

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class ActivitySubmission(AuditModel):
    """
    Activity information on a Well submitted by a user.
    """
    filing_number = models.AutoField(primary_key=True)
    activity_submission_guid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    well_tag_number = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    well_activity_type = models.ForeignKey(WellActivityCode, db_column='well_activity_code', on_delete=models.CASCADE, verbose_name='Type of Work')
    well_class = models.ForeignKey(WellClassCode, null=True, db_column='well_class_code', on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclassCode, db_column='well_subclass_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUseCode, db_column='intended_water_use_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Intended Water Use')
    driller_responsible = models.ForeignKey(Driller, db_column='driller_responsible_guid', on_delete=models.CASCADE, verbose_name='Person Responsible for Drilling')
    driller_name = models.CharField(max_length=200, blank=True, verbose_name='Name of Person Who Did the Work')
    consultant_name = models.CharField(max_length=200, blank=True, verbose_name='Consultant Name')
    consultant_company = models.CharField(max_length=200, blank=True, verbose_name='Consultant Company')
    work_start_date = models.DateField(verbose_name='Work Start Date')
    work_end_date = models.DateField(verbose_name='Work End Date')

    owner_full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    owner_mailing_address = models.CharField(max_length=100, verbose_name='Mailing Address')
    owner_city = models.CharField(max_length=100, verbose_name='Town/City')
    owner_province_state = models.ForeignKey(ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, verbose_name='Province')
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
    land_district = models.ForeignKey(LandDistrictCode, db_column='land_district_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(blank=True, null=True, verbose_name='PID')
    well_location_description = models.CharField(max_length=500, blank=True, verbose_name='Well Location Description')

    identification_plate_number = models.PositiveIntegerField(blank=True, null=True, verbose_name='Identification Plate Number')
    well_plate_attached = models.CharField(max_length=500, blank=True, verbose_name='Well Identification Plate Is Attached')

    latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    ground_elevation = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethodCode, db_column='ground_elevation_method_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Elevation Determined By')
    drilling_method = models.ForeignKey(DrillingMethodCode, db_column='drilling_method_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Drilling Method')
    other_drilling_method = models.CharField(max_length=50, blank=True, verbose_name='Specify Other Drilling Method')
    well_orientation = models.BooleanField(default=True, verbose_name='Orientation of Well', choices=((True, 'vertical'), (False, 'horizontal')))
    water_supply_system_name = models.CharField(max_length=50, blank=True, verbose_name='Water Supply System Name')
    water_supply_system_well_name = models.CharField(max_length=50, blank=True, verbose_name='Water Supply System Well Name')

    surface_seal_material = models.ForeignKey(SurfaceSealMaterialCode, db_column='surface_seal_material_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Surface Seal Material')
    surface_seal_depth = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Depth')
    surface_seal_thickness = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Thickness', validators=[MinValueValidator(Decimal('1.00'))])
    surface_seal_method = models.ForeignKey(SurfaceSealMethodCode, db_column='surface_seal_method_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Surface Seal Installation Method')
    backfill_above_surface_seal = models.CharField(max_length=250, blank=True, verbose_name='Backfill Material Above Surface Seal')
    backfill_above_surface_seal_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')

    liner_material = models.ForeignKey(LinerMaterialCode, db_column='liner_material_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Liner Material')
    liner_diameter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner Diameter', validators=[MinValueValidator(Decimal('0.00'))])
    liner_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Liner Thickness', validators=[MinValueValidator(Decimal('0.00'))])
    liner_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner From', validators=[MinValueValidator(Decimal('0.00'))])
    liner_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner To', validators=[MinValueValidator(Decimal('0.01'))])

    screen_intake_method = models.ForeignKey(ScreenIntakeMethodCode, db_column='screen_intake_method_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Intake')
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

    development_method = models.ForeignKey(DevelopmentMethodCode, db_column='development_method_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Development Method')
    development_hours = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name='Development Total Duration', validators=[MinValueValidator(Decimal('0.00'))])
    development_notes = models.CharField(max_length=255, blank=True, verbose_name='Development Notes')

    water_quality_characteristics = models.ManyToManyField(WaterQualityCharacteristic, db_table='activity_submission_water_quality', blank=True, verbose_name='Obvious Water Quality Characteristics')
    water_quality_colour = models.CharField(max_length=60, blank=True, verbose_name='Water Quality Colour')
    water_quality_odour = models.CharField(max_length=60, blank=True, verbose_name='Water Quality Odour')

    total_depth_drilled = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Total Depth Drilled')
    finished_well_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Finished Well Depth')
    final_casing_stick_up = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Final Casing Stick Up')
    bedrock_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Depth to Bedrock')
    static_water_level = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Static Water Level (BTOC)')
    well_yield = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, verbose_name='Estimated Well Yield')
    artesian_flow = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Flow')
    artesian_pressure = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure')
    well_cap_type = models.CharField(max_length=40, blank=True, verbose_name='Well Cap Type')
    well_disinfected = models.BooleanField(default=False, verbose_name='Well Disinfected?', choices=((False, 'No'), (True, 'Yes')))

    comments = models.CharField(max_length=3000, blank=True)
    alternative_specs_submitted = models.BooleanField(default=False, verbose_name='Alternative specs submitted (if required)')

    well_yield_unit = models.ForeignKey(WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True)
    diameter = models.CharField(max_length=9, blank=True)  #want to be integer in future

    tracker = FieldTracker()

    def create_well(self):
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
        w.land_district = self.land_district
        w.legal_pid = self.legal_pid
        w.well_location_description = self.well_location_description

        w.identification_plate_number = self.identification_plate_number
        w.latitude = self.latitude
        w.longitude = self.longitude
        w.ground_elevation = self.ground_elevation
        w.ground_elevation_method = self.ground_elevation_method
        w.drilling_method = self.drilling_method
        w.other_drilling_method = self.other_drilling_method
        w.well_orientation = self.well_orientation

        w.surface_seal_material = self.surface_seal_material
        w.surface_seal_depth = self.surface_seal_depth
        w.surface_seal_thickness = self.surface_seal_thickness
        w.surface_seal_method = self.surface_seal_method
        w.backfill_above_surface_seal = self.backfill_above_surface_seal
        w.backfill_above_surface_seal_depth = self.backfill_above_surface_seal_depth

        w.liner_material = self.liner_material
        w.liner_diameter = self.liner_diameter
        w.liner_thickness = self.liner_thickness
        w.liner_from = self.liner_from
        w.liner_to = self.liner_to

        w.screen_intake = self.screen_intake
        w.screen_type = self.screen_type
        w.screen_material = self.screen_material
        w.other_screen_material = self.other_screen_material
        w.screen_opening = self.screen_opening
        w.screen_bottom = self.screen_bottom
        w.other_screen_bottom = self.other_screen_bottom

        w.filter_pack_from = self.filter_pack_from
        w.filter_pack_to = self.filter_pack_to
        w.filter_pack_thickness = self.filter_pack_thickness
        w.filter_pack_material = self.filter_pack_material
        w.filter_pack_material_size = self.filter_pack_material_size

        w.development_method = self.development_method
        w.development_hours = self.development_hours
        w.development_notes = self.development_notes

        w.water_quality_colour = self.water_quality_colour
        w.water_quality_odour = self.water_quality_odour

        w.total_depth_drilled = self.total_depth_drilled
        w.finished_well_depth = self.finished_well_depth
        w.final_casing_stick_up = self.final_casing_stick_up
        w.bedrock_depth = self.bedrock_depth
        w._water_level = self.static_water_level
        w.well_yield = self.well_yield
        w.artestian_flow = self.artestian_flow
        w.artestian_pressure = self.artestian_pressure
        w.well_cap_type = self.well_cap_type
        w.well_disinfected = self.well_disinfected

        w.comments = self.comments
        w.alternative_specs_submitted = self.alternative_specs_submitted
        #TODO

        return w;

    class Meta:
        db_table = 'activity_submission'

    def __str__(self):
        if self.filing_number:
            return '%s %d %s %s' % (self.activity_submission_guid, self.filing_number, self.well_activity_type.well_activity_code, self.street_address)
        else:
            return '%s %s' % (self.activity_submission_guid, self.street_address)
