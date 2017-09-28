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
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
#from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
#from django.utils import timezone
from formtools.wizard.views import SessionWizardView
from .models import WellActivityType, WellYieldUnit, Well, ActivitySubmission, WellClass, ScreenIntake, LandDistrict
from .forms import SearchForm, ActivitySubmissionTypeAndClassForm, WellOwnerForm, ActivitySubmissionLocationForm, ActivitySubmissionGpsForm
from .forms import ActivitySubmissionLithologyFormSet, ActivitySubmissionCasingFormSet, ActivitySubmissionSurfaceSealForm, ActivitySubmissionLinerPerforationFormSet
from .forms import ActivitySubmissionScreenIntakeForm, ActivitySubmissionScreenFormSet, ActivitySubmissionFilterPackForm, ActivitySubmissionDevelopmentForm, ProductionDataFormSet
from .forms import ActivitySubmissionWaterQualityForm, WellCompletionForm, ActivitySubmissionCommentForm
import json
from django.core.serializers.json import DjangoJSONEncoder

def health(request):
    return HttpResponse(WellActivityType.objects.count())

class HomeView(generic.TemplateView):
    template_name = 'gwells/index.html'
    context_object_name = 'yield_unit_list'

    def get_context_data(self, **kwargs):
        """
        Return the context for the page.
        """
        context = super(HomeView, self).get_context_data(**kwargs) 
        context['ENABLE_DATA_ENTRY'] = settings.ENABLE_DATA_ENTRY
        context['ENABLE_GOOGLE_ANALYTICS'] = settings.ENABLE_GOOGLE_ANALYTICS
        return context

def common_well_search(request):
    """
        Returns json and array data for a well search.  Used by both the map and text search.
    """
    well_results = None
    well_results_json = '[]'
   
    form = SearchForm(request.GET)
    if form.is_valid():
        well_results = form.process()

    if well_results and not len(well_results) > SearchForm.WELL_RESULTS_LIMIT:
        well_results_json = json.dumps(
            [well.as_dict() for well in well_results],
            cls=DjangoJSONEncoder)
    return form, well_results, well_results_json

def well_search(request):
    """
        Text search.
    """
    well_results = None
    well_results_overflow = None
    well_results_json = '[]'
    form = None
    lat_long_box = '{}'

    if request.method == 'GET' and 'well' in request.GET:
        # The lat_long_box is returned as a JSON string regardless of the validity of the form,
        # provided the request has both a start_lat_long and an end_lat_long
        if 'start_lat_long' in request.GET and 'end_lat_long' in request.GET:
            start_lat_long = request.GET['start_lat_long']
            end_lat_long = request.GET['end_lat_long']
            lat_long_box = json.dumps(
                {'startCorner': start_lat_long, 'endCorner': end_lat_long}, 
                cls=DjangoJSONEncoder)
        form, well_results, well_results_json = common_well_search(request)
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

    # create an object that will be used to render the names for land districts.
    land_districts = {}
    all_land_districts = LandDistrict.objects.all()
    for land_district in all_land_districts:
        land_districts[land_district.land_district_guid] = land_district.name

    return render(request, 'gwells/search.html',
                  {'form': form, 'well_list': well_results,
                   'too_many_wells': well_results_overflow,
                   'wells_json': well_results_json,
                   'lat_long_box': lat_long_box,
                   'land_districts' : land_districts,
                   'ENABLE_GOOGLE_ANALYTICS' : settings.ENABLE_GOOGLE_ANALYTICS
                  })

def map_well_search(request):
    """
        Map search.
    """
    well_results = None
    well_results_json = '[]'
    form = None
    if (request.method == 'GET' and 'start_lat_long' in request.GET
            and 'end_lat_long' in request.GET):
        form, well_results, well_results_json = common_well_search(request)
    return JsonResponse(well_results_json, safe=False)

class WellDetailView(generic.DetailView):
    model = Well
    context_object_name = 'well'

    def get_context_data(self, **kwargs):
        """
        Return the context for the home page.
        """
        context = super(WellDetailView, self).get_context_data(**kwargs) 
        context['ENABLE_GOOGLE_ANALYTICS'] = settings.ENABLE_GOOGLE_ANALYTICS
        return context


#class DetailView(generic.DetailView):
#    model = ActivitySubmission
#    context_object_name = 'activity_submission'



class ActivitySubmissionListView(generic.ListView):
    model = ActivitySubmission
    context_object_name = 'activity_submission_list'
    template_name = 'gwells/activity_submission_list.html'

    def get_context_data(self, **kwargs):
        """
        Return the context for the page.
        """
        context = super(ActivitySubmissionListView, self).get_context_data(**kwargs) 
        context['ENABLE_GOOGLE_ANALYTICS'] = settings.ENABLE_GOOGLE_ANALYTICS
        return context


class ActivitySubmissionDetailView(generic.DetailView):
    model = ActivitySubmission
    context_object_name = 'activity_submission'
    template_name = 'gwells/activity_submission_detail.html'

    def get_context_data(self, **kwargs):
        """
        Return the context for the page.
        """
        context = super(ActivitySubmissionDetailView, self).get_context_data(**kwargs) 
        context['ENABLE_GOOGLE_ANALYTICS'] = settings.ENABLE_GOOGLE_ANALYTICS
        return context

