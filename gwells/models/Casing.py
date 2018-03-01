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
from .AuditModel import AuditModel
from .ActivitySubmission import ActivitySubmission
from .Well import Well
from .CasingCode import CasingCode
from .CasingMaterialCode import CasingMaterialCode

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class Casing(AuditModel):
    """
    Casing information
    """
    casing_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well_tag_number = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    casing_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='From', null=True, blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    casing_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='To', null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    diameter = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='Diameter', null=True, blank=True, validators=[MinValueValidator(Decimal('0.5'))])
    casing_code = models.ForeignKey(CasingCode, db_column='casing_code', on_delete=models.CASCADE, verbose_name='Casing Code', null=True)
    casing_material = models.ForeignKey(CasingMaterialCode, db_column='casing_material_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Casing Material Code')
    wall_thickness = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Wall Thickness', blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    drive_shoe = models.NullBooleanField(default=False, null=True, verbose_name='Drive Shoe', choices=((False, 'No'), (True, 'Yes')))

    class Meta:
        ordering = ["casing_from", "casing_to"]
        db_table = 'casing'


    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.casing_from, self.casing_to)
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
