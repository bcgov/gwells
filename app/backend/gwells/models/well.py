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

from model_utils import FieldTracker

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

from gwells.models import AuditModel, ProvinceStateCode, ScreenIntakeMethodCode, ScreenMaterialCode,\
    ScreenOpeningCode, ScreenBottomCode, ScreenTypeCode, ScreenAssemblyTypeCode
from registries.models import Person


class DecommissionMethodCode(AuditModel):
    decommission_method_code = models.CharField(primary_key=True, max_length=10, editable=False,
                                                verbose_name="Code")
    description = models.CharField(max_length=255, verbose_name="Description")
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'decommission_method_code'
        ordering = ['display_order']

    def __str__(self):
        return self.description


class BCGS_Numbers(AuditModel):
    bcgs_id = models.BigIntegerField(primary_key=True, default=uuid.uuid4, editable=False)
    bcgs_number = models.CharField(max_length=20, verbose_name="BCGS Mapsheet Number")

    class Meta:
        db_table = 'bcgs_number'
        ordering = ['bcgs_number']

    def __str__(self):
        return self.description


class ObsWellStatusCode(AuditModel):
    """
    Observation Well Status.
    """
    obs_well_status_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'obs_well_status_code'
        ordering = ['display_order', 'obs_well_status_code']

    def save(self, *args, **kwargs):
        self.validate()
        super(WellStatusCode, self).save(*args, **kwargs)


class YieldEstimationMethodCode(AuditModel):
    """
     The method used to estimate the yield of a well, e.g. Air Lifting, Bailing, Pumping.
    """
    yield_estimation_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'yield_estimation_method_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class WaterQualityCharacteristic(AuditModel):
    """
     The characteristic of the well water, e.g. Fresh, Salty, Clear.
    """
    water_quality_characteristic_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'water_quality_characteristic'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class DevelopmentMethodCode(AuditModel):
    """
     How the well was developed in order to remove the fine sediment and other organic or inorganic material
     that immediately surrounds the well screen, the drill hole or the intake area at the bottom of the well,
     e.g. air lifting, pumping, bailing.
    """
    development_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'development_method_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class FilterPackMaterialSizeCode(AuditModel):
    """
     The size of material used to pack a well filter, e.g. 1.0 - 2.0 mm, 2.0 - 4.0 mm, 4.0 - 8.0 mm.
    """
    filter_pack_material_size_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'filter_pack_material_size_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class FilterPackMaterialCode(AuditModel):
    """
     The material used to pack a well filter, e.g. Very coarse sand, Very fine gravel, Fine gravel.
    """
    filter_pack_material_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'filter_pack_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class LinerMaterialCode(AuditModel):
    """
     Liner material installed in a well to protect the well pump or other works in the well from damage.
    """
    liner_material_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'liner_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class SurfaceSealMethodCode(AuditModel):
    """
     Method used to install the surface seal in the annular space around the outside of the outermost casing
     and between mulitple casings of a well.
    """
    surface_seal_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'surface_seal_method_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class SurfaceSealMaterialCode(AuditModel):
    """
     Sealant material used that is installed in the annular space around the outside of the outermost casing
     and between multiple casings of a well.
    """
    surface_seal_material_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'surface_seal_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class DrillingMethodCode(AuditModel):
    """
    The method used to drill a well. For example, air rotary, dual rotary, cable tool, excavating, other.
    """
    drilling_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'drilling_method_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


# TODO: Remove this class - now using registries.something
# Not a Code table, but a representative sample of data to support search
class DrillingCompany(AuditModel):
    """
    Companies who perform drilling.
    """
    drilling_company_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    drilling_company_code = models.CharField(
        max_length=10, blank=True, null=True)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'drilling_company'
        verbose_name_plural = 'Drilling Companies'

    def __str__(self):
        return self.name