FORMS = [('type_and_class', ActivitySubmissionTypeAndClassForm),
         ('owner', WellOwnerForm),
         ('location', ActivitySubmissionLocationForm),
         ('gps', ActivitySubmissionGpsForm),
         ('lithology', ActivitySubmissionLithologyFormSet),
         ('casing', ActivitySubmissionCasingFormSet),
         ('surface_seal', ActivitySubmissionSurfaceSealForm),
         ('liner_perforation', ActivitySubmissionLinerPerforationFormSet),
         ('screen_intake', ActivitySubmissionScreenIntakeForm),
         ('screen', ActivitySubmissionScreenFormSet),
         ('filter_pack', ActivitySubmissionFilterPackForm),
         ('development', ActivitySubmissionDevelopmentForm),
         ('production_data', ProductionDataFormSet),
         ('water_quality', ActivitySubmissionWaterQualityForm),
         ('well_completion', WellCompletionForm),
         ('comments', ActivitySubmissionCommentForm),
        ]

TEMPLATES = {'type_and_class': 'gwells/activity_submission_form.html',
             'owner': 'gwells/activity_submission_form.html',
             'location': 'gwells/activity_submission_form.html',
             'gps': 'gwells/activity_submission_form.html',
             'lithology': 'gwells/activity_submission_lithology_form.html',
             'casing': 'gwells/activity_submission_casing_form.html',
             'surface_seal': 'gwells/activity_submission_form.html',
             'liner_perforation': 'gwells/activity_submission_liner_perforation_form.html',
             'screen_intake': 'gwells/activity_submission_form.html',
             'screen': 'gwells/activity_submission_screen_form.html',
             'filter_pack': 'gwells/activity_submission_form.html',
             'development': 'gwells/activity_submission_form.html',
             'production_data': 'gwells/activity_submission_form.html',
             'water_quality': 'gwells/activity_submission_form.html',
             'well_completion': 'gwells/activity_submission_form.html',
             'comments': 'gwells/activity_submission_form.html',
            }



class ActivitySubmissionWizardView(SessionWizardView):
    instance = None

    
    def get_context_data(self, **kwargs):
        """
        Return the context for the page.
        """
        context = super(ActivitySubmissionWizardView, self).get_context_data(**kwargs) 
        context['ENABLE_GOOGLE_ANALYTICS'] = settings.ENABLE_GOOGLE_ANALYTICS
        return context

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(ActivitySubmissionWizardView, self).get_context_data(form=form, **kwargs)
        context['wizard_data'] = self.get_all_cleaned_data()

        if self.steps.current == 'type_and_class' and not 'water_supply_well_class_guid' in context:
            # Get the pk of water supply well class so jquery can show/hide intended water use field
            try:
                water_supply_class = WellClass.objects.get(code='WATR_SPPLY')
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
            # Determine if casing exists so surface seal fields can be validated as required in their clean methods
            casing_data = self.get_cleaned_data_for_step('casing')
            initial.update({'casing_exists': False})
            if casing_data:
                for casing in casing_data:
                    if casing:
                        initial.update({'casing_exists': True})
                        break
        elif step == 'screen':
            # Make at least 1 row of screen required if Screen Intake == Screen on the previous step
            intake_data = self.get_cleaned_data_for_step('screen_intake')
            form_class = self.form_list[step]
            form_class.min_num = 0
            if intake_data and intake_data.get('screen_intake'):
                try:
                    screen_screen_intake = ScreenIntake.objects.get(code='SCREEN')
                except Exception as e:
                    screen_screen_intake = None
                if intake_data.get('screen_intake') == screen_screen_intake:
                    form_class.min_num = 1
        elif step == 'well_completion':
            # Determine well class to decide which fields are required
            initial.update({'well_class_code': ''})
            type_and_class_data = self.get_cleaned_data_for_step('type_and_class')
            if type_and_class_data and type_and_class_data.get('well_class'):
                initial.update({'well_class_code': type_and_class_data.get('well_class').code})
            
        return initial

    def done(self, form_list, form_dict, **kwargs):
        submission = self.instance
        cleaned_data = self.get_all_cleaned_data()
        characteristics_data = cleaned_data.pop('water_quality_characteristics')

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
            screen_list = form_dict['screen'].save()
            screen_list = list(screen_list)
            for screen in screen_list:
                screen.pk = None
                screen.activity_submission = None
                screen.well = w
                screen.save()
            production_list = form_dict['production_data'].save()
            production_list = list(production_list)
            for production in production_list:
                production.pk = None
                production.activity_submission = None
                production.well = w
                production.save()
            for characteristic in characteristics_data:
                submission.water_quality_characteristics.add(characteristic)
                w.water_quality_characteristics.add(characteristic)
        else:
            submission.save()
            lithology_list = form_dict['lithology'].save()
            casing_list = form_dict['casing'].save()
            perforation_list = form_dict['liner_perforation'].save()
            screen_list = form_dict['screen'].save()
            production_list = form_dict['production_data'].save()
            for characteristic in characteristics_data:
                submission.water_quality_characteristics.add(characteristic)

        return HttpResponseRedirect('/submission/')
