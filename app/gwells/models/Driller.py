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
from .DrillingCompany import DrillingCompany

from django.db import models
import uuid

class Driller(AuditModel):
    """
    People responsible for drilling.
    """
    driller_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drilling_company = models.ForeignKey(DrillingCompany, db_column='drilling_company_guid', on_delete=models.CASCADE, verbose_name='Drilling Company')
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)

    class Meta:
        db_table = 'driller'

    def __str__(self):
        return '%s %s - %s' % (self.first_name, self.surname, self.registration_number)
