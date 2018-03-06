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

"""
  Not a Code table, but a representative sample of data to support search
"""
class DrillingCompany(AuditModel):
    """
    Companies who perform drilling.
    """
    drilling_company_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drilling_company_code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'drilling_company'
        verbose_name_plural = 'Drilling Companies'

    def __str__(self):
        return self.name
