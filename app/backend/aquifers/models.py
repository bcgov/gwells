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
import zipfile
import tempfile
import os
import copy

from django.utils import timezone
from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from gwells.models import AuditModel, CodeTableModel, BasicCodeTableModel
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.prototypes.io import wkt_w
from django.contrib.gis import geos

from reversion.models import Version

from gwells.models import AuditModel, CodeTableModel
from gwells.db_comments.patch_fields import patch_fields

patch_fields()


class WaterRightsPurpose(AuditModel):
    """
    Material choices for describing Aquifer Material
    """
    code = models.CharField(primary_key=True, max_length=10,
                            db_column='water_rights_purpose_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)

    effective_date = models.DateTimeField(default=timezone.now, null=False)
    expiry_date = models.DateTimeField(default=timezone.make_aware(
        timezone.datetime.max, timezone.get_default_timezone()), null=False)

    class Meta:
        db_table = 'water_rights_purpose_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Water Rights Purpose Codes'

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class WaterRightsLicence(AuditModel):
    """
    Material choices for describing Aquifer Material
    """

    # Unique in the water rights database we import from.
    wrl_sysid = models.IntegerField(
        primary_key=True,
        verbose_name="Water Rights Licence System ID")

    purpose = models.ForeignKey(
        WaterRightsPurpose,
        db_column='water_rights_purpose_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Water Rights Purpose Reference",
        related_name='licences')

    # A non-unique licence number, used to calculate allocations along with
    # the quantity flag, below.
    licence_number = models.BigIntegerField(db_index=True)

    # QUANTITY FLAG is the code used to identify how the total quantity is assigned
    # across multiple Points of Well Diversion (PWD) for a particular licence and purpose use,
    # i.e., T, M, D, or P.
    # Only in the case of 'M', the quantity is shared across wells in the licence.
    quantity_flag = models.CharField(
        max_length=1,
        default='T',
        choices=(('T', 'T'), ('M', 'M'), ('D', 'D'), ('P', 'P')))

    quantity = models.DecimalField(
        max_digits=12, decimal_places=3, blank=True, null=True, verbose_name='Quanitity')

    effective_date = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        verbose_name_plural = 'Aquifer Licences'

    def __str__(self):
        return '{}'.format(self.licence_number)


class AquiferMaterial(CodeTableModel):
    """
    Material choices for describing Aquifer Material
    """
    code = models.CharField(
        primary_key=True, max_length=10, db_column='aquifer_material_code',
        db_comment=('Code for valid options for the broad grouping of geological material found in the'
                    ' aquifer, i.e. SG, S, G, B'))
    description = models.CharField(
        max_length=100,
        db_comment=('Describes the broad grouping of geological material found in the aquifer, i.e.,'
                    ' Sand and Gravel, Sand, Gravel, Bedrock'))

    class Meta:
        db_table = 'aquifer_material_code'
        ordering = ['code']
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
        db_comment=("Categorizes an aquifer based on how it was formed geologically (depositional description). Understanding of how aquifers were formed governs important attributes such as their productivity, vulnerability to contamination as well as proximity and likelihood of hydraulic connection to streams. The code value is a combination of an aquifer type represented by a number and an optional letter representing a more specific aquifer sub-type.   There are six major aquifer types, some with multiple subtypes.  E.g. aquifer sub-type code 6b is comprised of the aquifer type number (6: Crystalline bedrock aquifers) and subtype letter (b) specifically described as: Fractured crystalline (igneous intrusive or metamorphic, meta-sedimentary, meta-volcanic, volcanic) rock aquifers. Code values range from 1a to 6b."))
    description = models.CharField(
        max_length=100,
        db_comment=('Descriptions that define how the aquifer was formed geologically'
                    ' (depositional description). E.g. Unconfined sand and gravel - large river system,'
                    ' Confined sand and gravel - glacial, Flat-lying to gently-dipping volcanic bedrock.'))

    class Meta:
        db_table = 'aquifer_subtype_code'

    db_table_comment = ('Categorizes an aquifer based on how it was formed geologically (depositional'
                        ' description). Understanding of how aquifers were formed governs important'
                        ' attributes such as their productivity, vulnerability to contamination as well as'
                        ' proximity and likelihood of hydraulic connection to streams. The code value is a'
                        ' combination of an aquifer type represented by a number and an optional letter'
                        ' representing a more specific aquifer sub-type. E.g. Crystalline bedrock aquifers)'
                        ' and subtype letter, Fractured crystalline (igneous intrusive or metamorphic,'
                        ' meta-sedimentary, meta-volcanic, volcanic) rock aquifers. Code values range from'
                        ' 1a to 6b.')

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class AquiferProductivity(CodeTableModel):
    """
    Productivity choices for describing Aquifer
    -------------------
    """

    code = models.CharField(
        primary_key=True, max_length=1, db_column='aquifer_productivity_code',
        db_comment=('Valid code for the aquifer\'s productivity, which represent an aquifers ability to'
                    ' transmit and yield groundwater; i.e., L, M, H'))
    description = models.CharField(
        max_length=100,
        db_comment=('Describes the aquifer\'s productivity which represent an aquifers ability to'
                    ' transmit and yield groundwater; i.e., Low, Moderate, High'))

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
        Note on db_comments:  db_comment properties on model columns are
    overriden by the db_column_supplemental_comments provided below.
    db_column_supplemental_comments provides an easier way for the DA to add/update
    comments in bulk.
    """
    code = models.CharField(
        primary_key=True, max_length=1, db_column='aquifer_demand_code',
        db_comment=('Describes the level of groundwater use at the time aquifer was mapped; i.e., High,'
                    ' Moderate, Low.'))
    description = models.CharField(
        max_length=100,
        db_comment=('Describes the level of groundwater use at the time aquifer was mapped; i.e., High,'
                    ' Moderate, Low.'))

    class Meta:
        db_table = 'aquifer_demand_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Demand Codes'

    db_table_comment = ('Describes the level of groundwater use at the time aquifer was mapped; i.e., High, '
                        'Moderate, Low.')

    db_column_supplemental_comments = {

    }

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
        db_comment=('Code for the aquifer’s relative intrinsic vulnerability to impacts from human'
                    ' activities on the land surface. Vulnerability is based on: the type, thickness,'
                    ' and extent of geologic materials above the aquifer, depth to water table (or to'
                    ' top of confined aquifer), and type of aquifer materials, i.e., L, M, H.'))
    description = models.CharField(
        max_length=100,
        db_comment=('Describes an aquifer’s relative intrinsic vulnerability to impacts from human'
                    ' activities on the land surface. Vulnerability is based on: the type, thickness,'
                    ' and extent of geologic materials above the aquifer, depth to water table (or to'
                    ' top of confined aquifer), and type of aquifer materials, i.e., Low, Moderate, High.'))

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

    Note on db_comments:  db_comment properties on model columns are
    overriden by the db_column_supplemental_comments provided below.
    db_column_supplemental_comments provides an easier way for the DA to add/update
    comments in bulk.
    """
    aquifer_id = models.AutoField(
        primary_key=True, verbose_name="Aquifer ID Number",
        db_comment=('System generated unique sequential number assigned to each mapped aquifer. The'
                    ' aquifer_id identifies which aquifer a well is in. An aquifer can have multiple'
                    ' wells, while a single well can only be in one aquifer.'))
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
        db_comment=('Code for valid options for the broad grouping of geological material found in the'
                    ' aquifer, i.e. SG, S, G, B'))
    subtype = models.ForeignKey(
        AquiferSubtype,
        db_column='aquifer_subtype_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Subtype Reference",
        related_name='aquifers',
        db_comment=('Categorizes an aquifer based on how it was formed geologically (depositional'
                    ' description). Understanding of how aquifers were formed governs important'
                    ' attributes such as their productivity, vulnerability to contamination as well as'
                    ' proximity and likelihood of hydraulic connection to streams. The code value is a'
                    ' combination of an aquifer type represented by a number and an optional letter'
                    ' representing a more specific aquifer sub-type. E.g. 1a, 2, 6a.'))
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
        db_comment=('Valid code for the aquifer\'s productivity, which represent an aquifers ability to'
                    ' transmit and yield groundwater; i.e., L, M, H'))
    demand = models.ForeignKey(
        AquiferDemand,
        db_column='aquifer_demand_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Demand Reference",
        related_name='aquifers',
        db_comment=('Describes the level of groundwater use at the time aquifer was mapped; i.e., High,'
                    ' Moderate, Low.'))
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
        db_comment=('Details about the mapped aquifer that the province deems important to maintain such as'
                    ' local knowledge about the aquifer or decisions for changes related to attributes of'
                    ' the mapped aquifer.'))
    geom = models.PolygonField(srid=3005, null=True)
    # This version is pre-rendered in WGS 84 for display on web-maps.
    geom_simplified = models.PolygonField(srid=4326, null=True)

    history = GenericRelation(Version)

    def load_shapefile(self, f):
        """
        Given a shapefile with a single feature, update spatial fields of the aquifer.
        You must still call aquifer.save() afterwards.
        """
        try:
            zip_ref = zipfile.ZipFile(f)
        except zipfile.BadZipFile as e:
            raise Aquifer.BadShapefileException(str(e))

        ret = zip_ref.testzip()
        if ret is not None:
            raise Aquifer.BadShapefileException("Bad zipfile, info: %s" % ret)

        output_dir = tempfile.mkdtemp()
        for item in zip_ref.namelist():
            # Check filename endswith shp
            zip_ref.extract(item, output_dir)
            if item.endswith('.shp'):
                # Extract a single file from zip
                the_shapefile = os.path.join(output_dir, item)
                # break
        zip_ref.close()

        ds = DataSource(the_shapefile)
        self.update_geom_from_feature(ds[0][0])

    def update_geom_from_feature(self, feat):
        """
        Given a spatial feature with Geometry, update spatial fields of the aquifer.
        You must still call aquifer.save() afterwards.
        """

        geom = feat.geom

        # Make a GEOSGeometry object using the string representation.
        if not geom.srid == 3005:
            logging.info("Non BC-albers feature, skipping.")
            return
        # Eliminate any 3d geometry so it fits in PostGIS' 2d geometry schema.
        wkt = wkt_w(dim=2).write(GEOSGeometry(geom.wkt, srid=3005)).decode()
        geos_geom = GEOSGeometry(wkt, srid=3005)
        # Convert MultiPolygons to plain Polygons,
        # We assume the largest one is the one we want to keep, and the rest are artifacts/junk.
        if isinstance(geos_geom, geos.MultiPolygon):
            geos_geom_out = geos_geom[0]
            for g in geos_geom:
                if len(g.wkt) > len(geos_geom_out.wkt):
                    geos_geom_out = g
        elif isinstance(geos_geom, geos.Polygon):
            geos_geom_out = geos_geom
        else:
            logging.info("Bad geometry type: {}, skipping.".format(
                geos_geom.__class__))
            return

        self.geom = geos_geom_out

    class Meta:
        db_table = 'aquifer'
        ordering = ['aquifer_id']
        verbose_name_plural = 'Aquifers'

    db_table_comment = ('A geological formation, a group of geological formations, or a part of one or more '
                        'geological formations that is groundwater bearing and capable of storing, '
                        'transmitting and yielding groundwater.')

    class BadShapefileException(Exception):
        pass

    def __str__(self):
        return '{} - {}'.format(self.aquifer_id, self.aquifer_name)

    db_column_supplemental_comments = {
        "aquifer_demand_code": "Describes the level of groundwater use at the time the aquifer was mapped; i.e., High, Moderate, Low.",
        "aquifer_id": "System generated sequential number assigned to each aquifer. It is widely used by groundwater staff as it is the only consistent unique identifier for a mapped aquifer. It is also commonly referred to as Aquifer Number.",
        "aquifer_material_code": "Describes the broad grouping of geological material found in the aquifer, i.e., Sand and Gravel, Sand, Gravel, Bedrock",
        "aquifer_productivity_code": "Describes the aquifer's productivity which represent an aquifers ability to transmit and yield groundwater; i.e., Low, Moderate, High",
        "aquifer_subtype_code": "Categorizes an aquifer based on how it was formed geologically (depositional description). Understanding of how aquifers were formed governs important attributes such as their productivity, vulnerability to contamination as well as proximity and likelihood of hydraulic connection to streams. The code value is a combination of an aquifer type represented by a number and an optional letter representing a more specific aquifer sub-type.   There are six major aquifer types, some with multiple subtypes.  E.g. aquifer sub-type code 6b is comprised of the aquifer type number (6: Crystalline bedrock aquifers) and subtype letter (b) specifically described as: Fractured crystalline (igneous intrusive or metamorphic, meta-sedimentary, meta-volcanic, volcanic) rock aquifers. Code values range from 1a to 6b.",
        "aquifer_vulnerablity_code": "Describes an aquifer’s relative intrinsic vulnerability to impacts from human activities on the land surface. Vulnerability is based on: the type, thickness, and extent of geologic materials above the aquifer, depth to water table (or to top of confined aquifer), and type of aquifer materials, i.e., Low, Moderate, High.",
        "quality_concern_code": "Extent of documented concerns of contaminants in the aquifer at the time of mapping. i.e. isloated, local, regional, none.",
        "water_use_code": "Describes the type of known water use of an aquifer at the time of mapping. It indicates the variability or diversity of uses of the aquifer water as a supply source. I.e. Domestic, Multiple, Potential Domestic",
    }

