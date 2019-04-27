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

from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericRelation

from decimal import Decimal
import reversion
from reversion.signals import pre_revision_commit
from reversion.models import Version

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone
import uuid

from gwells.models import AuditModel, ProvinceStateCode, ScreenIntakeMethodCode, ScreenMaterialCode,\
    ScreenOpeningCode, ScreenBottomCode, ScreenTypeCode, ScreenAssemblyTypeCode, CodeTableModel,\
    BasicCodeTableModel
from gwells.models.common import AuditModelStructure
from gwells.models.lithology import (
    LithologyDescriptionCode, LithologyColourCode, LithologyHardnessCode,
    LithologyMaterialCode, BedrockMaterialCode, BedrockMaterialDescriptorCode, LithologyStructureCode,
    LithologyMoistureCode, SurficialMaterialCode)
from registries.models import Person, Organization
from submissions.models import WellActivityCode
from aquifers.models import Aquifer
from gwells.db_comments.patch_fields import patch_fields

patch_fields()


WELL_STATUS_CODE_CONSTRUCTION = 'NEW'
WELL_STATUS_CODE_DECOMMISSION = 'CLOSURE'
WELL_STATUS_CODE_ALTERATION = 'ALTERATION'
WELL_STATUS_CODE_OTHER = 'OTHER'


class DecommissionMethodCode(CodeTableModel):
    decommission_method_code = models.CharField(primary_key=True, max_length=10, editable=False,
                                                verbose_name="Code")
    description = models.CharField(max_length=255, verbose_name="Description")

    class Meta:
        db_table = 'decommission_method_code'
        ordering = ['display_order']

    db_table_comment = 'Describes the method used to fill the well to close it permanently.'

    def __str__(self):
        return self.description


class BCGS_Numbers(AuditModel):
    bcgs_id = models.BigIntegerField(primary_key=True, editable=False)
    bcgs_number = models.CharField(max_length=20, verbose_name="BCGS Mapsheet Number")

    class Meta:
        db_table = 'bcgs_number'

    db_table_comment = 'Placeholder table comment.'

    def __str__(self):
        return self.bcgs_number


class ObsWellStatusCode(CodeTableModel):
    """
    Observation Well Status.
    """
    obs_well_status_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'obs_well_status_code'
        ordering = ['display_order', 'obs_well_status_code']

    db_table_comment = ('Status of an observation well within the Provincial Groundwater Observation Well '
                        'Network. I.e. Active is a well that is currently being used to collect groundwater '
                        'information, and inactive is a well that is no longer being used to collect '
                        'groundwater information.')

    def save(self, *args, **kwargs):
        self.validate()
        super(WellStatusCode, self).save(*args, **kwargs)


class YieldEstimationMethodCode(CodeTableModel):
    """
     The method used to estimate the yield of a well, e.g. Air Lifting, Bailing, Pumping.
    """
    yield_estimation_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'yield_estimation_method_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Describes the valid methods that can be used to estimate the yield of a well. E.g.'
                        ' Air Lifting, Bailing, Pumping, Other.')

    def __str__(self):
        return self.description


class WaterQualityCharacteristic(AuditModel):
    """
     The characteristic of the well water, e.g. Fresh, Salty, Clear.
    """

    code = models.CharField(primary_key=True, max_length=10, db_column='water_quality_characteristic_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(
        db_comment='The order in which the codes may display on screen.'
    )

    class Meta:
        db_table = 'water_quality_characteristic'
        ordering = ['display_order', 'description']

    db_table_comment = ('Valid values that can be used to indicate the quality of the water for a well as'
                        ' recorded at time of work. E.g. Clear, Cloudy, Fresh, Gas, Salty, Sediment.')

    def __str__(self):
        return self.description


class DevelopmentMethodCode(CodeTableModel):
    """
     How the well was developed in order to remove the fine sediment and other organic or inorganic material
     that immediately surrounds the well screen, the drill hole or the intake area at the bottom of the well,
     e.g. air lifting, pumping, bailing.
    """
    development_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'development_method_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('The methods used to remove the fine sediment and other organic or inorganic '
                        'material that immediately surrounds the well screen, the drill hole or the intake '
                        'area at the bottom of the well. E.g. Air Lifting, Bailing, Jetting, Pumping, '
                        'Surging. \'Other\' can also be specified.')

    def __str__(self):
        return self.description


class FilterPackMaterialSizeCode(CodeTableModel):
    """
     The size of material used to pack a well filter, e.g. 1.0 - 2.0 mm, 2.0 - 4.0 mm, 4.0 - 8.0 mm.
    """
    filter_pack_material_size_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'filter_pack_material_size_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Codes for the sizes of the material used to pack a well filter. Some examples of '
                        'filter pack sizes are: 1.0 - 2.0 mm, 2.0 - 4.0 mm, 4.0 - 8.0 mm.')

    def __str__(self):
        return self.description


class FilterPackMaterialCode(CodeTableModel):
    """
     The material used to pack a well filter, e.g. Very coarse sand, Very fine gravel, Fine gravel.
    """
    filter_pack_material_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'filter_pack_material_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Materials used in the filter pack, which are placed in the annulus of the well '
                        'between the borehole wall and the well screen, and are used to settle-out fine '
                        'grained particles that may otherwise enter the well. I.e. Fine gravel, very course '
                        'sand, very fine gravel, other.')

    def __str__(self):
        return self.description


class LinerMaterialCode(CodeTableModel):
    """
     Liner material installed in a well to protect the well pump or other works in the well from damage.
    """
    code = models.CharField(
        primary_key=True, max_length=10, editable=False, db_column='liner_material_code')
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'liner_material_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Describes the material of the piping or tubing installed in a well which protects '
                        'the well pump or other works in the well from damage. i.e. PVC, Other')

    def __str__(self):
        return self.description


class SurfaceSealMethodCode(CodeTableModel):
    """
     Method used to install the surface seal in the annular space around the outside of the outermost casing
     and between mulitple casings of a well.
    """
    surface_seal_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'surface_seal_method_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Valid methods used to create the surface seal for a well. i.e. Poured, Pumped,'
                        ' Other.')

    def __str__(self):
        return self.description


class SurfaceSealMaterialCode(CodeTableModel):
    """
     Sealant material used that is installed in the annular space around the outside of the outermost casing
     and between multiple casings of a well.
    """
    surface_seal_material_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'surface_seal_material_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Valid materials used for creating the surface seal for a well. A surface seal is a'
                        ' plug that prevents surface runoff from getting into the aquifer or well and'
                        ' contaminating the water. E.g. Bentonite clay, Concrete grout, Sand cement grout,'
                        ' Other.')

    def __str__(self):
        return self.description


