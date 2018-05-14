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

class ActivitySubmissionScreenIntakeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Fieldset(
                'Screen Information',
                Div(
                    Div('screen_intake_method', css_class='col-md-2'),
                    css_class='row',
                ),
                Div(
                    Div('screen_type', css_class='col-md-2'),
                    Div('screen_material', css_class='col-md-2'),
                    Div('other_screen_material', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div('screen_opening', css_class='col-md-2'),
                    Div('screen_bottom', css_class='col-md-2'),
                    Div('other_screen_bottom', css_class='col-md-3'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionScreenIntakeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ActivitySubmissionScreenIntakeForm, self).clean()

        screen_intake_method = cleaned_data.get('screen_intake_method')
        screen_type = cleaned_data.get('screen_type')
        screen_material = cleaned_data.get('screen_material')
        other_screen_material = cleaned_data.get('other_screen_material')
        screen_opening = cleaned_data.get('screen_opening')
        screen_bottom = cleaned_data.get('screen_bottom')
        other_screen_bottom = cleaned_data.get('other_screen_bottom')
        errors = []

        screen_intake_method = None
        try:
            screen_intake_method = ScreenIntakeMethodCode.objects.get(code='SCREEN')
        except Exception as e:
            errors.append('Configuration error: Intake Method for Screen does not exist, please contact the administrator.')

        if screen_intake_method:
            if screen_intake_method == screen_screen_intake and not screen_type:
                self.add_error('screen_type', 'This field is required if Intake is a Screen.')

            if screen_intake_method == screen_screen_intake and not screen_material:
                self.add_error('screen_material', 'This field is required if Intake is a Screen.')

            if screen_intake_method == screen_screen_intake and not screen_opening:
                self.add_error('screen_opening', 'This field is required if Intake is a Screen.')

            if screen_intake_method == screen_screen_intake and not screen_bottom:
                self.add_error('screen_bottom', 'This field is required if Intake is a Screen.')

        try:
            if screen_material == ScreenMaterialCode.objects.get(code='OTHER') and not other_screen_material:
                self.add_error('other_screen_material', 'This field is required.')
        except Exception as e:
            errors.append('Configuration error: Other Screen Material does not exist, please contact the administrator.')

        try:
            if screen_bottom == ScreenBottomCode.objects.get(code='OTHER') and not other_screen_bottom:
                self.add_error('other_screen_bottom', 'This field is required.')
        except Exception as e:
            errors.append('Configuration error: Other Screen Bottom does not exist, please contact the administrator.')


        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['screen_intake_method', 'screen_type', 'screen_material', 'other_screen_material', 'screen_opening', 'screen_bottom', 'other_screen_bottom']
