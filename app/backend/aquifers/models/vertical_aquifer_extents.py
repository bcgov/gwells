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

from django.core.validators import MinValueValidator
from django.contrib.gis.db import models

from gwells.models import AuditModel, AuditModelStructure
from gwells.db_comments.patch_fields import patch_fields


patch_fields()


class VerticalAquiferExtent(AuditModel):
    """
    Aquifer 3d information
    """
    class Meta:
        db_table = "vertical_aquifer_extents"
        ordering = ['start']
        verbose_name_plural = 'VerticalAquiferExtent'

    db_table_comment = ('Stores aquifer top and bottom elevation information (measured from ground level).')

    id = models.AutoField(
        primary_key=True,
        verbose_name="VerticalAquiferExtent Resource Identifier",
        db_column='vertical_aquifer_extent_id',
        db_comment=('System generated unique sequential number assigned to each vertical'
            ' aquifer extent.'))
    well = models.ForeignKey(
        'wells.Well', db_column='well_tag_number', on_delete=models.PROTECT, blank=True, null=True,
        db_comment=('The optional well correlated with the aquifer.'))
    geom = models.PointField(
        blank=False, null=False,
        verbose_name='Geo-referenced location of aquifer\'s depth', srid=4326,
        db_comment=('Geo-referenced location of aquifer\'s depth'))
    aquifer = models.ForeignKey(
        'aquifers.Aquifer', db_column='aquifer_id', on_delete=models.PROTECT, blank=False,
        null=False, db_comment=('The referenced aquifer at this point.'))
    start = models.DecimalField(
        db_column='vertical_aquifer_extent_from', max_digits=7, decimal_places=2, null=False,
        blank=False, verbose_name='From', validators=[MinValueValidator(Decimal('0.00'))],
        db_comment=('Depth below ground surface of the start of the aquifer measured in meters.'))
    end = models.DecimalField(
        db_column='vertical_aquifer_extent_to', max_digits=7, decimal_places=2, verbose_name='To',
        null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))],
        db_comment=('Depth below ground surface of the end of the aquifer measured in meters.'))

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


class VerticalAquiferExtentsHistory(AuditModelStructure):
    """
    Keeps track of the changes to vertical aquifer extents
    """
    class Meta:
        db_table = 'vertical_aquifer_extents_history'
        ordering = ['-create_date']

    db_table_comment = ('Keeps track of the changes to the vertical aquifer extents '
                        'from a bulk change.')

    id = models.AutoField(
        db_column='vertical_aquifer_extents_history_id',
        primary_key=True, verbose_name='Vertical Aquifer Extents History Id',
        db_comment=('The primary key for the vertical_aquifer_extents_history table'))
    well_tag_number = models.IntegerField(
        db_column='well_tag_number',
        blank=True, null=True,
        db_comment=('The file number assigned to a particular well on a vertical aquifer extent'))
    aquifer_id = models.IntegerField(
        db_column='aquifer_id',
        blank=False, null=False,
        db_comment=('The id assigned to a particular aquifer on a vertical aquifer extent'))
    geom = models.PointField(
        blank=False, null=False,
        verbose_name='Geo-referenced location of aquifer\'s depth', srid=4326,
        db_comment=('Geo-referenced location of aquifer\'s depth'))
    start = models.DecimalField(
        db_column='vertical_aquifer_extent_from', max_digits=7, decimal_places=2, null=False,
        blank=False, verbose_name='From',
        db_comment=('Depth below ground surface of the start of the aquifer measured in meters.'))
    end = models.DecimalField(
        db_column='vertical_aquifer_extent_to', max_digits=7, decimal_places=2, verbose_name='To',
        null=True, blank=True,
        db_comment=('Depth below ground surface of the end of the aquifer measured in meters.'))
