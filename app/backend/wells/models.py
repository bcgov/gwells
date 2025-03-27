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

import uuid
import reversion
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.utils import timezone

from django.contrib.gis.db import models


from gwells.models import AuditModel, ProvinceStateCode, ScreenIntakeMethodCode, ScreenMaterialCode,\
    ScreenOpeningCode, ScreenBottomCode, ScreenTypeCode, ScreenAssemblyTypeCode, CodeTableModel,\
    BasicCodeTableModel
from gwells.models.common import AuditModelStructure
from gwells.models.lithology import (
    LithologyDescriptionCode, LithologyColourCode, LithologyHardnessCode,
    LithologyMaterialCode, BedrockMaterialCode, BedrockMaterialDescriptorCode, LithologyStructureCode,
    LithologyMoistureCode, SurficialMaterialCode)
from gwells.db_comments.patch_fields import patch_fields


# from aquifers.models import Aquifer

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
    bcgs_number = models.CharField(
        max_length=20, verbose_name="BCGS Mapsheet Number")

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
    yield_estimation_method_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
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

    code = models.CharField(primary_key=True, max_length=10,
                            db_column='water_quality_characteristic_code')
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
    development_method_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
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
    filter_pack_material_size_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'filter_pack_material_size_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Codes for the sizes of the material used to pack a well filter. Some examples of '
                        'filter pack sizes are: 1.0 - 2.0 mm, 2.0 - 4.0 mm, 4.0 - 8.0 mm.')

    def __str__(self):
        return self.description


class BoundaryEffectCode(CodeTableModel):
    """
     The observed boundary effect in the pumping test analysis.
    """
    boundary_effect_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'boundary_effect_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('The observed boundary effect in the pumping test analysis. Constant head or '
                        'no flow boundaries are two possible observations.')

    def __str__(self):
        return self.description


class PumpingTestDescriptionCode(CodeTableModel):
    """
     The pumping test method description in aquifer pumping tests.
    """
    pumping_test_description_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'pumping_test_description_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Type of the pumping test method used for aquifer pumping tests.')

    def __str__(self):
        return self.description


class AnalysisMethodCode(CodeTableModel):
    """
     The analysis method used in aquifer pumping tests.
    """
    analysis_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'analysis_method_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('The analysis method used in aquifer pumping tests.')

    def __str__(self):
        return self.description


class WellDisinfectedCode(CodeTableModel):
    """
     The status on whether the well has been disinfected or not.
    """
    well_disinfected_code = models.CharField(primary_key=True, max_length=100, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'well_disinfected_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Codes for the well disinfected status. If the disinfected status on a legacy well'
                        'is unkown, then the null status is mapped to the Unkown value.')

    def __str__(self):
        return self.description


class WellOrientationCode(CodeTableModel):
    """
     Codes describing the orientation of the well
    """
    well_orientation_code = models.CharField(primary_key=True, max_length=100, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'well_orientation_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Codes for the well orienation. Horizontal and Vertical are the only codes at this point')

    def __str__(self):
        return self.description


class DriveShoeCode(CodeTableModel):
    """
     The status on whether a casing has a drive shoe installed.
    """
    drive_shoe_code = models.CharField(primary_key=True, max_length=100, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'drive_shoe_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Codes for drive shoe installation on a casing.')

    def __str__(self):
        return self.description


class FilterPackMaterialCode(CodeTableModel):
    """
     The material used to pack a well filter, e.g. Very coarse sand, Very fine gravel, Fine gravel.
    """
    filter_pack_material_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'filter_pack_material_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Materials used in the filter pack, which are placed in the annulus of the well '
                        'between the borehole wall and the well screen, and are used to settle-out fine '
                        'grained particles that may otherwise enter the well. I.e. Fine gravel, very coarse '
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
    surface_seal_method_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
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
    surface_seal_material_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
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
    drilling_method_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'drilling_method_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Represents the method that was used to drill or construct a well. E.g. Excavated, '
                        'Dual Rotary, Driving, Other, Unknown.')

    def __str__(self):
        return self.description


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
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(
        max_length=255,
        verbose_name='Licence Status')

    class Meta:
        db_table = 'licenced_status_code'
        ordering = ['display_order', 'licenced_status_code']

    db_table_comment = ('Valid licencing options granted to a well under the Water Water Sustainability '
                        'Act. This information comes from eLicensing. i.e. Unlicensed, Licensed, Historical')

    db_column_supplemental_comments = {
        "description":"Descriptions of valid licensing options granted to a well under the Water Sustainability Act. This information comes from eLicensing. i.e. Unlicensed, Licensed, Historical",
        "licenced_status_code":"Valid licensing options granted to a well under the Water Sustainability Act. This information comes from eLicensing. i.e. Unlicensed, Licensed, Historical.",
    }

    def save(self, *args, **kwargs):
        self.validate()
        super(LicencedStatusCode, self).save(*args, **kwargs)


class IntendedWaterUseCode(CodeTableModel):
    """
    Usage of Wells (water supply).
    """
    intended_water_use_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(
        max_length=100,
        verbose_name='Intented Water Use')

    class Meta:
        db_table = 'intended_water_use_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('The intended use of the water in a water supply well as reported by the driller at '
                        'time of work completion on the well. E.g Private domestic, irrigation, water '
                        'supply system, Industrial commercial, and unknown.')

    db_column_supplemental_comments = {
        "description":"The intended use of the water in a water supply well as reported by the driller at time of work completion on the well. E.g Private Domestic, Irrigation, Water Supply System, Commercial and Industrial, Unknown, Other",
        "intended_water_use_code":"The intended use of the water in a water supply well as reported by the driller at time of work completion on the well. E.g,  DOM, IRR, DWS, COM, UNK, OTHER",
    }

    def __str__(self):
        return self.description


class GroundElevationMethodCode(CodeTableModel):
    """
    The method used to determine the ground elevation of a well.
    Some examples of methods to determine ground elevation include:
    GPS, Altimeter, Differential GPS, Level, 1:50,000 map, 1:20,000 map, 1:10,000 map, 1:5,000 map.
    """
    ground_elevation_method_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
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
        db_comment=('Valid classifications as defined in the Groundwater Protection Regulation of the'
                    ' Water Act. i.e. Water Supply, Monitoring, Recharge, Injection, Dewatering,'
                    ' Drainage, Remediation, Geotechnical, Closed-loop geoexchange.'))
    description = models.CharField(
        max_length=100, verbose_name='Well Class',
        db_comment=('Descriptions of valid classifications as defined in the Groundwater Protection'
                    ' Regulation of the Water Act. E.g. Water Supply, Monitoring, Recharge / Injection,'
                    ' Dewatering / Drainage, Remediation, Geotechnical.'))

    class Meta:
        db_table = 'well_class_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Valid classifications as defined in the Groundwater Protection Regulation of the'
                        ' Water Sustainability Act. E.g. Water Supply, Monitoring, Recharge / Injection,'
                        ' Dewatering / Drainage, Remediation, Geotechnical.')

    db_column_supplemental_comments = {
        "description":"Descriptions of valid classifications as defined in the Groundwater Protection Regulation of the Water Sustainability Act. E.g. Water Supply, Monitoring, Recharge / Injection, Dewatering / Drainage, Remediation, Geotechnical.",
        "well_class_code":"Valid classifications as defined in the Groundwater Protection Regulation of the Water Sustainability Act. i.e. Unknown, Water Supply, Monitoring, Recharge, Injection, Dewatering, Drainage, Remediation, Geotechnical, Closed-loop geoexchange.",
    }

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
        db_comment=('Status of a well indicates whether the report relates to the construction,'
                    ' alteration, or decommission of the well; e.g., Construction, Alteration,'
                    ' Abandoned, Deccommission.'))
    description = models.CharField(
        max_length=255,
        verbose_name='Well Status',
        db_comment=('Description of the status of a well as defined in the Groundwater Protection Regulation of the Water Sustainability Act. i.e. New, Abandoned (exists in Wells but will not be used for E-Wells), Alteration, Closure, Other.'))

    objects = models.Manager()
    types = WellStatusCodeTypeManager()

    class Meta:
        db_table = 'well_status_code'
        ordering = ['display_order', 'well_status_code']

    db_table_comment = ('Status of a well indicates whether the report relates to the construction,'
                        ' alteration, or decommission of the well; e.g., Construction, alteration,'
                        ' Abandoned, Deccommission.')


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
    well_class = models.ForeignKey(
        WellClassCode, null=True, db_column='well_class_code',
        on_delete=models.PROTECT, blank=True,
        db_comment=('Valid classifications as defined in the Groundwater Protection Regulation of the Water Sustainability Act. i.e. Water Supply, Monitoring, Recharge, Injection, Dewatering, Drainage, Remediation, Geotechnical, Closed-loop geoexchange.'))
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
        db_comment=('ASK DEVELOPER S TO DELETE THIS COLUMN once the \'yield\' column has been all'
                    ' converted to USGPM. Describes the unit of measure that was used for the well'
                    ' yield. All Code except the U.S. Gallons per Minute has been retired as all data'
                    ' from April 2019 will be reported in USGPM. E.g of other Code that have been used'
                    ' in the past are GPM, DRY, UNK.'))
    description = models.CharField(
        max_length=100, verbose_name='Well Yield Unit',
        db_comment=('Describes the unit of measure that was used for the well yield. All codes except'
                    ' the U.S. Gallons per Minute has been retired as all data from April 2019 will be'
                    ' reported in U.S. Gallons per Minute. E.g of other codes that have been used in the'
                    ' past are Gallons per Minute (U.S./Imperial), Dry Hole, Unknown Yield.'))

    class Meta:
        db_table = 'well_yield_unit_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Describes the unit of measure that was used for the well yield. All codes except'
                        ' the U.S. Gallons per Minute has been retired as all data from April 2019 will be'
                        ' reported in U.S. Gallons per Minute. E.g of other codes that have been used in the'
                        ' past are Gallons per Minute (U.S./Imperial), Dry Hole, Unknown Yield.')

    def __str__(self):
        return self.description


