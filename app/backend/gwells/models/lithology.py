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
from decimal import Decimal
import uuid

from django.db import models
from django.core.validators import MinValueValidator

from gwells.models import AuditModel


class BedrockMaterialDescriptorCode(AuditModel):
    """
    Further descriptor of the bedrock material encountered in lithology
    """
    bedrock_material_descriptor_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'bedrock_material_descriptor_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class BedrockMaterialCode(AuditModel):
    """
    The bedrock material encountered in lithology
    """
    bedrock_material_code = models.CharField(
        primary_key=True, max_length=10, editable=False,)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'bedrock_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class SurficialMaterialCode(AuditModel):
    """
    The surficial material encountered in lithology
    """
    surficial_material_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'surficial_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class LithologyColourCode(AuditModel):
    """
    Colour of the lithology
    """
    lithology_colour_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_colour_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class LithologyDescriptionCode(AuditModel):
    lithology_description_code = models.CharField(
        primary_key=True, max_length=10, editable=False, verbose_name='Code')
    description = models.CharField(max_length=255, verbose_name='Description')
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_description_code'
        ordering = ['display_order']

    def __str__(self):
        return 'lithology_description_code {} {}'.format(self.code, self.description)


class LithologyHardnessCode(AuditModel):
    """
    Hardness of the lithology
    """
    lithology_hardness_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_hardness_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class LithologyMaterialCode(AuditModel):
    lithology_material_code = models.CharField(
        primary_key=True, max_length=10, editable=False, verbose_name='Code')
    description = models.CharField(max_length=255, verbose_name='Description')
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_material_code'
        ordering = ['display_order']

    def __str__(self):
        return 'lithology_material {} {}'.format(self.code, self.description)


class LithologyStructureCode(AuditModel):
    """
    Structure of the lithology
    """
    lithology_structure_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_structure_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class LithologyMoistureCode(AuditModel):
    """
    Moisture of the lithology
    """
    lithology_moisture_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_moisture_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description
