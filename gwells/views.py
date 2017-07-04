from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
#from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
#from django.utils import timezone
from formtools.wizard.views import SessionWizardView
from .models import WellYieldUnit, Well, ActivitySubmission, WellClass
from .forms import SearchForm, ActivitySubmissionTypeAndClassForm, WellOwnerForm, ActivitySubmissionLocationForm, ActivitySubmissionGpsForm, ActivitySubmissionLithologyFormSet
import json
from django.core.serializers.json import DjangoJSONEncoder

class HelloWorldView(generic.ListView):
    template_name = 'gwells/index.html'
    context_object_name = 'yield_unit_list'

    def get_queryset(self):
        """
        Return the well yield units for hello world.
        """
        return WellYieldUnit.objects.order_by('-sort_order')

def well_search(request):
    well_results = None
    well_results_json = None

    if request.method == 'GET' and 'well' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            # process the data in form.cleaned_data
            well_results = form.process()
    else:
        form = SearchForm()

    if well_results:
        well_results_json = json.dumps(
            [well.as_dict() for well in well_results],
            cls=DjangoJSONEncoder)

    return render(request, 'gwells/search.html',
                  {'form': form, 'well_list': well_results, 'wells_json': well_results_json})


def map_well_search(request):
    well_results_json = None

    if (request.method == 'GET' and 'start_lat_long' in request.GET
            and 'end_lat_long' in request.GET):
        well_results_json = SearchForm(request.GET)
        if well_results_json.is_valid():
            well_results_json = well_results_json.process()

    if well_results_json:
        well_results_json = json.dumps(
            [well.as_dict() for well in well_results_json],
            cls=DjangoJSONEncoder)

    else:
        well_results_json = '[]'

    return JsonResponse(well_results_json, safe=False)


class WellDetailView(generic.DetailView):
    model = Well
    context_object_name = 'well'



#class DetailView(generic.DetailView):
#    model = ActivitySubmission
#    context_object_name = 'activity_submission'



class ActivitySubmissionListView(generic.ListView):
    model = ActivitySubmission
    context_object_name = 'activity_submission_list'
    template_name = 'gwells/activity_submission_list.html'



class ActivitySubmissionDetailView(generic.DetailView):
    model = ActivitySubmission
    context_object_name = 'activity_submission'
    template_name = 'gwells/activity_submission_detail.html'



FORMS = [('type_and_class', ActivitySubmissionTypeAndClassForm),
         ('owner', WellOwnerForm),
         ('location', ActivitySubmissionLocationForm),
         ('gps', ActivitySubmissionGpsForm),
         ('lithology', ActivitySubmissionLithologyFormSet),
        ]

TEMPLATES = {'type_and_class': 'gwells/activity_submission_form.html',
             'owner': 'gwells/activity_submission_form.html',
             'location': 'gwells/activity_submission_form.html',
             'gps': 'gwells/activity_submission_form.html',
             'lithology': 'gwells/activity_submission_lithology_form.html',
            }



class ActivitySubmissionWizardView(SessionWizardView):

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(ActivitySubmissionWizardView, self).get_context_data(form=form, **kwargs)
        context['wizard_data'] = self.get_all_cleaned_data()

        if self.steps.current == 'type_and_class':
            try:
                water_supply_class = WellClass.objects.filter(code='WATR_SPPLY')[0]
                context['water_supply_well_class_guid'] = water_supply_class.well_class_guid
            except Exception as e:
                context['water_supply_well_class_guid'] = None
       # elif self.steps.current == 'lithology':
       #     formset = ActivitySubmissionLithologyFormSet()
       #     helper = LithologyFormSetHelper()
       #     context.update({'formset': formset, 'helper': helper})
        return context

    def done(self, form_list, **kwargs):
        submission = ActivitySubmission()
        for form in form_list:
            for field, value in form.cleaned_data.items():
                setattr(submission, field, value)

        #if submission.well_activity_type.code == 'CON' and submission.well is None:
            #TODO
            #w = submission.createWell()
            #w = w.save()
            #submission.well = w
        #    submission.save()
        #else:
        submission.save()

        #lithology = form_dict['lithology'].save()
        return HttpResponseRedirect('/submission/')
