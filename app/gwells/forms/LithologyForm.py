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

class LithologyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        self.helper.render_required_fields = True
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            HTML('<tr valign="top">'),
            HTML('<td width="6%">'),
            'lithology_from',
            HTML('</td>'),
            HTML('<td width="6%">'),
            'lithology_to',
            HTML('</td>'),
            HTML('<td>'),
            'surficial_material',
            HTML('</td>'),
            HTML('<td>'),
            'secondary_surficial_material',
            HTML('</td>'),
            HTML('<td>'),
            'bedrock_material',
            HTML('</td>'),
            HTML('<td>'),
            'bedrock_material_descriptor',
            HTML('</td>'),
            HTML('<td>'),
            'lithology_structure',
            HTML('</td>'),
            HTML('<td>'),
            'lithology_colour',
            HTML('</td>'),
            HTML('<td>'),
            'lithology_hardness',
            HTML('</td>'),
            HTML('<td>'),
            'lithology_moisture',
            HTML('</td>'),
            HTML('<td>'),
            'water_bearing_estimated_flow',
            HTML('</td>'),
            HTML('<td>'),
            'lithology_observation',
            HTML('</td><td width="5%">{% if form.instance.pk %}{{ form.DELETE }}{% endif %}</td>'),
            HTML('</tr>'),
        )
        super(LithologyForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LithologyForm, self).clean()

        lithology_from = cleaned_data.get('lithology_from')
        lithology_to = cleaned_data.get('lithology_to')
        surficial_material = cleaned_data.get('surficial_material')
        bedrock_material = cleaned_data.get('bedrock_material')
        errors = []

        if lithology_from and lithology_to and lithology_to < lithology_from:
            errors.append('To must be greater than or equal to From.')

        if not surficial_material and not bedrock_material:
            errors.append('Surficial Material or Bedrock is required.')

        if bedrock_material:
            lithology_moisture = cleaned_data.get('lithology_moisture')
            water_bearing_estimated_flow = cleaned_data.get('water_bearing_estimated_flow')
            try:
                if lithology_moisture == LithologyMoistureCode.objects.get(code='Water Bear') and not water_bearing_estimated_flow:
                    errors.append('Water Bearing Estimated Flow is required for Water Bearing Bedrock.')
            except Exception as e:
                errors.append('Configuration error: Water Bearing Lithology Moisture does not exist, please contact the administrator.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = LithologyDescription
        fields = ['lithology_from', 'lithology_to', 'surficial_material', 'secondary_surficial_material', 'bedrock_material', 'bedrock_material_descriptor', 'lithology_structure', 'lithology_colour', 'lithology_hardness', 'lithology_moisture', 'water_bearing_estimated_flow', 'lithology_observation']
