from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from gwells.serializers import SurveySerializer
from gwells.models import Survey


class SurveyListView(ListAPIView):
    """
    get: returns a list of active surveys
    """

    serializer_class = SurveySerializer
    queryset = Survey.objects.filter(survey_enabled=True)
    pagination_class = None
