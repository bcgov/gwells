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

class ActivitySubmissionSurfaceSealForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Fieldset(
                'Surface Seal and Backfill Information',
                Div(
                    Div('surface_seal_material', css_class='col-md-3'),
                    Div(AppendedText('surface_seal_depth', 'ft'), css_class='col-md-2'),
                    Div(AppendedText('surface_seal_thickness', 'in'), css_class='col-md-2'),
                    css_class='row',
                ),
                Div(
                    Div('surface_seal_method', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('&nbsp;'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div('backfill_above_surface_seal', css_class='col-md-3'),
                    Div(AppendedText('backfill_above_surface_seal_depth', 'ft'), css_class='col-md-2'),
                    css_class='row',
                ),
            ),
            Fieldset(
                'Liner Information',
                Div(
                    Div('liner_material', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('liner_diameter', 'in'), css_class='col-md-2'),
                    Div(AppendedText('liner_thickness', 'in'), css_class='col-md-2'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('liner_from', 'ft (bgl)'), css_class='col-md-2'),
                    Div(AppendedText('liner_to', 'ft (bgl)'), css_class='col-md-2'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionSurfaceSealForm, self).__init__(*args, **kwargs)

    def clean_surface_seal_material(self):
        surface_seal_material = self.cleaned_data.get('surface_seal_material')

        if self.initial['casing_exists'] and not surface_seal_material:
            raise forms.ValidationError('This field is required.');

    def clean_surface_seal_depth(self):
        surface_seal_depth = self.cleaned_data.get('surface_seal_depth')

        if self.initial['casing_exists'] and not surface_seal_depth:
            raise forms.ValidationError('This field is required.');

    def clean_surface_seal_thickness(self):
        surface_seal_thickness = self.cleaned_data.get('surface_seal_thickness')

        if self.initial['casing_exists'] and not surface_seal_thickness:
            raise forms.ValidationError('This field is required.');

    def clean_surface_seal_method(self):
        surface_seal_method = self.cleaned_data.get('surface_seal_method')

        if self.initial['casing_exists'] and not surface_seal_method:
            raise forms.ValidationError('This field is required.');

    def clean(self):
        cleaned_data = super(ActivitySubmissionSurfaceSealForm, self).clean()

        liner_from = cleaned_data.get('liner_from')
        liner_to = cleaned_data.get('liner_to')
        errors = []

        if liner_from and liner_to and liner_to < liner_from:
            errors.append('Liner To must be greater than or equal to From.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['surface_seal_material', 'surface_seal_depth', 'surface_seal_thickness', 'surface_seal_method', 'backfill_above_surface_seal', 'backfill_above_surface_seal_depth', 'liner_material', 'liner_diameter', 'liner_thickness', 'liner_from', 'liner_to']
