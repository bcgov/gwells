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

class AquiferWell(AuditModel):
    """
    AquiferWell
    """

    aquifer_well_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aquifer_id = models.PositiveIntegerField(verbose_name="Aquifer Number", blank=True, null=True)
    well_tag_number = models.ForeignKey(Well, db_column='well_tag_number', to_field='well_tag_number', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'aquifer_well'
