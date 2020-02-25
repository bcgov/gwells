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
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.contrib.gis.db import models

from gwells.models import AuditModel

from aquifers.models import Aquifer

from wells.models import Well


@reversion.register()
class VerticalAquiferExtent(AuditModel):
    """
    Aquifer 3d information
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name="VerticalAquiferExtent Resource Identifier",
        db_column='vertical_aquifer_extent_id')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.PROTECT, blank=True, null=True,
        db_comment=('The optional well correlated with the aquifer.'))
    geom = models.PointField(
        blank=False, null=False,
        verbose_name='Geo-referenced location of aquifer\'s depth', srid=4326)
    aquifer = models.ForeignKey(
        Aquifer, db_column='aquifer_id', on_delete=models.PROTECT, blank=False, null=False,
        db_comment=('The referenced aquifer at this point.'))
    start = models.DecimalField(
        db_column='vertical_aquifer_extent_from', max_digits=7, decimal_places=2, verbose_name='From',
        null=False, blank=False, validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(
        db_column='vertical_aquifer_extent_to', max_digits=7, decimal_places=2, verbose_name='To',
        null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        db_table = "vertical_aquifer_extents"
        ordering = ['start']
        verbose_name_plural = 'VerticalAquiferExtent'

    def __str__(self):
        parts = [
            'VerticalAquiferExtent'
        ]

        if self.well:
            parts.append(' for well {}'.format(self.well))
        if self.geom:
            parts.append(' at POINT({}, {})'.format(self.geom.x, self.geom.y))
        parts.append(' between [{}, {}]'.format(self.start, self.end))
        parts.append(' for aquifer {}'.format(self.aquifer))

        return ''.join(parts)
