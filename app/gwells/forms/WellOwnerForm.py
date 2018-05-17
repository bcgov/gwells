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

class WellOwnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Owner Information',
                Div(
                    Div('owner_full_name', css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('owner_mailing_address', css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('owner_city', css_class='col-md-3 city'),
                    Div('owner_province_state', css_class='col-md-1'),
                    Div('owner_postal_code', css_class='col-md-3 postal'),
                    css_class='row',
                ),
            )
        )
        super(WellOwnerForm, self).__init__(*args, **kwargs)
        # Make fields required on the form even though they are not required in the DB due to legacy data issues
        # TODO - check admin or staff user and don't make these fields required
        self.fields['owner_postal_code'].required = True

        # display code instead of the value from __str__ in the model
        self.fields['owner_province_state'].label_from_instance = self.label_from_instance_code
        try:
            bc = ProvinceStateCode.objects.get(code='BC')
            self.initial['owner_province_state'] = bc
            self.fields['owner_province_state'].empty_label = None
        except Exception as e:
            pass

    @staticmethod
    def label_from_instance_code(obj):
        return obj.code

    class Meta:
        model = ActivitySubmission
        fields = ['owner_full_name', 'owner_mailing_address', 'owner_city', 'owner_province_state', 'owner_postal_code']
