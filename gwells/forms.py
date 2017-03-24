from django import forms
#from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .models import Well

class SearchForm(forms.Form):
    q = forms.CharField(label='', min_length=2, max_length=100, required=False, widget=forms.TextInput(attrs={'size':40}))

    def process(self):
        wellresults = None
        
        query = self.cleaned_data.get('q')
        
        if (len(query) > 1):
            wellresults = Well.objects.all().filter(address_line__icontains=query).order_by('-id')
            
            #wellresults = Well.objects.annotate(
            #    search=SearchVector('address_line')
            #    ).filter(search=query)
        
        return wellresults