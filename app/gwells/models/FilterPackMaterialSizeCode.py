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
from django.db import models

class FilterPackMaterialSizeCode(AuditModel):
    """
     The size of material used to pack a well filter, e.g. 1.0 - 2.0 mm, 2.0 - 4.0 mm, 4.0 - 8.0 mm.
    """
    filter_pack_material_size_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date    = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'filter_pack_material_size_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description
