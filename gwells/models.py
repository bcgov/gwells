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
import datetime
import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from model_utils import FieldTracker




class AuditModel(models.Model):
    """
    An abstract base class model that provides audit fields.
    """
    who_created = models.CharField(max_length=30)
    when_created = models.DateTimeField(blank=True, null=True)
    who_updated = models.CharField(max_length=30)
    when_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self._state.adding == True:
            self.when_created = timezone.now()
        self.when_updated = timezone.now()
        return super(AuditModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        
        
class ProvinceState(AuditModel):
    """
    Lookup of Provinces/States.
    Used to specify valid provinces or states for the address of the owner of a well.
    It provides for a standard commonly understood code and description for provinces and states.
    Some examples include: BC, AB, W
    """
    province_state_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_province_state'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class LandDistrict(AuditModel):
    """
    Lookup of Land Districts.
    """
    land_district_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_land_district'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name



class WellYieldUnit(AuditModel):
    """
    Units of Well Yield.
    """
    well_yield_unit_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_yield_unit'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class WellActivityType(AuditModel):
    """
    Types of Well Activity.
    """
    well_activity_type_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_activity_type'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class WellClass(AuditModel):
    """
    Class of Well type.
    """
    well_class_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_class'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class WellSubclass(AuditModel):
    """
    Subclass of Well type.
    """
    well_subclass_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well_class = models.ForeignKey(WellClass, db_column='well_class_guid', on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_well_subclass'
        ordering = ['sort_order', 'description']

    def validate_unique(self, exclude=None):
        qs = Room.objects.filter(name=self.code)
        if qs.filter(well_class__code=self.well_class__code).exists():
            raise ValidationError('Code must be unique per Well Class')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(WellSubclass, self).save(*args, **kwargs)

    def __str__(self):
        return self.description



class IntendedWaterUse(AuditModel):
    """
    Usage of Wells (water supply).
    """
    intended_water_use_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_intended_water_use'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class DrillingCompany(AuditModel):
    """
    Companies who perform drilling.
    """
    drilling_company_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    is_hidden = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'gwells_drilling_company'
        verbose_name_plural = 'Drilling Companies'

    def __str__(self):
        return self.name



class Driller(AuditModel):
    """
    People responsible for drilling.
    """
    driller_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drilling_company = models.ForeignKey(DrillingCompany, db_column='drilling_company_guid', on_delete=models.CASCADE, verbose_name='Drilling Company')
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'gwells_driller'

    def __str__(self):
        return '%s %s - %s' % (self.first_name, self.surname, self.registration_number)



class GroundElevationMethod(AuditModel):
    """
    The method used to determine the ground elevation of a well.
    Some examples of methods to determine ground elevation include:
    GPS, Altimeter, Differential GPS, Level, 1:50,000 map, 1:20,000 map, 1:10,000 map, 1:5,000 map.
    """
    ground_elevation_method_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_ground_elevation_method'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class DrillingMethod(AuditModel):
    """
    The method used to drill a well. For example, air rotary, dual rotary, cable tool, excavating, other.
    """
    drilling_method_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_drilling_method'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class SurficialMaterial(AuditModel):
    """
    The surficial material encountered in lithology
    """
    surficial_material_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_surficial_material'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class BedrockMaterial(AuditModel):
    """
    The bedrock material encountered in lithology
    """
    bedrock_material_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_bedrock_material'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class BedrockMaterialDescriptor(AuditModel):
    """
    Further descriptor of the bedrock material encountered in lithology
    """
    bedrock_material_descriptor_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_bedrock_material_descriptor'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class LithologyStructure(AuditModel):
    """
    Structure of the lithology
    """
    lithology_structure_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_lithology_structure'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class LithologyColour(AuditModel):
    """
    Colour of the lithology
    """
    lithology_colour_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_lithology_colour'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class LithologyHardness(AuditModel):
    """
    Hardness of the lithology
    """
    lithology_hardness_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_lithology_hardness'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class LithologyMoisture(AuditModel):
    """
    Moisture of the lithology
    """
    lithology_moisture_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_lithology_moisture'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class CasingType(AuditModel):
    """
    Type of Casing used on a well
    """
    casing_type_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_casing_type'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class CasingMaterial(AuditModel):
    """
     The material used for casing a well, e.g., Cement, Plastic, Steel.
    """
    casing_material_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_casing_material'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class SurfaceSealMaterial(AuditModel):
    """
     Sealant material used that is installed in the annular space around the outside of the outermost casing and between multiple casings of a well.
    """
    surface_seal_material_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_surface_seal_material'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class SurfaceSealMethod(AuditModel):
    """
     Method used to install the surface seal in the annular space around the outside of the outermost casing and between mulitple casings of a well.
    """
    surface_seal_method_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_surface_seal_method'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class LinerMaterial(AuditModel):
    """
     Liner material installed in a well to protect the well pump or other works in the well from damage.
    """
    liner_material_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_liner_material'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class ScreenIntake(AuditModel):
    """
     Refers to the type of intake mechanism for a well screen, i.e. Screen, Open Bottom, Uncased Hole.
    """
    screen_intake_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_screen_intake'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class ScreenType(AuditModel):
    """
     The possible types of well screens, i.e. Telescope, Pipe Size.
    """
    screen_type_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_screen_type'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class ScreenMaterial(AuditModel):
    """
     The material used to construct a well screen, i.e. Plastic, Stainless Steel, Other.
    """
    screen_material_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_screen_material'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class ScreenOpening(AuditModel):
    """
     The type of opening on a well screen, i.e. Continuous Slot, Slotted, Perforated Pipe.
    """
    screen_opening_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_screen_opening'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class ScreenBottom(AuditModel):
    """
     The type of bottom on a well screen, i.e. Bail, Plate, Plug, Other.
    """
    screen_bottom_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_screen_bottom'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class ScreenAssemblyType(AuditModel):
    """
     The category of screen assembly, i.e. K-Packer & Riser, K-Packer, Lead Packer, Riser Pipe, Screen, Screen Blank, Tail Pipe.
    """
    screen_assembly_type_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_screen_assembly_type'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class FilterPackMaterial(AuditModel):
    """
     The material used to pack a well filter, e.g. Very coarse sand, Very fine gravel, Fine gravel.
    """
    filter_pack_material_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_filter_pack_material'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class FilterPackMaterialSize(AuditModel):
    """
     The size of material used to pack a well filter, e.g. 1.0 - 2.0 mm, 2.0 - 4.0 mm, 4.0 - 8.0 mm.
    """
    filter_pack_material_size_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_filter_pack_material_size'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class DevelopmentMethod(AuditModel):
    """
     How the well was developed in order to remove the fine sediment and other organic or inorganic material that immediately surrounds the well screen, the drill hole or the intake area at the bottom of the well, e.g. air lifting, pumping, bailing.
    """
    development_method_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_development_method'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class YieldEstimationMethod(AuditModel):
    """
     The method used to estimate the yield of a well, e.g. Air Lifting, Bailing, Pumping.
    """
    yield_estimation_method_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_yield_estimation_method'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class WaterQualityCharacteristic(AuditModel):
    """
     The characteristic of the well water, e.g. Fresh, Salty, Clear.
    """
    water_quality_characteristic_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'gwells_water_quality_characteristic'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description



class Well(AuditModel):
    """
    Well information.
    """
    well_tag_number = models.AutoField(primary_key=True)
    well_guid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    well_class = models.ForeignKey(WellClass, db_column='well_class_guid', on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclass, db_column='well_subclass_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUse, db_column='intended_water_use_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Water Supply Well Intended Water Use')

    owner_full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    owner_mailing_address = models.CharField(max_length=100, verbose_name='Mailing Address')  
    owner_city = models.CharField(max_length=100, verbose_name='Town/City')
    owner_province_state = models.ForeignKey(ProvinceState, db_column='province_state_guid', on_delete=models.CASCADE, blank=True, verbose_name='Province')
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
    legal_land_district = models.ForeignKey(LandDistrict, db_column='legal_land_district_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(blank=True, null=True, verbose_name='PID')
    well_location_description = models.CharField(max_length=500, blank=True, verbose_name='Well Location Description')

    identification_plate_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    where_plate_attached = models.CharField(max_length=500, blank=True, verbose_name='Where Identification Plate Is Attached')

    latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    ground_elevation = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethod, db_column='ground_elevation_method_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Method for Determining Ground Elevation')
    drilling_method = models.ForeignKey(DrillingMethod, db_column='drilling_method_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Drilling Method')
    other_drilling_method = models.CharField(max_length=50, blank=True, verbose_name='Specify Other Drilling Method')
    orientation_vertical = models.BooleanField(default=True, verbose_name='Well Orientation', choices=((True, 'vertical'), (False, 'horizontal')))

    surface_seal_material = models.ForeignKey(SurfaceSealMaterial, db_column='surface_seal_material_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Surface Seal Material')
    surface_seal_depth = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Depth')
    surface_seal_thickness = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Thickness')
    surface_seal_method = models.ForeignKey(SurfaceSealMethod, db_column='surface_seal_method_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Surface Seal Installation Method')
    backfill_above_surface_seal = models.CharField(max_length=250, blank=True, verbose_name='Backfill Material Above Surface Seal')
    backfill_above_surface_seal_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')

    liner_material = models.ForeignKey(LinerMaterial, db_column='liner_material_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Liner Material')
    liner_diameter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner Diameter', validators=[MinValueValidator(Decimal('0.00'))])
    liner_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Liner Thickness', validators=[MinValueValidator(Decimal('0.00'))])
    liner_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner From', validators=[MinValueValidator(Decimal('0.00'))])
    liner_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner To', validators=[MinValueValidator(Decimal('0.01'))])

    screen_intake = models.ForeignKey(ScreenIntake, db_column='screen_intake_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Intake')
    screen_type = models.ForeignKey(ScreenType, db_column='screen_type_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Screen Type')
    screen_material = models.ForeignKey(ScreenMaterial, db_column='screen_material_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Screen Material')
    other_screen_material = models.CharField(max_length=50, blank=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpening, db_column='screen_opening_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Screen Opening')
    screen_bottom = models.ForeignKey(ScreenBottom, db_column='screen_bottom_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Screen Bottom')
    other_screen_bottom = models.CharField(max_length=50, blank=True, verbose_name='Specify Other Screen Bottom')

    filter_pack_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Filter Pack From', validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Filter Pack To', validators=[MinValueValidator(Decimal('0.01'))])
    filter_pack_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Filter Pack Thickness', validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_material = models.ForeignKey(FilterPackMaterial, db_column='filter_pack_material_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Filter Pack Material')
    filter_pack_material_size = models.ForeignKey(FilterPackMaterialSize, db_column='filter_pack_material_size_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Filter Pack Material Size')

    development_method = models.ForeignKey(DevelopmentMethod, db_column='development_method_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Development Method')
    development_hours = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name='Development Total Duration', validators=[MinValueValidator(Decimal('0.00'))])
    development_notes = models.CharField(max_length=255, blank=True, verbose_name='Development Notes')

    water_quality_characteristics = models.ManyToManyField(WaterQualityCharacteristic, db_table='gwells_well_water_quality', blank=True, verbose_name='Obvious Water Quality Characteristics')
    water_quality_colour = models.CharField(max_length=60, blank=True, verbose_name='Water Quality Colour')
    water_quality_odour = models.CharField(max_length=60, blank=True, verbose_name='Water Quality Odour')

    total_depth_drilled = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Total Depth Drilled')
    finished_well_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Finished Well Depth')
    final_casing_stick_up = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Final Stick Up')
    bedrock_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Depth to Bedrock')
    static_water_level = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Static Water Level')
    well_yield = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, verbose_name='Estimated Well Yield')
    artestian_flow = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Flow')
    artestian_pressure = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure')
    well_cap_type = models.CharField(max_length=40, blank=True, verbose_name='Well Cap Type')
    well_disinfected = models.BooleanField(default=False, verbose_name='Well Disinfected?', choices=((False, 'No'), (True, 'Yes')))

    comments = models.CharField(max_length=3000, blank=True)
    alternative_specs_submitted = models.BooleanField(default=False, verbose_name='Alternative specs submitted (if required)')


    well_yield_unit = models.ForeignKey(WellYieldUnit, db_column='well_yield_unit_guid', on_delete=models.CASCADE, blank=True, null=True)
    diameter = models.CharField(max_length=9, blank=True)  #want to be integer in future
    
    tracker = FieldTracker()
    
    class Meta:
        db_table = 'gwells_well'

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
    activity_submission_guid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    well_activity_type = models.ForeignKey(WellActivityType, db_column='well_activity_type_guid', on_delete=models.CASCADE, verbose_name='Type of Work')
    well_class = models.ForeignKey(WellClass, db_column='well_class_guid', on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclass, db_column='well_subclass_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUse, db_column='intended_water_use_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Water Supply Well Intended Water Use')
    driller_responsible = models.ForeignKey(Driller, db_column='driller_responsible_guid', on_delete=models.CASCADE, verbose_name='Person Responsible for Drilling')
    driller_name = models.CharField(max_length=200, blank=True, verbose_name='Name of Person Who Did the Work')
    consultant_name = models.CharField(max_length=200, blank=True, verbose_name='Consultant Name')
    consultant_company = models.CharField(max_length=200, blank=True, verbose_name='Consultant Company')
    work_start_date = models.DateField(verbose_name='Work Start Date')
    work_end_date = models.DateField(verbose_name='Work End Date')

    owner_full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    owner_mailing_address = models.CharField(max_length=100, verbose_name='Mailing Address')  
    owner_city = models.CharField(max_length=100, verbose_name='Town/City')
    owner_province_state = models.ForeignKey(ProvinceState, db_column='province_state_guid', on_delete=models.CASCADE, verbose_name='Province')
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
    legal_land_district = models.ForeignKey(LandDistrict, db_column='legal_land_district_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(blank=True, null=True, verbose_name='PID')
    well_location_description = models.CharField(max_length=500, blank=True, verbose_name='Well Location Description')

    identification_plate_number = models.PositiveIntegerField(blank=True, null=True, verbose_name='Identification Plate Number')
    where_plate_attached = models.CharField(max_length=500, blank=True, verbose_name='Where Identification Plate Is Attached')

    latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    ground_elevation = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethod, db_column='ground_elevation_method_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Method for Determining Ground Elevation')
    drilling_method = models.ForeignKey(DrillingMethod, db_column='drilling_method_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Drilling Method')
    other_drilling_method = models.CharField(max_length=50, blank=True, verbose_name='Specify Other Drilling Method')
    orientation_vertical = models.BooleanField(default=True, verbose_name='Well Orientation', choices=((True, 'vertical'), (False, 'horizontal')))

    surface_seal_material = models.ForeignKey(SurfaceSealMaterial, db_column='surface_seal_material_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Surface Seal Material')
    surface_seal_depth = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Depth')
    surface_seal_thickness = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Thickness', validators=[MinValueValidator(Decimal('1.00'))])
    surface_seal_method = models.ForeignKey(SurfaceSealMethod, db_column='surface_seal_method_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Surface Seal Installation Method')
    backfill_above_surface_seal = models.CharField(max_length=250, blank=True, verbose_name='Backfill Material Above Surface Seal')
    backfill_above_surface_seal_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')

    liner_material = models.ForeignKey(LinerMaterial, db_column='liner_material_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Liner Material')
    liner_diameter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner Diameter', validators=[MinValueValidator(Decimal('0.00'))])
    liner_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Liner Thickness', validators=[MinValueValidator(Decimal('0.00'))])
    liner_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner From', validators=[MinValueValidator(Decimal('0.00'))])
    liner_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner To', validators=[MinValueValidator(Decimal('0.01'))])

    screen_intake = models.ForeignKey(ScreenIntake, db_column='screen_intake_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Intake')
    screen_type = models.ForeignKey(ScreenType, db_column='screen_type_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Screen Type')
    screen_material = models.ForeignKey(ScreenMaterial, db_column='screen_material_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Screen Material')
    other_screen_material = models.CharField(max_length=50, blank=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpening, db_column='screen_opening_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Screen Opening')
    screen_bottom = models.ForeignKey(ScreenBottom, db_column='screen_bottom_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Screen Bottom')
    other_screen_bottom = models.CharField(max_length=50, blank=True, verbose_name='Specify Other Screen Bottom')

    filter_pack_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Filter Pack From', validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Filter Pack To', validators=[MinValueValidator(Decimal('0.01'))])
    filter_pack_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Filter Pack Thickness', validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_material = models.ForeignKey(FilterPackMaterial, db_column='filter_pack_material_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Filter Pack Material')
    filter_pack_material_size = models.ForeignKey(FilterPackMaterialSize, db_column='filter_pack_material_size_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Filter Pack Material Size')

    development_method = models.ForeignKey(DevelopmentMethod, db_column='development_method_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Development Method')
    development_hours = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name='Development Total Duration', validators=[MinValueValidator(Decimal('0.00'))])
    development_notes = models.CharField(max_length=255, blank=True, verbose_name='Development Notes')

    water_quality_characteristics = models.ManyToManyField(WaterQualityCharacteristic, db_table='gwells_activity_submission_water_quality', blank=True, verbose_name='Obvious Water Quality Characteristics')
    water_quality_colour = models.CharField(max_length=60, blank=True, verbose_name='Water Quality Colour')
    water_quality_odour = models.CharField(max_length=60, blank=True, verbose_name='Water Quality Odour')

    total_depth_drilled = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Total Depth Drilled')
    finished_well_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Finished Well Depth')
    final_casing_stick_up = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Final Stick Up')
    bedrock_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Depth to Bedrock')
    static_water_level = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Static Water Level')
    well_yield = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, verbose_name='Estimated Well Yield')
    artestian_flow = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Flow')
    artestian_pressure = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure')
    well_cap_type = models.CharField(max_length=40, blank=True, verbose_name='Well Cap Type')
    well_disinfected = models.BooleanField(default=False, verbose_name='Well Disinfected?', choices=((False, 'No'), (True, 'Yes')))

    comments = models.CharField(max_length=3000, blank=True)
    alternative_specs_submitted = models.BooleanField(default=False, verbose_name='Alternative specs submitted (if required)')


    well_yield_unit = models.ForeignKey(WellYieldUnit, db_column='well_yield_unit_guid', on_delete=models.CASCADE, blank=True, null=True)
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
        w.legal_land_district = self.legal_land_district
        w.legal_pid = self.legal_pid
        w.well_location_description = self.well_location_description

        w.identification_plate_number = self.identification_plate_number
        w.latitude = self.latitude
        w.longitude = self.longitude
        w.ground_elevation = self.ground_elevation
        w.ground_elevation_method = self.ground_elevation_method
        w.drilling_method = self.drilling_method
        w.other_drilling_method = self.other_drilling_method
        w.orientation_vertical = self.orientation_vertical

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
        w.static_water_level = self.static_water_level
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
        db_table = 'gwells_activity_submission'

    def __str__(self):
        if self.filing_number:
            return '%s %d %s %s' % (self.activity_submission_guid, self.filing_number, self.well_activity_type.code, self.street_address)
        else:
            return '%s %s' % (self.activity_submission_guid, self.street_address)



