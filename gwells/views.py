from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
#from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
#from django.utils import timezone
from .models import WellYieldUnit, WellActivity, WellOwner
from .forms import SearchForm, WellActivityTypeAndClassForm, WellOwnerForm, WellActivityLocationForm



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
    model = WellActivity
    context_object_name = 'well'



class WellActivityDetailView(generic.DetailView):
    model = WellActivity
    context_object_name = 'well_activity'



class WellActivityCreateView(FormView):
    model = WellActivity
    form_class = WellActivityTypeAndClassForm
    template_name = 'gwells/well_activity_form.html'
    success_url = '/well-activity/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        well_owner_form = WellOwnerForm()
        well_activity_location_form = WellActivityLocationForm()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  well_owner_form=well_owner_form,
                                  well_activity_location_form=well_activity_location_form,
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
        well_owner_form = WellOwnerForm(self.request.POST)
        well_activity_location_form = WellActivityLocationForm(self.request.POST)
        if (form.is_valid() and well_owner_form.is_valid() and well_activity_location_form.is_valid()):
            return self.form_valid(form, well_owner_form, well_activity_location_form)
        else:
            return self.form_invalid(form, well_owner_form, well_activity_location_form)

    def form_valid(self, form, well_owner_form, well_activity_location_form):
        """
        Called if all forms are valid. Creates a WellActivity instance along with
        associated WellOwner, Lithology, etc and then redirects to a
        success page.
        """
        self.object = form.save()
        well_owner_form.instance = self.object
        well_owner_form.save()
        well_activity_location_form.instance = self.object
        well_activity_location_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, well_owner_form, well_activity_location_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  well_owner_form=well_owner_form,
                                  well_activity_location_form=well_activity_location_form,
                                  ))
