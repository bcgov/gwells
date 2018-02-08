from django.db import models
from gwells.models.AuditModel import AuditModel
from django.urls import reverse
import uuid

class Survey(AuditModel):
    """
    Survey
    """

    survey_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey_name = models.CharField(verbose_name="Survey Name", max_length=50, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('survey_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'survey {} {}'.format(self.survey_guid, self.survey_name)
    class Meta:
        db_table = 'gwells_survey'
