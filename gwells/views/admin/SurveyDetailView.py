from django.views import generic
from gwells.models.Survey import Survey

class SurveyDetailView(generic.DetailView):
    model = Survey
    context_object_name = 'survey'
    template_name = 'gwells/survey_detail.html'

    def get_context_data(self, **kwargs):
        """
        Return the context for the well details page.
        """

        context = super(SurveyDetailView, self).get_context_data(**kwargs)

        return context
