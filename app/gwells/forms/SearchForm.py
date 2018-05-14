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
from ..search import Search

class SearchForm(forms.Form):
    well = forms.IntegerField(
        label=mark_safe('Well Tag Number or Well Identification Plate Number <a id="well_tag_question" href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Well electronic filing number or physical identification plate number"> \
            <em class="fa fa-question-circle" style="color:blue"></em></a>'),
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'example: 123456'}),
    )

    addr = forms.CharField(
        label=mark_safe('Street Address <a id="address_question" href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="For best results, try searching using the street name only."> \
            <em class="fa fa-question-circle" style="color:blue"></em></a>'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: 123 main'}),
    )

    legal = forms.CharField(
        label=mark_safe('Legal Plan or District Lot or Parcel Identification Number (PID) <a id="legal_id_question" href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Find the legal plan, district lot, or 9-digit PID (parcel identifier) on the property assessment, property tax notice, or real estate transaction."> \
            <em class="fa fa-question-circle" style="color:blue"></em></a>'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: 123a'}),
    )

    owner = forms.CharField(
        label=mark_safe('Owner Name <a id="owner_question" href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="The owner name is usually the name of the well owner at time of drilling."> \
            <em class="fa fa-question-circle" style="color:blue"></em></a>'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: Smith or smi'}),
    )

    start_lat_long = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    end_lat_long = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    WELL_RESULTS_LIMIT = 1000

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = 'id-searchForm'
        helper.form_method = 'get'
        helper.form_action = ''

        helper.layout = Layout(
            Fieldset(
                '',
                'well',
                'addr',
                'legal',
                'owner',
                # start_lat_long and end_lat_long are programatically generated
                # based on an identifyWells operation on the client.
                Hidden('start_lat_long', ''),
                Hidden('end_lat_long', ''),
            ),
            FormActions(
                Submit('s', 'Search', css_class='formButtons'),
                HTML('<a class="btn btn-default" id="reset-id-s" href="{% url \'search\' %}">Reset</a>'),
                )
        )

        return helper


    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        well = cleaned_data.get('well')
        addr = cleaned_data.get('addr')
        legal = cleaned_data.get('legal')
        owner = cleaned_data.get('owner')
        # start_lat_long and end_lat_long are programatically-generated, and
        # should consist of a dictionary of a comma-separated list consisting
        # of two floats that comprise latitude and longitude. They are used
        # in the identifyWells operation to query all wells whose lat/long info
        # place them within a user-drawn rectangle on the search page map.
        start_lat_long = cleaned_data.get('start_lat_long')
        end_lat_long = cleaned_data.get('end_lat_long')

        # If only one of the rectangle's points exist, we cannot perform the query.
        if bool(start_lat_long) != bool(end_lat_long):
            raise forms.ValidationError(
                "Identify Wells operation did not provide sufficient data. "
                "The map may not accurately reflect query results."
            )
        if (not well and not addr and not legal and
                not owner and not (start_lat_long and end_lat_long)):
            raise forms.ValidationError(
                "At least 1 search field is required."
            )

    def process(self):
        well_results = None

        well = self.cleaned_data.get('well')
        addr = self.cleaned_data.get('addr')
        legal = self.cleaned_data.get('legal')
        owner = self.cleaned_data.get('owner')
        start_lat_long = self.cleaned_data.get('start_lat_long')
        end_lat_long = self.cleaned_data.get('end_lat_long')
        lat_long_box = {'start_corner': start_lat_long, 'end_corner': end_lat_long}

        well_results = Search.well_search(well, addr, legal, owner, lat_long_box, self.WELL_RESULTS_LIMIT)

        return well_results
