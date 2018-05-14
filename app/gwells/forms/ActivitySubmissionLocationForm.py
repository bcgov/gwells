"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from django import forms
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Submit, Hidden, HTML, Field
from crispy_forms.bootstrap import FormActions, AppendedText, InlineRadios
from django.forms.models import inlineformset_factory
from ..models import *
from datetime import date

class ActivitySubmissionLocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Well Location',
                Div(
                    Div(HTML('Please provide as much well location information as possible. A minimum of one type of well location information is required below.<br /><br />'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('<label>1) Civic Address</label>'), css_class='col-md-2'),
                    Div(HTML('<input type="checkbox" id="chkSameAsOwnerAddress" /> <label for="chkSameAsOwnerAddress">Same as Owner Address</label>'), css_class='col-md-10'),
                    css_class='row',
                ),
                Div(
                    Div('street_address', css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('city', css_class='col-md-4 city'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('OR'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('&nbsp;'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('<label>2) Legal Description</label>'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div('legal_lot', css_class='col-md-2 city'),
                    Div('legal_plan', css_class='col-md-2 city'),
                    Div('legal_district_lot', css_class='col-md-2 city'),
                    Div('legal_block', css_class='col-md-2 city'),
                    css_class='row',
                ),
                Div(
                    Div('legal_section', css_class='col-md-2 city'),
                    Div('legal_township', css_class='col-md-2 city'),
                    Div('legal_range', css_class='col-md-2 city'),
                    Div('land_district', css_class='col-md-2 city'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('OR'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('&nbsp;'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('<label>3) Parcel Identifier</label>'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div('legal_pid', css_class='col-md-2'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('&nbsp;'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('&nbsp;'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div('well_location_description', css_class='col-md-8'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionLocationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ActivitySubmissionLocationForm, self).clean()

        street_address = cleaned_data.get('street_address')
        city = cleaned_data.get('city')
        address_provided = street_address and city

        legal_lot = cleaned_data.get('legal_lot')
        legal_plan = cleaned_data.get('legal_plan')
        land_district = cleaned_data.get('land_district')
        legal_provided = legal_lot and legal_plan and land_district

        if not address_provided and not legal_provided and not cleaned_data.get('legal_pid'):
            raise forms.ValidationError('At least 1 of Civic Address, Legal Description (Lot, Plan and Land District) or Parcel Identifier must be provided.')
        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['street_address', 'city', 'legal_lot', 'legal_plan', 'legal_district_lot', 'legal_block', 'legal_section', 'legal_township', 'legal_range', 'land_district', 'legal_pid', 'well_location_description']
        help_texts = {'well_location_description': "Provide any additional well location details, such as physical landmarks",}