class DrillingMethodCode(CodeTableModel):
    """
    The method used to drill a well. For example, air rotary, dual rotary, cable tool, excavating, other.
    """
    drilling_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'drilling_method_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Represents the method that was used to drill or construct a well. E.g. Excavated, '
                        'Dual Rotary, Driving, Other, Unknown.')

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

    db_table_comment = ('Company or organization that was associated with the individual that conducted '
                        'the work on the well.')

    def __str__(self):
        return self.name


class LandDistrictCode(CodeTableModel):
    """
    Lookup of Legal Land Districts.
    """
    land_district_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'land_district_code'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    db_table_comment = ('Legal Land District used to help identify the property where the well is located. '
                        'E.g. Alberni, Barclay, Cariboo.')


class LicencedStatusCode(CodeTableModel):
    """
    LicencedStatusCode of Well.
    """
    licenced_status_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('Valid licencing options granted to a well under the Water Water Sustainability Act. '
                    'This information comes from eLicensing. i.e. Unlicensed, Licensed, Historical.'))
    description = models.CharField(
        max_length=255,
        verbose_name='Licenced Status',
        db_comment=('Descriptions of valid licencing options granted to a well under the Water Water '
                    'Sustainability Act. This information comes from eLicensing. i.e. Unlicensed, '
                    'Licensed, Historical'))

    class Meta:
        db_table = 'licenced_status_code'
        ordering = ['display_order', 'licenced_status_code']

    db_table_comment = ('Valid licencing options granted to a well under the Water Water Sustainability '
                        'Act. This information comes from eLicensing. i.e. Unlicensed, Licensed, Historical')

    def save(self, *args, **kwargs):
        self.validate()
        super(LicencedStatusCode, self).save(*args, **kwargs)


class IntendedWaterUseCode(CodeTableModel):
    """
    Usage of Wells (water supply).
    """
    intended_water_use_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('The intended use of the water in a water supply well as reported by the driller at time '
                    'of work completion on the well. E.g DOM, IRR, DWS, COM'))
    description = models.CharField(
        max_length=100,
        verbose_name='Intented Water Use',
        db_comment=('Descriptions of the intended use codes of the water in a water supply well as reported '
                    'by the driller at time of work completion on the well. E.g Private domestic, '
                    'irrigation, water supply system, Commdercial and Industrial, and unknown.'))

    class Meta:
        db_table = 'intended_water_use_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('The intended use of the water in a water supply well as reported by the driller at '
                        'time of work completion on the well. E.g Private domestic, irrigation, water '
                        'supply system, Industrial commercial, and unknown.')

    def __str__(self):
        return self.description


class GroundElevationMethodCode(CodeTableModel):
    """
    The method used to determine the ground elevation of a well.
    Some examples of methods to determine ground elevation include:
    GPS, Altimeter, Differential GPS, Level, 1:50,000 map, 1:20,000 map, 1:10,000 map, 1:5,000 map.
    """
    ground_elevation_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'ground_elevation_method_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Method used to determine the ground elevation of a well. E.g. GPS, Altimeter, '
                        'Differential GPS, Level, 1:50,000 map, 1:20,000 map.')

    def __str__(self):
        return self.description


class WellClassCode(CodeTableModel):
    """
    Class of Well type.
    """
    well_class_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('Valid classifications as defined in the Groundwater Protection Regulation of the Water '
                    'Act. E.g. Water Supply, Monitoring, Recharge / Injection, Dewatering / Drainage, '
                    'Remediation, Geotechnical.'))
    description = models.CharField(
        max_length=100, verbose_name='Well Class',
        db_comment=('Descriptions of valid classifications as defined in the Groundwater Protection '
                    'Regulation of the Water Act. E.g. Water Supply, Monitoring, Recharge / Injection, '
                    'Dewatering / Drainage, Remediation, Geotechnical.'))

    class Meta:
        db_table = 'well_class_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Valid classifications as defined in the Groundwater Protection Regulation of the'
                        ' Water Act. E.g. Water Supply, Monitoring, Recharge / Injection, Dewatering /'
                        ' Drainage, Remediation, Geotechnical.')

    def __str__(self):
        return self.description


class WellStatusCodeTypeManager(models.Manager):
    """
    Provides additional methods for returning well status codes that correspond
    to activity submissions
    """

    # Construction reports correspond to "NEW" status
    def construction(self):
        return self.get_queryset().get(well_status_code=WELL_STATUS_CODE_CONSTRUCTION)

    # Decommission reports trigger a "CLOSURE" status
    def decommission(self):
        return self.get_queryset().get(well_status_code=WELL_STATUS_CODE_DECOMMISSION)

    # Alteration reports trigger an "ALTERATION" status
    def alteration(self):
        return self.get_queryset().get(well_status_code=WELL_STATUS_CODE_ALTERATION)

    def other(self):
        return self.get_queryset().get(well_status_code=WELL_STATUS_CODE_OTHER)


class WellStatusCode(CodeTableModel):
    """
    Well Status.
    """
    well_status_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('Represents the status of a well as defined in the Groundwater Protection Regulation of '
                    'the Water Act. i.e. New, Abandoned (exists in Wells but will not be used for E-Wells), '
                    'Alteration, Closure, Other.'))
    description = models.CharField(
        max_length=255,
        verbose_name='Well Status',
        db_comment=('Description of the status of a well as defined in the Groundwater Protection '
                    'Regulation of the Water Act. i.e. New, Abandoned (exists in Wells but will not be used '
                    'for E-Wells), Alteration, Closure, Other.'))

    objects = models.Manager()
    types = WellStatusCodeTypeManager()

    class Meta:
        db_table = 'well_status_code'
        ordering = ['display_order', 'well_status_code']

    db_table_comment = ('Represents the status of a well as defined in the Groundwater Protection Regulation'
                        ' of the Water Act. i.e. New, Abandoned (exists in Wells but will not be used for'
                        ' E-Wells), Alteration, Closure, Other.')


class WellPublicationStatusCode(CodeTableModel):
    """
    Well Publication Status.
    """
    well_publication_status_code = models.CharField(
        primary_key=True, max_length=20, editable=False, null=False)
    description = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'well_publication_status_code'
        ordering = ['display_order', 'well_publication_status_code']