class CoordinateAcquisitionCode(BasicCodeTableModel):
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
    code = models.CharField(
        primary_key=True, max_length=1, editable=False,
        db_column='coordinate_acquisition_code',
        db_comment=('Codes for the accuracy of the coordinate position, which is best estimated based on'
                    ' the information provided by the data submitter and analysis done by staff. E.g. A,'
                    ' B, C.'))
    description = models.CharField(
        max_length=250,
        db_comment=('A description of the coordinate_aquisition_code.  It describes how accurate the coordinate position is  estimated based on the information provided by the data submitter and analysis done by staff. E.g. (10 m accuracy) ICF cadastre and good location sketch, (200 m accuracy) Digitized from 1:50,000 mapping, (unknown, accuracy based on parcel size) ICF cadastre, poor or no location sketch, arbitraily located in center of parcel.'))

    class Meta:
        db_table = 'coordinate_acquisition_code'
        ordering = ['code', ]

    db_table_comment = ('A description of how accurate the coordinate position is best estimated to be based'
                        ' on the information provided by the data submitter and analysis done by staff. E.g.'
                        ' (10 m accuracy) ICF cadastre and good location sketch, (200 m accuracy) Digitized'
                        ' from 1:50,000 mapping, (unknown, accuracy based on parcel size) ICF cadastre, poor'
                        ' or no location sketch, arbitraily located in center of parcel.')

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
    owner_city = models.CharField(max_length=100, verbose_name='Town/City', blank=True, null=True)
    owner_province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.PROTECT, blank=True,
        verbose_name='Province', null=True)
    owner_postal_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Postal Code')
    owner_email = models.EmailField(
        null=True, blank=True, verbose_name='Email address')
    owner_tel = models.CharField(
        null=True, blank=True, max_length=25, verbose_name='Telephone number')

    well_class = models.ForeignKey(
        WellClassCode, db_column='well_class_code', blank=True, null=False, default='UNK',
        on_delete=models.PROTECT, verbose_name='Well Class',
        db_comment=('Valid classifications as defined in the Groundwater Protection Regulation of the'
                    ' Water Act. i.e. Water Supply, Monitoring, Recharge, Injection, Dewatering,'
                    ' Drainage, Remediation, Geotechnical, Closed-loop geoexchange.'))
    well_subclass = models.ForeignKey(WellSubclassCode, db_column='well_subclass_guid',
                                      on_delete=models.PROTECT, blank=True, null=True,
                                      verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(
        IntendedWaterUseCode, db_column='intended_water_use_code',
        on_delete=models.PROTECT, blank=True, null=False, default='NA',
        verbose_name='Intended Water Use',
        db_comment=('The intended use of the water in a water supply well as reported by the driller at'
                    ' time of work completion on the well. E.g DOM, IRR, DWS, COM'))
    well_status = models.ForeignKey(
        WellStatusCode, db_column='well_status_code',
        on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Well Status',
        db_comment=('Status of a well indicates whether the report relates to the construction,'
                    ' alteration, or decommission of the well; e.g., Construction, Alteration,'
                    ' Abandoned, Deccommission.'))
    well_publication_status = models.ForeignKey(WellPublicationStatusCode,
                                                db_column='well_publication_status_code',
                                                on_delete=models.PROTECT,
                                                verbose_name='Well Publication Status',
                                                default='Published')
    licences = models.ManyToManyField('aquifers.WaterRightsLicence')

    street_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Street Address',
        db_comment='Street address for where the property that the well is physically located on.')
    city = models.CharField(
        max_length=50, blank=True, null=True,
        verbose_name='Town/City',
        db_comment='The city or town in which the well is located as part of the well location address.')
    legal_lot = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Lot')
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
                                      on_delete=models.PROTECT, blank=True, null=True,
                                      verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(blank=True, null=True,
                                            verbose_name='Property Identification Description (PID)')
    well_location_description = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Description of Well Location',
        db_comment=('Descriptive details of a well\'s location. E.g. the well is located 20\' south west of '
                    'the house; or the well is located in the pump house near the pond.'))

    construction_start_date = models.DateField(
        null=True, verbose_name='Construction Start Date',
        db_comment='The date when well construction started.')
    construction_end_date = models.DateField(
        null=True, verbose_name='Construction Date',
        db_comment='The date when well construction ended.')

    alteration_start_date = models.DateField(
        null=True, verbose_name='Alteration Start Date',
        db_comment='The date when the alteration on a well started.')
    alteration_end_date = models.DateField(
        null=True, verbose_name='Alteration Date',
        db_comment='The date when the alteration on a well was ended.')

    decommission_start_date = models.DateField(
        null=True, verbose_name='Decommission Start Date',
        db_comment='The start date of when the well was decommissioned.')
    decommission_end_date = models.DateField(
        null=True, verbose_name='Decommission Date')

    well_identification_plate_attached = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Well Identification Plate Is Attached',
        db_comment=('Description of where the well identification plate has been attached on or near the '
                    'well.'))
    id_plate_attached_by = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Well identification plate attached by')

    # Contains Well Longitude and Latitude in that order,
    # Values are BC Albers. but we are using WGS84 Lat Lon to avoid rounding errors
    geom = models.PointField(
        blank=True, null=True, verbose_name='Geo-referenced Location of the Well', srid=4326)

    ground_elevation = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethodCode,
                                                db_column='ground_elevation_method_code',
                                                on_delete=models.PROTECT, blank=True, null=True,
                                                verbose_name='Elevation Determined By')
    drilling_methods = models.ManyToManyField(DrillingMethodCode, verbose_name='Drilling Methods',
                                              blank=True)
    well_orientation = models.BooleanField(default=True, verbose_name='Orientation of Well', choices=(
        (True, 'vertical'), (False, 'horizontal')))
    well_orientation_status = models.ForeignKey(WellOrientationCode, db_column='well_orientation_code',
                                                on_delete=models.PROTECT, blank=True, null=True,
                                                verbose_name='Well Orientation Code')

    surface_seal_material = models.ForeignKey(SurfaceSealMaterialCode, db_column='surface_seal_material_code',
                                              on_delete=models.PROTECT, blank=True, null=True,
                                              verbose_name='Surface Seal Material')
    surface_seal_depth = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Depth')
    surface_seal_thickness = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Thickness')
    surface_seal_method = models.ForeignKey(SurfaceSealMethodCode, db_column='surface_seal_method_code',
                                            on_delete=models.PROTECT, blank=True, null=True,
                                            verbose_name='Surface Seal Installation Method')
    backfill_type = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Backfill Material Above Surface Seal',
        db_comment=('Indicates the type of backfill material that is placed above the surface seal'
                    ' during the construction or alteration of well.'))
    backfill_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth',
        db_comment='The depth in feet of any backfill placed above the surface seal of a well.')

    liner_material = models.ForeignKey(LinerMaterialCode, db_column='liner_material_code',
                                       on_delete=models.PROTECT, blank=True, null=True,
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
                                             on_delete=models.PROTECT, blank=True, null=True,
                                             verbose_name='Intake Method')
    screen_type = models.ForeignKey(ScreenTypeCode, db_column='screen_type_code',
                                    on_delete=models.PROTECT, blank=True, null=True, verbose_name='Type')
    screen_material = models.ForeignKey(ScreenMaterialCode, db_column='screen_material_code',
                                        on_delete=models.PROTECT, blank=True, null=True,
                                        verbose_name='Material')
    other_screen_material = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpeningCode, db_column='screen_opening_code',
                                       on_delete=models.PROTECT, blank=True, null=True,
                                       verbose_name='Opening')
    screen_bottom = models.ForeignKey(ScreenBottomCode, db_column='screen_bottom_code',
                                      on_delete=models.PROTECT, blank=True, null=True, verbose_name='Bottom')
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
                                             on_delete=models.PROTECT, blank=True, null=True,
                                             verbose_name='Filter Pack Material')
    filter_pack_material_size = models.ForeignKey(FilterPackMaterialSizeCode,
                                                  db_column='filter_pack_material_size_code',
                                                  on_delete=models.PROTECT, blank=True, null=True,
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
        db_comment=('Measurement of the artesian well\'s water flow that occurs naturally due to inherent'
                    ' water pressure in the well. Pressure within the aquifer forces the groundwater to rise'
                    ' above the land surface naturally without using a pump. Flowing artesian wells can flow'
                    ' on an intermittent or continuous basis. Measured in US Gallons/minute.'))
    artesian_pressure = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure',
        db_comment=('Pressure of the water coming out of an artesian well as measured at the time of '
                    'construction. Measured in PSI (pounds per square inch).'))
    artesian_pressure_head = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure head',
        db_comment=('Pressure of the water coming out of an artesian well as measured at the time of '
                    'construction. Measured in ft agl (feet above ground level).'))
    artesian_conditions = models.BooleanField(default=False, verbose_name='Artesian Conditions',
                                              db_comment=('Artesian conditions arise when there is a movement of '
                                                          'groundwater from a recharge area under a confining '
                                                          'formation to a point of discharge at a lower elevation. '
                                                          'An example of this is a natural spring, or in the '
                                                          'example of the drilling industry, a flowing water well.'))
    well_cap_type = models.CharField(
        max_length=40, blank=True, null=True, verbose_name='Well Cap')
    well_disinfected = models.BooleanField(
        default=False, verbose_name='Well Disinfected', choices=((False, 'No'), (True, 'Yes')))
    well_disinfected_status = models.ForeignKey(WellDisinfectedCode, db_column='well_disinfected_code',
                                                on_delete=models.PROTECT, blank=True, null=True,
                                                verbose_name='Well Disinfected Code')

    comments = models.CharField(
        max_length=3000, blank=True, null=True,
        db_comment=('Free form text used by the user (driller or staff) to include comments for the well.'
                    ' Investiate how staff/developer comments are put in here from activity submission.'))
    internal_comments = models.CharField(
        max_length=3000, blank=True, null=True)

    alternative_specs_submitted = models.BooleanField(
        default=False,
        verbose_name='Alternative specs submitted (if required)',
        choices=((False, 'No'), (True, 'Yes')),
        db_comment=('Indicates if an alternative specification was used for siting of a water supply'
                    ' well, or a permanent dewatering well, or for the method used for decommissioning a'
                    ' well.'))
    
    technical_report = models.BooleanField(default=False, verbose_name='Technical Report',
                                          db_comment=('Highlights the existence of a technical assessment '
                                                      'or Environmental Flow Needs report.'))
    
    drinking_water_protection_area_ind = models.BooleanField(
        default=False,
        verbose_name='Drinking Water Protection Area',
        choices=((False, 'No'), (True, 'Yes')),
        db_comment=('Indicate if a well is in a delineated capture zone for drinking water.'))

    well_yield_unit = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.PROTECT, blank=True, null=True)
    # want to be integer in future
    diameter = models.CharField(max_length=9, blank=True)

    observation_well_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Observation Well Number",
        db_comment=('A unique number assigned to a well that has been included as part '
                    'of the Provincial Groundwater Observation Well Network, e.g., 406.'))

    observation_well_status = models.ForeignKey(
        ObsWellStatusCode, db_column='obs_well_status_code', blank=True, null=True,
        verbose_name="Observation Well Status", on_delete=models.PROTECT,
        db_comment=('Status of an observation well within the Provincial Groundwater Observation Well '
                    'Network, i.e. Active (a well that is currently being used to collect '
                    'groundwater information), Inactive (a well that is no longer being used to '
                    'collect groundwater information).'))

    ems = models.CharField(max_length=10, blank=True, null=True,
                           verbose_name="Environmental Monitoring System (EMS) ID")

    utm_zone_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Zone")
    utm_northing = models.IntegerField(
        blank=True, null=True, verbose_name="UTM Northing")
    utm_easting = models.IntegerField(
        blank=True, null=True, verbose_name="UTM Easting")
    coordinate_acquisition_code = models.ForeignKey(
        CoordinateAcquisitionCode, default='H', blank=True, null=True, verbose_name="Location Accuracy Code",
        db_column='coordinate_acquisition_code', on_delete=models.PROTECT,
        db_comment=('Codes for the accuracy of the coordinate position, which is best estimated based on'
                    ' the information provided by the data submitter and analysis done by staff. E.g. A,'
                    ' B, C.'))
    bcgs_id = models.ForeignKey(BCGS_Numbers, db_column='bcgs_id', on_delete=models.PROTECT, blank=True,
                                null=True, verbose_name="BCGS Mapsheet Number")

    decommission_reason = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Reason for Decommission")
    decommission_method = models.ForeignKey(
        DecommissionMethodCode, db_column='decommission_method_code', blank=True, null="True",
        verbose_name="Method of Decommission", on_delete=models.PROTECT,
        db_comment='Valid code for the method used to fill the well to close it permanently.')
    decommission_sealant_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Decommission Sealant Material")
    decommission_backfill_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Decommission Backfill Material")
    decommission_details = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Decommission Details")
    aquifer = models.ForeignKey(
        'aquifers.Aquifer', db_column='aquifer_id', on_delete=models.PROTECT, blank=True,
        null=True, verbose_name='Aquifer ID Number',
        db_comment=('System generated unique sequential number assigned to each mapped aquifer. The'
                    ' aquifer_id identifies which aquifer a well is in. An aquifer can have multiple'
                    ' wells, while a single well can only be in one aquifer.'))

    person_responsible = models.ForeignKey('registries.Person', db_column='person_responsible_guid',
                                           on_delete=models.PROTECT,
                                           verbose_name='Person Responsible for Drilling',
                                           null=True, blank=True)
    company_of_person_responsible = models.ForeignKey(
        'registries.Organization', db_column='org_of_person_responsible_guid', on_delete=models.PROTECT,
        verbose_name='Company of person responsible for drilling', null=True, blank=True)
    driller_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Name of Person Who Did the Work')
    consultant_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Consultant Name',
        db_comment=('Name of consultant (person) that was involved in the construction, alteration, or'
                    ' decommision of a well.'))
    consultant_company = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Consultant Company',
        db_comment=('Name of consultant company that was involved in the construction, alteration, or'
                    ' decommision of a well.'))

    # Aquifer related data
    aquifer_vulnerability_index = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='AVI',
        db_comment=('Valid codes that Indicate the aquifer’s relative intrinsic vulnerability to impacts'
                    ' from human activities at the land surface. Vulnerability is based on: the type,'
                    ' thickness, and extent of geologic materials above the aquifer, depth to water'
                    ' table (or to top of confined aquifer), and type of aquifer materials. E.g. H, L, M'))
    storativity = models.DecimalField(
        max_digits=8, decimal_places=7, blank=True, null=True, verbose_name='Storativity')
    transmissivity = models.DecimalField(
        max_digits=30, decimal_places=10, blank=True, null=True, verbose_name='Transmissivity')
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
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Analytic Solution Type',
        db_comment='Mathematical formulation used to estimate hydraulic parameters.')
    boundary_effect = models.ForeignKey(BoundaryEffectCode, db_column='boundary_effect_code',
                                        on_delete=models.PROTECT, blank=True, null=True,
                                        verbose_name='Boundary Effect',
                                        db_comment='Valid codes for the boundaries observed in '
                                                   'pumping test analysis. i.e. CH, NF.')
    aquifer_lithology = models.ForeignKey(
        AquiferLithologyCode, db_column='aquifer_lithology_code', blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name='Aquifer Lithology',
        db_comment=('Valid codes for the type of material an aquifer consists of. i.e., Unconsolidated, '
                    'Bedrock, Unknown.'))
    # Production data related data
    yield_estimation_method = models.ForeignKey(
        YieldEstimationMethodCode, db_column='yield_estimation_method_code',
        on_delete=models.PROTECT, blank=True, null=True,
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
    # QaQc Fields for internal use
    geocode_distance = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2, verbose_name='Geocode Distance',
        db_comment='Distance calculated during geocoding process.')
    distance_to_pid = models.DecimalField(
        null=True, blank=True, max_digits=12, decimal_places=2, verbose_name='Distance to PID',
        db_comment='Distance to the Property Identification Description.')
    score_address = models.DecimalField(
        null=True, blank=True, max_digits=7, decimal_places=2, verbose_name='Score for Address',
        db_comment='Score representing the accuracy or confidence of the address geocoding.')
    score_city = models.DecimalField(
        null=True, blank=True, max_digits=7, decimal_places=2, verbose_name='Score for City',
        db_comment='Score representing the accuracy or confidence of the city geocoding.')
    cross_referenced = models.BooleanField(
        default=False, verbose_name='Cross Referenced',
        db_comment='Indicates if the record has been cross-referenced by an internal team member.')
    cross_referenced_date = models.DateTimeField(
        null=True, verbose_name='Cross Referenced Date',
        db_comment='The date when a well was cross referenced by an internal team member.')
    cross_referenced_by = models.CharField(
        max_length=100, blank=True, null=True, 
        verbose_name="Internal team member who cross referenced well.")
    natural_resource_region = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Natural Resource Region",
        db_comment='The Natural Resource Region the well is located within.')

    class Meta:
        db_table = 'well'
        verbose_name = 'A well record'

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

    @property
    def licenced_status(self):
        return LicencedStatusCode.objects.get(licenced_status_code='LICENSED') if self.licences.all().exists() \
            else LicencedStatusCode.objects.get(licenced_status_code='UNLICENSED')

    @property
    def latitude(self):
        if self.geom:
            return self.geom.y
        else:
            return None

    @property
    def longitude(self):
        if self.geom:
            return self.geom.x
        else:
            return None

    db_table_comment = ('Describes how a well was constructed, altered, decomissioned over time. Includes '
                        'information related to who owns the well, location of well, the lithologic '
                        'description as well as other information related to the construction of the well.')

    db_column_supplemental_comments = {
        "alternative_specs_submitted":"Indicates if an alternative specification was used for siting of a water supply well or a permanent dewatering well, or if an alternative specification was used for decommissioning a well.",
        "technical_report":"Highlights the existence of a technical assessment or Environmental Flow Needs report.",
        "drinking_water_protection_area_ind": "Indicate if a well is in a delineated capture zone for drinking water.",
        "aquifer_id":"System generated sequential number assigned to each aquifer. It is widely used by groundwater staff as it is the only consistent unique identifier for a mapped aquifer. It is also commonly referred to as Aquifer Number.",
        "artesian_flow":"Measurement of the artesian well's water flow that occurs naturally due to inherent water pressure in the well. Pressure within the aquifer forces the groundwater to rise above the land surface naturally without using a pump. Flowing artesian wells can flow on an intermittent or continuous basis. Recorded in US Gallons Per Minute.",
        "artesian_pressure":"Pressure of the water coming out of an artesian well as measured at the time of construction. Measured in PSI (pounds per square inch).",
        "artesian_pressure_head":"Pressure of the water coming out of an artesian well as measured at the time of construction. Measured in ft agl (feet above ground level).",
        "artesian_conditions":"Artesian conditions arise when there is a movement of groundwater from a recharge area under a confining formation to a point of discharge at a lower elevation. An example of this is a natural spring, or in the example of the drilling industry, a flowing water well.",
        "bcgs_id":"TO BE DELETED?",
        "boundary_effect_code":"Valid codes for the boundaries observed in pumping test analysis. i.e. CH, NF.",
        "decommission_backfill_material":"Backfill material used to decommission a well.  ",
        "decommission_details":"Information about the decommissioning of a well as provided by the driller.",
        "decommission_end_date":"The end date of when the decommissioning of the well was completed.",
        "decommission_method_code":"Valid code for the method used to fill the well to decommission it permanently.",
        "decommission_reason":"The reason why the well was decomssioned as provided by the driller.",
        "decommission_sealant_material":"Describes the sealing material or a mixture of the sealing material used to decommission a well.",
        "decommission_start_date":"The start date of when the decommissioning of the well began.",
        "development_hours":"Total hours devoted to developing as well ('develop' in relation to a well, means remove from an aquifer the fine sediment and other organic or inorganic material that immediately surrounds the well screen, the drill hole or the intake area at the bottom of the well)",
        "development_notes":"Information about the  development of the well.",
        "drawdown":"Drawdown is the drop in water level when water is being pumped. ",
        "ems":"Unique ID assigned through the Environmental Monitoring System (EMS) that relates to water quality data within the EMS application.",
        "filter_pack_from":"The starting depth in feet below ground level at which the filter pack was placed.",
        "filter_pack_material_code":"Codes for the materials used in the filter pack, which are placed in the annulus of the well between the borehole wall and the well screen, and are used to settle-out fine grained particles that may otherwise enter the well. I.e. Fine gravel, very course sand, very fine gravel, other",
        "filter_pack_material_size_code":"Codes for the sizes of the material used in the well filter pack. E.g. 1.0 - 2.0 mm, 2.0 - 4.0 mm, 4.0 - 8.0 mm.",
        "filter_pack_thickness":"The thickness in inches of the filter pack material used for a well.",
        "filter_pack_to":"The end depth in feet below ground level at which the filter pack was placed.",
        "final_casing_stick_up":"The length in inches of the production casing in the well that is above the surface of the ground adjacent to the well, or the floor of the well sump, pump house or well pit.",
        "finished_well_depth":"The depth at which the well was 'finished'. It can be shallower than the total well depth which is the total depth drilled. Recorded in feet below ground level.",
        "geom":"Estimated point location of the well.  All UTM coordinates are converted to this geom column for storage and display.   The geometry of the well should be considered aong with the coordinate acquisition code to get the estimated accuracy of the location.",
        "ground_elevation":"The elevation above sea-level of the ground surface at the well, measured in feet.",
        "ground_elevation_method_code":"Code for method used to determine the ground elevation of a well. E.g. GPS, Altimeter, Differential GPS, Level, 1:50,000 map, 1:20,000 map.",
        "hydraulic_conductivity":"The ability of the rock or unconsolidated material to transmit water.",
        "hydro_fracturing_performed":"Indicates if high pressure water was injected into the well to help break apart the bedrock in order to get more water out of the well.",
        "hydro_fracturing_yield_increase":"How much the well yeild increases once hydro fracturing was performed, recorded in US gallons per minute.",
        "id_plate_attached_by":"The person who attached the id plate to the well.",
        "identification_plate_number":"Steel plate with a unique number that is attached to wells as required wells under the Groundwater Protection Regulationsuch as water supply wells, recharge or injection wells made by drilling or boring, and permanent dewatering wells.",
        "intended_water_use_code":"The intended use of the water in a water supply well as reported by the driller at time of work completion on the well. E.g,  DOM, IRR, DWS, COM, UNK, OTHER",
        "internal_comments":"Staff only comments and information related to the well, and for internal use only, not to be made public.",
        "land_district_code":"Codes used to identify legal land district used to help identify the property where the well is located. E.g. Alberni, Barclay, Cariboo.",
        "legal_pid":"A Parcel Identifier or PID is a nine-digit number that uniquely identifies a parcel in the land title register of in BC. The Registrar of Land Titles assigns PID numbers to parcels for which a title is being entered in the land title register as a registered title. The Land Title Act refers to the PID as “the permanent parcel identifier”.",
        "liner_diameter":"Diameter of the liner placed inside the well.  Measured in inches.",
        "liner_from":"Depth below ground level at which the liner starts inside the well. Measured in feet.",
        "liner_material_code":"Code that describes the material noted for lithology. E.g. Rock, Clay, Sand, Unspecified,",
        "liner_thickness":"Thickness of the liner inside the well. Measured in inches.",
        "liner_to":"Depth below ground level at which the liner ends inside the well. Measured in feet.",
        "other_screen_bottom":"Describes the type of bottom installed on a well screen when the bottom type is different from all the types in the screen bottom drop down list and the data submitter picks 'Other ' from the list.",
        "other_screen_material":"Describes the material that makes up the screen on a well when the material is different from all the drop down options and the data submitter picks 'Other ' from the list.",
        "owner_city":"City where the owner of the well resides.",
        "owner_email":"Email address of the well owner, not to be published to the public. ",
        "owner_full_name":"First name and last name of the well owner.  ",
        "owner_mailing_address":"Street name and number of the well owner.",
        "owner_postal_code":"Postal code of the well owner attached to the owner mailing address.",
        "owner_tel":"Telephone number for the well owner, not to be published to the public.",
        "province_state_code":"Province or state code used for the mailing address for the company",
        "recommended_pump_depth":"Depth of the a pump placed within the well, as recommended by the well driller or well pump installer, measured in feet below depth of the top of the production casing.",
        "recommended_pump_rate":"The rate at which to withdraw water from the well as recommended by the well driller or well pump installer, measured in US gallons per minute.",
        "screen_bottom_code":"Valid categories used to identify the type of bottom on a well screen. It provides for a standard commonly understood code and description for screen bottoms. Some examples include: Bail, Plate, Plug. 'Other' can also be specified.",
        "screen_information":"Information about the screen that is not captured elsewhere, as provided by the well driller.",
        "screen_intake_method_code":"Valid categories used to identify the type of intake mechanism for a well screen. It provides for a standard commonly understood code and description for screen intake codes. Some examples include: Open bottom, Screen, Uncased hole.",
        "screen_material_code":"Describes the different materials that makes up the screen on a well. E.g. Plastic, Stainless Steel, Other.",
        "screen_opening_code":"Valid categories used to identify the type of opening on a well screen. It provides for a standard commonly understood code and description for screen openings. E.g. Continuous Slot, Perforated Pipe, Slotted.",
        "screen_type_code":"Valid categories for the type of well screen installed in a well. i.e. Pipe size, Telescope, Other",
        "specific_storage":"The volume of water that the aquifer releases from storage, per volume per aquifer of hydraulic unit head.",
        "static_level_before_test":"Resting static water level prior to pumping, measured in feet below ground level or feet below top of the production casing.",
        "storativity":"The storativity (or storage coefficient ) is the amount of water stored or released per unit area of aquifer given unit change in head.  ",
        "surface_seal_depth":"The depth at the bottom of the surface seal, measured in feet.",
        "surface_seal_material_code":"Valid materials used for creating the surface seal for a well. A surface seal is a plug that prevents surface runoff from getting into the aquifer or well and contaminating the water. E.g. Bentonite clay, Concrete grout, Sand cement grout, Other.",
        "surface_seal_method_code":"Valid methods used to create the surface seal for a well. i.e. Poured, Pumped, Other.",
        "surface_seal_thickness":"The thickness of the surface sealant placed in the annular space around the outside of the outermost well casing, measured in inches.",
        "total_depth_drilled":"Total depth drilled when constructing or altering a well.  It may be different from the finished well depth which can be shallower than the total well depth.  Measured in feet below ground level.",
        "transmissivity":"Transmissivity is the rate of flow under a unit hydraulic gradient through a unit width of aquifer of thickness ",
        "water_quality_colour":"Valid codes for the colour of the water as recorded at time of work. E.g. Orange, Black, Clear, Other",
        "water_quality_odour":"Description of the odour of the water as recorded at time of work.",
        "well_cap_type":"Description of the type of well cap used on the well.",
        "well_class_code":"Valid classifications as defined in the Groundwater Protection Regulation of the Water Sustainability Act. i.e. Water Supply, Monitoring, Recharge, Injection, Dewatering, Drainage, Remediation, Geotechnical, Closed-loop geoexchange.",
        "well_disinfected":"Indicates if the well was disinfected after the well construction or alteration was completed.",
        "well_orientation":"Describes the physical orientation of a well as being either horizontal or vertical.",
        "well_publication_status_code":"Codes that describe if a well record is published for public consumption or unpublished and not available to the public due to data duplication and other data quality issues.",
        "well_tag_number":"System generated sequential number assigned to each well. It is widely used by groundwater staff as it is the only consistent unique identifier for each well. It is different from a well ID plate number.",
        "well_yield_unit_code":"Codes for the unit of measure that was used for the well yield. All codes except the U.S. Gallons per Minute has been retired as all data from April 2019 will be reported in U.S. Gallons per Minute. E.g of other codes that have been used in the past are Gallons per Minute (U.S./Imperial), Dry Hole, Unknown Yield.",
        "yield_estimation_duration":"Total length of time that a well yield test took to complete, measured in hours.",
        "yield_estimation_method_code":"Codes for the valid methods that can be used to estimate the well yield. E.g. Air Lifting, Bailing, Pumping, Other.",
        "yield_estimation_rate":"Rate at which the well water was pumped during the well yield test, measured in US gallons per minute.",
    }


