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


class WellCompletionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Well Completion Details',
                Div(
                    Div(AppendedText('total_depth_drilled', 'ft'), css_class='col-md-3'),
                    Div(AppendedText('finished_well_depth', 'ft (bgl)'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('final_casing_stick_up', 'in'), css_class='col-md-3'),
                    Div(AppendedText('bedrock_depth', 'ft (bgl)'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('static_water_level', 'ft (btoc)'), css_class='col-md-3'),
                    Div(AppendedText('well_yield', 'USgpm'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('artesian_flow', 'USgpm'), css_class='col-md-3'),
                    Div(AppendedText('artesian_pressure', 'ft'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div('well_cap_type', css_class='col-md-3'),
                    Div(InlineRadios('well_disinfected'), css_class='col-md-3'),
                    css_class='row',
                ),
            )
        )
        super(WellCompletionForm, self).__init__(*args, **kwargs)
        # Make fields required on the form even though they are not required in the DB due to legacy data issues
        # TODO - check admin or staff user and don't make these fields required
        self.fields['total_depth_drilled'].required = True
        self.fields['finished_well_depth'].required = True

        # Make final casing stick up required for water supply well, injection well, recharge well, etc.
        if self.initial['well_class_code'] == 'WATR_SPPLY' or self.initial['well_class_code'] == 'INJECTION' or self.initial['well_class_code'] == 'RECHARGE':
            self.fields['final_casing_stick_up'].required = True

    def clean(self):
        cleaned_data = super(WellCompletionForm, self).clean()

        total_depth_drilled = cleaned_data.get('total_depth_drilled')
        finished_well_depth = cleaned_data.get('finished_well_depth')
        errors = []

        if total_depth_drilled and finished_well_depth and total_depth_drilled < finished_well_depth:
            errors.append('Finished Well Depth can\'t be greater than Total Depth Drilled.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['total_depth_drilled', 'finished_well_depth', 'final_casing_stick_up', 'bedrock_depth', 'static_water_level', 'well_yield', 'artesian_flow', 'artesian_pressure', 'well_cap_type', 'well_disinfected']
        widgets = {'well_disinfected': forms.RadioSelect}
