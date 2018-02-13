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
import uuid

class LithologyDescriptionCode(AuditModel):
    lithology_description_code_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, verbose_name='Code')
    description = models.CharField(max_length=255, verbose_name='Description')
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'lithology_description_code'
        ordering=['sort_order']
    def __str__(self):
        return 'lithology_description_code {} {}'.format(self.code, self.description)
