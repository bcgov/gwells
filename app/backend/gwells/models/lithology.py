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
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator

from gwells.models import AuditModel, CodeTableModel


class BedrockMaterialDescriptorCode(CodeTableModel):
    """
    Further descriptor of the bedrock material encountered in lithology
    """
    bedrock_material_descriptor_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('Code for adjective that describes the characteristics of the bedrock material in'
                    ' more detail.'))
    description = models.CharField(
        max_length=100,
        db_comment=('An adjective that describes the characteristics of the bedrock material in more'
                    ' detail.'))

    class Meta:
        db_table = 'bedrock_material_descriptor_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('An adjective that describes the characteristics of the bedrock material in more '
                        'detail.')

    def __str__(self):
        return self.description


class BedrockMaterialCode(CodeTableModel):
    """
    The bedrock material encountered in lithology
    """
    bedrock_material_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('Code for the bedrock material encountered during drilling and reported in'
                    ' lithologic description.'))
    description = models.CharField(
        max_length=100,
        db_comment='Bedrock material encountered during drilling and reported in lithologic description.')

    class Meta:
        db_table = 'bedrock_material_code'
        ordering = ['display_order', 'description']

    db_table_comment = 'Bedrock material encountered during drilling and reported in lithologic description.'

    def __str__(self):
        return self.description


class SurficialMaterialCode(CodeTableModel):
    """
    The surficial material encountered in lithology
    """
    surficial_material_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'surficial_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class LithologyColourCode(CodeTableModel):
    """
    Colour of the lithology
    """
    lithology_colour_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('Numeric code used for choosing the colour of the lithologic material identified at'
                    ' time of drilling. E.g. 01, 02, 03, 04'))
    description = models.CharField(
        max_length=100,
        verbose_name='Colour Description',
        db_comment=('Describes the colour of the lithologic material identified at time of drilling.'
                    ' E.g. Black, dark, tan, rust-coloured'))

    class Meta:
        db_table = 'lithology_colour_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Describes the colour of the lithologic material identified at time of drilling. '
                        'E.g. Black, dark, tan, rust-coloured')

    def __str__(self):
        return self.description


class LithologyDescriptionCode(CodeTableModel):
    lithology_description_code = models.CharField(
        primary_key=True, max_length=10, editable=False, verbose_name='Code',
        db_comment=('Numeric code used to characterize the different qualities of lithologic materials.'
                    ' E.g. 01, 02, 03.'))
    description = models.CharField(
        max_length=255,
        verbose_name='Description',
        db_comment=('Describes the different qualities of lithologic materials. E.g. dry, loose,'
                    ' weathered, soft.'))

    class Meta:
        db_table = 'lithology_description_code'
        ordering = ['display_order']

    db_table_comment = ('Standard terms used to characterize the different qualities of lithologic '
                        'materials. E.g. dry, loose, weathered, soft.')

    def __str__(self):
        return 'lithology_description_code {} {}'.format(self.lithology_description_code, self.description)


class LithologyHardnessCode(CodeTableModel):
    """
    Hardness of the lithology
    """
    lithology_hardness_code = models.CharField(
        primary_key=True, max_length=10, editable=False,
        db_comment=('The hardness of the material that a well is drilled into (the lithology), e.g. Very'
                    ' hard, Medium, Very Soft.'))
    description = models.CharField(
        max_length=100, verbose_name='Hardness',
        db_comment=('The hardness of the material that a well is drilled into (the lithology), e.g. Very'
                    ' hard, Medium, Very Soft.'))

    class Meta:
        db_table = 'lithology_hardness_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Code that represents the hardness of the material that a well is drilled into (the'
                        ' lithology). E.g. Very hard, Hard, Dense, Stiff, Medium, Loose, Soft, Very soft.')

    def __str__(self):
        return self.description


class LithologyMaterialCode(CodeTableModel):
    lithology_material_code = models.CharField(
        primary_key=True, max_length=10, editable=False, verbose_name='Code',
        db_comment='Numerical code for the materials noted for the lithology. E.g. 01, 02, 03.')
    description = models.CharField(
        max_length=255, verbose_name='Material Description',
        db_comment='Description of the lithologic material using standardized terms, e.g. Rock, Clay, Sand, Unspecified.')

    class Meta:
        db_table = 'lithology_material_code'
        ordering = ['display_order']

    db_table_comment = ('Code that describes the material noted for lithology. E.g. Rock, Clay, Sand,'
                        ' Unspecified,')

    def __str__(self):
        return 'lithology_material {} {}'.format(self.lithology_material_code, self.description)


class LithologyStructureCode(CodeTableModel):
    """
    Structure of the lithology
    """
    lithology_structure_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'lithology_structure_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class LithologyMoistureCode(CodeTableModel):
    """
    Moisture of the lithology
    """
    lithology_moisture_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'lithology_moisture_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Code that describes the level of water within the lithologic layer. i.e. Dry, '
                        'Damp, Moist, Wet')

    def __str__(self):
        return self.description
