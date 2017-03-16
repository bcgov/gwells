from django import forms
#from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .models import Well

class SearchForm(forms.Form):
    q = forms.CharField(label='', min_length=2, max_length=100, required=False, widget=forms.TextInput(attrs={'size':40}))

    def process(self):
        query = self.cleaned_data.get('q')
        wellresults = None
        #wellresults = Well.objects.annotate(
		#    search=SearchVector('street_name')
		#).filter(search=query)
        return wellresults