class CasingMaterialCode(CodeTableModel):
    """
     The material used for casing a well, e.g., Cement, Plastic, Steel.
    """
    code = models.CharField(primary_key=True, max_length=10,
                            editable=False, db_column='casing_material_code')
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
    code = models.CharField(primary_key=True, max_length=10,
                            editable=False, db_column='casing_code')
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'casing_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Describes the casing component (piping or tubing installed in a well) as either '
                        'production (inner tube), surface (outer tube), or open hole.')

    def __str__(self):
        return self.description


# TODO: This class needs to be moved to submissions.models (in order to do that, the fk references for a
# number of other models needs to be updated)
@reversion.register()
class ActivitySubmission(AuditModelStructure):
    """
    Activity information on a Well submitted by a user.

    Note on db_comments:  db_comment properties on model columns are
    overriden by the db_column_supplemental_comments provided below.
    db_column_supplemental_comments provides an easier way for the DA to add/update
    comments in bulk.
    """
    filing_number = models.AutoField(primary_key=True)
    activity_submission_guid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.PROTECT, blank=True, null=True,
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    well_activity_type = models.ForeignKey(
        'submissions.WellActivityCode', db_column='well_activity_code', on_delete=models.PROTECT,
        null=True, verbose_name='Type of Work')
    well_status = models.ForeignKey(
        WellStatusCode, db_column='well_status_code',
        on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Well Status',
        db_comment=('Status of a well indicates whether the report relates to the construction,'
                    ' alteration, or decommission of the well; e.g., Construction, Alteration,'
                    ' Abandoned, Deccommission.'))
    well_publication_status = models.ForeignKey(
        WellPublicationStatusCode, db_column='well_publication_status_code',
        on_delete=models.PROTECT, verbose_name='Well Publication Status',
        null=True, default='Published')
    well_class = models.ForeignKey(
        WellClassCode, blank=True, null=True, db_column='well_class_code',
        on_delete=models.PROTECT, verbose_name='Well Class',
        db_comment=('Valid classifications as defined in the Groundwater Protection Regulation of the'
                    ' Water Act. i.e. Water Supply, Monitoring, Recharge, Injection, Dewatering,'
                    ' Drainage, Remediation, Geotechnical, Closed-loop geoexchange.'))
    well_subclass = models.ForeignKey(WellSubclassCode, db_column='well_subclass_guid',
                                      on_delete=models.PROTECT, blank=True, null=True,
                                      verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(
        IntendedWaterUseCode, db_column='intended_water_use_code',
        on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Intended Water Use',
        db_comment=('The intended use of the water in a water supply well as reported by the driller at'
                    ' time of work completion on the well. E.g DOM, IRR, DWS, COM'))
    # Driller responsible should be a required field on all submissions, but for legacy well
    # information this may not be available, so we can't enforce this on a database level.
    person_responsible = models.ForeignKey('registries.Person', db_column='person_responsible_guid',
                                           on_delete=models.PROTECT,
                                           verbose_name='Person Responsible for Drilling',
                                           blank=True, null=True)
    company_of_person_responsible = models.ForeignKey(
        'registries.Organization', db_column='org_of_person_responsible_guid', on_delete=models.PROTECT,
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

    owner_full_name = models.CharField(
        max_length=200, verbose_name='Owner Name', blank=True, null=True)
    owner_mailing_address = models.CharField(
        max_length=100, verbose_name='Mailing Address', blank=True, null=True)
    owner_city = models.CharField(
        max_length=100, verbose_name='Town/City', blank=True, null=True)
    owner_province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.PROTECT, verbose_name='Province',
        blank=True, null=True)
    owner_postal_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Postal Code')
    owner_email = models.EmailField(
        null=True, blank=True, verbose_name='Email address')
    owner_tel = models.CharField(
        null=True, blank=True, max_length=25, verbose_name='Telephone number')

    street_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, null=True,
                            verbose_name='Town/City')
    legal_lot = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Lot')
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
                                      on_delete=models.PROTECT, blank=True, null=True,
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
        CoordinateAcquisitionCode, blank=True, null=True, verbose_name="Location Accuracy Code",
        db_column='coordinate_acquisition_code', on_delete=models.PROTECT,
        db_comment=('Codes for the accuracy of the coordinate position, which is best estimated based on'
                    ' the information provided by the data submitter and analysis done by staff. E.g. A,'
                    ' B, C.'))
    ground_elevation = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethodCode,
                                                db_column='ground_elevation_method_code',
                                                on_delete=models.PROTECT, blank=True, null=True,
                                                verbose_name='Elevation Determined By')
    drilling_methods = models.ManyToManyField(DrillingMethodCode, verbose_name='Drilling Methods',
                                              blank=True)
    well_orientation = models.BooleanField(null=True, verbose_name='Orientation of Well', choices=(
        (True, 'vertical'), (False, 'horizontal')))
    well_orientation_status = models.ForeignKey(WellOrientationCode, db_column='well_orientation_code',
                                                on_delete=models.PROTECT, blank=True, null=True,
                                                verbose_name='Well Orientation Code')

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
                                              on_delete=models.PROTECT, blank=True, null=True,
                                              verbose_name='Surface Seal Material')
    surface_seal_depth = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Depth')
    surface_seal_thickness = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                 verbose_name='Surface Seal Thickness',
                                                 validators=[MinValueValidator(Decimal('0.00'))])
    surface_seal_method = models.ForeignKey(SurfaceSealMethodCode, db_column='surface_seal_method_code',
                                            on_delete=models.PROTECT, blank=True, null=True,
                                            verbose_name='Surface Seal Installation Method')

    backfill_above_surface_seal = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Backfill Material Above Surface Seal')
    backfill_above_surface_seal_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')
    backfill_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth',
        db_comment='The depth in feet of any backfill placed above the surface seal of a well.')

    backfill_type = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Backfill Material Above Surface Seal',
        db_comment=('Indicates the type of backfill material that is placed above the surface seal'
                    ' during the construction or alteration of well.'))
    liner_material = models.ForeignKey(LinerMaterialCode, db_column='liner_material_code',
                                       on_delete=models.PROTECT, blank=True, null=True,
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
                                             on_delete=models.PROTECT, blank=True, null=True,
                                             verbose_name='Intake')
    screen_type = models.ForeignKey(ScreenTypeCode, db_column='screen_type_code',
                                    on_delete=models.PROTECT, blank=True, null=True, verbose_name='Type')
    screen_material = models.ForeignKey(ScreenMaterialCode, db_column='screen_material_code',
                                        on_delete=models.PROTECT, blank=True, null=True,
                                        verbose_name='Material')
    other_screen_material = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpeningCode, db_column='screen_opening_code',
                                       on_delete=models.PROTECT, blank=True, null=True,
                                       verbose_name='Opening')
    screen_bottom = models.ForeignKey(ScreenBottomCode, db_column='screen_bottom_code',
                                      on_delete=models.PROTECT, blank=True, null=True,
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
                                             on_delete=models.PROTECT, blank=True, null=True,
                                             verbose_name='Filter Pack Material')
    filter_pack_material_size = models.ForeignKey(FilterPackMaterialSizeCode,
                                                  db_column='filter_pack_material_size_code',
                                                  on_delete=models.PROTECT, blank=True, null=True,
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
        db_comment=('Measurement of the artesian well\'s water flow that occurs naturally due to'
                    ' inherent water pressure in the well. Pressure within the aquifer forces the'
                    ' groundwater to rise above the land surface naturally without using a pump. Flowing'
                    ' artesian wells can flow on an intermittent or continuous basis. Measured in US'
                    ' Gallons/minute.'))
    artesian_pressure = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure',
        db_comment=('Pressure of the water coming out of an artesian well as measured at the time of'
                    ' construction. Measured in PSI (pounds per square inch).'))
    artesian_pressure_head = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure head',
        db_comment=('Pressure of the water coming out of an artesian well as measured at the time of '
                    'construction. Measured in ft agl (feet above ground level).'))
    artesian_conditions = models.BooleanField(null=True, verbose_name='Artesian Conditions',
                                              db_comment=('Artesian conditions arise when there is a movement of '
                                                          'groundwater from a recharge area under a confining '
                                                          'formation to a point of discharge at a lower elevation. '
                                                          'An example of this is a natural spring, or in the '
                                                          'example of the drilling industry, a flowing water well.'))
    well_cap_type = models.CharField(
        max_length=40, blank=True, null=True, verbose_name='Well Cap Type')
    well_disinfected = models.BooleanField(null=True, verbose_name='Well Disinfected?',
                                           choices=((False, 'No'), (True, 'Yes')))
    well_disinfected_status = models.ForeignKey(WellDisinfectedCode, db_column='well_disinfected_code',
                                                on_delete=models.PROTECT, blank=True, null=True,
                                                verbose_name='Well Disinfected Code')

    comments = models.CharField(max_length=3000, blank=True, null=True)
    internal_comments = models.CharField(
        max_length=3000, blank=True, null=True)

    alternative_specs_submitted = models.BooleanField(
        null=True,
        verbose_name='Alternative specs submitted (if required)', choices=((False, 'No'), (True, 'Yes')))

    technical_report = models.BooleanField(default=False, verbose_name='Technical Report',
                                          db_comment=('Highlights the existence of a technical assessment '
                                                      'or Environmental Flow Needs report.'))
    
    drinking_water_protection_area_ind = models.BooleanField(
        default=False,
        verbose_name='Drinking Water Protection Area',
        choices=((False, 'No'), (True, 'Yes')),
        db_comment=('Indicate if a well is in a delineated capture zone for drinking water.'))

    well_yield_unit = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.PROTECT, blank=True, null=True)
    # want to be integer in future
    diameter = models.CharField(max_length=9, blank=True, null=True)
    ems = models.CharField(max_length=30, blank=True, null=True)

    # Observation well details
    observation_well_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Observation Well Number",
        db_comment=('A unique number assigned to a well that has been included as part '
                    'of the Provincial Groundwater Observation Well Network.'))

    observation_well_status = models.ForeignKey(
        ObsWellStatusCode, db_column='obs_well_status_code', blank=True, null=True,
        verbose_name="Observation Well Status", on_delete=models.PROTECT,
        db_comment=('Status of an observation well within the Provincial Groundwater Observation Well '
                    'Network. I.e. Active is a well that is currently being used to collect groundwater '
                    'information, and inactive is a well that is no longer being used to collect '
                    'groundwater information.'))

    # aquifer association
    aquifer = models.ForeignKey(
        'aquifers.Aquifer', db_column='aquifer_id', on_delete=models.PROTECT, blank=True,
        null=True, verbose_name='Aquifer ID Number',
        db_comment=('System generated unique sequential number assigned to each mapped aquifer. The'
                    ' aquifer_id identifies which aquifer a well is in. An aquifer can have multiple'
                    ' wells, while a single well can only be in one aquifer.'))

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
        max_digits=30, decimal_places=10, blank=True, null=True, verbose_name='Transmissivity')
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
    boundary_effect = models.ForeignKey(BoundaryEffectCode, db_column='boundary_effect_code',
                                        on_delete=models.PROTECT, blank=True, null=True,
                                        verbose_name='Boundary Effect',
                                        db_comment='Valid codes for the boundaries observed in '
                                                   'pumping test analysis. i.e. CH, NF.')
    aquifer_lithology = models.ForeignKey(
        AquiferLithologyCode, db_column='aquifer_lithology_code', blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name="Aquifer Lithology")

    # Production data related data
    yield_estimation_method = models.ForeignKey(
        YieldEstimationMethodCode, db_column='yield_estimation_method_code',
        on_delete=models.PROTECT, blank=True, null=True,
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
        null=True,
        verbose_name='Hydro-fracturing Performed?',
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
    db_column_supplemental_comments = {
        "alternative_specs_submitted":"Indicates if an alternative specification was used for siting of a water supply well, or a permanent dewatering well, or for the method used for decommissioning a well.",
        "technical_report":"Highlights the existence of a technical assessment or Environmental Flow Needs report.",
        "drinking_water_protection_area_ind": "Indicate if a well is in a delineated capture zone for drinking water.",
        "analytic_solution_type":"Mathematical formulation used to estimate hydraulic parameters.",
        "aquifer_id":"System generated sequential number assigned to each aquifer. It is widely used by groundwater staff as it is the only consistent unique identifier for a mapped aquifer. It is also commonly referred to as Aquifer Number.",
        "artesian_conditions": "Artesian conditions arise when there is a movement of groundwater from a recharge area under a confining formation to a point of discharge at a lower elevation. An example of this is a natural spring, or in the example of the drilling industry, a flowing water well.",
        "aquifer_lithology_code":"Valid codes for the type of material an aquifer consists of. i.e., Unconsolidated, Bedrock, Unknown.",
        "aquifer_vulnerability_index":"Valid codes that Indicate the aquifer’s relative intrinsic vulnerability to impacts from human activities at the land surface. Vulnerability is based on: the type, thickness, and extent of geologic materials above the aquifer, depth to water table (or to top of confined aquifer), and type of aquifer materials. E.g. H, L, M",
        "bedrock_depth":"Depth below ground level at which bedrock starts, measured in feet.",
        "boundary_effect_code":"Valid codes for the boundaries observed in pumping test analysis. i.e. CH, NF.",
        "city":"The city or town in which the well is located as part of the well location address.",
        "comments":"Free form text used by the user (driller or staff) to include comments for the well. ",
        "consultant_company":"Name of consultant company that was involved in the construction, alteration, or decommision of a well.",
        "consultant_name":"Name of consultant (person) that was involved in the construction, alteration, or decommision of a well.",
        "decommission_backfill_material":"Backfill material used to decommission a well.  ",
        "decommission_details":"Information about the decommissioning of a well as provided by the driller.",
        "decommission_method_code":"Valid code for the method used to fill the well to close it permanently.",
        "decommission_reason":"The reason why the well was decomssioned as provided by the driller.",
        "decommission_sealant_material":"Describes the sealing material or a mixture of the sealing material used to decommission a well.",
        "development_hours":"Total hours devoted to developing as well ('develop' in relation to a well, means remove from an aquifer the fine sediment and other organic or inorganic material that immediately surrounds the well screen, the drill hole or the intake area at the bottom of the well)",
        "development_notes":"Information about the  development of the well.",
        "drawdown":"Drawdown is the drop in water level when water is being pumped. ",
        "filter_pack_from":"The starting depth below ground level at which the filter pack was placed.",
        "filter_pack_material_code":"Codes for the materials used in the filter pack, which are placed in the annulus of the well between the borehole wall and the well screen, and are used to settle-out fine grained particles that may otherwise enter the well. I.e. Fine gravel, very course sand, very fine gravel, other",
        "filter_pack_material_size_code":"Codes for the sizes of the material used to pack a well filter. E.g. 1.0 - 2.0 mm, 2.0 - 4.0 mm, 4.0 - 8.0 mm.",
        "filter_pack_thickness":"The thickness in inches of the filter pack material used for a well.",
        "filter_pack_to":"The end depth below ground level at which the filter pack was placed.",
        "final_casing_stick_up":"The length of the production casing in the well that is above the surface of the ground adjacent to the well, or the floor of the well sump, pump house or well pit.",
        "geom":"Estimated point location of the well.  All UTM coordinates are converted to this geom column for storage and display.   The geometry of the well should be considered aong with the coordinate acquisition code to get the estimated accuracy of the location.",
        "ground_elevation":"The elevation above sea-level at the ground-level of the well, measured in feet.",
        "ground_elevation_method_code":"Code for method used to determine the ground elevation of a well. E.g. GPS, Altimeter, Differential GPS, Level, 1:50,000 map, 1:20,000 map.",
        "hydraulic_conductivity":"The ability of the rock or unconsolidated material to transmit water.",
        "hydro_fracturing_performed":"Indicates if high pressure water was injected into the well to help break apart the bedrock in order to get more water out of the well.",
        "hydro_fracturing_yield_increase":"How much the well yeild increases once hydro fracturing was performed, measured in US gallons per minute.",
        "id_plate_attached_by":"The person who attached the id plate to the well.",
        "intended_water_use_code":"The intended use of the water in a water supply well as reported by the driller at time of work completion on the well. E.g,  DOM, IRR, DWS, COM, UNK, OTHER",
        "internal_comments":"Staff only comments and information related to the well, and for internal use only, not to be made public.",
        "land_district_code":"Codes used to identify legal land district used to help identify the property where the well is located. E.g. Alberni, Barclay, Cariboo.",
        "legal_pid":"A Parcel Identifier or PID is a nine-digit number that uniquely identifies a parcel in the land title register of in BC. The Registrar of Land Titles assigns PID numbers to parcels for which a title is being entered in the land title register as a registered title. The Land Title Act refers to the PID as “the permanent parcel identifier”.",
        "liner_diameter":"Diameter of the liner placed inside the well.  Measured in inches.",
        "liner_from":"Depth below ground level at which the liner starts inside the well. Measured in feet.",
        "liner_material_code":"Code that describes the material noted for lithology. E.g. Rock, Clay, Sand, Unspecified,",
        "liner_thickness":"Thickness of the liner inside the well. Measured in inches.",
        "liner_to":"Depth below ground level at which the liner ends inside the well. Measured in feet.",
        "other_screen_bottom":"Describes the type of bottom installed on a well screen of when the bottom type is different from all the types in the screen bottom drop down list and the data submitter picks 'Other ' from the list.",
        "other_screen_material":"Describes the material that makes up the screen on a well when the material is different from all the drop down options and the data submitter picks 'Other ' from the list.",
        "owner_city":"City where the owner of the well resides.",
        "owner_email":"Email address of the well owner, not to be published to the public. ",
        "owner_full_name":"First name and last name of the well owner.  ",
        "owner_mailing_address":"Street name and number of the well owner.",
        "owner_postal_code":"Postal code of the well owner attached to the owner mailing address.",
        "owner_tel":"Telephone number for the well owner, not to be published to the public.",
        "province_state_code":"Province or state code used for the mailing address for the company",
        "recommended_pump_depth":"Depth of the a pump placed within the well, as recommended by the well driller or pump installer, measured in feet below depth of the production casing.",
        "recommended_pump_rate":"The rate at which to withdraw water from the well as recommended by the well driller or pump installer, measured in US gallons per minute.",
        "screen_bottom_code":"Valid categories used to identify the type of bottom on a well screen. It provides for a standard commonly understood code and description for screen bottoms. Some examples include: Bail, Plate, Plug. 'Other' can also be specified.",
        "screen_information":"Information about the screen that is not captured elsewhere, as provided by the well driller.",
        "screen_intake_method_code":"Valid categories used to identify the type of intake mechanism for a well screen. It provides for a standard commonly understood code and description for screen intake codes. Some examples include: Open bottom, Screen, Uncased hole.",
        "screen_material_code":"Describes the different materials that makes up the screen on a well. E.g. Plastic, Stainless Steel, Other.",
        "screen_opening_code":"Valid categories used to identify the type of opening on a well screen. It provides for a standard commonly understood code and description for screen openings. E.g. Continuous Slot, Perforated Pipe, Slotted.",
        "screen_type_code":"Valid categories for the type of well screen installed in a well. i.e. Pipe size, Telescope, Other",
        "specific_storage":"The volume of water that the aquifer releases from storage, per volume per aquifer of hydraulic unit head.",
        "static_level_before_test":"Resting static water level prior to pumping, measured in feet below ground level.",
        "storativity":"The storativity (or storage coefficient ) is the amount of water stored or released per unit area of aquifer given unit change in head.  ",
        "street_address":"Street address for where the property that the well is physically located on.",
        "surface_seal_depth":"The depth at the bottom of the surface seal, measured in feet.",
        "surface_seal_material_code":"Valid materials used for creating the surface seal for a well. A surface seal is a plug that prevents surface runoff from getting into the aquifer or well and contaminating the water. E.g. Bentonite clay, Concrete grout, Sand cement grout, Other.",
        "surface_seal_method_code":"Valid methods used to create the surface seal for a well. i.e. Poured, Pumped, Other.",
        "surface_seal_thickness":"The thickness of the surface sealant placed in the annular space around the outside of the outermost well casing, measured in inches.",
        "total_depth_drilled":"Total depth of drilling done when constructing or altering a well.  It is different from the finished well depth which can be shallower than the total well depth.  Measured in feet.",
        "transmissivity":"Transmissivity is the rate of flow under a unit hydraulic gradient through a unit width of aquifer of thickness ",
        "water_quality_odour":"Description of the odour of the water as recorded at time of work.",
        "well_cap_type":"Description of the type of well cap used on the well.",
        "well_disinfected":"Indicates if the well was disinfected after the well construction or alteration was completed.",
        "well_orientation":"Describes the physical orientation of a well as being either horizontal or vertical.",
        "well_publication_status_code":"Codes that describe if a well record is published for public consumption or unpublished and not available to the public due to data duplication and other data quality issues.",
        "well_tag_number":"System generated sequential number assigned to each well. It is widely used by groundwater staff as it is the only consistent unique identifier for each well. It is different from a well ID plate number.",
        "well_yield":"An approximate estimate of the capacity of the well to produce groundwater. Estimated by the well driller during construction by conducting a well yield test. Measured in US Gallons/minute.",
        "well_yield_unit_code":"Codes for the unit of measure that was used for the well yield. All codes except the U.S. Gallons per Minute has been retired as all data from April 2019 will be reported in U.S. Gallons per Minute. E.g of other codes that have been used in the past are Gallons per Minute (U.S./Imperial), Dry Hole, Unknown Yield.",
        "yield_estimation_duration":"Total length of time that a well yield test took to complete, measured in hours.",
        "yield_estimation_method_code":"Codes for the valid methods that can be used to estimate the yield of a well. E.g. Air Lifting, Bailing, Pumping, Other.",
        "yield_estimation_rate":"Rate at which the well water was pumped during the well yield test, measured in US gallons per minute.",
    }

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


class FieldsProvided(models.Model):
    """ Fields that were filled out in a submission report or staff edit.
        Not all fields are provided in every report or edit, and this model
        helps track which fields the user intended to update.
    """
    activity_submission = models.OneToOneField(ActivitySubmission, on_delete=models.PROTECT, primary_key=True, db_column="filing_number", related_name="fields_provided")

    well_activity_type = models.BooleanField(default=False)
    well_status = models.BooleanField(default=False)
    well_publication_status = models.BooleanField(default=False)
    well_class = models.BooleanField(default=False)
    well_subclass = models.BooleanField(default=False)
    intended_water_use = models.BooleanField(default=False)
    person_responsible = models.BooleanField(default=False)
    company_of_person_responsible = models.BooleanField(default=False)
    driller_name = models.BooleanField(default=False)
    consultant_name = models.BooleanField(default=False)
    consultant_company = models.BooleanField(default=False)
    work_start_date = models.BooleanField(default=False)
    work_end_date = models.BooleanField(default=False)
    construction_start_date = models.BooleanField(default=False)
    construction_end_date = models.BooleanField(default=False)
    alteration_start_date = models.BooleanField(default=False)
    alteration_end_date = models.BooleanField(default=False)
    decommission_start_date = models.BooleanField(default=False)
    decommission_end_date = models.BooleanField(default=False)
    owner_full_name = models.BooleanField(default=False)
    owner_mailing_address = models.BooleanField(default=False)
    owner_city = models.BooleanField(default=False)
    owner_province_state = models.BooleanField(default=False)
    owner_postal_code = models.BooleanField(default=False)
    owner_email = models.BooleanField(default=False)
    owner_tel = models.BooleanField(default=False)
    street_address = models.BooleanField(default=False)
    city = models.BooleanField(default=False)
    legal_lot = models.BooleanField(default=False)
    legal_plan = models.BooleanField(default=False)
    legal_district_lot = models.BooleanField(default=False)
    legal_block = models.BooleanField(default=False)
    legal_section = models.BooleanField(default=False)
    legal_township = models.BooleanField(default=False)
    legal_range = models.BooleanField(default=False)
    land_district = models.BooleanField(default=False)
    legal_pid = models.BooleanField(default=False)
    well_location_description = models.BooleanField(default=False)
    identification_plate_number = models.BooleanField(default=False)
    well_identification_plate_attached = models.BooleanField(default=False)
    id_plate_attached_by = models.BooleanField(default=False)
    geom = models.BooleanField(default=False)
    coordinate_acquisition_code = models.BooleanField(default=False)
    ground_elevation = models.BooleanField(default=False)
    ground_elevation_method = models.BooleanField(default=False)
    drilling_methods = models.BooleanField(default=False)
    well_orientation = models.BooleanField(default=False)
    well_orientation_status = models.BooleanField(default=False)
    water_supply_system_name = models.BooleanField(default=False)
    water_supply_system_well_name = models.BooleanField(default=False)
    surface_seal_material = models.BooleanField(default=False)
    surface_seal_depth = models.BooleanField(default=False)
    surface_seal_thickness = models.BooleanField(default=False)
    surface_seal_method = models.BooleanField(default=False)
    backfill_above_surface_seal = models.BooleanField(default=False)
    backfill_above_surface_seal_depth = models.BooleanField(default=False)
    backfill_depth = models.BooleanField(default=False)
    backfill_type = models.BooleanField(default=False)
    liner_material = models.BooleanField(default=False)
    liner_diameter = models.BooleanField(default=False)
    liner_thickness = models.BooleanField(default=False)
    liner_from = models.BooleanField(default=False)
    liner_to = models.BooleanField(default=False)
    screen_intake_method = models.BooleanField(default=False)
    screen_type = models.BooleanField(default=False)
    screen_material = models.BooleanField(default=False)
    other_screen_material = models.BooleanField(default=False)
    screen_opening = models.BooleanField(default=False)
    screen_bottom = models.BooleanField(default=False)
    other_screen_bottom = models.BooleanField(default=False)
    screen_information = models.BooleanField(default=False)
    filter_pack_from = models.BooleanField(default=False)
    filter_pack_to = models.BooleanField(default=False)
    filter_pack_thickness = models.BooleanField(default=False)
    filter_pack_material = models.BooleanField(default=False)
    filter_pack_material_size = models.BooleanField(default=False)
    development_methods = models.BooleanField(default=False)
    development_hours = models.BooleanField(default=False)
    development_notes = models.BooleanField(default=False)
    water_quality_characteristics = models.BooleanField(default=False)
    water_quality_colour = models.BooleanField(default=False)
    water_quality_odour = models.BooleanField(default=False)
    total_depth_drilled = models.BooleanField(default=False)
    finished_well_depth = models.BooleanField(default=False)
    final_casing_stick_up = models.BooleanField(default=False)
    bedrock_depth = models.BooleanField(default=False)
    static_water_level = models.BooleanField(default=False)
    well_yield = models.BooleanField(default=False)
    artesian_flow = models.BooleanField(default=False)
    artesian_pressure = models.BooleanField(default=False)
    artesian_pressure_head = models.BooleanField(default=False)
    artesian_conditions = models.BooleanField(default=False)
    well_cap_type = models.BooleanField(default=False)
    well_disinfected = models.BooleanField(default=False)
    well_disinfected_status = models.BooleanField(default=False)
    comments = models.BooleanField(default=False)
    internal_comments = models.BooleanField(default=False)
    alternative_specs_submitted = models.BooleanField(default=False)
    technical_report = models.BooleanField(default=False)
    drinking_water_protection_area_ind = models.BooleanField(default=False)
    well_yield_unit = models.BooleanField(default=False)
    diameter = models.BooleanField(default=False)
    ems = models.BooleanField(default=False)
    observation_well_number = models.BooleanField(default=False)
    observation_well_status = models.BooleanField(default=False)
    aquifer = models.BooleanField(default=False)
    decommission_reason = models.BooleanField(default=False)
    decommission_method = models.BooleanField(default=False)
    decommission_sealant_material = models.BooleanField(default=False)
    decommission_backfill_material = models.BooleanField(default=False)
    decommission_details = models.BooleanField(default=False)
    aquifer_vulnerability_index = models.BooleanField(default=False)
    storativity = models.BooleanField(default=False)
    transmissivity = models.BooleanField(default=False)
    hydraulic_conductivity = models.BooleanField(default=False)
    specific_storage = models.BooleanField(default=False)
    specific_yield = models.BooleanField(default=False)
    testing_method = models.BooleanField(default=False)
    testing_duration = models.BooleanField(default=False)
    analytic_solution_type = models.BooleanField(default=False)
    boundary_effect = models.BooleanField(default=False)
    aquifer_lithology = models.BooleanField(default=False)
    yield_estimation_method = models.BooleanField(default=False)
    yield_estimation_rate = models.BooleanField(default=False)
    yield_estimation_duration = models.BooleanField(default=False)
    static_level_before_test = models.BooleanField(default=False)
    drawdown = models.BooleanField(default=False)
    hydro_fracturing_performed = models.BooleanField(default=False)
    hydro_fracturing_yield_increase = models.BooleanField(default=False)
    recommended_pump_depth = models.BooleanField(default=False)
    recommended_pump_rate = models.BooleanField(default=False)
    lithologydescription_set = models.BooleanField(default=False)
    casing_set = models.BooleanField(default=False)
    aquifer_parameters_set = models.BooleanField(default=False)
    decommission_description_set = models.BooleanField(default=False)
    screen_set = models.BooleanField(default=False)
    linerperforation_set = models.BooleanField(default=False)

    class Meta:
        db_table = 'fields_provided'


class LithologyDescription(AuditModel):
    """
    Lithology information details
    """
    lithology_description_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(
        ActivitySubmission, db_column='filing_number', on_delete=models.PROTECT, blank=True, null=True,
        related_name='lithologydescription_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.PROTECT, blank=True, null=True,
        related_name='lithologydescription_set',
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    start = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='From',
        blank=True, null=True,
        db_column='lithology_from',
        validators=[MinValueValidator(Decimal('0.00'))],
        db_comment=('Depth below ground surface of the start of the lithology material for a particular '
                    'lithology layer, as observed during the construction or alteration of a well, '
                    'measured in feet.'))
    end = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='To',
        db_column='lithology_to',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))],
        db_comment=('Depth below ground surface of the end of the lithology material for a particular '
                    'lithology layer as observed during the construction or alteration of a well, measured '
                    'in feet.'))
    lithology_raw_data = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Raw Data',
        db_comment=('Lithologic material as described verbatim by the driller (not necessarily using '
                    'standardized terms).'))

    lithology_description = models.ForeignKey(
        LithologyDescriptionCode,
        db_column='lithology_description_code',
        on_delete=models.PROTECT, blank=True, null=True,
        verbose_name="Description",
        db_comment=('Standard terms used to characterize the different qualities of lithologic'
                    ' materials. E.g. dry, loose, weathered, soft.'))
    lithology_colour = models.ForeignKey(
        LithologyColourCode, db_column='lithology_colour_code',
        on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Colour',
        db_comment=('Valid options for the colour of the lithologic material identified at time of'
                    ' drilling. E.g. Black, dark, tan, rust-coloured'))
    lithology_hardness = models.ForeignKey(
        LithologyHardnessCode, db_column='lithology_hardness_code',
        on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Hardness',
        db_comment=('The hardness of the material that a well is drilled into (the lithology), e.g. Very'
                    ' hard, Medium, Very Soft.'))
    lithology_material = models.ForeignKey(
        LithologyMaterialCode, db_column='lithology_material_code',
        on_delete=models.PROTECT, blank=True, null=True,
        verbose_name="Material",
        db_comment=('Description of the lithologic material using standardized terms, '
                    'e.g. Rock, Clay, Sand, Unspecified.'))

    water_bearing_estimated_flow = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True, verbose_name='Water Bearing Estimated Flow')
    water_bearing_estimated_flow_units = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Units')
    lithology_observation = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Observations',
        db_comment=('Free form text used by the driller to describe observations made of the well '
                    'lithology including, but not limited to, the lithologic material.'))

    bedrock_material = models.ForeignKey(
        BedrockMaterialCode, db_column='bedrock_material_code',
        on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Bedrock Material',
        db_comment=('Code for the bedrock material encountered during drilling and reported in'
                    ' lithologic description.'))
    bedrock_material_descriptor = models.ForeignKey(
        BedrockMaterialDescriptorCode, db_column='bedrock_material_descriptor_code', on_delete=models.PROTECT,
        blank=True, null=True, verbose_name='Descriptor',
        db_comment=('Code for adjective that describes the characteristics of the bedrock material in'
                    ' more detail.'))
    lithology_structure = models.ForeignKey(LithologyStructureCode, db_column='lithology_structure_code',
                                            on_delete=models.PROTECT, blank=True, null=True,
                                            verbose_name='Bedding')
    lithology_moisture = models.ForeignKey(LithologyMoistureCode, db_column='lithology_moisture_code',
                                           on_delete=models.PROTECT, blank=True, null=True,
                                           verbose_name='Moisture')
    surficial_material = models.ForeignKey(SurficialMaterialCode, db_column='surficial_material_code',
                                           related_name='surficial_material_set', on_delete=models.PROTECT,
                                           blank=True, null=True, verbose_name='Surficial Material')
    secondary_surficial_material = models.ForeignKey(SurficialMaterialCode,
                                                     db_column='secondary_surficial_material_code',
                                                     related_name='secondary_surficial_material_set',
                                                     on_delete=models.PROTECT, blank=True, null=True,
                                                     verbose_name='Secondary Surficial Material')

    lithology_sequence_number = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_description'
        ordering = ["start", "end"]

    db_table_comment = ('Describes the different lithologic qualities, characteristics, and materials found '
                        'at different depths while drilling.')
    db_column_supplemental_comments = {
        "bedrock_material_code":"Code for the bedrock material encountered during drilling and reported in lithologic description. ",
        "lithology_moisture_code":"Code that describes the level of water within the lithologic layer. i.e. Dry, Damp, Moist, Wet",
        "lithology_sequence_number":"Check with developers to see if this is being used, or if it can be deleted.",
        "water_bearing_estimated_flow":"Estimated flow of water within the lithologic layer, either recorded in US Gallons Per Minute or as per the well_yield_unit_code column.",
        "well_tag_number":"System generated sequential number assigned to each well. It is widely used by groundwater staff as it is the only consistent unique identifier for each well. It is different from a well ID plate number.",
    }

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.start,
                                                         self.end)
        else:
            return 'well {} {} {}'.format(self.well, self.start, self.end)