class LtsaOwner(AuditModel):
    """
    Well owner information.
    """
    lsts_owner_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    mailing_address = models.CharField(max_length=100, verbose_name='Mailing Address')
    
    city = models.CharField(max_length=100, verbose_name='Town/City')
    province_state = models.ForeignKey(ProvinceState, db_column='province_state_guid', on_delete=models.CASCADE, verbose_name='Province')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')

    tracker = FieldTracker()

    class Meta:
        db_table = 'gwells_ltsa_owner'

    def __str__(self):
        return '%s %s' % (self.full_name, self.mailing_address)



class LithologyDescription(AuditModel):
    """
    Lithology information details
    """
    lithology_description_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    lithology_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='From', blank=False, validators=[MinValueValidator(Decimal('0.00'))])
    lithology_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='To', blank=False, validators=[MinValueValidator(Decimal('0.01'))])
    surficial_material = models.ForeignKey(SurficialMaterial, db_column='surficial_material_guid', related_name='surficial_material_set', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Surficial Material')
    secondary_surficial_material = models.ForeignKey(SurficialMaterial, db_column='secondary_surficial_material_guid', related_name='secondary_surficial_material_set', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Secondary Surficial Material')
    bedrock_material = models.ForeignKey(BedrockMaterial, db_column='bedrock_material_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Bedrock Material')
    bedrock_material_descriptor = models.ForeignKey(BedrockMaterialDescriptor, db_column='bedrock_material_descriptor_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Descriptor')
    lithology_structure = models.ForeignKey(LithologyStructure, db_column='lithology_structure_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Bedding')
    lithology_colour = models.ForeignKey(LithologyColour, db_column='lithology_colour_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Colour')
    lithology_hardness = models.ForeignKey(LithologyHardness, db_column='lithology_hardness_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Hardness')
    lithology_moisture = models.ForeignKey(LithologyMoisture, db_column='lithology_moisture_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Moisture')
    water_bearing_estimated_flow = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, verbose_name='Water Bearing Estimated Flow')
    lithology_observation = models.CharField(max_length=250, blank=True, verbose_name='Observations')
    
    class Meta:
        db_table = 'gwells_lithology_description'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.lithology_from, self.lithology_to)
        else:
            return 'well {} {} {}'.format(self.well, self.lithology_from, self.lithology_to)



