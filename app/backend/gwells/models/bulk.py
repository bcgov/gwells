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
from  django.db import models
from  django.contrib.postgres.fields import JSONField

from gwells.models.common import AuditModelStructure
from gwells.db_comments.patch_fields import patch_fields

patch_fields()

class BulkHistory(AuditModelStructure):
    """
    A model to keep a record of bulk chanegs performed on the db
    """
    class Meta:
        db_table = 'bulk_history'
        ordering = ['-created_date']

    id = models.AutoField(
        db_column='bulk_history_id',
        primary_key=True, verbose_name='Bulk History Id',
        db_comment=('The primary key for the bulk_history table'))
    operation_name = models.CharField(
        max_length=60, null=False,
        db_comment=('The kind of bulk operation performed'))
    record = JSONField(
        null=False,
        db_comment=('The JSON Patch diff of the bulk changes.'))
