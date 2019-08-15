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
from django.contrib.gis.db import models
from django.utils import timezone

from gwells.db_comments.model_mixins import DBComments
from gwells.db_comments.patch_fields import patch_fields

patch_fields()


class AuditModelStructure(models.Model, DBComments):
    """
    An abstract base class model that provides audit fields, but does not auto-populate values.

    There are some exceptional cases where models do not extend off this class.
    Notably:
        - Wells : well create/update dates should reflect the dates in the submissions that make them up.
        - Submissions: Legacy submissions must retain the update and create dates of the wells on which
            they are based.
    """
    create_user = models.CharField(
        max_length=60, null=False,
        db_comment=('The user who created this record in the database.'))
    create_date = models.DateTimeField(
        default=timezone.now, null=False,
        db_comment=('Date and time (UTC) when the physical record was created in the database.'))
    # We don't set a default for the update_user, the update user must always be explicitly stated.
    # If it's the backend bootstrapping something, the correct value to use is: gwells.models.DATALOAD_USER
    update_user = models.CharField(
        max_length=60, null=False,
        db_comment=('The user who last updated this record in the database.'))
    update_date = models.DateTimeField(
        default=timezone.now, null=False,
        db_comment=('Date and time (UTC) when the physical record was updated in the database. '
                    'It will be the same as the create_date until the record is first updated after '
                    'creation.'))

    def serialize(self):
        data = serializers.serialize('json', [self, ])
        struct = json.loads(data)
        return json.dumps(struct[0])

    class Meta:
        abstract = True


class AuditModel(AuditModelStructure):
    """
    An abstract base class model that provides audit fields and automatically populates them.

    Only in exceptional cases should any model deviate from extending this model.
    """

    def save(self, *args, **kwargs):
        ''' For all saves, populate "Update" fields '''
        self.update_date = timezone.now()

        ''' For "new" content, populate "Add" fields '''
        if self._state.adding is True:
            self.create_date = timezone.now()

        return super(AuditModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class BasicCodeTableModel(AuditModel):
    """
    An abstract class for code table models, without an order field
    """
    effective_date = models.DateTimeField(
        default=timezone.now, null=False,
        db_comment='The date and time that the code became valid and could be used.')
    expiry_date = models.DateTimeField(
        default=timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone()), null=False,
        db_comment='The date and time after which the code is no longer valid and should not be used.')

    class Meta:
        abstract = True


class CodeTableModel(AuditModel):
    """
    An abstract class for code table models.
    """
    display_order = models.PositiveIntegerField(
        db_comment='The order in which the codes may display on screen.')
    effective_date = models.DateTimeField(
        default=timezone.now, null=False,
        db_comment='The date and time that the code became valid and could be used.')
    expiry_date = models.DateTimeField(
        default=timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone()), null=False,
        db_comment='The date and time after which the code is no longer valid and should not be used.')

    class Meta:
        abstract = True


class ProvinceStateCode(CodeTableModel):
    """
    Lookup of Provinces/States.
    Used to specify valid provinces or states for the address of the owner of a well.
    It provides for a standard commonly understood code and description for provinces and states.
    Some examples include: BC, AB, WA
    """
    province_state_code = models.CharField(primary_key=True, max_length=10)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(
        db_index=True,
        db_comment='The order in which the codes may display on screen.')

    """
    Tue 13 Feb 22:24:26 2018 GW Disabled for now until Code With Us sprint is complete
    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date    = models.DateTimeField(blank=True, null=True)
    """
    class Meta:
        db_table = 'province_state_code'
        ordering = ['display_order']

    db_table_comment = 'Province or state used for the mailing address for the company'

    def __str__(self):
        return self.description