class WellSubclassCode(CodeTableModel):
    """
    Subclass of Well type; we use GUID here as Django doesn't support multi-column PK's
    """
    well_subclass_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    well_class = models.ForeignKey(WellClassCode, null=True, db_column='well_class_code',
                                   on_delete=models.PROTECT, blank=True)
    well_subclass_code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'well_subclass_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Valid methods used to further classify a well within the main classification'
                        ' (well_class_code). It provides for a standard commonly understood code and'
                        ' description for well sub-classifcation as defined in the Groundwater Protection'
                        ' Regulation of the Water Act . i.e. Domestic, Borehole, Closed Loop Geothermal,'
                        ' Non-domestic,Permanent, Special, Temporary, Test Pit.')

    def validate_unique(self, exclude=None):
        qs = Room.objects.filter(name=self.well_subclass_code)
        if qs.filter(well_class__well_class_code=self.well_class__well_class_code).exists():
            raise ValidationError('Code must be unique per Well Class')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(WellSubclassCode, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class WellYieldUnitCode(CodeTableModel):
    """
    Units of Well Yield.
    """
    well_yield_unit_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('Describes the unit of measure that was used for the well yield. All codes except the '
                    'U.S. Gallons per Minute has been retired as all data from April 2019 will be reported '
                    'in USGPM. E.g of other codes that have been used in the past are GPM, DRY, UNK.'))
    description = models.CharField(
        max_length=100, verbose_name='Well Yield Unit',
        db_comment=('Describes the unit of measure that was used for the well yield. All codes except the '
                    'U.S. Gallons per Minute has been retired as all data from April 2019 will be reported '
                    'in U.S. Gallons per Minute. E.g of other codes that have been used in the past are '
                    'Gallons per Minute (U.S./Imperial), Dry Hole, Unknown Yield.'))

    class Meta:
        db_table = 'well_yield_unit_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Describes the unit of measure that was used for the well yield. All codes except'
                        ' the U.S. Gallons per Minute has been retired as all data from April 2019 will be'
                        ' reported in U.S. Gallons per Minute. E.g of other codes that have been used in the'
                        ' past are Gallons per Minute (U.S./Imperial), Dry Hole, Unknown Yield.')

    def __str__(self):
        return self.description


class CoordinateAcquisitionCode(AuditModel):
    """
    •	A = (10 m accuracy) ICF cadastre and good location sketch
    •	B = (20 m accuracy) Digitized from 1:5,000 mapping
    •	C = (50 m accuracy) Digitized from 1:20,000 mapping
    •	D = (100 m accuracy) Digitized from old Dept. of Lands, Forests and Water Resources maps
    •	E = (200 m accuracy) Digitized from 1:50,000 maps
    •	F = (1 m accuracy) CDGPS
    •	G = (unknown, accuracy based on parcel size) No ICF cadastre, poor or no location sketch; site
        located in center of primary parcel
    •	H = (10 m accuracy) Handheld GPS with accuracy of +/- 10 metres
    •	I = (20 m accuracy) No ICF cadastre but good location sketch or good written description
    •	J = (unknown, accuracy based on parcel size) ICF cadastre, poor or no location sketch, arbitrarily
        located in center of parcel
    """
    code = models.CharField(primary_key=True, max_length=1, editable=False,
                            db_column='coordinate_acquisition_code')
    description = models.CharField(max_length=250)

    effective_date = models.DateTimeField(default=timezone.now, null=False)
    expiry_date = models.DateTimeField(default=timezone.make_aware(timezone.datetime.max,
                                       timezone.get_default_timezone()), null=False)

    class Meta:
        db_table = 'coordinate_acquisition_code'
        ordering = ['code', ]

    def __str__(self):
        return self.description


class AquiferLithologyCode(CodeTableModel):
    """
    Choices for describing Completed Aquifer Lithology
    """
    aquifer_lithology_code = models.CharField(primary_key=True, max_length=100,
                                              db_column='aquifer_lithology_code')
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'aquifer_lithology_code'
        ordering = ['display_order', 'aquifer_lithology_code']
        verbose_name_plural = 'Aquifer Lithology Codes'

    def __str__(self):
        return '{} - {}'.format(self.aquifer_lithology_code, self.description)


