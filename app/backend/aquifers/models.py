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
import reversion

from django.utils import timezone
from django.contrib.gis.db import models

from gwells.models import AuditModel, CodeTableModel
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from reversion.models import Version
from gwells.db_comments.patch_fields import patch_fields

patch_fields()


class AquiferMaterial(CodeTableModel):
    """
    Material choices for describing Aquifer Material
    """
    code = models.CharField(
        primary_key=True, max_length=10, db_column='aquifer_material_code',
        db_comment=('Standard terms used to define the broad grouping of geological material found in'
                    ' the aquifer, i.e., Sand and Gravel, Sand, Gravel, Bedrock'))
    description = models.CharField(
        max_length=100,
        db_comment=('Describes the broad grouping of geological material found in the aquifer, i.e.,'
                    ' Sand and Gravel, Sand, Gravel, Bedrock'))

    class Meta:
        db_table = 'aquifer_material_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Material Codes'

    db_table_comment = ('Describes the broad grouping of geological material found in the aquifer, i.e., '
                        'Sand and Gravel, Sand, Gravel, Bedrock')

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class AquiferSubtype(CodeTableModel):
    """
    Subtypes of Aquifer
    """
    code = models.CharField(
        primary_key=True, max_length=3, db_column='aquifer_subtype_code',
        db_comment=('Valid codes to define how the aquifer was formed geologically (depositional'
                    ' description). The code value is a combination of an aquifer type represented by a'
                    ' number and an optional letter representing a more specific aquifer sub-type. E.g.'
                    ' aquifer sub-type code 6b is comprised of the aquifer type number (6: Crystalline'
                    ' bedrock aquifers) and subtype letter (b) specifically described as: Fractured'
                    ' crystalline (igneous intrusive or metamorphic, meta-sedimentary, meta-volcanic,'
                    ' volcanic) rock aquifers. Code values range from 1a to 6b.'))
    description = models.CharField(
        max_length=100,
        db_comment=('Descriptions of codes that define how the aquifer was formed geologically'
                    ' (depositional description). The code value is a combination of an aquifer type'
                    ' represented by a number and an optional letter representing a more specific'
                    ' aquifer sub-type. E.g. aquifer sub-type code 6b is comprised of the aquifer type'
                    ' number (6: Crystalline bedrock aquifers) and subtype letter (b) specifically'
                    ' described as: Fractured crystalline (igneous intrusive or metamorphic,'
                    ' meta-sedimentary, meta-volcanic, volcanic) rock aquifers. Code values range from'
                    ' 1a to 6b.'))

    class Meta:
        db_table = 'aquifer_subtype_code'

    db_table_comment = ('Categorizes an aquifer based on how it was formed geologically (depositional'
                        ' description).   The code value is a combination of an aquifer type represented by'
                        ' a number and an optional letter representing a more specific aquifer sub-type.'
                        ' E.g. aquifer sub-type code 6b is comprised of the aquifer type number (6:'
                        ' Crystalline bedrock aquifers) and subtype letter (b) specifically described as:'
                        ' Fractured crystalline (igneous intrusive or metamorphic, meta-sedimentary,'
                        ' meta-volcanic, volcanic) rock aquifers. Code values range from 1a to 6b.')

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class AquiferProductivity(CodeTableModel):
    """
    Productivity choices for describing Aquifer
    -------------------
    """
    code = models.CharField(
        primary_key=True, max_length=1, db_column='aquifer_productivity_code',
        db_comment=('Standard terms that define the aquifer\'s productivity which represent an aquifers'
                    ' ability to transmit and yield groundwater; i.e., Low, Moderate, High'))
    description = models.CharField(
        max_length=100,
        db_comment=('Description of the standard terms that define the aquifer\'s productivity which'
                    ' represent an aquifers ability to transmit and yield groundwater; i.e., Low,'
                    ' Moderate, High'))

    class Meta:
        db_table = 'aquifer_productivity_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Productivity Codes'

    db_table_comment = ('Describes the aquifer\'s productivity which represent an aquifers ability to '
                        'transmit and yield groundwater; i.e., Low, Moderate, High')

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class AquiferDemand(CodeTableModel):
    """
    Demand choices for describing Aquifer
    """
    code = models.CharField(
        primary_key=True, max_length=1, db_column='aquifer_demand_code',
        db_comment=('Standard terms that define the level of groundwater use at the time aquifer was'
                    ' mapped; i.e., High, Moderate, Low.'))
    description = models.CharField(
        max_length=100,
        db_comment=('Description of the standard terms that define the level of groundwater use at the'
                    ' time aquifer was mapped; i.e., High, Moderate, Low.'))

    class Meta:
        db_table = 'aquifer_demand_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Demand Codes'

    db_table_comment = ('Describes the level of groundwater use at the time aquifer was mapped; i.e., High, '
                        'Moderate, Low.')

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class WaterUse(CodeTableModel):
    """
    Type of Known Water Use choices for describing Aquifer
    -------------------
    """
    code = models.CharField(
        primary_key=True, max_length=2, db_column='water_use_code',
        db_comment=('Standard terms that define the type of known water use of an aquifer at the time of'
                    ' mapping. It indicates the variability or diversity of uses of the aquifer water as'
                    ' a supply source. I.e. Domestic, Multiple, Potential Domestic'))
    description = models.CharField(
        max_length=100,
        db_comment=('Description of the standard terms that define the type of known water use of an'
                    ' aquifer at the time of mapping. It indicates the variability or diversity of uses'
                    ' of the aquifer water as a supply source. I.e. Domestic, Multiple, Potential'
                    ' Domestic'))

    class Meta:
        db_table = 'water_use_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Water Use Codes'

    db_table_comment = ('Describes the type of known water use of an aquifer at the time of mapping. It'
                        ' indicates the variability or diversity of uses of the aquifer water as a supply'
                        ' source. I.e. Domestic, Multiple, Potential Domestic')

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class QualityConcern(CodeTableModel):
    code = models.CharField(
        primary_key=True, max_length=2, db_column='quality_concern_code',
        db_comment=('Standard terms used to represent the extent of documented concerns of contaminants'
                    ' in the aquifer at the time of mapping. i.e. isloated, local, regional, none.'))
    description = models.CharField(
        max_length=100,
        db_comment=('Description of the standard terms used to represent the extent of documented'
                    ' concerns of contaminants in the aquifer at the time of mapping. i.e. isloated,'
                    ' local, regional, none.'))

    class Meta:
        db_table = 'quality_concern_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Quality Concern Codes'

    db_table_comment = ('Extent of documented concerns of contaminants in the aquifer at the time of'
                        ' mapping. i.e. isloated, local, regional, none.')

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class AquiferVulnerabilityCode(CodeTableModel):
    """
    Demand choices for describing Aquifer
    """
    code = models.CharField(
        primary_key=True, max_length=1, db_column='aquifer_vulnerability_code',
        db_comment=('Standard terms used to define an aquifer’s relative intrinsic vulnerability to'
                    ' impacts from human activities on the land surface. Vulnerability is based on: the'
                    ' type, thickness, and extent of geologic materials above the aquifer, depth to'
                    ' water table (or to top of confined aquifer), and type of aquifer materials, i.e.,'
                    ' Low, Moderate, High.'))
    description = models.CharField(
        max_length=100,
        db_comment=('Description of the standard terms used to define an aquifer’s relative intrinsic'
                    ' vulnerability to impacts from human activities on the land surface. Vulnerability'
                    ' is based on: the type, thickness, and extent of geologic materials above the'
                    ' aquifer, depth to water table (or to top of confined aquifer), and type of aquifer'
                    ' materials, i.e., Low, Moderate, High.'))

    class Meta:
        db_table = 'aquifer_vulnerability_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Vulnerability Codes'

    db_table_comment = ('Describes an aquifer’s relative intrinsic vulnerability to impacts from human '
                        'activities on the land surface. Vulnerability is based on: the type, thickness, '
                        'and extent of geologic materials above the aquifer, depth to water table (or to '
                        'top of confined aquifer), and type of aquifer materials, i.e., Low, Moderate, High.')

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


