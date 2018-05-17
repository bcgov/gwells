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

class LithologyMaterialCode(AuditModel):
    lithology_material_code = models.CharField(primary_key=True, max_length=10, editable=False, verbose_name='Code')
    description = models.CharField(max_length=255, verbose_name='Description')
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date    = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_material_code'
        ordering=['display_order']
    def __str__(self):
        return 'lithology_material {} {}'.format(self.code, self.description)