class LandDistrictCode(AuditModel):
    """
    Lookup of Legal Land Districts.
    """
    land_district_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    name = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'land_district_code'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class LicencedStatusCode(AuditModel):
    """
    LicencedStatusCode of Well.
    """
    licenced_status_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'licenced_status_code'
        ordering = ['display_order', 'licenced_status_code']

    def save(self, *args, **kwargs):
        self.validate()
        super(LicencedStatusCode, self).save(*args, **kwargs)


class IntendedWaterUseCode(AuditModel):
    """
    Usage of Wells (water supply).
    """
    intended_water_use_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'intended_water_use_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class GroundElevationMethodCode(AuditModel):
    """
    The method used to determine the ground elevation of a well.
    Some examples of methods to determine ground elevation include:
    GPS, Altimeter, Differential GPS, Level, 1:50,000 map, 1:20,000 map, 1:10,000 map, 1:5,000 map.
    """
    ground_elevation_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'ground_elevation_method_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class WellClassCode(AuditModel):
    """
    Class of Well type.
    """
    well_class_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'well_class_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class WellStatusCode(AuditModel):
    """
    Well Status.
    """
    well_status_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'well_status_code'
        ordering = ['display_order', 'well_status_code']

    def save(self, *args, **kwargs):
        self.validate()
        super(WellStatusCode, self).save(*args, **kwargs)


