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

class ActivitySubmissionWaterQualityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Water Quality',
                Div(
                    Div('water_quality_characteristics', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div('water_quality_colour', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div('water_quality_odour', css_class='col-md-3'),
                    css_class='row',
                ),
            )
        )

        super(ActivitySubmissionWaterQualityForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ActivitySubmission
        fields = ['water_quality_characteristics', 'water_quality_colour', 'water_quality_odour']
        widgets = {'water_quality_characteristics': forms.CheckboxSelectMultiple}
