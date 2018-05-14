from rest_framework.generics import ListAPIView
from gwells.serializers import SurveySerializer
from gwells.models.Survey import Survey


class SurveyListView(ListAPIView):
    """
    get: returns a list of active surveys
    """

    serializer_class = SurveySerializer
    queryset = Survey.objects.filter(survey_enabled=True)
    pagination_class = None
