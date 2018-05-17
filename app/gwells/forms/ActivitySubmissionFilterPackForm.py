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

class ActivitySubmissionFilterPackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Filter Pack',
                Div(
                    Div(AppendedText('filter_pack_from', 'ft'), css_class='col-md-2'),
                    Div(AppendedText('filter_pack_to', 'ft'), css_class='col-md-2'),
                    Div(AppendedText('filter_pack_thickness', 'in'), css_class='col-md-2'),
                    css_class='row',
                ),
                Div(
                    Div('filter_pack_material', css_class='col-md-3'),
                    Div('filter_pack_material_size', css_class='col-md-3'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionFilterPackForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ActivitySubmissionFilterPackForm, self).clean()

        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['filter_pack_from', 'filter_pack_to', 'filter_pack_thickness', 'filter_pack_material', 'filter_pack_material_size']
