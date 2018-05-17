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
from .Well import Well
from .ActivitySubmission import ActivitySubmission
from .YieldEstimationMethodCode import YieldEstimationMethodCode
from .WellYieldUnitCode import WellYieldUnitCode

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class ProductionData(AuditModel):
    """
    Water production of a well measured by a driller
    """
    production_data_guid = models.UUIDField(
      primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(
      ActivitySubmission, db_column='filing_number',
      on_delete=models.CASCADE, blank=True, null=True)
    well = models.ForeignKey(
      Well, db_column='well_tag_number', on_delete=models.CASCADE,
      blank=True, null=True)
    yield_estimation_method = models.ForeignKey(
      YieldEstimationMethodCode, db_column='yield_estimation_method_code',
      on_delete=models.CASCADE, blank=True, null=True,
      verbose_name='Estimation Method')
    yield_estimation_rate = models.DecimalField(
      max_digits=7, decimal_places=2, verbose_name='Estimation Rate',
      blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    yield_estimation_duration = models.DecimalField(
      max_digits=9, decimal_places=2, verbose_name='Estimation Duration',
      blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    well_yield_unit = models.ForeignKey(
      WellYieldUnitCode, db_column='well_yield_unit_code', blank=True,
      null=True)
    static_level = models.DecimalField(
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

    class Meta:
        db_table = 'production_data'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(
              self.activity_submission, self.yield_estimation_method,
              self.yield_estimation_rate)
        else:
            return 'well {} {} {}'.format(
              self.well, self.yield_estimation_method,
              self.yield_estimation_rate)
