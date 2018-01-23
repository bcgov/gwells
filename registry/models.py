from django.db import models
from gwells.models import AuditModel

import uuid

class Applicant(AuditModel):
    applicant_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