# TODO: Consider having Well and Submission extend off a common base class, given that
#   they mostly have the exact same fields!
@reversion.register()
class Well(AuditModelStructure):
    """
    Well information.
    """
    well_guid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    well_tag_number = models.AutoField(
        primary_key=True, verbose_name='Well Tag Number',
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    identification_plate_number = models.PositiveIntegerField(
        unique=True, blank=True, null=True, verbose_name="Well Identification Plate Number",
        db_comment=('Steel plate with a unique number that is attached to required wells under the '
                    'groundwater protection regulations such as water supply wells, recharge or injection '
                    'wells made by drilling or boring, and permanent dewatering wells.'))
    owner_full_name = models.CharField(
        max_length=200, verbose_name='Owner Name')
    owner_mailing_address = models.CharField(
        max_length=100, verbose_name='Mailing Address')
    owner_city = models.CharField(max_length=100, verbose_name='Town/City')
    owner_province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, blank=True,
        verbose_name='Province', null=True)
    owner_postal_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Postal Code')
    owner_email = models.EmailField(null=True, blank=True, verbose_name='Email address')
    owner_tel = models.CharField(
        null=True, blank=True, max_length=25, verbose_name='Telephone number')

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
    well_publication_status = models.ForeignKey(WellPublicationStatusCode,
                                                db_column='well_publication_status_code',
                                                on_delete=models.CASCADE,
                                                verbose_name='Well Publication Status',
                                                default='Published')
    licenced_status = models.ForeignKey(LicencedStatusCode, db_column='licenced_status_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Licenced Status')

    street_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Street Address',
        db_comment='Street address for where the property that the well is physically located on.')
    city = models.CharField(max_length=50, blank=True, null=True,
                            verbose_name='Town/City')
    legal_lot = models.CharField(max_length=10, blank=True, null=True, verbose_name='Lot')
    legal_plan = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Plan')
    legal_district_lot = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='District Lot')
    legal_block = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Block')
    legal_section = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Section')
    legal_township = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Township')
    legal_range = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Range')
    land_district = models.ForeignKey(LandDistrictCode, db_column='land_district_code',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(blank=True, null=True,
                                            verbose_name='Property Identification Description (PID)')
    well_location_description = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Description of Well Location',
        db_comment=('Descriptive details of a well\'s location. E.g. the well is located 20\' south west of '
                    'the house; or the well is located in the pump house near the pond.'))

    construction_start_date = models.DateField(
        null=True, verbose_name="Construction Start Date",
        db_comment='The date when well construction started.')
    construction_end_date = models.DateField(
        null=True, verbose_name="Construction Date",
        db_comment='The date when well construction ended.')

    alteration_start_date = models.DateField(
        null=True, verbose_name="Alteration Start Date",
        db_comment='The date when alteration on a well started.')
    alteration_end_date = models.DateField(
        null=True, verbose_name="Alteration Date")

    decommission_start_date = models.DateField(
        null=True, verbose_name="Decommission Start Date",
        db_comment='The start date of when the well was decommissioned.')
    decommission_end_date = models.DateField(
        null=True, verbose_name="Decommission Date")

    drilling_company = models.ForeignKey(DrillingCompany, db_column='drilling_company_guid',
                                         on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name='Drilling Company')

    well_identification_plate_attached = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Well Identification Plate Is Attached',
        db_comment=('Description of where the well identification plate has been attached on or near the '
                    'well.'))
    id_plate_attached_by = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Well identification plate attached by')

    # Contains Well Longitude and Latitude in that order,
    # Values are BC Albers. but we are using WGS84 Lat Lon to avoid rounding errors
    geom = models.PointField(blank=True, null=True, verbose_name='Geo-referenced Location of the Well',
                             srid=4326)

    ground_elevation = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethodCode,
                                                db_column='ground_elevation_method_code',
                                                on_delete=models.CASCADE, blank=True, null=True,
                                                verbose_name='Elevation Determined By')
    drilling_methods = models.ManyToManyField(DrillingMethodCode, verbose_name='Drilling Methods',
                                              blank=True)
    well_orientation = models.BooleanField(default=True, verbose_name='Orientation of Well', choices=(
        (True, 'vertical'), (False, 'horizontal')))

    surface_seal_material = models.ForeignKey(SurfaceSealMaterialCode, db_column='surface_seal_material_code',
                                              on_delete=models.CASCADE, blank=True, null=True,
                                              verbose_name='Surface Seal Material')
    surface_seal_length = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Length')
    surface_seal_depth = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Depth')
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
        max_length=50, blank=True, null=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpeningCode, db_column='screen_opening_code',
                                       on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Opening')
    screen_bottom = models.ForeignKey(ScreenBottomCode, db_column='screen_bottom_code',
                                      on_delete=models.CASCADE, blank=True, null=True, verbose_name='Bottom')
    other_screen_bottom = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Specify Other Screen Bottom')
    screen_information = models.CharField(
        max_length=300, blank=True, null=True, verbose_name="Screen Information"
    )
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
    development_methods = models.ManyToManyField(DevelopmentMethodCode, blank=True,
                                                 verbose_name='Development Methods')
    development_hours = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,
                                            verbose_name='Development Total Duration',
                                            validators=[MinValueValidator(Decimal('0.00'))])
    development_notes = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Development Notes')

    water_quality_characteristics = models.ManyToManyField(
        WaterQualityCharacteristic, db_table='well_water_quality', blank=True,
        verbose_name='Obvious Water Quality Characteristics')
    water_quality_colour = models.CharField(
        max_length=60, blank=True, null=True, verbose_name='Water Quality Colour')
    water_quality_odour = models.CharField(
        max_length=60, blank=True, null=True, verbose_name='Water Quality Odour')

    total_depth_drilled = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Total Depth Drilled')
    finished_well_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Finished Well Depth',
        db_comment=('The depth at which the well was \'finished\'. It can be shallower from the total well '
                    'depth which is the total depth at which the well was drilled. The finished depth is '
                    'represented in units of feet bgl (below ground level).'))
    final_casing_stick_up = models.DecimalField(
        max_digits=6, decimal_places=3, blank=True, null=True, verbose_name='Final Casing Stick Up')
    bedrock_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Depth to Bedrock',
        db_comment='Depth below ground level at which bedrock starts, measured in feet.')
    water_supply_system_name = models.CharField(
        max_length=80, blank=True, null=True, verbose_name='Water Supply System Name',
        db_comment=('Name or identifier given to a well that serves as a water supply system. '
                    'Often, the name is a reflection of the community or system it serves; e.g. Town of '
                    'Osoyoos or Keremeos Irrigation District.'))
    water_supply_system_well_name = models.CharField(
        max_length=80, blank=True, null=True, verbose_name='Water Supply System Well Name',
        db_comment=('The specific name given to a water supply system well. Often, the name reflects which '
                    'well it is within the system, e.g. Well 1 or South Well'))
    static_water_level = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Static Water Level (BTOC)',
        db_comment='The level (depth below ground) to which water will naturally rise in a well without '
                   'pumping, measured in feet.')
    well_yield = models.DecimalField(
        max_digits=8, decimal_places=3, blank=True, null=True, verbose_name='Estimated Well Yield',
        db_comment=('An approximate estimate of the capacity of the well to produce groundwater. Estimated '
                    'by the well driller during construction by conducting a well yield test. Measured in US '
                    'Gallons/minute.'))
    artesian_flow = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Flow',
        db_comment=('Measurement of the artesian well\'s water flow that occurs naturally due to inherent '
                    'water pressure in the well. Pressure within the aquifer forces the groundwater to rise '
                    'above the land surface naturally without using a pump. Flowing artesian wells can flow '
                    'on an intermittent or continuous basis. Measured in US Gallons/minute.'))
    artesian_pressure = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure',
        db_comment=('Pressure of the water coming out of an artesian well as measured at the time of '
                    'construction. Measured in PSI (parts per square inch).'))
    well_cap_type = models.CharField(
        max_length=40, blank=True, null=True, verbose_name='Well Cap')
    well_disinfected = models.BooleanField(
        default=False, verbose_name='Well Disinfected', choices=((False, 'No'), (True, 'Yes')))

    comments = models.CharField(max_length=3000, blank=True, null=True)
    internal_comments = models.CharField(max_length=3000, blank=True, null=True)

    alternative_specs_submitted = \
        models.BooleanField(default=False,
                            verbose_name='Alternative specs submitted (if required)',
                            choices=((False, 'No'), (True, 'Yes')))

    well_yield_unit = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True)
    # want to be integer in future
    diameter = models.CharField(max_length=9, blank=True)

    observation_well_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Observation Well Number")

    observation_well_status = models.ForeignKey(
        ObsWellStatusCode, db_column='obs_well_status_code', blank=True, null=True,
        verbose_name="Observation Well Status", on_delete=models.PROTECT)

    ems = models.CharField(max_length=10, blank=True, null=True,
                           verbose_name="Environmental Monitoring System (EMS) ID")

    utm_zone_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Zone")
    utm_northing = models.IntegerField(
        blank=True, null=True, verbose_name="UTM Northing")
    utm_easting = models.IntegerField(
        blank=True, null=True, verbose_name="UTM Easting")
    coordinate_acquisition_code = models.ForeignKey(
        CoordinateAcquisitionCode, null=True, blank=True, verbose_name="Location Accuracy Code",
        db_column='coordinate_acquisition_code', on_delete=models.PROTECT)
    bcgs_id = models.ForeignKey(BCGS_Numbers, db_column='bcgs_id', on_delete=models.PROTECT, blank=True,
                                null=True, verbose_name="BCGS Mapsheet Number")

    decommission_reason = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Reason for Decommission")
    decommission_method = models.ForeignKey(
        DecommissionMethodCode, db_column='decommission_method_code', blank=True, null="True",
        verbose_name="Method of Decommission", on_delete=models.PROTECT)
    decommission_sealant_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Decommission Sealant Material")
    decommission_backfill_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Decommission Backfill Material")
    decommission_details = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Decommission Details")
    ems_id = models.CharField(max_length=30, blank=True, null=True)
    aquifer = models.ForeignKey(
        Aquifer, db_column='aquifer_id', on_delete=models.PROTECT, blank=True,
        null=True, verbose_name='Aquifer ID Number',
        db_comment=('System generated sequential number assigned to each aquifer. It is widely used by '
                    'ground water administration staff as it is the only consistent unique identifier for a '
                    'mapped aquifer. It is also commonly referred to as Aquifer Number.'))

    person_responsible = models.ForeignKey(Person, db_column='person_responsible_guid',
                                           on_delete=models.PROTECT,
                                           verbose_name='Person Responsible for Drilling',
                                           null=True, blank=True)
    company_of_person_responsible = models.ForeignKey(
        Organization, db_column='org_of_person_responsible_guid', on_delete=models.PROTECT,
        verbose_name='Company of person responsible for drilling', null=True, blank=True)
    driller_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Name of Person Who Did the Work')
    consultant_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Consultant Name')
    consultant_company = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Consultant Company')

    # Aquifer related data
    aquifer_vulnerability_index = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='AVI')
    storativity = models.DecimalField(
        max_digits=8, decimal_places=7, blank=True, null=True, verbose_name='Storativity')
    transmissivity = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='Transmissivity')
    hydraulic_conductivity = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Hydraulic Conductivity')
    specific_storage = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Specific Storage')
    specific_yield = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Specific Yield')
    testing_method = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Testing Method')
    testing_duration = models.PositiveIntegerField(blank=True, null=True)
    analytic_solution_type = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Analytic Solution Type')
    boundary_effect = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Boundary Effect')
    aquifer_lithology = models.ForeignKey(
        AquiferLithologyCode, db_column='aquifer_lithology_code', blank=True, null=True,
        on_delete=models.CASCADE,
        verbose_name="Aquifer Lithology")

    # Production data related data
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
    static_level_before_test = models.DecimalField(
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
    recommended_pump_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                 verbose_name='Recommended pump depth',
                                                 validators=[MinValueValidator(Decimal('0.00'))])
    recommended_pump_rate = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                verbose_name='Recommended pump rate',
                                                validators=[MinValueValidator(Decimal('0.00'))])

    history = GenericRelation(Version)

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

    def latitude(self):
        if self.geom:
            return self.geom.y
        else:
            return None

    def longitude(self):
        if self.geom:
            return self.geom.x
        else:
            return None

    db_table_comment = ('Describes how a well was constructed, altered, decomissioned over time. Includes '
                        'information related to who owns the well, location of well, the lithologic '
                        'description as well as other information related to the construction of the well.')


