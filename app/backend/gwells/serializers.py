from rest_framework import serializers
from gwells.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    """ Serializes Survey model fields """

    class Meta:
        model = Survey
        fields = (
            'survey_guid',
            'survey_introduction_text',
            'survey_link',
            'survey_page'
        )
