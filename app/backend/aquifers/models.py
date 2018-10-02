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
from django.utils import timezone
from django.db import models
from gwells.models import AuditModel
from django.core.validators import MinValueValidator, MaxValueValidator


class AquiferMaterial(AuditModel):
    """
    Material choices for describing Aquifer Material
    """
    code = models.CharField(primary_key=True, max_length=10, db_column='aquifer_material_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'aquifer_material_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Material Codes'

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class AquiferSubtype(AuditModel):
    """
    Subtypes of Aquifer
    """
    code = models.CharField(primary_key=True, max_length=3, db_column='aquifer_subtype_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'aquifer_subtype_code'

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class AquiferProductivity(AuditModel):
    """
    Productivity choices for describing Aquifer
    -------------------
    """
    code = models.CharField(primary_key=True, max_length=1, db_column='aquifer_productivity_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'aquifer_productivity_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Productivity Codes'

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class AquiferDemand(AuditModel):
    """
    Demand choices for describing Aquifer
    """
    code = models.CharField(primary_key=True, max_length=1, db_column='aquifer_demand_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'aquifer_demand_code' 
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Demand Codes'

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class WaterUse(AuditModel):
    """
    Type of Known Water Use choices for describing Aquifer 
    -------------------
    """
    code = models.CharField(primary_key=True, max_length=2, db_column='water_use_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'water_use_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Water Use Codes'

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class QualityConcern(AuditModel):
    code = models.CharField(primary_key=True, max_length=2, db_column='quality_concern_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'quality_concern_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Quality Concern Codes'

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class AquiferVulnerabilityCode(AuditModel):
    """
    Demand choices for describing Aquifer
    """
    code = models.CharField(primary_key=True, max_length=1, db_column='aquifer_vulnerability_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'aquifer_vulnerability_code'
        ordering = ['display_order', 'code']
        verbose_name_plural = 'Aquifer Vulnerability Codes'

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class Aquifer(AuditModel):
    """
    An underground layer of water-bearing permeable rock, rock fractures or unconsolidated materials
    (gravel, sand, or silt), from which groundwater is extracted using a water well. 

    This table holds ONLY the aquifers to which we have associated one or more wells.  It is not
    the definitive source of all aquifers in the province. 
    """
    aquifer_id = models.PositiveIntegerField(
        primary_key=True, verbose_name="Aquifer ID Number")
    aquifer_name = models.CharField(max_length=100, blank=True, null=True)
    location_description = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Description of Location')
    material = models.ForeignKey(
        AquiferMaterial,
        db_column='aquifer_material_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Material Reference",
        related_name='aquifers')
    subtype = models.ForeignKey(
        AquiferSubtype,
        db_column='aquifer_subtype_code',
        blank=True,
        null=True,        
        on_delete=models.PROTECT,
        verbose_name="Subtype Reference",
        related_name='aquifers')
    area = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name='Size (square km)')
    vulnerability = models.ForeignKey(
        AquiferVulnerabilityCode,
        db_column='aquifer_vulnerablity_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Aquifer Vulnerabiliy")   
    productivity = models.ForeignKey(
        AquiferProductivity,
        db_column='aquifer_productivity_code',
        blank=True,
        null=True,        
        on_delete=models.PROTECT,
        verbose_name="Productivity Reference",
        related_name='aquifers')
    demand = models.ForeignKey(
        AquiferDemand,
        db_column='aquifer_demand_code',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Demand Reference",
        related_name='aquifers')
    known_water_use = models.ForeignKey(
        WaterUse,
        db_column='water_use_code',
        blank=True,
        null=True,        
        on_delete=models.PROTECT,
        verbose_name="Known Water Use Reference",
        related_name='aquifers')
    quality_concert = models.ForeignKey(
        QualityConcern,
        db_column='quality_concern_code',
        blank=True,
        null=True,        
        on_delete=models.PROTECT,
        verbose_name="Quality Concern Reference",
        related_name='aquifers')
    litho_stratographic_unit = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Lithographic Stratographic Unit')
    mapping_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1990), 
            MaxValueValidator(timezone.now().year)],
        blank=True,
        null=True,                
        verbose_name="Date of Mapping",    
        help_text="Use the following format: <YYYY>")
    notes = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name='Notes on Aquifer, for internal use only.')

    class Meta:
        db_table = 'aquifer'
        ordering = ['aquifer_id']
        verbose_name_plural = 'Aquifers'

    def __str__(self):
        return '{} - {}'.format(self.aquifer_id, self.aquifer_name)