# @receiver(pre_revision_commit)
# def pre_revision_commit_receiver(sender, revision, versions, **kwargs):
#      print(sender)
#      print(revision)
#      print(versions)


class Perforation(AuditModel):
    """
    Liner Details
    """
    perforation_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    well_tag_number = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True,
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
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
    well = models.ForeignKey(
        Well, db_column='well_tag_number',
        on_delete=models.CASCADE, blank=True, null=True,
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    mailing_address = models.CharField(
        max_length=100, verbose_name='Mailing Address')

    city = models.CharField(max_length=100, verbose_name='Town/City')
    province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, verbose_name='Province')
    postal_code = models.CharField(
        max_length=10, blank=True, verbose_name='Postal Code')

    class Meta:
        db_table = 'ltsa_owner'

    def __str__(self):
        return '%s %s' % (self.full_name, self.mailing_address)


class CasingMaterialCode(CodeTableModel):
    """
     The material used for casing a well, e.g., Cement, Plastic, Steel.
    """
    code = models.CharField(primary_key=True, max_length=10, editable=False, db_column='casing_material_code')
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'casing_material_code'
        ordering = ['display_order', 'description']

    db_table_comment = 'Describes the material that the casing is made of.'

    def __str__(self):
        return self.description


class CasingCode(CodeTableModel):
    """
    Type of Casing used on a well
    """
    code = models.CharField(primary_key=True, max_length=10, editable=False, db_column='casing_code')
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'casing_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Describes the casing component (piping or tubing installed in a well) as either '
                        'production (inner tube), surface (outer tube), or open hole.')

    def __str__(self):
        return self.description


class AquiferWell(AuditModel):
    """
    AquiferWell
    """

    aquifer_well_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aquifer_id = models.PositiveIntegerField(
        verbose_name="Aquifer Number", blank=True, null=True,
        db_comment=('System generated sequential number assigned to each aquifer. It is widely used by '
                    'ground water administration staff as it is the only consistent unique identifier for a '
                    'mapped aquifer. It is also commonly referred to as Aquifer Number.'))
    well_tag_number = models.ForeignKey(
        Well, db_column='well_tag_number', to_field='well_tag_number',
        on_delete=models.CASCADE, blank=False, null=False,
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))

    class Meta:
        db_table = 'aquifer_well'

    db_table_comment = ('Cross reference table that connects the well to the aquifer. It resolves the many '
                        'to many relationship between wells and aquifers. One well can be in 1-many '
                        'aquifers, and one aquifer can have 1-many wells in it.')


