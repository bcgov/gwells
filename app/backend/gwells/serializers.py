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


class AuditModelSerializer(serializers.ModelSerializer):
    """
    Serializes AuditModel fields.
    Can be inherited into serializers for models that inherit from AuditModel
    """
    create_user = serializers.ReadOnlyField()
    create_date = serializers.ReadOnlyField()
    update_user = serializers.ReadOnlyField()
    update_date = serializers.ReadOnlyField()
