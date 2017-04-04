from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
#from django.urls import reverse
from django.views import generic
from django.utils import timezone

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
   
   
   
#class SearchResultsView(generic.ListView):
#    template_name = 'gwells/searchresults.html'
#    context_object_name = 'search_results'

#    def get_queryset(self):
#        """
#        Return the search results.
#        """
#        return Well.objects.annotate(
#		    search=SearchVector('street_name')
#		).filter(search='Main st')



#class WellView(generic.DetailView):
#    model = Well
#    template_name = 'gwells/well.html'
#    context_object_name = 'well'

#    def get_queryset(self):
#        """
#        Return the details of a well record.
#        """
#        return Well.objects.filter(
#            last_modified__lte=timezone.now()
#        ).order_by('-last_modified')[:5]



