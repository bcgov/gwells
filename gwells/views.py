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
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
#from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
#from django.utils import timezone
from formtools.wizard.views import SessionWizardView
from .models import WellYieldUnit, Well, ActivitySubmission, WellClass
from .forms import SearchForm, ActivitySubmissionTypeAndClassForm, WellOwnerForm, ActivitySubmissionLocationForm, ActivitySubmissionGpsForm
from .forms import ActivitySubmissionLithologyFormSet, ActivitySubmissionCasingFormSet, ActivitySubmissionSurfaceSealForm, ActivitySubmissionLinerForm, ActivitySubmissionLinerPerforationFormSet
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
    well_results_overflow = None
    well_results_json = '[]'
    lat_long_box = '{}'

    if request.method == 'GET' and 'well' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            # process the data in form.cleaned_data
            well_results = form.process()
    else:
        form = SearchForm()
  
    if well_results:
        if len(well_results) > SearchForm.WELL_RESULTS_LIMIT:
            well_results_overflow = ('Query returned more than %d wells. Please refine your search or select a smaller area to look for wells in.' % SearchForm.WELL_RESULTS_LIMIT)
            well_results = None
        else:
            well_results_json = json.dumps(
                [well.as_dict() for well in well_results],
                cls=DjangoJSONEncoder)
        start_lat_long = form.cleaned_data.get('start_lat_long')
        end_lat_long = form.cleaned_data.get('end_lat_long')
        lat_long_box = json.dumps(
            {'startCorner': start_lat_long, 'endCorner': end_lat_long}, 
            cls=DjangoJSONEncoder)

    return render(request, 'gwells/search.html',
                  {'form': form, 'well_list': well_results,
                   'too_many_wells': well_results_overflow,
                   'wells_json': well_results_json,
                   'lat_long_box': lat_long_box
                  })


def map_well_search(request):
    well_results = None
    well_results_json = '[]'

    if (request.method == 'GET' and 'start_lat_long' in request.GET
            and 'end_lat_long' in request.GET):
        well_results = SearchForm(request.GET)
        if well_results.is_valid():
            well_results = well_results.process()

    if well_results and not len(well_results) > SearchForm.WELL_RESULTS_LIMIT:
        well_results_json = json.dumps(
            [well.as_dict() for well in well_results],
            cls=DjangoJSONEncoder)

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
         ('casing', ActivitySubmissionCasingFormSet),
         ('surface_seal', ActivitySubmissionSurfaceSealForm),
         ('liner', ActivitySubmissionLinerForm),
         ('liner_perforation', ActivitySubmissionLinerPerforationFormSet),
        ]

TEMPLATES = {'type_and_class': 'gwells/activity_submission_form.html',
             'owner': 'gwells/activity_submission_form.html',
             'location': 'gwells/activity_submission_form.html',
             'gps': 'gwells/activity_submission_form.html',
             'lithology': 'gwells/activity_submission_lithology_form.html',
             'casing': 'gwells/activity_submission_casing_form.html',
             'surface_seal': 'gwells/activity_submission_form.html',
             'liner': 'gwells/activity_submission_form.html',
             'liner_perforation': 'gwells/activity_submission_liner_perforation_form.html',
            }



class ActivitySubmissionWizardView(SessionWizardView):
    instance = None

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
        return context

    def get_form_instance(self, step):
        if self.instance is None:
            self.instance = ActivitySubmission()
        return self.instance
    
    def get_form_initial(self, step):
        initial = {}

        if step == 'surface_seal':
            casing_data = self.get_cleaned_data_for_step('casing')
            initial.update({'casing_exists': False})
            if casing_data:
                for casing in casing_data:
                    if casing:
                        initial.update({'casing_exists': True})
                        break
        
        return initial

    def done(self, form_list, form_dict, **kwargs):
        submission = self.instance

        if submission.well_activity_type.code == 'CON' and not submission.well:
            #TODO
            w = submission.create_well()
            w.save()
            submission.well = w
            submission.save()
            lithology_list = form_dict['lithology'].save()
            lithology_list = list(lithology_list)
            for lith in lithology_list:
                lith.pk = None
                lith.activity_submission = None
                lith.well = w
                lith.save()
            casing_list = form_dict['casing'].save()
            casing_list = list(casing_list)
            for casing in casing_list:
                casing.pk = None
                casing.activity_submission = None
                casing.well = w
                casing.save()
            perforation_list = form_dict['liner_perforation'].save()
            perforation_list = list(perforation_list)
            for perforation in perforation_list:
                perforation.pk = None
                perforation.activity_submission = None
                perforation.well = w
                perforation.save()
        else:
            submission.save()
            lithology_list = form_dict['lithology'].save()
            casing_list = form_dict['casing'].save()
            perforation_list = form_dict['liner_perforation'].save()

        return HttpResponseRedirect('/submission/')
