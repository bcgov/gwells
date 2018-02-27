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

class ActivitySubmissionTypeAndClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Type of Work and Well Class',
                Div(
                    Div('well_activity_type', css_class='col-md-4'),
                    Div(HTML('<label for="units">Measurement units for data entry</label><br /><input type="radio" name="units" value="Imperial" checked /> Imperial<br /><input type="radio" name="units" value="Metric" disabled /> Metric<br /><br />'), css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('well_class', css_class='col-md-4'),
                    Div(Div('well_subclass', id='divSubclass'), Div('intended_water_use', id='divIntendedWaterUseCode'), css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('identification_plate_number', css_class='col-md-4'),
                    Div('well_plate_attached', css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('driller_responsible', css_class='col-md-4'),
                    Div('driller_name', css_class='col-md-4'),
                    Div(HTML('<input type="checkbox" id="chkSameAsPersonResponsible" /> <label for="chkSameAsPersonResponsible">Same as Person Responsible for Drilling</label>'), css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('consultant_name', css_class='col-md-4'),
                    Div('consultant_company', css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('work_start_date', css_class='col-md-4 date'),
                    Div('work_end_date', css_class='col-md-4 date'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionTypeAndClassForm, self).__init__(*args, **kwargs)

        try:
            con = WellActivityCode.objects.get(code='CON')
            self.initial['well_activity_type'] = con
            self.fields['well_activity_type'].empty_label = None
        except Exception as e:
            pass

    def clean_work_start_date(self):
        work_start_date = self.cleaned_data.get('work_start_date')
        if work_start_date > date.today():
            raise forms.ValidationError('Work start date cannot be in the future.')
        return work_start_date

    def clean(self):
        cleaned_data = super(ActivitySubmissionTypeAndClassForm, self).clean()
        identification_plate_number = cleaned_data.get('identification_plate_number')
        well = cleaned_data.get('well_plate_attached')
        work_start_date = cleaned_data.get('work_start_date')
        work_end_date = cleaned_data.get('work_end_date')

        errors = []

        if identification_plate_number and not well:
            errors.append('Well Identification Plate Is Attached is required when specifying Identification Plate Number.')

        if work_start_date and work_end_date and work_end_date < work_start_date:
            errors.append('Work End Date cannot be earlier than Work Start Date.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    def save(self, commit=True):
        instance = super(ActivitySubmissionTypeAndClassForm, self).save(commit=False)
        # Force subclass to None for closed loop geo-exchange
        if instance.well_class.well_class_code == 'CLS_LP_GEO':
            instance.well_subclass = None
        if commit:
            instance.save()
        return instance

    class Meta:
        model = ActivitySubmission
        fields = ['well_activity_type', 'well_class', 'well_subclass', 'intended_water_use', 'identification_plate_number', 'well_plate_attached', 'driller_responsible', 'driller_name', 'consultant_name', 'consultant_company', 'work_start_date', 'work_end_date']
        help_texts = {'work_start_date': "yyyy-mm-dd", 'work_end_date': "yyyy-mm-dd",}
        widgets = {'well_activity_type': forms.RadioSelect}
