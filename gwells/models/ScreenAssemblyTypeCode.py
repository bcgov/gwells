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

class ScreenAssemblyTypeCode(AuditModel):
    """
     The category of screen assembly, i.e. K-Packer & Riser, K-Packer, Lead Packer, Riser Pipe, Screen, Screen Blank, Tail Pipe.
    """
    screen_assembly_type_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    screen_assembly_type_code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'screen_assembly_type_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description
