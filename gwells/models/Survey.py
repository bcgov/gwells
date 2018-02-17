from django.db import models
from gwells.models.AuditModel import AuditModel
from django.urls import reverse
import uuid

class Survey(AuditModel):
    """
    Survey
    """

    WELL = 'w'
    REGISTRY = 'r'
    SEARCH = 's'

    SURVEY_PAGE_CHOICES = (
        (WELL, "well"),
        (REGISTRY, "registry"),
        (SEARCH, "search")
    )

    survey_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey_introduction_text = models.CharField(verbose_name="Introduction Text", max_length=50, blank=True, null=True)
    survey_link = models.CharField(verbose_name="Link", max_length=100, blank=True, null=True)
    survey_enabled = models.BooleanField(verbose_name="Enabled", blank=False, null=False, default=False)
    survey_page = models.CharField(verbose_name="Page", choices=SURVEY_PAGE_CHOICES, max_length=1, default=WELL)

    def get_absolute_url(self):
        return reverse('survey', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {} {} {} {}'.format(self.survey_guid, self.survey_introduction_text, self.survey_link, self.survey_enabled, self.survey_page)
    class Meta:
        db_table = 'gwells_survey'
