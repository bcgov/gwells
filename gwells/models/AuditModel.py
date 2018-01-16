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

class AuditModel(models.Model):
    """
    An abstract base class model that provides audit fields.
    """
    who_created = models.CharField(max_length=30)
    when_created = models.DateTimeField(blank=True, null=True)
    who_updated = models.CharField(max_length=30, null=True)
    when_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self._state.adding == True:
            self.when_created = timezone.now()
        self.when_updated = timezone.now()
        return super(AuditModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