# TODO: This class needs to be moved to submissions.models (in order to do that, the fk references for a
# number of other models needs to be updated)
class ActivitySubmission(AuditModelStructure):
    """
    Activity information on a Well submitted by a user.
    """
    filing_number = models.AutoField(primary_key=True)
    activity_submission_guid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True,
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    well_activity_type = models.ForeignKey(
        WellActivityCode, db_column='well_activity_code', on_delete=models.CASCADE,
        verbose_name='Type of Work')
    well_status = models.ForeignKey(WellStatusCode, db_column='well_status_code',
                                    on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='Well Status')
    well_publication_status = models.ForeignKey(
        WellPublicationStatusCode, db_column='well_publication_status_code',
        on_delete=models.CASCADE, verbose_name='Well Publication Status',
        default='Published')
    well_class = models.ForeignKey(WellClassCode, blank=True, null=True, db_column='well_class_code',
                                   on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclassCode, db_column='well_subclass_guid',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUseCode, db_column='intended_water_use_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='Intended Water Use')
    # Driller responsible should be a required field on all submissions, but for legacy well
    # information this may not be available, so we can't enforce this on a database level.
    person_responsible = models.ForeignKey(Person, db_column='person_responsible_guid',
                                           on_delete=models.PROTECT,
                                           verbose_name='Person Responsible for Drilling',
                                           blank=True, null=True)
    company_of_person_responsible = models.ForeignKey(
        Organization, db_column='org_of_person_responsible_guid', on_delete=models.PROTECT,
        verbose_name='Company of person responsible for drilling', null=True, blank=True)
    driller_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Name of Person Who Did the Work')
    consultant_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Consultant Name')
    consultant_company = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Consultant Company')
    # Work start & end date should be required fields on all submissions, but for legacy well
    # information this may not be available, so we can't enforce this on a database level.
    work_start_date = models.DateField(
        verbose_name='Work Start Date', null=True, blank=True,
        db_comment=('The date when an activity such as well construction, well alteration, or well '
                    'decommission was started.'))
    work_end_date = models.DateField(
        verbose_name='Work End Date', null=True, blank=True,
        db_comment=('The date when an activity such as well construction, well alteration, or well '
                    'decommission was ended.'))

    owner_full_name = models.CharField(
        max_length=200, verbose_name='Owner Name', blank=True, null=True)
    owner_mailing_address = models.CharField(
        max_length=100, verbose_name='Mailing Address', blank=True, null=True)
    owner_city = models.CharField(max_length=100, verbose_name='Town/City', blank=True, null=True)
    owner_province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, verbose_name='Province',
        blank=True, null=True)
    owner_postal_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Postal Code')
    owner_email = models.EmailField(null=True, blank=True, verbose_name='Email address')
    owner_tel = models.CharField(
        null=True, blank=True, max_length=25, verbose_name='Telephone number')

    street_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, null=True,
                            verbose_name='Town/City')
    legal_lot = models.CharField(max_length=10, blank=True, null=True, verbose_name='Lot')
    legal_plan = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Plan')
    legal_district_lot = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='District Lot')
    legal_block = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Block')
    legal_section = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Section')
    legal_township = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Township')
    legal_range = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Range')
    land_district = models.ForeignKey(LandDistrictCode, db_column='land_district_code',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='PID')
    well_location_description = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Well Location Description',
        db_comment=('Descriptive details of a well\'s location. E.g. the well is located 20\' south west '
                    'of the house; or the well is located in the pump house near the pond.'))

    identification_plate_number = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Identification Plate Number',
        db_comment=('Steel plate with a unique number that is attached to required wells under the '
                    'groundwater protection regulations such as water supply wells, recharge or injection '
                    'wells made by drilling or boring, and permanent dewatering wells.'))
    well_identification_plate_attached = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Well Identification Plate Is Attached',
        db_comment=('Description of where the well identification plate has been attached on or near the '
                    'well.'))

    id_plate_attached_by = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Well identification plate attached by')

    # Contains Well Longitude and Latitude in that order
    # Values are BC Albers. but we are using WGS84 Lat Lon to avoid rounding errors
    geom = models.PointField(
        blank=True, null=True, verbose_name='Geo-referenced Location of the Well', srid=4326)

    coordinate_acquisition_code = models.ForeignKey(
        CoordinateAcquisitionCode, null=True, blank=True, verbose_name="Location Accuracy Code",
        db_column='coordinate_acquisition_code', on_delete=models.PROTECT)
    ground_elevation = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethodCode,
                                                db_column='ground_elevation_method_code',
                                                on_delete=models.CASCADE, blank=True, null=True,
                                                verbose_name='Elevation Determined By')
    drilling_methods = models.ManyToManyField(DrillingMethodCode, verbose_name='Drilling Methods',
                                              blank=True)
    well_orientation = models.BooleanField(default=True, verbose_name='Orientation of Well', choices=(
        (True, 'vertical'), (False, 'horizontal')))
    water_supply_system_name = models.CharField(
        max_length=80, blank=True, null=True, verbose_name='Water Supply System Name',
        db_comment=('Name or identifier given to a well that serves as a water supply system. Often, the '
                    'name is a reflection of the community or system it serves, e.g. Town of Osoyoos or '
                    'Keremeos Irrigation District.'))
    water_supply_system_well_name = models.CharField(
        max_length=80, blank=True, null=True, verbose_name='Water Supply System Well Name',
        db_comment=('The specific name given to a water supply system well. Often, the name reflects which '
                    'well it is within the system, e.g. Well 1 or South Well'))

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
        max_length=250, blank=True, null=True, verbose_name='Backfill Material Above Surface Seal')
    backfill_above_surface_seal_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')
    backfill_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')

    backfill_type = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Backfill Material Above Surface Seal")
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
        max_length=50, blank=True, null=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpeningCode, db_column='screen_opening_code',
                                       on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Opening')
    screen_bottom = models.ForeignKey(ScreenBottomCode, db_column='screen_bottom_code',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Bottom')
    other_screen_bottom = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Specify Other Screen Bottom')

    screen_information = models.CharField(
        max_length=300, blank=True, null=True, verbose_name="Screen Information"
    )

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
    development_methods = models.ManyToManyField(DevelopmentMethodCode, blank=True,
                                                 verbose_name='Development Methods')
    development_hours = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,
                                            verbose_name='Development Total Duration',
                                            validators=[MinValueValidator(Decimal('0.00'))])
    development_notes = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Development Notes')

    water_quality_characteristics = models.ManyToManyField(
        WaterQualityCharacteristic, db_table='activity_submission_water_quality', blank=True,
        verbose_name='Obvious Water Quality Characteristics')
    water_quality_colour = models.CharField(
        max_length=60, blank=True, null=True, verbose_name='Water Quality Colour')
    water_quality_odour = models.CharField(
        max_length=60, blank=True, null=True, verbose_name='Water Quality Odour')

    total_depth_drilled = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Total Depth Drilled')
    finished_well_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Finished Well Depth',
        db_comment=('The depth at which the well was \'finished\'. It can be shallower from the total well '
                    'depth which is the total depth at which the well was drilled. The finished depth is '
                    'represented in units of feet bgl (below ground level).'))
    final_casing_stick_up = models.DecimalField(
        max_digits=6, decimal_places=3, blank=True, null=True, verbose_name='Final Casing Stick Up')
    bedrock_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Depth to Bedrock')
    static_water_level = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Static Water Level (BTOC)',
        db_comment=('The level (depth below ground) to which water will naturally rise in a well without '
                    'pumping, measured in feet.'))
    well_yield = models.DecimalField(
        max_digits=8, decimal_places=3, blank=True, null=True, verbose_name='Estimated Well Yield')
    artesian_flow = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Flow',
        db_comment=('Measurement of the artesian well\'s water flow that occurs naturally due to inherent '
                    'water pressure in the well. Pressure within the aquifer forces the groundwater to '
                    'rise above the land surface naturally without using a pump. Flowing artesian wells '
                    'can flow on an intermittent or continuous basis.  Measured in US Gallons/minute.'))
    artesian_pressure = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure',
        db_comment=('Pressure of the water coming out of an artesian well as measured at the time of '
                    'construction. Measured in PSI (parts per square inch).'))
    well_cap_type = models.CharField(
        max_length=40, blank=True, null=True, verbose_name='Well Cap Type')
    well_disinfected = models.BooleanField(
        default=False, verbose_name='Well Disinfected?', choices=((False, 'No'), (True, 'Yes')))

    comments = models.CharField(max_length=3000, blank=True, null=True)
    internal_comments = models.CharField(max_length=3000, blank=True, null=True)

    alternative_specs_submitted = models.BooleanField(
        default=False,
        verbose_name='Alternative specs submitted (if required)', choices=((False, 'No'), (True, 'Yes')))

    well_yield_unit = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True)
    # want to be integer in future
    diameter = models.CharField(max_length=9, blank=True, null=True)
    ems = models.CharField(max_length=30, blank=True, null=True)

    # Observation well details
    observation_well_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Observation Well Number")

    observation_well_status = models.ForeignKey(
        ObsWellStatusCode, db_column='obs_well_status_code', blank=True, null=True,
        verbose_name="Observation Well Status", on_delete=models.PROTECT)
    # aquifer association
    aquifer = models.ForeignKey(
        Aquifer, db_column='aquifer_id', on_delete=models.PROTECT, blank=True,
        null=True, verbose_name='Aquifer ID Number',
        db_comment=('System generated sequential number assigned to each aquifer. It is widely used by '
                    'ground water administration staff as it is the only consistent unique identifier for a '
                    'mapped aquifer. It is also commonly referred to as Aquifer Number.'))

    # Decommission info
    decommission_reason = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Reason for Decommission")
    decommission_method = models.ForeignKey(
        DecommissionMethodCode, db_column='decommission_method_code', blank=True, null=True,
        verbose_name="Method of Decommission", on_delete=models.PROTECT)
    decommission_sealant_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Sealant Material")
    decommission_backfill_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Backfill Material")
    decommission_details = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Decommission Details")

    # Aquifer related data
    aquifer_vulnerability_index = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='AVI')
    storativity = models.DecimalField(
        max_digits=8, decimal_places=7, blank=True, null=True, verbose_name='Storativity')
    transmissivity = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='Transmissivity')
    hydraulic_conductivity = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Hydraulic Conductivity')
    specific_storage = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Specific Storage')
    specific_yield = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Specific Yield')
    testing_method = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Testing Method')
    testing_duration = models.PositiveIntegerField(blank=True, null=True)
    analytic_solution_type = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Analytic Solution Type')
    boundary_effect = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Boundary Effect')
    aquifer_lithology = models.ForeignKey(
        AquiferLithologyCode, db_column='aquifer_lithology_code', blank=True, null=True,
        on_delete=models.CASCADE,
        verbose_name="Aquifer Lithology")

    # Production data related data
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
    static_level_before_test = models.DecimalField(
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
    recommended_pump_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                 verbose_name='Recommended pump depth',
                                                 validators=[MinValueValidator(Decimal('0.00'))])
    recommended_pump_rate = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                verbose_name='Recommended pump rate',
                                                validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'activity_submission'

    db_table_comment = 'Submission of data and information related to a groundwater wells.'

    def __str__(self):
        if self.filing_number:
            return '%s %d %s %s' % (self.activity_submission_guid, self.filing_number,
                                    self.well_activity_type.code, self.street_address)
        else:
            return '%s %s' % (self.activity_submission_guid, self.street_address)

    def latitude(self):
        if self.geom:
            return self.geom.y
        else:
            return None

    def longitude(self):
        if self.geom:
            return self.geom.x
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.update_date:
            self.update_date = timezone.now()

        if self._state.adding is True:
            if not self.create_date:
                self.create_date = timezone.now()

        return super().save(*args, **kwargs)