class PerforationBase(AuditModel):
    """
    Perforation in a well liner
    """
    liner_perforation_guid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                              editable=False)
    start = models.DecimalField(db_column='liner_perforation_from', max_digits=7, decimal_places=2,
                                verbose_name='Perforated From', blank=False,
                                validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(db_column='liner_perforation_to', max_digits=7, decimal_places=2,
                              verbose_name='Perforated To', blank=False,
                              validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        abstract = True


class LinerPerforation(PerforationBase):
    """
    Perforation in a well liner
    """
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.PROTECT, blank=True,
        null=True, related_name='linerperforation_set',
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))

    class Meta:
        ordering = ["start", "end"]
        db_table = 'liner_perforation'

    db_table_comment = ('Describes the depths at which the liner is perforated in a well to help improve '
                        'water flow at the bottom of the well. Some wells are perforated instead of having '
                        'a screen installed.')

    db_column_supplemental_comments = {
        "liner_perforation_from":"The depth at the top of the liner perforation, measured in feet below ground level.",
        "liner_perforation_to":"The depth at the bottom of the liner perforation, measured in feet below ground level.",
        "well_tag_number":"System generated sequential number assigned to each well. It is widely used by groundwater staff as it is the only consistent unique identifier for each well. It is different from a well ID plate number.",
    }

    def __str__(self):
        return 'well {} {} {}'.format(self.well, self.start, self.end)


