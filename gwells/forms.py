from django import forms
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Hidden
from crispy_forms.bootstrap import FormActions
from .search import Search

class SearchForm(forms.Form):
    well = forms.IntegerField(
        label=mark_safe('Well Tag Number or Well Identification Plate Number <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Well electronic filing number or physical identification plate number"> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'example: 123456'}),
    )

    addr = forms.CharField(
        label='Street Address',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: 123 main st'}),
    )

    legal = forms.CharField(
        label=mark_safe('Legal Plan, District Lot or PID <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Find the legal plan, district lot, or PID (parcel identifier) on the property assessment, property tax notice, or real estate transaction."> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: 123a'}),
    )

    owner = forms.CharField(
        label='Owner Name',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: Smith or smi'}),
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
                'owner',
                Hidden('sort', 'well_tag_number'),
                Hidden('dir', 'asc')
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