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
from .ScreenAssemblyTypeCode import ScreenAssemblyTypeCode

from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
import uuid

class Screen(AuditModel):
    """
    Screen in a well
    """
    screen_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    screen_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='From', blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    screen_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='To', blank=False, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    internal_diameter = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Diameter', blank=True, null=True, validators=[MinValueValidator(Decimal('0.0'))])
    assembly_type = models.ForeignKey(ScreenAssemblyTypeCode, db_column='screen_assembly_type_code', on_delete=models.CASCADE, blank=True, null=True)
    slot_size = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Slot Size', blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'screen'
        ordering = ['screen_from', 'screen_to']
    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.screen_from, self.screen_to)
        else:
            return 'well {} {} {}'.format(self.well, self.screen_from, self.screen_to)
