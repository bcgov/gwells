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

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class LinerPerforation(AuditModel):
    """
    Perforation in a well liner
    """
    liner_perforation_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    liner_perforation_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Perforated From', blank=False, validators=[MinValueValidator(Decimal('0.00'))])
    liner_perforation_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Perforated To', blank=False, validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        db_table = 'liner_perforation'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.liner_perforation_from, self.liner_perforation_to)
        else:
            return 'well {} {} {}'.format(self.well, self.liner_perforation_from, self.liner_perforation_to)