class WellActivityCode(AuditModel):
    """
    Types of Well Activity.
    """
    well_activity_type_code = models.CharField(
        primary_key=True, max_length=10,  editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'well_activity_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class WellSubclassCode(AuditModel):
    """
    Subclass of Well type; we use GUID here as Django doesn't support multi-column PK's
    """
    well_subclass_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    well_class = models.ForeignKey(WellClassCode, null=True, db_column='well_class_code',
                                   on_delete=models.PROTECT, blank=True)
    well_subclass_code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'well_subclass_code'
        ordering = ['display_order', 'description']

    def validate_unique(self, exclude=None):
        qs = Room.objects.filter(name=self.well_subclass_code)
        if qs.filter(well_class__well_class_code=self.well_class__well_class_code).exists():
            raise ValidationError('Code must be unique per Well Class')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(WellSubclassCode, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class WellYieldUnitCode(AuditModel):
    """
    Units of Well Yield.
    """
    well_yield_unit_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'well_yield_unit_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class Well(AuditModel):
    """
    Well information.
    """
    well_guid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    well_tag_number = models.AutoField(
        primary_key=True, verbose_name='Well Tag Number')
    identification_plate_number = models.PositiveIntegerField(
        unique=True, blank=True, null=True, verbose_name="Well Identification Plate Number")

    owner_full_name = models.CharField(
        max_length=200, verbose_name='Owner Name')
    owner_mailing_address = models.CharField(
        max_length=100, verbose_name='Mailing Address')
    owner_city = models.CharField(max_length=100, verbose_name='Town/City')
    owner_province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, blank=True,
        verbose_name='Province')
    owner_postal_code = models.CharField(
        max_length=10, blank=True, verbose_name='Postal Code')

    well_class = models.ForeignKey(WellClassCode, null=True, db_column='well_class_code',
                                   on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclassCode, db_column='well_subclass_guid',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUseCode, db_column='intended_water_use_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='Intended Water Use')
    well_status = models.ForeignKey(WellStatusCode, db_column='well_status_code',
                                    on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='Well Status')
    licenced_status = models.ForeignKey(LicencedStatusCode, db_column='licenced_status_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Licenced Status')

    street_address = models.CharField(
        max_length=100, blank=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True,
                            verbose_name='Town/City')
    legal_lot = models.CharField(max_length=10, blank=True, verbose_name='Lot')
    legal_plan = models.CharField(
        max_length=20, blank=True, verbose_name='Plan')
    legal_district_lot = models.CharField(
        max_length=20, blank=True, verbose_name='District Lot')
    legal_block = models.CharField(
        max_length=10, blank=True, verbose_name='Block')
    legal_section = models.CharField(
        max_length=10, blank=True, verbose_name='Section')
    legal_township = models.CharField(
        max_length=20, blank=True, verbose_name='Township')
    legal_range = models.CharField(
        max_length=10, blank=True, verbose_name='Range')
    land_district = models.ForeignKey(LandDistrictCode, db_column='land_district_code',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Land District')
    legal_pid = models.CharField(max_length=9, blank=True, null=True,
                                 verbose_name='Property Identification Description (PID)')
    well_location_description = models.CharField(
        max_length=500, blank=True, verbose_name='Description of Well Location')

    construction_start_date = models.DateTimeField(
        null=True, verbose_name="Construction Start Date")
    construction_end_date = models.DateTimeField(
        null=True, verbose_name="Construction Date")

    alteration_start_date = models.DateTimeField(
        null=True, verbose_name="Alteration Start Date")
    alteration_end_date = models.DateTimeField(
        null=True, verbose_name="Alteration Date")

    decommission_start_date = models.DateTimeField(
        null=True, verbose_name="Decommission Start Date")
    decommission_end_date = models.DateTimeField(
        null=True, verbose_name="Decommission Date")

    drilling_company = models.ForeignKey(DrillingCompany, db_column='drilling_company_guid',
                                         on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name='Drilling Company')

    well_identification_plate_attached = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Well Identification Plate Is Attached')

    latitude = models.DecimalField(
        max_digits=8, decimal_places=6, blank=True, null=True, verbose_name='Latitude')
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Longitude')
    ground_elevation = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethodCode,
                                                db_column='ground_elevation_method_code',
                                                on_delete=models.CASCADE, blank=True, null=True,
                                                verbose_name='Elevation Determined By')
    drilling_method = models.ForeignKey(DrillingMethodCode, db_column='drilling_method_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Drilling Method')
    other_drilling_method = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Specify Other Drilling Method')
    well_orientation = models.BooleanField(default=True, verbose_name='Orientation of Well', choices=(
        (True, 'vertical'), (False, 'horizontal')))

    surface_seal_material = models.ForeignKey(SurfaceSealMaterialCode, db_column='surface_seal_material_code',
                                              on_delete=models.CASCADE, blank=True, null=True,
                                              verbose_name='Surface Seal Material')
    surface_seal_length = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Length')
    surface_seal_thickness = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Thickness')
    surface_seal_method = models.ForeignKey(SurfaceSealMethodCode, db_column='surface_seal_method_code',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name='Surface Seal Installation Method')
    backfill_type = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Backfill Material Above Surface Seal")
    backfill_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')

    liner_material = models.ForeignKey(LinerMaterialCode, db_column='liner_material_code',
                                       on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Liner Material')
    liner_diameter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                         verbose_name='Liner Diameter',
                                         validators=[MinValueValidator(Decimal('0.00'))])
    liner_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                          verbose_name='Liner Thickness',
                                          validators=[MinValueValidator(Decimal('0.00'))])
    liner_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                     verbose_name='Liner From',
                                     validators=[MinValueValidator(Decimal('0.00'))])
    liner_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                   verbose_name='Liner To', validators=[MinValueValidator(Decimal('0.01'))])

    screen_intake_method = models.ForeignKey(ScreenIntakeMethodCode, db_column='screen_intake_method_code',
                                             on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name='Intake Method')
    screen_type = models.ForeignKey(ScreenTypeCode, db_column='screen_type_code',
                                    on_delete=models.CASCADE, blank=True, null=True, verbose_name='Type')
    screen_material = models.ForeignKey(ScreenMaterialCode, db_column='screen_material_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Material')
    other_screen_material = models.CharField(
        max_length=50, blank=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpeningCode, db_column='screen_opening_code',
                                       on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Opening')
    screen_bottom = models.ForeignKey(ScreenBottomCode, db_column='screen_bottom_code',
                                      on_delete=models.CASCADE, blank=True, null=True, verbose_name='Bottom')
    other_screen_bottom = models.CharField(
        max_length=50, blank=True, verbose_name='Specify Other Screen Bottom')

    filter_pack_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                           verbose_name='Filter Pack From',
                                           validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                         verbose_name='Filter Pack To',
                                         validators=[MinValueValidator(Decimal('0.01'))])
    filter_pack_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                                verbose_name='Filter Pack Thickness',
                                                validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_material = models.ForeignKey(FilterPackMaterialCode, db_column='filter_pack_material_code',
                                             on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name='Filter Pack Material')
    filter_pack_material_size = models.ForeignKey(FilterPackMaterialSizeCode,
                                                  db_column='filter_pack_material_size_code',
                                                  on_delete=models.CASCADE, blank=True, null=True,
                                                  verbose_name='Filter Pack Material Size')

    development_method = models.ForeignKey(DevelopmentMethodCode, db_column='development_method_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='Developed By')
    development_hours = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,
                                            verbose_name='Development Total Duration',
                                            validators=[MinValueValidator(Decimal('0.00'))])
    development_notes = models.CharField(
        max_length=255, blank=True, verbose_name='Development Notes')

    water_quality_characteristics = models.ManyToManyField(
        WaterQualityCharacteristic, db_table='well_water_quality', blank=True,
        verbose_name='Obvious Water Quality Characteristics')
    water_quality_colour = models.CharField(
        max_length=60, blank=True, verbose_name='Water Quality Colour')
    water_quality_odour = models.CharField(
        max_length=60, blank=True, verbose_name='Water Quality Odour')

    total_depth_drilled = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Total Depth Drilled')
    finished_well_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Finished Well Depth')
    final_casing_stick_up = models.DecimalField(
        max_digits=6, decimal_places=3, blank=True, null=True, verbose_name='Final Casing Stick Up')
    bedrock_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Depth to Bedrock')
    water_supply_system_name = models.CharField(
        max_length=80, blank=True, null=True, verbose_name='Water Supply System Name')
    water_supply_system_well_name = models.CharField(
        max_length=80, blank=True, null=True, verbose_name='Water Supply System Well Name')
    static_water_level = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Static Water Level (BTOC)')
    well_yield = models.DecimalField(
        max_digits=8, decimal_places=3, blank=True, null=True, verbose_name='Estimated Well Yield')
    artesian_flow = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Flow')
    artesian_pressure = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure')
    well_cap_type = models.CharField(
        max_length=40, blank=True, null=True, verbose_name='Well Cap')
    well_disinfected = models.BooleanField(
        default=False, verbose_name='Well Disinfected', choices=((False, 'No'), (True, 'Yes')))

    comments = models.CharField(max_length=3000, blank=True, null=True)
    alternative_specs_submitted = \
        models.BooleanField(default=False,
                            verbose_name='Alternative specs submitted (if required)',
                            choices=((False, 'No'), (True, 'Yes')))

    well_yield_unit = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True)
    # want to be integer in future
    diameter = models.CharField(max_length=9, blank=True)

    observation_well_number = models.CharField(
        max_length=3, blank=True, null=True, verbose_name="Observation Well Number")

    observation_well_status = models.ForeignKey(
        ObsWellStatusCode, db_column='obs_well_status_code', blank=True, null="True",
        verbose_name="Observation Well Status")

    ems = models.CharField(max_length=10, blank=True, null=True,
                           verbose_name="Environmental Monitoring System (EMS) ID")

    utm_zone_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Zone")
    utm_northing = models.IntegerField(
        blank=True, null=True, verbose_name="UTM Northing")
    utm_easting = models.IntegerField(
        blank=True, null=True, verbose_name="UTM Easting")
    utm_accuracy_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Location Accuracy Code")
    bcgs_id = models.ForeignKey(BCGS_Numbers, db_column='bcgs_id', on_delete=models.CASCADE,
                                blank=True, null=True, verbose_name="BCGS Mapsheet Number")

    decommission_reason = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Reason for Decommission")
    decommission_method = models.ForeignKey(
        DecommissionMethodCode, db_column='decommission_method_code', blank=True, null="True",
        verbose_name="Method of Decommission")
    sealant_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Sealant Material")
    backfill_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Backfill Material")
    decommission_details = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Decommission Details")

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


