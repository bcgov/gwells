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


class ActivitySubmissionCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'General Comments',
                Div(
                    Div('comments', css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div('alternative_specs_submitted', css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('<p style="font-style: italic;">Declaration: By submitting this well construction, alteration or decommission report, as the case may be, I declare that it has been done in accordance with the requirements of the Water Sustainability Act and the Groundwater Protection Regulation.</p>'), css_class='col-md-12'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionCommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ActivitySubmission
        fields = ['comments', 'alternative_specs_submitted']
        widgets = {'comments': forms.Textarea}
