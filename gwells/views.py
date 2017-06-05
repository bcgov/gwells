from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
#from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
#from django.utils import timezone
from formtools.wizard.views import SessionWizardView
from .models import WellYieldUnit, Well, ActivitySubmission
from .forms import SearchForm, ActivitySubmissionTypeAndClassForm, WellOwnerForm, ActivitySubmissionLocationForm



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

    if request.method == 'GET' and 'well' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            # process the data in form.cleaned_data
            well_results = form.process()
    else:
        form = SearchForm()

    return render(request, 'gwells/search.html', {'form': form, 'well_list': well_results})  

   

class DetailView(generic.DetailView):
    model = ActivitySubmission
    context_object_name = 'activity_submission'



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
         ('location', ActivitySubmissionLocationForm)]

TEMPLATES = {'type_and_class': 'gwells/activity_submission/type_and_class_form.html',
             'owner': 'gwells/activity_submission/owner_form.html',
             'location': 'gwells/activity_submission/location_form.html'}



class ActivitySubmissionWizardView(SessionWizardView):

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

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