class ActivitySubmissionLinerPerforation(PerforationBase):
    """
    Perforation in a well liner
    """
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.PROTECT, blank=True, null=True,
                                            related_name='linerperforation_set')

    class Meta:
        ordering = ["start", "end"]

    db_table_comment = ('Describes the depths at which the liner is perforated in a well to help improve '
                        'water flow at the bottom of the well. Some wells are perforated instead of having '
                        'a screen installed.')

    def __str__(self):
        return 'activity_submission {} {} {}'.format(self.activity_submission,
                                                     self.start,
                                                     self.end)


class Casing(AuditModel):
    """
    Casing information

    A casing may be associated to a particular submission, or to a well.
    """
    casing_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.PROTECT, blank=True, null=True,
                                            related_name='casing_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.PROTECT,
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
    # NOTE: Diameter should be pulling from screen.diameter
    diameter = models.DecimalField(
        max_digits=8, decimal_places=3, verbose_name='Diameter', null=True,
        blank=True, validators=[MinValueValidator(Decimal('0.5'))],
        db_comment=('The diameter as measure in inches of the casing of the well. There can be multiple '
                    'casings in a well, e.g. surface casing, and production casing. Diameter of casing made '
                    'available to the public is generally the production casing.'))
    casing_code = models.ForeignKey(CasingCode, db_column='casing_code', on_delete=models.PROTECT,
                                    verbose_name='Casing Type Code', null=True)
    casing_material = models.ForeignKey(CasingMaterialCode, db_column='casing_material_code',
                                        on_delete=models.PROTECT, blank=True, null=True,
                                        verbose_name='Casing Material Code')
    wall_thickness = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Wall Thickness',
                                         blank=True, null=True,
                                         validators=[MinValueValidator(Decimal('0.01'))])
    drive_shoe_status = models.ForeignKey(DriveShoeCode, db_column='drive_shoe_code',
                                                on_delete=models.PROTECT, blank=True, null=True,
                                                verbose_name='Drive Shoe Code')

    class Meta:
        ordering = ["start", "end"]
        db_table = 'casing'

    db_table_comment = ('Piping or tubing installed in a well to support the sides of the well. The casing '
                        'is comprised of a production (inner tube) and surface (outer tube) and can be made '
                        'of a variety of materials.')

    db_column_supplemental_comments = {
        "casing_code":"Describes the casing component (piping or tubing installed in a well) as either production casing, surface casing (outer casing), or open hole.",
        "casing_from":"The depth below ground level at which the casing begins.  Measured in feet below ground level.",
        "casing_to":"The depth below ground level at which the casing ends.  Measured in feet below ground level.",
        "diameter":"The diameter of the casing measured in inches. There can be multiple casings in a well, e.g. surface casing, and production casing. Diameter of casing made available to the public is generally the production casing.",
        "drive_shoe_code":"Indicates Y or N if a drive shoe was used in the installation of the casing.  A drive shoe is attached to the end of a casing and it helps protect it during installation.",
        "wall_thickness":"The thickness of the casing wall, measured in inches.",
        "well_tag_number":"System generated sequential number assigned to each well. It is widely used by groundwater staff as it is the only consistent unique identifier for each well. It is different from a well ID plate number.",
    }

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
            "drive_shoe_status": self.drive_shoe_status
        }


