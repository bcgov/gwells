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
from .WellClass import WellClass
from django.db import models
import uuid

class WellSubclass(AuditModel):
    """
    Subclass of Well type.
    """
    well_subclass_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well_class = models.ForeignKey(WellClass, null=True, db_column='well_class_guid', on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'gwells_well_subclass'
        ordering = ['sort_order', 'description']

    def validate_unique(self, exclude=None):
        qs = Room.objects.filter(name=self.code)
        if qs.filter(well_class__code=self.well_class__code).exists():
            raise ValidationError('Code must be unique per Well Class')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(WellSubclass, self).save(*args, **kwargs)

    def __str__(self):
        return self.description