class ActivitySubmission(AuditModel):
    """
    Activity information on a Well submitted by a user.
    """
    filing_number = models.AutoField(primary_key=True)
    activity_submission_guid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    well_tag_number = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    well_activity_type = models.ForeignKey(
        WellActivityCode, db_column='well_activity_code', on_delete=models.CASCADE,
        verbose_name='Type of Work')
    well_class = models.ForeignKey(WellClassCode, null=True, db_column='well_class_code',
                                   on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclassCode, db_column='well_subclass_guid',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUseCode, db_column='intended_water_use_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='Intended Water Use')
    driller_responsible = models.ForeignKey(Person, db_column='driller_responsible_guid',
                                            on_delete=models.PROTECT,
                                            verbose_name='Person Responsible for Drilling')
    driller_name = models.CharField(
        max_length=200, blank=True, verbose_name='Name of Person Who Did the Work')
    consultant_name = models.CharField(
        max_length=200, blank=True, verbose_name='Consultant Name')
    consultant_company = models.CharField(
        max_length=200, blank=True, verbose_name='Consultant Company')
    work_start_date = models.DateField(verbose_name='Work Start Date')
    work_end_date = models.DateField(verbose_name='Work End Date')

    owner_full_name = models.CharField(
        max_length=200, verbose_name='Owner Name')
    owner_mailing_address = models.CharField(
        max_length=100, verbose_name='Mailing Address')
    owner_city = models.CharField(max_length=100, verbose_name='Town/City')
    owner_province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, verbose_name='Province')
    owner_postal_code = models.CharField(
        max_length=10, blank=True, verbose_name='Postal Code')

    street_address = models.CharField(
        max_length=100, blank=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True,
                            verbose_name='Town/City')
    legal_lot = models.CharField(max_length=10, blank=True, verbose_name='Lot')
    legal_plan = models.CharField(
        max_length=20, blank=True, verbose_name='Plan')
    legal_district_lot = models.CharField(
        max_length=20, blank=True, verbose_name='District Lot')
    legal_block = models.CharField(
        max_length=10, blank=True, verbose_name='Block')
    legal_section = models.CharField(
        max_length=10, blank=True, verbose_name='Section')
    legal_township = models.CharField(
        max_length=20, blank=True, verbose_name='Township')
    legal_range = models.CharField(
        max_length=10, blank=True, verbose_name='Range')
    land_district = models.ForeignKey(LandDistrictCode, db_column='land_district_code',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='PID')
    well_location_description = models.CharField(
        max_length=500, blank=True, verbose_name='Well Location Description')

    identification_plate_number = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Identification Plate Number')
    well_plate_attached = models.CharField(
        max_length=500, blank=True, verbose_name='Well Identification Plate Is Attached')

    latitude = models.DecimalField(
        max_digits=8, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    ground_elevation = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethodCode,
                                                db_column='ground_elevation_method_code',
                                                on_delete=models.CASCADE, blank=True, null=True,
                                                verbose_name='Elevation Determined By')
    drilling_method = models.ForeignKey(DrillingMethodCode, db_column='drilling_method_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Drilling Method')
    other_drilling_method = models.CharField(
        max_length=50, blank=True, verbose_name='Specify Other Drilling Method')
    well_orientation = models.BooleanField(default=True, verbose_name='Orientation of Well', choices=(
        (True, 'vertical'), (False, 'horizontal')))
    water_supply_system_name = models.CharField(
        max_length=50, blank=True, verbose_name='Water Supply System Name')
    water_supply_system_well_name = models.CharField(
        max_length=50, blank=True, verbose_name='Water Supply System Well Name')

    surface_seal_material = models.ForeignKey(SurfaceSealMaterialCode, db_column='surface_seal_material_code',
                                              on_delete=models.CASCADE, blank=True, null=True,
                                              verbose_name='Surface Seal Material')
    surface_seal_depth = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Depth')
    surface_seal_thickness = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                 verbose_name='Surface Seal Thickness',
                                                 validators=[MinValueValidator(Decimal('1.00'))])
    surface_seal_method = models.ForeignKey(SurfaceSealMethodCode, db_column='surface_seal_method_code',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name='Surface Seal Installation Method')
    backfill_above_surface_seal = models.CharField(
        max_length=250, blank=True, verbose_name='Backfill Material Above Surface Seal')
    backfill_above_surface_seal_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')

    liner_material = models.ForeignKey(LinerMaterialCode, db_column='liner_material_code',
                                       on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Liner Material')
    liner_diameter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                         verbose_name='Liner Diameter',
                                         validators=[MinValueValidator(Decimal('0.00'))])
    liner_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                          verbose_name='Liner Thickness',
                                          validators=[MinValueValidator(Decimal('0.00'))])
    liner_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                     verbose_name='Liner From',
                                     validators=[MinValueValidator(Decimal('0.00'))])
    liner_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                   verbose_name='Liner To', validators=[MinValueValidator(Decimal('0.01'))])

    screen_intake_method = models.ForeignKey(ScreenIntakeMethodCode, db_column='screen_intake_method_code',
                                             on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name='Intake')
    screen_type = models.ForeignKey(ScreenTypeCode, db_column='screen_type_code',
                                    on_delete=models.CASCADE, blank=True, null=True, verbose_name='Type')
    screen_material = models.ForeignKey(ScreenMaterialCode, db_column='screen_material_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Material')
    other_screen_material = models.CharField(
        max_length=50, blank=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpeningCode, db_column='screen_opening_code',
                                       on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Opening')
    screen_bottom = models.ForeignKey(ScreenBottomCode, db_column='screen_bottom_code',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Bottom')
    other_screen_bottom = models.CharField(
        max_length=50, blank=True, verbose_name='Specify Other Screen Bottom')

    filter_pack_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                           verbose_name='Filter Pack From',
                                           validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                         verbose_name='Filter Pack To',
                                         validators=[MinValueValidator(Decimal('0.01'))])
    filter_pack_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                                verbose_name='Filter Pack Thickness',
                                                validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_material = models.ForeignKey(FilterPackMaterialCode, db_column='filter_pack_material_code',
                                             on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name='Filter Pack Material')
    filter_pack_material_size = models.ForeignKey(FilterPackMaterialSizeCode,
                                                  db_column='filter_pack_material_size_code',
                                                  on_delete=models.CASCADE, blank=True, null=True,
                                                  verbose_name='Filter Pack Material Size')

    development_method = models.ForeignKey(DevelopmentMethodCode, db_column='development_method_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='Development Method')
    development_hours = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,
                                            verbose_name='Development Total Duration',
                                            validators=[MinValueValidator(Decimal('0.00'))])
    development_notes = models.CharField(
        max_length=255, blank=True, verbose_name='Development Notes')

    water_quality_characteristics = models.ManyToManyField(
        WaterQualityCharacteristic, db_table='activity_submission_water_quality', blank=True,
        verbose_name='Obvious Water Quality Characteristics')
    water_quality_colour = models.CharField(
        max_length=60, blank=True, verbose_name='Water Quality Colour')
    water_quality_odour = models.CharField(
        max_length=60, blank=True, verbose_name='Water Quality Odour')

    total_depth_drilled = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Total Depth Drilled')
    finished_well_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Finished Well Depth')
    final_casing_stick_up = models.DecimalField(
        max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Final Casing Stick Up')
    bedrock_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Depth to Bedrock')
    static_water_level = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Static Water Level (BTOC)')
    well_yield = models.DecimalField(
        max_digits=8, decimal_places=3, blank=True, null=True, verbose_name='Estimated Well Yield')
    artesian_flow = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Flow')
    artesian_pressure = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure')
    well_cap_type = models.CharField(
        max_length=40, blank=True, verbose_name='Well Cap Type')
    well_disinfected = models.BooleanField(
        default=False, verbose_name='Well Disinfected?', choices=((False, 'No'), (True, 'Yes')))

    comments = models.CharField(max_length=3000, blank=True)
    alternative_specs_submitted = models.BooleanField(
        default=False, verbose_name='Alternative specs submitted (if required)')

    well_yield_unit = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True)
    # want to be integer in future
    diameter = models.CharField(max_length=9, blank=True)

    tracker = FieldTracker()

    def create_well(self):
        w = Well(well_class=self.well_class)
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
        # TODO

        return w

    class Meta:
        db_table = 'activity_submission'

    def __str__(self):
        if self.filing_number:
            return '%s %d %s %s' % (self.activity_submission_guid, self.filing_number,
                                    self.well_activity_type.well_activity_code, self.street_address)
        else:
            return '%s %s' % (self.activity_submission_guid, self.street_address)


class ProductionData(AuditModel):
    """
    Water production of a well measured by a driller
    """
    production_data_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(
        ActivitySubmission, db_column='filing_number',
        on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE,
        blank=True, null=True)
    yield_estimation_method = models.ForeignKey(
        YieldEstimationMethodCode, db_column='yield_estimation_method_code',
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Estimation Method')
    yield_estimation_rate = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='Estimation Rate',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    yield_estimation_duration = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Estimation Duration',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    well_yield_unit = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', blank=True,
        null=True)
    static_level = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='SWL Before Test',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.0'))])
    drawdown = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True,
        validators=[MinValueValidator(Decimal('0.00'))])
    hydro_fracturing_performed = models.BooleanField(
        default=False, verbose_name='Hydro-fracturing Performed?',
        choices=((False, 'No'), (True, 'Yes')))
    hydro_fracturing_yield_increase = models.DecimalField(
        max_digits=7, decimal_places=2,
        verbose_name='Well Yield Increase Due to Hydro-fracturing',
        blank=True, null=True,
        validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'production_data'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(
                self.activity_submission, self.yield_estimation_method,
                self.yield_estimation_rate)
        else:
            return 'well {} {} {}'.format(
                self.well, self.yield_estimation_method,
                self.yield_estimation_rate)


class Perforation(AuditModel):
    """
    Liner Details
    """
    perforation_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    well_tag_number = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    liner_thickness = models.DecimalField(
        max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Liner Thickness')
    liner_diameter = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner Diameter')
    liner_from = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner From')
    liner_to = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner To')
    liner_perforation_from = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Perforation From')
    liner_perforation_to = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Perforation To')

    class Meta:
        db_table = 'perforation'
        ordering = ['liner_from', 'liner_to', 'liner_perforation_from',
                    'liner_perforation_to', 'perforation_guid']

    def __str__(self):
        return self.description


class LtsaOwner(AuditModel):
    """
    Well owner information.
    """
    lsts_owner_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(Well, db_column='well_tag_number',
                             on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    mailing_address = models.CharField(
        max_length=100, verbose_name='Mailing Address')

    city = models.CharField(max_length=100, verbose_name='Town/City')
    province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, verbose_name='Province')
    postal_code = models.CharField(
        max_length=10, blank=True, verbose_name='Postal Code')

    tracker = FieldTracker()

    class Meta:
        db_table = 'ltsa_owner'

    def __str__(self):
        return '%s %s' % (self.full_name, self.mailing_address)


class LinerPerforation(AuditModel):
    """
    Perforation in a well liner
    """
    liner_perforation_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(
        ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(Well, db_column='well_tag_number',
                             on_delete=models.CASCADE, blank=True, null=True)
    liner_perforation_from = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='Perforated From', blank=False,
        validators=[MinValueValidator(Decimal('0.00'))])
    liner_perforation_to = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='Perforated To', blank=False,
        validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        db_table = 'liner_perforation'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission,
                                                         self.liner_perforation_from,
                                                         self.liner_perforation_to)
        else:
            return 'well {} {} {}'.format(self.well, self.liner_perforation_from, self.liner_perforation_to)


class CasingMaterialCode(AuditModel):
    """
     The material used for casing a well, e.g., Cement, Plastic, Steel.
    """
    casing_material_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'casing_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class CasingCode(AuditModel):
    """
    Type of Casing used on a well
    """
    casing_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'casing_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class Casing(AuditModel):
    """
    Casing information
    """
    casing_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.CASCADE, blank=True, null=True)
    well_tag_number = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE,
                                        blank=True, null=True)
    casing_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='From', null=True,
                                      blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    casing_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='To', null=True, blank=True,
                                    validators=[MinValueValidator(Decimal('0.01'))])
    diameter = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='Diameter', null=True,
                                   blank=True, validators=[MinValueValidator(Decimal('0.5'))])
    casing_code = models.ForeignKey(CasingCode, db_column='casing_code', on_delete=models.CASCADE,
                                    verbose_name='Casing Code', null=True)
    casing_material = models.ForeignKey(CasingMaterialCode, db_column='casing_material_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Casing Material Code')
    wall_thickness = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Wall Thickness',
                                         blank=True, null=True,
                                         validators=[MinValueValidator(Decimal('0.01'))])
    drive_shoe = models.NullBooleanField(default=False, null=True, verbose_name='Drive Shoe',
                                         choices=((False, 'No'), (True, 'Yes')))

    class Meta:
        ordering = ["casing_from", "casing_to"]
        db_table = 'casing'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.casing_from,
                                                         self.casing_to)
        else:
            return 'well {} {} {}'.format(self.well, self.casing_from, self.casing_to)

    def as_dict(self):
        return {
            "casing_from": self.casing_from,
            "casing_to": self.casing_to,
            "casing_guid": self.casing_guid,
            "well_tag_number": self.well_tag_number,
            "diameter": self.diameter,
            "wall_thickness": self.wall_thickness,
            "casing_material": self.casing_material,
            "drive_shoe": self.drive_shoe
        }


class AquiferWell(AuditModel):
    """
    AquiferWell
    """

    aquifer_well_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aquifer_id = models.PositiveIntegerField(verbose_name="Aquifer Number", blank=True, null=True)
    well_tag_number = models.ForeignKey(Well, db_column='well_tag_number', to_field='well_tag_number',
                                        on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'aquifer_well'


class Screen(AuditModel):
    """
    Screen in a well
    """
    screen_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(
        ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(Well, db_column='well_tag_number',
                             on_delete=models.CASCADE, blank=True, null=True)
    screen_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='From',
                                      blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    screen_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='To',
                                    blank=False, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    internal_diameter = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Diameter',
                                            blank=True, null=True,
                                            validators=[MinValueValidator(Decimal('0.0'))])
    assembly_type = models.ForeignKey(
        ScreenAssemblyTypeCode, db_column='screen_assembly_type_code', on_delete=models.CASCADE, blank=True,
        null=True)
    slot_size = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Slot Size',
                                    blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'screen'
        ordering = ['screen_from', 'screen_to']

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.screen_from,
                                                         self.screen_to)
        else:
            return 'well {} {} {}'.format(self.well, self.screen_from, self.screen_to)