@reversion.register(fields=['lithology_from', 'lithology_to', 'lithology_raw_data', 'lithology_description',
                            'lithology_colour', 'lithology_hardness', 'lithology_material', 'lithology_observation',
                            'water_bearing_estimated_flow', 'water_bearing_estimated_flow_units',  'lithology_moisture',
                            'bedrock_material', 'bedrock_material_descriptor', 'lithology_structure',
                            'surficial_material', 'secondary_surficial_material', 'lithology_sequence_number'])
class LithologyDescription(AuditModel):
    """
    Lithology information details
    """
    lithology_description_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(
        ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True,
        related_name='lithologydescription_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True,
        related_name='lithologydescription_set',
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    lithology_from = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='From',
        blank=True, null=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        db_comment=('Depth below ground surface of the start of the lithology material for a particular '
                    'lithology layer, as observed during the construction or alteration of a well, '
                    'measured in feet.'))
    lithology_to = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='To',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))],
        db_comment=('Depth below ground surface of the end of the lithology material for a particular '
                    'lithology layer as observed during the construction or alteration of a well, measured '
                    'in feet.'))
    lithology_raw_data = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Raw Data')

    lithology_description = models.ForeignKey(
        LithologyDescriptionCode,
        db_column='lithology_description_code',
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name="Description",
        db_comment=('Standard terms used to characterize the different qualities of lithologic'
                    ' materials. E.g. dry, loose, weathered, soft.'))
    lithology_colour = models.ForeignKey(
        LithologyColourCode, db_column='lithology_colour_code',
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Colour',
        db_comment=('Valid options for the colour of the lithologic material identified at time of'
                    ' drilling. E.g. Black, dark, tan, rust-coloured'))
    lithology_hardness = models.ForeignKey(
        LithologyHardnessCode, db_column='lithology_hardness_code',
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Hardness',
        db_comment=('Code that represents the hardness of the material that a well is drilled into (the'
                    ' lithology). E.g. Very hard, Hard, Dense, Stiff, Medium, Loose, Soft, Very soft.'))
    lithology_material = models.ForeignKey(
        LithologyMaterialCode, db_column='lithology_material_code',
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name="Material",
        db_comment=('Standard terms used for defining the material noted for lithology. E.g. Rock, Clay,'
                    ' Sand, Unspecified.'))

    water_bearing_estimated_flow = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True, verbose_name='Water Bearing Estimated Flow')
    water_bearing_estimated_flow_units = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Units')
    lithology_observation = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Observations',
        db_comment='Free form text used by the driller to describe observations made of the well lithology.')

    bedrock_material = models.ForeignKey(BedrockMaterialCode, db_column='bedrock_material_code',
                                         on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name='Bedrock Material')
    bedrock_material_descriptor = models.ForeignKey(
        BedrockMaterialDescriptorCode, db_column='bedrock_material_descriptor_code', on_delete=models.CASCADE,
        blank=True, null=True, verbose_name='Descriptor')
    lithology_structure = models.ForeignKey(LithologyStructureCode, db_column='lithology_structure_code',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name='Bedding')
    lithology_moisture = models.ForeignKey(LithologyMoistureCode, db_column='lithology_moisture_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='Moisture')
    surficial_material = models.ForeignKey(SurficialMaterialCode, db_column='surficial_material_code',
                                           related_name='surficial_material_set', on_delete=models.CASCADE,
                                           blank=True, null=True, verbose_name='Surficial Material')
    secondary_surficial_material = models.ForeignKey(SurficialMaterialCode,
                                                     db_column='secondary_surficial_material_code',
                                                     related_name='secondary_surficial_material_set',
                                                     on_delete=models.CASCADE, blank=True, null=True,
                                                     verbose_name='Secondary Surficial Material')

    lithology_sequence_number = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_description'
        ordering = ["lithology_sequence_number"]

    db_table_comment = ('Describes the different lithologic qualities, characteristics, and materials found '
                        'at different depths while drilling.')

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.lithology_from,
                                                         self.lithology_to)
        else:
            return 'well {} {} {}'.format(self.well, self.lithology_from, self.lithology_to)


