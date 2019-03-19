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
from decimal import Decimal
from django.utils import timezone

from django.db import models
from django.core.validators import MinValueValidator

from gwells.models import AuditModel, CodeTableModel


class ScreenTypeCode(CodeTableModel):
    """
     The possible types of well screens, i.e. Telescope, Pipe Size.
    """
    screen_type_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'screen_type_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Valid categories for the type of well screen installed in a well. i.e. Pipe size,'
                        ' Telescope, Other')

    def __str__(self):
        return self.description


class ScreenAssemblyTypeCode(CodeTableModel):
    """
     The category of screen assembly, i.e. K-Packer & Riser, K-Packer, Lead Packer, Riser Pipe, Screen,
     Screen Blank, Tail Pipe.
    """
    screen_assembly_type_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'screen_assembly_type_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Describes the different components of a screen. A single well screen could be'
                        ' composed of several assembly layers, each layer may have a different screen'
                        ' assembly type. Some examples include: K-packer, Riser Pipe, Screen, Screen blank,'
                        ' Tail Pipe.')

    def __str__(self):
        return self.description


class ScreenBottomCode(CodeTableModel):
    """
     The type of bottom on a well screen, i.e. Bail, Plate, Plug, Other.
    """
    screen_bottom_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'screen_bottom_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Valid categories used to identify the type of bottom on a well screen. It provides'
                        ' for a standard commonly understood code and description for screen bottoms. Some'
                        ' examples include: Bail, Plate, Plug. \'Other\' can also be specified.')

    def __str__(self):
        return self.description


class ScreenIntakeMethodCode(CodeTableModel):
    """
     Refers to the type of intake mechanism for a well screen, i.e. Screen, Open Bottom, Uncased Hole.
    """
    screen_intake_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'screen_intake_method_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Valid categories used to identify the type of intake mechanism for a well screen.'
                        ' It provides for a standard commonly understood code and description for screen'
                        ' intake codes. Some examples include: Open bottom, Screen, Uncased hole.')

    def __str__(self):
        return self.description


class ScreenMaterialCode(CodeTableModel):
    """
     The material used to construct a well screen, i.e. Plastic, Stainless Steel, Other.
    """
    screen_material_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'screen_material_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Describes the different materials that makes up the screen on a well. E.g. Plastic,'
                        ' Stainless Steel, Other.')

    def __str__(self):
        return self.description


class ScreenOpeningCode(CodeTableModel):
    """
     The type of opening on a well screen, i.e. Continuous Slot, Slotted, Perforated Pipe.
    """
    screen_opening_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'screen_opening_code'
        ordering = ['display_order', 'description']

    db_table_comment = ('Valid categories used to identify the type of opening on a well screen. It provides'
                        ' for a standard commonly understood code and description for screen openings. E.g.'
                        ' Continuous Slot, Perforated Pipe, Slotted.')

    def __str__(self):
        return self.description