class Casing(AuditModel):
    """
    Casing information
    """
    casing_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    casing_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='From', blank=False, validators=[MinValueValidator(Decimal('0.00'))])
    casing_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='To', blank=False, validators=[MinValueValidator(Decimal('0.01'))])
    internal_diameter = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='Diameter', blank=False, validators=[MinValueValidator(Decimal('0.5'))])
    casing_type = models.ForeignKey(CasingType, db_column='casing_type_guid', on_delete=models.CASCADE, verbose_name='Casing Type')
    casing_material = models.ForeignKey(CasingMaterial, db_column='casing_material_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Casing Material')
    wall_thickness = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Wall Thickness', blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    drive_shoe = models.BooleanField(default=False, verbose_name='Drive Shoe', choices=((False, 'No'), (True, 'Yes')))
    
    class Meta:
        db_table = 'gwells_casing'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.casing_from, self.casing_to)
        else:
            return 'well {} {} {}'.format(self.well, self.casing_from, self.casing_to)



class LinerPerforation(AuditModel):
    """
    Perforation in a well liner
    """
    liner_perforation_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    liner_perforation_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Perforated From', blank=False, validators=[MinValueValidator(Decimal('0.00'))])
    liner_perforation_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Perforated To', blank=False, validators=[MinValueValidator(Decimal('0.01'))])
    
    class Meta:
        db_table = 'gwells_liner_perforation'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.liner_perforation_from, self.liner_perforation_to)
        else:
            return 'well {} {} {}'.format(self.well, self.liner_perforation_from, self.liner_perforation_to)



