from django import forms
from .models import Well

class SearchForm(forms.Form):
    q = forms.CharField(label='', min_length=2, max_length=100, required=False, widget=forms.TextInput(attrs={'size':40}))

    def process(self):
        query = self.cleaned_data.get('q')
        wellresults = None

        return wellresults