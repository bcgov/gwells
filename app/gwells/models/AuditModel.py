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
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from model_utils import FieldTracker
from django.core import serializers
import json

class AuditModel(models.Model):
    """
    An abstract base class model that provides audit fields.
    """
    create_user = models.CharField(max_length=60)
    # Fri  9 Feb 20:40:38 2018 GW note to remove null=True from next three..
    create_date = models.DateTimeField(blank=True, null=True)
    update_user = models.CharField(max_length=60, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' For all saves, populate "Update" fields '''
        self.update_date = timezone.now()

        ''' For "new" content, populate "Add" fields '''
        if self._state.adding == True:
            self.create_date = timezone.now()

        return super(AuditModel, self).save(*args, **kwargs)

    def serialize(self):
        data = serializers.serialize('json', [self, ])
        struct = json.loads(data)
        return json.dumps(struct[0])

    class Meta:
        abstract = True