@receiver(pre_save, sender=Aquifer)
def update_geom_simplified(sender, instance, **kwargs):
    geos_geom_simplified = copy.deepcopy(instance.geom)
    geos_geom_simplified.transform(4326)
    geos_geom_simplified = geos_geom_simplified.simplify(0.0005, preserve_topology=True)
    instance.geom_simplified = geos_geom_simplified

class AquiferResourceSection(BasicCodeTableModel):
    """
    Defines the available sections (categories) of aquifer resources.
    """
    code = models.CharField(primary_key=True, max_length=1,
                            db_column='aquifer_resource_section_code')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="")

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Aquifer Resource Sections'
        db_table = 'aquifer_resource_section_code'

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)

    def __str__(self):
        return self.name


class AquiferResource(AuditModel):
    """
    A PDF document associated with a given aquifer.
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name="Aquifer Resource Identifier",
        db_column='aquifer_resource_id')
    aquifer = models.ForeignKey(
        Aquifer,
        related_name='resources',
        on_delete=models.CASCADE,
        db_comment=('System generated sequential number assigned to each aquifer. It is widely used by groundwater staff as it is the only consistent unique identifier for a mapped aquifer. It is also commonly referred to as Aquifer Number.'))
    section = models.ForeignKey(
        AquiferResourceSection,
        db_column='aquifer_resource_section_code',
        verbose_name="Aquifer Resource Section",
        on_delete=models.PROTECT,
        help_text="The section (category) of this resource.")
    name = models.CharField(
        max_length=255,
        verbose_name="Aquifer Resource Name",
        help_text="",
        db_comment=('Descriptive name of the document at the URL that contains the internal or external information about the aquifer.')
    )
    url = models.URLField(
        verbose_name="PDF Document URL",
        max_length=255,
        help_text="A resolvable link to the PDF document associated with this aquifer resource.",
        db_comment=('The web address where the internal or external information about the aquifer can be found.'))

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Aquifer Resource'

    def __str__(self):
        return self.name
