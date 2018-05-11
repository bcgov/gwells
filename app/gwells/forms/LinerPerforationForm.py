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

class LinerPerforationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        self.helper.render_required_fields = True
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            HTML('<tr valign="top">'),
            HTML('<td>'),
            'liner_perforation_from',
            HTML('</td>'),
            HTML('<td>'),
            'liner_perforation_to',
            HTML('</td><td width="75">&nbsp;{% if form.instance.pk %}{{ form.DELETE }}{% endif %}</td>'),
            HTML('</tr>'),
        )
        super(LinerPerforationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LinerPerforationForm, self).clean()

        liner_perforation_from = cleaned_data.get('liner_perforation_from')
        liner_perforation_to = cleaned_data.get('liner_perforation_to')
        errors = []

        if liner_perforation_from and liner_perforation_to and liner_perforation_to < liner_perforation_from:
            errors.append('To must be greater than or equal to From.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = LinerPerforation
        fields = ['liner_perforation_from', 'liner_perforation_to']