class Screen(AuditModel):
    """
    Screen in a well
    """
    screen_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.PROTECT, blank=True, null=True,
                                            related_name='screen_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.PROTECT, blank=True,
        null=True, related_name='screen_set',
        db_comment=('System generated sequential number assigned to each well. It is widely used by groundwater staff as it is the only consistent unique identifier for each well. It is different from a well ID plate number.'))
    start = models.DecimalField(db_column='screen_from', max_digits=7, decimal_places=2, verbose_name='From',
                                blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(db_column='screen_to', max_digits=7, decimal_places=2, verbose_name='To',
                              blank=False, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    diameter = models.DecimalField(db_column='screen_diameter', max_digits=7, decimal_places=2, verbose_name='Diameter',
                                            blank=True, null=True,
                                            validators=[MinValueValidator(Decimal('0.0'))])
    assembly_type = models.ForeignKey(
        ScreenAssemblyTypeCode, db_column='screen_assembly_type_code', on_delete=models.PROTECT, blank=True,
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
    code = models.CharField(primary_key=True, max_length=32,
                            db_column='water_quality_colour_code')
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
    hydraulic_property_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(
        Well, db_column='well_tag_number', to_field='well_tag_number',
        on_delete=models.PROTECT, blank=False, null=False,
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    avi = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='AVI')
    storativity = models.DecimalField(
        max_digits=8, decimal_places=7, blank=True, null=True, verbose_name='Storativity')
    transmissivity = models.DecimalField(
        max_digits=30, decimal_places=10, blank=True, null=True, verbose_name='Transmissivity')
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

    db_table_comment = 'Placeholder table comment.'

    db_column_supplemental_comments = {
        "analytic_solution_type":"The mathematical solution to the groundwater flow equation used to fit the observational data and estimate hydraulic parameters e.g. Theis 1935",
        "avi":"The Aquifer Vulnerability Index (AVI) method for calculating aquifer vulnerability to contamination based on the thickness of each sedimentary unit above the uppermost aquifer and estimated hydraulic conductivity of each of these layers.  ",
        "boundary_effect":"Identification of any boundary effects observed during hydraulic testing (e.g. specified head to represent streams or no-flow to represent a low conductivity interface) ",
        "hydraulic_conductivity":"Hydraulic conductivity estimated from hydraulic testing in metres per second.",
        "specific_storage":"Specific Storage estimated from hydraulic testing in units of per metre of aquifer thickness.",
        "specific_yield":"Specific Yield estimated from hydraulic testing (dimensionless).",
        "storativity":"Storativity estimated from hydraulic testing (dimensionless).",
        "testing_duration":"The duration of the hydraulic testing period.  For consistency, do not include the recovery period.",
        "testing_method":"Identification of the testing method (e.g.basic pumping test, pumping test with monitoring wells, single-well-response/slug test, constant head).",
        "transmissivity":"Transmissivity estimated from hydraulic testing.",
        "well_tag_number":"System generated sequential number assigned to each well. It is widely used by groundwater staff as it is the only consistent unique identifier for each well. It is different from a well ID plate number.",
    }

    def __str__(self):
        return '{} - {}'.format(self.well, self.hydraulic_property_guid)


class DecommissionMaterialCode(BasicCodeTableModel):
    """Codes for decommission materials"""
    code = models.CharField(primary_key=True, max_length=30,
                            db_column='decommission_material_code')
    description = models.CharField(max_length=100)

    db_table_comment = ('Describes the material used to fill a well when decomissioned. E.g. Bentonite'
                        ' chips, Native sand or gravel, Commercial gravel/pea gravel.')

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class DecommissionDescription(AuditModel):
    """Provides a description of the ground conditions (between specified start and end depth) for
        decommissioning"""

    decommission_description_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.PROTECT, blank=True, null=True,
                                            related_name='decommission_description_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.PROTECT, blank=True,
        null=True, related_name='decommission_description_set',
        db_comment=('System generated sequential number assigned to each well. It is widely used by groundwater staff as it is the only consistent unique identifier for each well. It is different from a well ID plate number.'))
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


class AquiferParameters(AuditModel):
    """
    Aquifer Parameter information from well pumping tests

    There can be many pumping tests done for a well so there may be many aquifer parameter records per well
    """
    aquifer_parameters_guid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    
    testing_number = models.AutoField(
        primary_key=True, verbose_name='Testing Number',
        db_comment=('The testing number is automatically assigned to each pumping test record that gets created'))
    
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.PROTECT, blank=True, null=True,
                                            related_name='aquifer_parameters_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='aquifer_parameters_set',
        db_comment=('The file number assigned to a particular well in the in the province\'s Groundwater '
                    'Wells and Aquifers application.'))
    
    start_date_pumping_test = models.DateField(
        null=True, verbose_name='Start date of pumping test',
        db_comment='The date when the analysis started.')
    
    pumping_test_description = models.ForeignKey(PumpingTestDescriptionCode, db_column='pumping_test_description_code',
                                    on_delete=models.PROTECT, blank=True, null=True,
                                    verbose_name='Testing Type',
                                    db_comment='Valid codes for the testing types used in '
                                                'pumping test analysis. i.e. ST, PTPW, PTOW, RT, OTHER')
    
    test_duration = models.PositiveIntegerField(blank=True, null=True)

    boundary_effect = models.ForeignKey(BoundaryEffectCode, db_column='boundary_effect_code',
                                on_delete=models.PROTECT, blank=True, null=True,
                                verbose_name='Boundary Effect',
                                db_comment='Valid codes for the boundaries observed in '
                                            'pumping test analysis. i.e. CH, NF.')

    private = models.BooleanField(
      default=False, choices=((False, 'No'), (True, 'Yes'))
    )
    
    storativity = models.DecimalField(
        max_digits=8, decimal_places=7, blank=True, null=True, verbose_name='Storativity')
    
    transmissivity = models.DecimalField(
        max_digits=30, decimal_places=10, blank=True, null=True, verbose_name='Transmissivity')
    
    hydraulic_conductivity = models.DecimalField(
        max_digits=30, decimal_places=10, blank=True, null=True, verbose_name='Hydraulic Conductivity')
    
    specific_yield = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Specific Yield')
    
    specific_capacity = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Specific Yield')
   
    analysis_method = models.ForeignKey(AnalysisMethodCode, db_column='analysis_method_code',
                                    on_delete=models.PROTECT, blank=True, null=True,
                                    verbose_name='Analysis Method',
                                    db_comment='Valid codes for the analysis methods used in '
                                                'pumping test analysis. i.e. TH, CJ, HJ, N, B, PC, OTHER')
    
    comments = models.TextField(
        max_length=350,
        blank=True,
        null=True,
        verbose_name='Testing Comments')

    class Meta:
        ordering = ["start_date_pumping_test"]
        db_table = 'aquifer_parameters'

    db_table_comment = ('Aquifer parameter testing stats from well pumping tests.')

    db_column_supplemental_comments = {
        "testing_number":"System generated sequential number assigned to each pumping test record.",
        "aquifer_parameters_guid":"System generated unique guid assigned to each pumping test record.",
        "well_tag_number":"System generated sequential number assigned to each well. It is widely used by groundwater staff as it is the only consistent unique identifier for each well. It is different from a well ID plate number.",
        "start_date_pumping_test":"Start date of the pumping test.",
        "pumping_test_description_code":"Identification of the testing method (e.g.basic pumping test, pumping test with monitoring wells, single-well-response/slug test, constant head).",
        "test_duration":"The duration of the hydraulic testing period.  For consistency, do not include the recovery period.",
        "boundary_effect_code":"Valid codes for the boundaries observed in pumping test analysis. i.e. CH, NF.",
        "private":"If a hydrogeological consultant has not provided permission with a signed data sharing agreement to share their interpretations publicly.",
        "storativity":"Storativity estimated from hydraulic testing (dimensionless).",
        "transmissivity":"Transmissivity estimated from hydraulic testing.",
        "hydraulic_conductivity":"Hydraulic conductivity estimated from hydraulic testing in metres per second.",
        "specific_yield":"Specific Yield estimated from hydraulic testing (dimensionless).",
        "specific_capacity":"Specific Capacity.",
        "analysis_method_code":"The mathematical solution to the groundwater flow equation used to fit the observational data and estimate hydraulic parameters e.g. Theis 1935",
        "comments":"Any additional comments about the pumping test.",
    }

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {}'.format(self.activity_submission, self.aquifer_parameters_guid)
        else:
            return 'well {} {}'.format(self.well, self.aquifer_parameters_guid)

    def as_dict(self):
        return {
            "testing_number": self.testing_number,
            "aquifer_parameters_guid": self.aquifer_parameters_guid,
            "well_tag_number": self.well,
            "start_date_pumping_test": self.start_date_pumping_test,
            "pumping_test_description_code": self.pumping_test_description,
            "test_duration": self.test_duration,
            "storativity": self.storativity,
            "transmissivity": self.transmissivity,
            "hydraulic_conductivity": self.hydraulic_conductivity,
            "specific_yield": self.specific_yield,
            "specific_capacity": self.specific_capacity,
            "analysis_method": self.analysis_method,
            "comments": self.comments
        }

class WellAttachment(models.Model):
    well_tag_number = models.ForeignKey(Well, on_delete=models.PROTECT, blank=True, null = False)
    # Public Tags
    well_construction = models.PositiveSmallIntegerField(default=0)
    well_alteration = models.PositiveSmallIntegerField(default=0)
    well_decommission = models.PositiveSmallIntegerField(default=0)
    photo = models.PositiveSmallIntegerField(default=0)
    well_pump_installation = models.PositiveSmallIntegerField(default=0)
    pumping_test_data = models.PositiveSmallIntegerField(default=0)
    directions_artesianconditions = models.PositiveSmallIntegerField(default=0)
    map = models.PositiveSmallIntegerField(default=0)
    additional_details = models.PositiveSmallIntegerField(default=0)
    # Private Tags
    well_inspection = models.PositiveSmallIntegerField(default=0)
    artesianmgmtreport = models.PositiveSmallIntegerField(default=0)
    alternative_specs = models.PositiveSmallIntegerField(default=0)
    water_quality = models.PositiveSmallIntegerField(default=0)
    health_authority = models.PositiveSmallIntegerField(default=0)
    consultants_report = models.PositiveSmallIntegerField(default=0)
    sharing_agreement = models.PositiveSmallIntegerField(default=0)
    pumping_test_info = models.PositiveSmallIntegerField(default=0)
    class Meta:
        db_table = "well_attachment_count"
        
    
    def __str__(self):
        template = "{} File count: {}\n"
        return_string = "Files for WTN: {}\n".format(self.well_tag_number)
        return_string += template.format('Well Construction',self.well_construction)
        return_string += template.format('Well Alteration',self.well_alteration)
        return_string += template.format('Well Decommission',self.well_decommission)
        return_string += template.format('Well Photos',self.photo)
        return_string += template.format('Well Pump Installations',self.well_pump_installation)
        return_string += template.format('Pumping Test',self.pumping_test_data)
        return_string += template.format('Map',self.map)
        return_string += template.format('Additional Detail',self.additional_details)
        return_string += template.format('Well Inspections',self.well_inspection)
        return_string += template.format('Alternative Specs',self.alternative_specs)
        return_string += template.format('Water Quality',self.water_quality)
        return_string += template.format('Health Authority',self.health_authority)
        return_string += "{} File count: {}".format('Consultants Report',self.consultants_report)
        
        return return_string

class WellLicence(models.Model):
    id = models.IntegerField(primary_key=True)
    well_id = models.IntegerField()
    waterrightslicence_id = models.IntegerField()
    class Meta:
        db_table = "well_licences"
        managed = False
    def __str__(self):
        return "Well Number: " + str(self.well_id) + ", License #: " + str(self.waterrightslicence_id)
