from django.views.generic.edit import CreateView
from gwells.models import *
from django.forms import modelform_factory
from django.shortcuts import render

class AddSurveyView(CreateView):
    model = Survey
    fields=['survey_name']
    template_name='gwells/survey_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        SurveyForm = modelform_factory(Survey, fields=('survey_name',))

        context['form'] = SurveyForm()
        return context
