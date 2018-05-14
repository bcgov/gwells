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


from django.db import models
import uuid

class Perforation(AuditModel):
    """
    Liner Details
    """
    perforation_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well_tag_number = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    liner_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Liner Thickness')
    liner_diameter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner Diameter')
    liner_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner From')
    liner_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner To')
    liner_perforation_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Perforation From')
    liner_perforation_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Perforation To')

    class Meta:
        db_table = 'perforation'
        ordering = ['liner_from', 'liner_to', 'liner_perforation_from', 'liner_perforation_to', 'perforation_guid']

    def __str__(self):
        return self.description
