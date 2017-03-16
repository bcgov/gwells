from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
#from django.urls import reverse
from django.views import generic
from django.utils import timezone
#from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from .models import WellYieldUnit, Well
from .forms import SearchForm



class HelloWorldView(generic.ListView):
    template_name = 'gwells/index.html'
    context_object_name = 'helloworld'

    def get_queryset(self):
        """
        Return the well yield units for hello world.
        """
        return WellYieldUnit.objects.order_by('-sort_order')



def well_search(request):
    wellresults = None
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            #TODO
            # process the data in form.cleaned_data
            wellresults = form.process()
            #pass
    
    else:
        form = SearchForm()

    return render(request, 'gwells/search.html', {'form': form, 'wellresults': wellresults})
   
   
   
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



