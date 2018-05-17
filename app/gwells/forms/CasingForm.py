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

class CasingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        self.helper.render_required_fields = True
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            HTML('<tr valign="top">'),
            HTML('<td width="5%">'),
            'casing_from',
            HTML('</td>'),
            HTML('<td width="5%">'),
            'casing_to',
            HTML('</td>'),
            HTML('<td width="10%">'),
            'diameter',
            HTML('</td>'),
            HTML('<td>'),
            'casing_code',
            HTML('</td>'),
            HTML('<td>'),
            'casing_material',
            HTML('</td>'),
            HTML('<td width="10%">'),
            'wall_thickness',
            HTML('</td>'),
            HTML('<td>'),
            InlineRadios('drive_shoe'),
            HTML('</td><td width="5%">{% if form.instance.pk %}{{ form.DELETE }}{% endif %}</td>'),
            HTML('</tr>'),
        )
        super(CasingForm, self).__init__(*args, **kwargs)

        self.fields['drive_shoe'].label = False

    def clean(self):
        cleaned_data = super(CasingForm, self).clean()

        casing_from = cleaned_data.get('casing_from')
        casing_to = cleaned_data.get('casing_to')
        casing_code = cleaned_data.get('casing_code')
        casing_material = cleaned_data.get('casing_material')
        wall_thickness = cleaned_data.get('wall_thickness')
        errors = []

        if casing_from and casing_to and casing_to < casing_from:
            errors.append('To must be greater than or equal to From.')

        open_casing_code = None
        try:
            open_casing_code = CasingCode.objects.get(code='OPEN')
        except Exception as e:
            errors.append('Configuration error: Open Hole Casing Code does not exist, please contact the administrator.')

        if open_casing_code:
            if casing_code != open_casing_code and not casing_material:
                self.add_error('casing_material', 'This field is required.')

            if casing_code != open_casing_code and not wall_thickness:
                self.add_error('wall_thickness', 'This field is required.')

            if casing_code == open_casing_code and casing_material:
                self.add_error('casing_material', 'Open Hole cannot have a casing material.')


        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = Casing
        fields = ['casing_from', 'casing_to', 'diameter', 'casing_code', 'casing_material', 'wall_thickness', 'drive_shoe']
