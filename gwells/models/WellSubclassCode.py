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
from .WellClassCode import WellClassCode
from django.db import models
import uuid

class WellSubclassCode(AuditModel):
    """
    Subclass of Well type; we use GUID here as Django doesn't support multi-column PK's
    """
    well_subclass_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well_class = models.ForeignKey(WellClassCode, null=True, db_column='well_class_code', on_delete=models.CASCADE, blank=True)
    well_subclass_code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date    = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'well_subclass_code'
        ordering = ['display_order', 'description']

    def validate_unique(self, exclude=None):
        qs = Room.objects.filter(name=self.well_subclass_code)
        if qs.filter(well_class__well_class_code=self.well_class__well_class_code).exists():
            raise ValidationError('Code must be unique per Well Class')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(WellSubclassCode, self).save(*args, **kwargs)

    def __str__(self):
        return self.description