@reversion.register(fields=['start', 'end'])
class LinerPerforation(AuditModel):
    """
    Perforation in a well liner
    """
    liner_perforation_guid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                              editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='linerperforation_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True,
        null=True, related_name='linerperforation_set',
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    start = models.DecimalField(db_column='liner_perforation_from', max_digits=7, decimal_places=2,
                                verbose_name='Perforated From', blank=False,
                                validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(db_column='liner_perforation_to', max_digits=7, decimal_places=2,
                              verbose_name='Perforated To', blank=False,
                              validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        ordering = ["start", "end"]
        db_table = 'liner_perforation'

    db_table_comment = ('Describes the depths at which the liner is perforated in a well to help improve '
                        'water flow at the bottom of the well. Some wells are perforated instead of having '
                        'a screen installed.')

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission,
                                                         self.start,
                                                         self.end)
        else:
            return 'well {} {} {}'.format(self.well, self.start, self.end)


@reversion.register(fields=['start', 'end', 'diameter', 'casing_code',
                            'casing_material', 'wall_thickness', 'drive_shoe'])
class Casing(AuditModel):
    """
    Casing information

    A casing may be associated to a particular submission, or to a well.
    """
    casing_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='casing_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='casing_set',
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    # 2018/Sep/26 - According to PO (Lindsay), diameter, start and end are required fields.
    # There is however a lot of legacy data that does not have this field.
    start = models.DecimalField(db_column='casing_from', max_digits=7, decimal_places=2, verbose_name='From',
                                null=True, blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(db_column='casing_to', max_digits=7, decimal_places=2, verbose_name='To',
                              null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    # NOTE: Diameter should be pulling from internal_diameter
    diameter = models.DecimalField(
        max_digits=8, decimal_places=3, verbose_name='Diameter', null=True,
        blank=True, validators=[MinValueValidator(Decimal('0.5'))],
        db_comment=('The diameter as measure in inches of the casing of the well. There can be multiple '
                    'casings in a well, e.g. surface casing, and production casing. Diameter of casing made '
                    'available to the public is generally the production casing.'))
    casing_code = models.ForeignKey(CasingCode, db_column='casing_code', on_delete=models.CASCADE,
                                    verbose_name='Casing Type Code', null=True)
    casing_material = models.ForeignKey(CasingMaterialCode, db_column='casing_material_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Casing Material Code')
    wall_thickness = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Wall Thickness',
                                         blank=True, null=True,
                                         validators=[MinValueValidator(Decimal('0.01'))])
    drive_shoe = models.NullBooleanField(default=False, null=True, verbose_name='Drive Shoe',
                                         choices=((False, 'No'), (True, 'Yes')))

    class Meta:
        ordering = ["start", "end"]
        db_table = 'casing'

    db_table_comment = ('Piping or tubing installed in a well to support the sides of the well. The casing '
                        'is comprised of a production (inner tube) and surface (outer tube) and can be made '
                        'of a variety of materials.')

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.start, self.end)
        else:
            return 'well {} {} {}'.format(self.well, self.start, self.end)

    def as_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "casing_guid": self.casing_guid,
            "well_tag_number": self.well_tag_number,
            "diameter": self.diameter,
            "wall_thickness": self.wall_thickness,
            "casing_material": self.casing_material,
            "drive_shoe": self.drive_shoe
        }


@reversion.register(fields=['start', 'end', 'internal_diameter', 'assembly_type', 'slot_size'])
class Screen(AuditModel):
    """
    Screen in a well
    """
    screen_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='screen_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True,
        null=True, related_name='screen_set',
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    start = models.DecimalField(db_column='screen_from', max_digits=7, decimal_places=2, verbose_name='From',
                                blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(db_column='screen_to', max_digits=7, decimal_places=2, verbose_name='To',
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
        ordering = ['start', 'end']

    db_table_comment = ('Describes the screen type, diameter of screen, and the depth at which the screen is'
                        ' installed in a well.')

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.start,
                                                         self.end)
        else:
            return 'well {} {} {}'.format(self.well, self.start, self.end)


class WaterQualityColour(CodeTableModel):
    """
    Colour choices for describing water quality
    """
    code = models.CharField(primary_key=True, max_length=32, db_column='water_quality_colour_code')
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'water_quality_colour_code'

    db_table_comment = ('Valid values of the colour of the water as recorded at time of work. E.g. Orange,'
                        ' Black, Clear, Other')

    def __str__(self):
        return self.description


class HydraulicProperty(AuditModel):
    """
    Hydraulic properties of the well, usually determined via tests.
    """
    hydraulic_property_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(
        Well, db_column='well_tag_number', to_field='well_tag_number',
        on_delete=models.CASCADE, blank=False, null=False,
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    avi = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='AVI')
    storativity = models.DecimalField(
        max_digits=8, decimal_places=7, blank=True, null=True, verbose_name='Storativity')
    transmissivity = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='Transmissivity')
    hydraulic_conductivity = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Hydraulic Conductivity')
    specific_storage = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Specific Storage')
    specific_yield = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Specific Yield')
    testing_method = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Testing Method')
    testing_duration = models.PositiveIntegerField(blank=True, null=True)
    analytic_solution_type = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Analytic Solution Type')
    boundary_effect = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Boundary Effect')

    class Meta:
        db_table = 'hydraulic_property'
        verbose_name_plural = 'Hydraulic Properties'

    def __str__(self):
        return '{} - {}'.format(self.well, self.hydraulic_property_guid)


class DecommissionMaterialCode(BasicCodeTableModel):
    """Codes for decommission materials"""
    code = models.CharField(primary_key=True, max_length=30, db_column='decommission_material_code')
    description = models.CharField(max_length=100)

    db_table_comment = ('Describes the material used to fill a well when decomissioned. E.g. Bentonite'
                        ' chips, Native sand or gravel, Commercial gravel/pea gravel.')

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


@reversion.register(fields=['start', 'end', 'material', 'observations'])
class DecommissionDescription(AuditModel):
    """Provides a description of the ground conditions (between specified start and end depth) for
        decommissioning"""

    decommission_description_guid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='decommission_description_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True,
        null=True, related_name='decommission_description_set',
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    start = models.DecimalField(db_column='decommission_description_from', max_digits=7, decimal_places=2,
                                verbose_name='Decommissioned From', blank=False,
                                validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(db_column='decommission_description_to', max_digits=7, decimal_places=2,
                              verbose_name='Decommissioned To', blank=False,
                              validators=[MinValueValidator(Decimal('0.01'))])
    material = models.ForeignKey(DecommissionMaterialCode, db_column='decommission_material_code',
                                 on_delete=models.PROTECT)
    observations = models.CharField(max_length=255, null=True, blank=True)

    db_table_comment = ('A cross refernce table maintaining the list of wells that have been decomissioned'
                        ' and the materials used to fill the well when decomissioned. E.g. Bentonite chips,'
                        ' Native sand or gravel, Commercial gravel/pea gravel.')
