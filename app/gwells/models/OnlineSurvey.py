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
import uuid

class OnlineSurvey(models.Model):
    """
     OnlineSurvey, providing a reference to customizable online surveys (e.g. SurveyMonkey)
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
    survey_introduction_text = models.TextField(verbose_name="Introduction Text", max_length=200, blank=True, null=True)
    survey_link = models.URLField(verbose_name="Link", blank=True, null=True)
    survey_enabled = models.BooleanField(verbose_name="Enabled", blank=False, null=False, default=False)
    survey_page = models.CharField(verbose_name="Page", choices=SURVEY_PAGE_CHOICES, max_length=1, default=WELL)

    effective_date = models.DateField(default=timezone.now,blank=False, null=False)
    expiry_date    = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}: {} | {} | {}'.format(self.survey_introduction_text, self.survey_link, self.survey_enabled, self.survey_page)

    class Meta:
        db_table = 'online_survey'
        ordering = ['effective_date']

"""
    def __str__(self):
        return self.description


        return '{} {} {} {} {}'.format(self.survey_guid, self.survey_introduction_text, self.survey_link, self.survey_enabled, self.survey_page)

"""  
