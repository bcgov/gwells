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

class ProductionDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Well Yield Estimation',
                Div(
                    Div('yield_estimation_method', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('yield_estimation_rate', 'USgpm'), css_class='col-md-3'),
                    Div(AppendedText('yield_estimation_duration', 'hrs'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('static_level', 'ft (btoc)'), css_class='col-md-3'),
                    Div(AppendedText('drawdown', 'ft (btoc)'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(InlineRadios('hydro_fracturing_performed'), css_class='col-md-3'),
                    Div(AppendedText('hydro_fracturing_yield_increase', 'USgpm'), css_class='col-md-3'),
                    css_class='row',
                ),
            )
        )
        super(ProductionDataForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ProductionData
        fields = ['yield_estimation_method', 'yield_estimation_rate', 'yield_estimation_duration', 'static_level', 'drawdown', 'hydro_fracturing_performed', 'hydro_fracturing_yield_increase']
        widgets = {'hydro_fracturing_performed': forms.RadioSelect}
