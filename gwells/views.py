from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
#from django.urls import reverse
from django.views import generic
#from django.utils import timezone
from .models import WellYieldUnit, Well
from .forms import SearchForm



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
    model = Well
    context_object_name = 'well'




