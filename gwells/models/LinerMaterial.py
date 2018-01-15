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

class LinerMaterial(AuditModel):
    """
     Liner material installed in a well to protect the well pump or other works in the well from damage.
    """
    liner_material_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    liner_material_code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'gwells_liner_material'
        ordering = ['sort_order', 'description']

    def __str__(self):
        return self.description
