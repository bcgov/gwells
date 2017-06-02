from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
#from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
#from django.utils import timezone
from formtools.wizard.views import SessionWizardView
from .models import WellYieldUnit, Well, ActivitySubmission
from .forms import SearchForm, ActivitySubmissionTypeAndClassForm, WellOwnerForm, ActivitySubmissionLocationForm
from .forms import ActivitySubmissionForm



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



class ActivitySubmissionWizardView(SessionWizardView):
    form_list = [ActivitySubmissionTypeAndClassForm, WellOwnerForm, ActivitySubmissionLocationForm]
    template_name = 'gwells/activity_submission_form.html'

    def done(self, form_list, **kwargs):
        submission = ActivitySubmission()
        for form in form_list:
            for field, value in form.cleaned_data.items():
                setattr(submission, field, value)

        if submission.well_activity_type.code == 'CON' and submission.well is None:
            #TODO
            #w = submission.createWell()
            #w = w.save()
            #submission.well = w
            submission.save()
        else:
            submission.save()

        #lithology = form_dict['lithology'].save()
        return HttpResponseRedirect('/submission/')


class ActivitySubmissionCreateView(FormView):
    model = ActivitySubmission
    form_class = ActivitySubmissionForm
    template_name = 'gwells/activity_submission_form.html'
    success_url = '/submission/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #well_activity_location_form = WellActivityLocationForm()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  #well_activity_location_form=well_activity_location_form,
                                  ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #well_activity_location_form = WellActivityLocationForm(self.request.POST)
        #if (form.is_valid() and lithology_description.is_valid() and well_activity_location_form.is_valid()):
        #    return self.form_valid(form, lithology_description, well_activity_location_form)
        #else:
        #    return self.form_invalid(form, lithology_description, well_activity_location_form)
        if (form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Called if all forms are valid. Creates a WellActivity instance along with
        associated WellOwner, Lithology, etc and then redirects to a
        success page.
        """
        self.object = form.save()
        
        #full_name = form.cleaned_data.get('full_name')
        #mailing_address = form.cleaned_data.get('mailing_address')
        #city = form.cleaned_data.get('city')
        #province_state = form.cleaned_data.get('province_state')
        #postal_code = form.cleaned_data.get('postal_code')
        #well_owner = WellOwner(full_name=full_name, mailing_address=mailing_address, city=city, province_state=province_state, postal_code=postal_code)
        #well_owner.save()

        #well_activity_location_form.instance = self.object
        #well_activity_location_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  #well_activity_location_form=well_activity_location_form,
                                  ))