@reversion.register()
class Aquifer(AuditModel):
    """
    An underground layer of water-bearing permeable rock, rock fractures or unconsolidated materials
    (gravel, sand, or silt), from which groundwater is extracted using a water well.

    This table holds ONLY the aquifers to which we have associated one or more wells.  It is not
    the definitive source of all aquifers in the province.
    """
    aquifer_id = models.AutoField(
        primary_key=True, verbose_name="Aquifer ID Number",
        db_comment=('System generated sequential number assigned to each aquifer. It is widely used by '
                    'ground water administration staff as it is the only consistent unique identifier for a '
                    'mapped aquifer. It is also commonly referred to as Aquifer Number.'))
    aquifer_name = models.CharField(
        max_length=100, blank=True, null=True,
        db_comment=('Name assigned for a specific aquifer. Typically derived from geographic names or names '
                    'in common use, but may also be lithologic or litho-stratigraphic units, e.g. '
                    'Abbotsford-Sumas, McDougall Creek Deltaic.'))
    location_description = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Description of Location',
        db_comment=('Brief description of the geographic location of the aquifer. The description is usually '
                    'referenced to a nearby major natural geographic area or community, e.g., Grand Forks.'))
    material = models.ForeignKey(
        AquiferMaterial,
        db_column='aquifer_material_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Material Reference",
        related_name='aquifers',
        db_comment=('Standard terms used to define the broad grouping of geological material found in'
                    ' the aquifer, i.e., Sand and Gravel, Sand, Gravel, Bedrock'))
    subtype = models.ForeignKey(
        AquiferSubtype,
        db_column='aquifer_subtype_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Subtype Reference",
        related_name='aquifers',
        db_comment=('Valid codes to define how the aquifer was formed geologically (depositional'
                    ' description). The code value is a combination of an aquifer type represented by a'
                    ' number and an optional letter representing a more specific aquifer sub-type. E.g.'
                    ' aquifer sub-type code 6b is comprised of the aquifer type number (6: Crystalline'
                    ' bedrock aquifers) and subtype letter (b) specifically described as: Fractured'
                    ' crystalline (igneous intrusive or metamorphic, meta-sedimentary, meta-volcanic,'
                    ' volcanic) rock aquifers. Code values range from 1a to 6b.'))
    area = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name='Size (square km)',
        db_comment='Approximate size of the aquifer in square kilometers.')
    vulnerability = models.ForeignKey(
        AquiferVulnerabilityCode,
        # TODO: Spelling mistake below!
        db_column='aquifer_vulnerablity_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Aquifer Vulnerabiliy",
        db_comment=('Standard terms used to define an aquifer’s relative intrinsic vulnerability to'
                    ' impacts from human activities on the land surface. Vulnerability is based on: the'
                    ' type, thickness, and extent of geologic materials above the aquifer, depth to'
                    ' water table (or to top of confined aquifer), and type of aquifer materials, i.e.,'
                    ' Low, Moderate, High.'))
    productivity = models.ForeignKey(
        AquiferProductivity,
        db_column='aquifer_productivity_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Productivity Reference",
        related_name='aquifers',
        db_comment=('Standard terms that define the aquifer\'s productivity which represent an aquifers'
                    ' ability to transmit and yield groundwater; i.e., Low, Moderate, High'))
    demand = models.ForeignKey(
        AquiferDemand,
        db_column='aquifer_demand_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Demand Reference",
        related_name='aquifers',
        db_comment=('Standard terms that define the level of groundwater use at the time aquifer was '
                    'mapped; i.e., High, Moderate, Low.'))
    known_water_use = models.ForeignKey(
        WaterUse,
        db_column='water_use_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Known Water Use Reference",
        related_name='aquifers',
        db_comment=('Standard terms that define the type of known water use of an aquifer at the time of'
                    ' mapping. It indicates the variability or diversity of uses of the aquifer water as'
                    ' a supply source. I.e. Domestic, Multiple, Potential Domestic'))
    quality_concern = models.ForeignKey(
        QualityConcern,
        db_column='quality_concern_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Quality Concern Reference",
        related_name='aquifers',
        db_comment=('Standard terms used to represent the extent of documented concerns of contaminants'
                    ' in the aquifer at the time of mapping. i.e. isloated, local, regional, none.'))
    litho_stratographic_unit = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Lithographic Stratographic Unit',
        db_comment=('Permeable geologic unit (where available) that comprises the aquifer. It is typically '
                    'either; the era of deposition, the name of a specific formation and\or the broad '
                    'material types, e.g., Paleozoic to Mesozoic Era, Cache Creek Complex, Intrusive Rock.'))
    mapping_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1990),
            MaxValueValidator(timezone.now().year)],
        blank=True,
        null=True,
        verbose_name="Date of Mapping",
        help_text="Use the following format: <YYYY>",
        db_comment='The year the aquifer was initially mapped or last updated.')
    notes = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name='Notes on Aquifer, for internal use only.',
        db_comment=('Details about the aquifer that the province deems important to maintain e.g. local '
                    'knowledge about the aquifer, and decisions for changes.'))
    geom = models.PolygonField(srid=3005, null=True)

    history = GenericRelation(Version)

    class Meta:
        db_table = 'aquifer'
        ordering = ['aquifer_id']
        verbose_name_plural = 'Aquifers'

    db_table_comment = ('A geological formation, a group of geological formations, or a part of one or more '
                        'geological formations that is groundwater bearing and capable of storing, '
                        'transmitting and yielding groundwater.')

    def __str__(self):
        return '{} - {}'.format(self.aquifer_id, self.aquifer_name)
