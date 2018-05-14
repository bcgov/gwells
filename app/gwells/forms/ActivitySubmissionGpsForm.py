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

class ActivitySubmissionGpsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Geographic Coordinates',
                Div(
                    Div(HTML('To determine coordinates using a Global Positioning System (GPS), set the datum to the North American Datum of 1983 (NAD 83), the current ministry standard for mapping.<br /><br />'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(
                        Div(
                            Div(HTML('<div id="coord-error-pane" class="alert alert-warning" style="display:none"></div>')),
                            css_class='row',
                        ),
                        Div(
                            Div(AppendedText('latitude', 'decimal degrees'), css_class='col-md-4'),
                            Div(AppendedText('longitude', 'decimal degrees'), css_class='col-md-4'),
                            css_class='row',
                        ),
                        Div(
                            Div(HTML('OR'), css_class='col-md-12'),
                            css_class='row',
                        ),
                        Div(
                            Div(HTML('&nbsp;'), css_class='col-md-12'),
                            css_class='row',
                        ),
                        Div(
                            Div(HTML('<div id="div_id_gps-latitude_dms" class="form-group"> <label for="id_gps-latitude_d" class="control-label ">Latitude</label> <div class="controls "> <div class="input-group"> <input class="numberinput form-control" id="id_gps-latitude_d" name="gps-latitude_d" step="1" type="number" /> <span class="input-group-addon">deg</span> <input class="numberinput form-control" id="id_gps-latitude_m" name="gps-latitude_m" step="1" type="number" /> <span class="input-group-addon">min</span> <input class="numberinput form-control" id="id_gps-latitude_s" name="gps-latitude_s" step="0.01" type="number" /> <span class="input-group-addon">sec</span> </div> </div> </div>'), css_class='col-md-5'),
                            Div(HTML('<div id="div_id_gps-longitude_dms" class="form-group"> <label for="id_gps-longitude_d" class="control-label ">Longitude</label> <div class="controls "> <div class="input-group"> <input class="numberinput form-control" id="id_gps-longitude_d" name="gps-longitude_d" step="1" type="number" /> <span class="input-group-addon">deg</span> <input class="numberinput form-control" id="id_gps-longitude_m" name="gps-longitude_m" step="1" type="number" /> <span class="input-group-addon">min</span> <input class="numberinput form-control" id="id_gps-longitude_s" name="gps-longitude_s" step="0.01" type="number" /> <span class="input-group-addon">sec</span> </div> </div> </div>'), css_class='col-md-5'),
                            css_class='row',
                        ),
                        Div(
                            Div(HTML('OR'), css_class='col-md-12'),
                            css_class='row',
                        ),
                        Div(
                            Div(HTML('&nbsp;'), css_class='col-md-12'),
                            css_class='row',
                        ),
                        Div(
                            Div(HTML('<div id="div_id_gps-zone" class="form-group"> <label for="id_gps-zone" class="control-label ">Zone</label> <div class="controls "> <select class="select form-control" id="id_gps-zone" name="gps-zone"><option value="" selected="selected">---------</option><option value="8">8</option><option value="9">9</option><option value="10">10</option><option value="11">11</option></select> </div> </div>'), css_class='col-md-2'),
                            Div(HTML('<div id="div_id_gps-utm_easting" class="form-group"> <label for="id_gps-utm_easting" class="control-label ">UTM Easting</label> <div class="controls "> <div class="input-group"> <input class="numberinput form-control" id="id_gps-utm_easting" name="gps-utm_easting" step="1" type="number" min="200000" max="800000" /> <span class="input-group-addon">m</span> </div> </div> </div>'), css_class='col-md-3'),
                            Div(HTML('<div id="div_id_gps-utm_northing" class="form-group"> <label for="id_gps-utm_northing" class="control-label ">UTM Northing</label> <div class="controls "> <div class="input-group"> <input class="numberinput form-control" id="id_gps-utm_northing" name="gps-utm_northing" step="1" type="number" min="5350500" max="6655250" /> <span class="input-group-addon">m</span> </div> </div> </div>'), css_class='col-md-3'),
                            css_class='row',
                        ),
                        css_class='col-md-8',
                    ),
                    Div(
                        Div(
                            id='add-map',
                            aria_label='This map shows the location of a prospective well as a light blue pushpin, as well as any existing wells as dark blue circles. Coordinates for the prospective well may be refined by dragging the pushpin with the mouse.'
                        ),
                        Div(
                            id='attribution'
                        ),
                        Div(HTML('<br />After the GPS coordinates are entered, the pushpin can be moved by clicking and dragging it on the map. The GPS coordinates will be updated automatically.')
                        ),
                        css_class='col-md-4',
                    ),
                    css_class='row',
                ),
            ),
            Fieldset(
                'Method of Drilling',
                Div(
                    Div(AppendedText('ground_elevation', 'ft (asl)'), css_class='col-md-2'),
                    Div('ground_elevation_method', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div('drilling_method', css_class='col-md-2'),
                    Div('other_drilling_method', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('&nbsp;'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div('well_orientation', css_class='col-md-3'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionGpsForm, self).__init__(*args, **kwargs)
        # Make fields required on the form even though they are not required in the DB due to legacy data issues
        # TODO - check admin or staff user and don't make these fields required
        self.fields['latitude'].required = True
        self.fields['longitude'].required = True
        self.fields['drilling_method'].required = True

    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')

        if latitude < 48.204555 or latitude > 60.0223:
            raise forms.ValidationError('Latitude must be between 48.204556 and 60.02230.')

        decimal_places =  max(0,-latitude.as_tuple().exponent)
        if decimal_places < 5:
            raise forms.ValidationError('Latitude must be specified to at least 5 decimal places.')

        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')

        if longitude < -139.073671 or longitude > -114.033822:
            raise forms.ValidationError('Longitude must be between -139.073671 and -114.033822.')

        decimal_places =  max(0,-longitude.as_tuple().exponent)
        if decimal_places < 5:
            raise forms.ValidationError('Longitude must be specified to at least 5 decimal places.')

        return longitude

    def clean(self):
        cleaned_data = super(ActivitySubmissionGpsForm, self).clean()

        ground_elevation = cleaned_data.get('ground_elevation')
        ground_elevation_method = cleaned_data.get('ground_elevation_method')
        drilling_method = cleaned_data.get('drilling_method')
        other_drilling_method = cleaned_data.get('other_drilling_method')
        errors = []

        if ground_elevation and not ground_elevation_method:
            errors.append('Method for Determining Ground Elevation is required when specifying Ground Elevation.')

        try:
            if drilling_method == DrillingMethodCode.objects.get(code='OTHER') and not other_drilling_method:
                errors.append('Specify Other Drilling Method.')
        except Exception as e:
            errors.append('Configuration error: Other Drilling Method does not exist, please contact the administrator.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['latitude', 'longitude', 'ground_elevation', 'ground_elevation_method', 'drilling_method', 'other_drilling_method', 'well_orientation']
        widgets = {'well_orientation': forms.RadioSelect,
                   'latitude': forms.TextInput(attrs={'type': 'number', 'min': '48.20456', 'max': '60.0222', 'step': 'any'}),
                   'longitude': forms.TextInput(attrs={'type': 'number', 'min': '-139.07367', 'max': '-114.03383', 'step': 'any'})}
