from django import forms
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Submit, Hidden, HTML, Field
from crispy_forms.bootstrap import FormActions
from django.forms.models import inlineformset_factory
from .search import Search
from .models import ActivitySubmission

class SearchForm(forms.Form):
    well = forms.IntegerField(
        label=mark_safe('Well Tag Number or Well Identification Plate Number <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Well electronic filing number or physical identification plate number"> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'example: 123456'}),
    )

    addr = forms.CharField(
        label=mark_safe('Street Address <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="For best results, try searching using the street name only."> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: 123 main'}),
    )

    legal = forms.CharField(
        label=mark_safe('Legal Plan or District Lot or PID <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Find the legal plan, district lot, or 9-digit PID (parcel identifier) on the property assessment, property tax notice, or real estate transaction."> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: 123a'}),
    )

    owner = forms.CharField(
        label=mark_safe('Owner Name <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="The owner name is usually the name of the well owner at time of drilling."> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
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
                Submit('s', 'Search'),
                HTML('<a class="btn btn-default" href="{% url \'search\' %}">Reset</a>'),
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



class WellOwnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Owner Information',
                Div(
                    Div(Field('owner_full_name', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div(Field('owner_mailing_address', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div(Field('owner_city', css_class='city'), css_class='col-sm-3'),
                    Div('owner_province_state', css_class='col-sm-1'),
                    Div(Field('owner_postal_code', css_class='postal'), css_class='col-sm-8'),
                    css_class='row',
                ),
            )
        )
        super(WellOwnerForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = ActivitySubmission
        fields = ['owner_full_name', 'owner_mailing_address', 'owner_city', 'owner_province_state', 'owner_postal_code']



class ActivitySubmissionTypeAndClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Div(Field('well_activity_type', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div('well_class', css_class='col-sm-3'),
                    #Div('well_subclass', css_class='col-sm-3'),
                    Div('intended_water_use', css_class='col-sm-6'),
                    css_class='row',
                ),
                Div(
                    Div(Field('driller_responsible', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div(Field('driller_name', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div(Field('consultant_name', css_class='name'), css_class='col-sm-4'),
                    Div(Field('consultant_company', css_class='name'), css_class='col-sm-8'),
                    css_class='row',
                ),
                Div(
                    Div('work_start_date', css_class='col-sm-6'),
                    Div('work_end_date', css_class='col-sm-6'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionTypeAndClassForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = ActivitySubmission
        fields = ['well_activity_type', 'well_class', 'intended_water_use', 'driller_responsible', 'driller_name', 'consultant_name', 'consultant_company', 'work_start_date', 'work_end_date']


class ActivitySubmissionLocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Well Location',
                Div(
                    Div(Field('street_address', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div(Field('city', css_class='city'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div('legal_lot', css_class='col-sm-3'),
                    Div('legal_plan', css_class='col-sm-3'),
                    Div('legal_district_lot', css_class='col-sm-3'),
                    Div('legal_block', css_class='col-sm-3'),
                    css_class='row',
                ),
                Div(
                    Div('legal_section', css_class='col-sm-3'),
                    Div('legal_township', css_class='col-sm-3'),
                    Div('legal_range', css_class='col-sm-3'),
                    Div('legal_land_district', css_class='col-sm-3'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionLocationForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = ActivitySubmission
        fields = ['street_address', 'city', 'legal_lot', 'legal_plan', 'legal_district_lot', 'legal_block', 'legal_section', 'legal_township', 'legal_range', 'legal_land_district']


class ActivitySubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Div(Field('well_activity_type', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div('well_class', css_class='col-sm-3'),
                    Div('well_subclass', css_class='col-sm-3'),
                    Div('intended_water_use', css_class='col-sm-6'),
                    css_class='row',
                ),
                Div(
                    Div(Field('driller_responsible', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div(Field('driller_name', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div(Field('consultant_name', css_class='name'), css_class='col-sm-4'),
                    Div(Field('consultant_company', css_class='name'), css_class='col-sm-8'),
                    css_class='row',
                ),
                Div(
                    Div('work_start_date', css_class='col-sm-6'),
                    Div('work_end_date', css_class='col-sm-6'),
                    css_class='row',
                ),
            ),
            Fieldset(
                'Owner Information',
                Div(
                    Div(Field('owner_full_name', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div(Field('owner_mailing_address', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div(Field('owner_city', css_class='city'), css_class='col-sm-3'),
                    Div('owner_province_state', css_class='col-sm-1'),
                    Div(Field('owner_postal_code', css_class='postal'), css_class='col-sm-8'),
                    css_class='row',
                ),
            ),
            Fieldset(
                'Well Location',
                Div(
                    Div(Field('street_address', css_class='name'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div(Field('city', css_class='city'), css_class='col-sm-12'),
                    css_class='row',
                ),
                Div(
                    Div('legal_lot', css_class='col-sm-3'),
                    Div('legal_plan', css_class='col-sm-3'),
                    Div('legal_district_lot', css_class='col-sm-3'),
                    Div('legal_block', css_class='col-sm-3'),
                    css_class='row',
                ),
                Div(
                    Div('legal_section', css_class='col-sm-3'),
                    Div('legal_township', css_class='col-sm-3'),
                    Div('legal_range', css_class='col-sm-3'),
                    Div('legal_land_district', css_class='col-sm-3'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = ActivitySubmission
        fields = ['well_activity_type', 'well_class', 'intended_water_use', 'driller_responsible', 'driller_name', 'consultant_name', 'consultant_company', 'work_start_date', 'work_end_date',
            'owner_full_name', 'owner_mailing_address', 'owner_city', 'owner_province_state', 'owner_postal_code',
            'street_address', 'city', 'legal_lot', 'legal_plan', 'legal_district_lot', 'legal_block', 'legal_section', 'legal_township', 'legal_range', 'legal_land_district']



#WellCompletionDataFormSet = inlineformset_factory(ActivitySubmission, WellCompletionData, max_num=1, can_delete=False)
#LithologyFormSet = inlineformset_factory(ActivitySubmission, Lithology, extra=5)