class Screen(AuditModel):
    """
    Screen in a well
    """
    screen_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    screen_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='From', blank=False, validators=[MinValueValidator(Decimal('0.00'))])
    screen_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='To', blank=False, validators=[MinValueValidator(Decimal('0.01'))])
    internal_diameter = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Diameter', blank=True, null=True, validators=[MinValueValidator(Decimal('0.0'))])
    assembly_type = models.ForeignKey(ScreenAssemblyType, db_column='screen_assembly_type_guid', on_delete=models.CASCADE, blank=True, null=True)
    slot_size = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Slot Size', blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    
    class Meta:
        db_table = 'gwells_screen'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.screen_from, self.screen_to)
        else:
            return 'well {} {} {}'.format(self.well, self.screen_from, self.screen_to)



class ProductionData(AuditModel):
    """
    Water production of a well measured by a driller
    """
    production_data_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    yield_estimation_method = models.ForeignKey(YieldEstimationMethod, db_column='yield_estimation_method_guid', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Yield Estimation Method')
    yield_estimation_rate = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Yield Estimation Rate', blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    yield_estimation_duration = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Yield Estimation Duration', blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    static_level = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='SWL Before Test', blank=True, null=True, validators=[MinValueValidator(Decimal('0.0'))])
    drawdown = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    hydro_fracturing_performed = models.BooleanField(default=False, verbose_name='Hydro-fracturing Performed?', choices=((False, 'No'), (True, 'Yes')))
    hydro_fracturing_yield_increase = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Well Yield Increase Due to Hydro-fracturing', blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    
    class Meta:
        db_table = 'gwells_production_data'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.yield_estimation_method, self.yield_estimation_rate)
        else:
            return 'well {} {} {}'.format(self.well, self.yield_estimation_method, self.yield_estimation_rate)



