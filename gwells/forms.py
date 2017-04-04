from django import forms
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions
from django.db.models import Q
#from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .models import Well
from .search import Search

class SearchForm(forms.Form):
    well = forms.IntegerField(
        label=mark_safe('Well Number <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Enter the Identification Plate Number or Tag Number"> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'example: 123456'}),
        #help_text='Enter the Identification Plate Number or Tag Number',
    )

    addr = forms.CharField(
        label='Street Address',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: 123 main st'}),
    )

    legal = forms.CharField(
        label=mark_safe('Legal Description <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Enter one of Lot, Plan, District Lot or PID"> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: 123a'}),
        #help_text='Enter one of Lot, Plan, District Lot or PID',
    )

    owner = forms.CharField(
        label=mark_safe('Owner Name <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Enter part of the Owner\'s name"> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        max_length=100,
        required=False,
        #help_text='Enter part of the Owner\'s name',
    )
    

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'get'
        helper.form_action = ''

        helper.layout = Layout(
            Fieldset(
                '',
                'well',
                'addr',
                'legal',
                'owner'
            ),
            FormActions(
                Submit('s', 'Search')
            )
        )

        return helper



    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        well = cleaned_data.get('well')
        addr = cleaned_data.get('addr')
        legal = cleaned_data.get('legal')
        owner = cleaned_data.get('owner')

        if not well and not addr and not legal and not owner:
            raise forms.ValidationError(
                "At least 1 search field is required."
            )



    def process(self):
        well_results = None
        
        well = self.cleaned_data.get('well')
        addr = self.cleaned_data.get('addr')
        legal = self.cleaned_data.get('legal')
        owner = self.cleaned_data.get('owner')
        
        well_results = Search.well_search(well, addr, legal, owner)

            
        return well_results