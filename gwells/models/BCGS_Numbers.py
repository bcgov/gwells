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

class BCGS_Numbers(AuditModel):
    bcgs_id = models.BigIntegerField(primary_key=True, default=uuid.uuid4, editable=False)
    bcgs_number = models.CharField(max_length=20, verbose_name="BCGS Mapsheet Number")

    class Meta:
        db_table = 'bcgs_number'
        ordering = ['bcgs_number']

    def __str__(self):
        return self.description
