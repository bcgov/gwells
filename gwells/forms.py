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
from .search import Search
from .models import ActivitySubmission, WellActivityType, ProvinceState, DrillingMethod, LithologyDescription, LithologyMoisture, Casing, CasingType, LinerPerforation
from .models import ScreenIntake, ScreenMaterial, ScreenBottom, Screen, ProductionData, WaterQualityCharacteristic
from datetime import date

class SearchForm(forms.Form):
    well = forms.IntegerField(
        label=mark_safe('Well Tag Number or Well Identification Plate Number <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Well electronic filing number or physical identification plate number"> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'example: 123456'}),
    )

    addr = forms.CharField(
        label=mark_safe('Street Address <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="For best results, try searching using the street name only."> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: 123 main'}),
    )

    legal = forms.CharField(
        label=mark_safe('Legal Plan or District Lot or PID <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="Find the legal plan, district lot, or 9-digit PID (parcel identifier) on the property assessment, property tax notice, or real estate transaction."> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: 123a'}),
    )

    owner = forms.CharField(
        label=mark_safe('Owner Name <a href="#" data-toggle="popover" data-container="body" data-placement="right" \
            data-content="The owner name is usually the name of the well owner at time of drilling."> \
            <i class="fa fa-question-circle" style="color:blue"></i></a>'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example: Smith or smi'}),
    )
    
    start_lat_long = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    end_lat_long = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
 
    WELL_RESULTS_LIMIT = 1000

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = 'id-searchForm'
        helper.form_method = 'get'
        helper.form_action = ''

        helper.layout = Layout(
            Fieldset(
                '',
                'well',
                'addr',
                'legal',
                'owner',
                Hidden('sort', 'well_tag_number'),
                Hidden('dir', 'asc'),
                # start_lat_long and end_lat_long are programatically generated
                # based on an identifyWells operation on the client.
                Hidden('start_lat_long', ''),
                Hidden('end_lat_long', ''),
            ),
            FormActions(
                Submit('s', 'Search'),
                HTML('<a class="btn btn-default" href="{% url \'search\' %}">Reset</a>'),
                css_class='form-group formButtons',
            )
        )

        return helper


    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        well = cleaned_data.get('well')
        addr = cleaned_data.get('addr')
        legal = cleaned_data.get('legal')
        owner = cleaned_data.get('owner')
        # start_lat_long and end_lat_long are programatically-generated, and
        # should consist of a dictionary of a comma-separated list consisting
        # of two floats that comprise latitude and longitude. They are used
        # in the identifyWells operation to query all wells whose lat/long info
        # place them within a user-drawn rectangle on the search page map.
        start_lat_long = cleaned_data.get('start_lat_long')
        end_lat_long = cleaned_data.get('end_lat_long')

        # If only one of the rectangle's points exist, we cannot perform the query.
        if bool(start_lat_long) != bool(end_lat_long):
            raise forms.ValidationError(
                "identifyWells operation did not provide sufficient data. "
                "The map may not accurately reflect query results."
            )
        if (not well and not addr and not legal and
                not owner and not (start_lat_long and end_lat_long)):
            raise forms.ValidationError(
                "At least 1 search field is required."
            )

    def process(self):
        well_results = None

        well = self.cleaned_data.get('well')
        addr = self.cleaned_data.get('addr')
        legal = self.cleaned_data.get('legal')
        owner = self.cleaned_data.get('owner')
        start_lat_long = self.cleaned_data.get('start_lat_long')
        end_lat_long = self.cleaned_data.get('end_lat_long')
        lat_long_box = {'start_corner': start_lat_long, 'end_corner': end_lat_long}

        well_results = Search.well_search(well, addr, legal, owner, lat_long_box, self.WELL_RESULTS_LIMIT)

        return well_results



class WellOwnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Owner Information',
                Div(
                    Div('owner_full_name', css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('owner_mailing_address', css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('owner_city', css_class='col-md-3 city'),
                    Div('owner_province_state', css_class='col-md-1'),
                    Div('owner_postal_code', css_class='col-md-3 postal'),
                    css_class='row',
                ),
            )
        )
        super(WellOwnerForm, self).__init__(*args, **kwargs)
        # Make fields required on the form even though they are not required in the DB due to legacy data issues
        # TODO - check admin or staff user and don't make these fields required
        self.fields['owner_postal_code'].required = True

        # display code instead of the value from __str__ in the model
        self.fields['owner_province_state'].label_from_instance = self.label_from_instance_code
        try:
            bc = ProvinceState.objects.get(code='BC')
            self.initial['owner_province_state'] = bc
            self.fields['owner_province_state'].empty_label = None
        except Exception as e:
            pass

    @staticmethod
    def label_from_instance_code(obj):
        return obj.code
    
    class Meta:
        model = ActivitySubmission
        fields = ['owner_full_name', 'owner_mailing_address', 'owner_city', 'owner_province_state', 'owner_postal_code']



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
                    Div(Div('well_subclass', id='divSubclass'), Div('intended_water_use', id='divIntendedWaterUse'), css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('identification_plate_number', css_class='col-md-4'),
                    Div('where_plate_attached', css_class='col-md-4'),
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
            con = WellActivityType.objects.get(code='CON')
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
        where_plate_attached = cleaned_data.get('where_plate_attached')
        work_start_date = cleaned_data.get('work_start_date')
        work_end_date = cleaned_data.get('work_end_date')

        errors = []

        if identification_plate_number and not where_plate_attached:
            errors.append('Where Identification Plate Is Attached is required when specifying Identification Plate Number.')

        if work_start_date and work_end_date and work_end_date < work_start_date:
            errors.append('Work End Date cannot be earlier than Work Start Date.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['well_activity_type', 'well_class', 'well_subclass', 'intended_water_use', 'identification_plate_number', 'where_plate_attached', 'driller_responsible', 'driller_name', 'consultant_name', 'consultant_company', 'work_start_date', 'work_end_date']
        help_texts = {'work_start_date': "yyyy-mm-dd", 'work_end_date': "yyyy-mm-dd",}
        widgets = {'well_activity_type': forms.RadioSelect}



class ActivitySubmissionLocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Well Location',
                Div(
                    Div(HTML('Please provide as much well location information as possible. A minimum of one type of well location information is required below.<br /><br />'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('<label>1) Civic Address</label>'), css_class='col-md-2'),
                    Div(HTML('<input type="checkbox" id="chkSameAsOwnerAddress" /> <label for="chkSameAsOwnerAddress">Same as Owner Address</label>'), css_class='col-md-10'),
                    css_class='row',
                ),
                Div(
                    Div('street_address', css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('city', css_class='col-md-4 city'),
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
                    Div(HTML('<label>2) Legal Description</label>'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div('legal_lot', css_class='col-md-2 city'),
                    Div('legal_plan', css_class='col-md-2 city'),
                    Div('legal_district_lot', css_class='col-md-2 city'),
                    Div('legal_block', css_class='col-md-2 city'),
                    css_class='row',
                ),
                Div(
                    Div('legal_section', css_class='col-md-2 city'),
                    Div('legal_township', css_class='col-md-2 city'),
                    Div('legal_range', css_class='col-md-2 city'),
                    Div('legal_land_district', css_class='col-md-2 city'),
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
                    Div(HTML('<label>3) Parcel Identifier</label>'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div('legal_pid', css_class='col-md-2'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('&nbsp;'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(HTML('&nbsp;'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div('well_location_description', css_class='col-md-8'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionLocationForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(ActivitySubmissionLocationForm, self).clean()
        
        street_address = cleaned_data.get('street_address') 
        city = cleaned_data.get('city')
        address_provided = street_address and city

        legal_lot = cleaned_data.get('legal_lot')
        legal_plan = cleaned_data.get('legal_plan')
        legal_land_district = cleaned_data.get('legal_land_district')
        legal_provided = legal_lot and legal_plan and legal_land_district

        if not address_provided and not legal_provided and not cleaned_data.get('legal_pid'):
            raise forms.ValidationError('At least 1 of Civic Address, Legal Description (Lot, Plan and Land District) or Parcel Identifier must be provided.')
        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['street_address', 'city', 'legal_lot', 'legal_plan', 'legal_district_lot', 'legal_block', 'legal_section', 'legal_township', 'legal_range', 'legal_land_district', 'legal_pid', 'well_location_description']
        help_texts = {'well_location_description': "Provide any additional well location details, such as physical landmarks",}



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
                    Div('orientation_vertical', css_class='col-md-3'),
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
            if drilling_method == DrillingMethod.objects.get(code='OTHER') and not other_drilling_method:
                errors.append('Specify Other Drilling Method.')
        except Exception as e:
            errors.append('Configuration error: Other Drilling Method does not exist, please contact the administrator.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['latitude', 'longitude', 'ground_elevation', 'ground_elevation_method', 'drilling_method', 'other_drilling_method', 'orientation_vertical']
        widgets = {'orientation_vertical': forms.RadioSelect,
                   'latitude': forms.TextInput(attrs={'type': 'number', 'min': '48.20456', 'max': '60.0222', 'step': 'any'}),
                   'longitude': forms.TextInput(attrs={'type': 'number', 'min': '-139.07367', 'max': '-114.03383', 'step': 'any'})}



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
                if lithology_moisture == LithologyMoisture.objects.get(code='Water Bear') and not water_bearing_estimated_flow:
                    errors.append('Water Bearing Estimated Flow is required for Water Bearing Bedrock.')
            except Exception as e:
                errors.append('Configuration error: Water Bearing Lithology Moisture does not exist, please contact the administrator.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = LithologyDescription
        fields = ['lithology_from', 'lithology_to', 'surficial_material', 'secondary_surficial_material', 'bedrock_material', 'bedrock_material_descriptor', 'lithology_structure', 'lithology_colour', 'lithology_hardness', 'lithology_moisture', 'water_bearing_estimated_flow', 'lithology_observation']



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
            'internal_diameter',
            HTML('</td>'),
            HTML('<td>'),
            'casing_type',
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
        casing_type = cleaned_data.get('casing_type')
        casing_material = cleaned_data.get('casing_material')
        wall_thickness = cleaned_data.get('wall_thickness')
        errors = []

        if casing_from and casing_to and casing_to < casing_from:
            errors.append('To must be greater than or equal to From.')

        open_casing_type = None
        try:
            open_casing_type = CasingType.objects.get(code='OPEN')
        except Exception as e:
            errors.append('Configuration error: Open Hole Casing Type does not exist, please contact the administrator.')

        if open_casing_type:
            if casing_type != open_casing_type and not casing_material:
                self.add_error('casing_material', 'This field is required.')

            if casing_type != open_casing_type and not wall_thickness:
                self.add_error('wall_thickness', 'This field is required.')

            if casing_type == open_casing_type and casing_material:
                self.add_error('casing_material', 'Open Hole cannot have a casing material.')


        if len(errors) > 0:
            raise forms.ValidationError(errors)        

        return cleaned_data

    class Meta:
        model = Casing
        fields = ['casing_from', 'casing_to', 'internal_diameter', 'casing_type', 'casing_material', 'wall_thickness', 'drive_shoe']



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
                    Div('screen_intake', css_class='col-md-2'),
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

        screen_intake = cleaned_data.get('screen_intake')
        screen_type = cleaned_data.get('screen_type')
        screen_material = cleaned_data.get('screen_material')
        other_screen_material = cleaned_data.get('other_screen_material')
        screen_opening = cleaned_data.get('screen_opening')
        screen_bottom = cleaned_data.get('screen_bottom')
        other_screen_bottom = cleaned_data.get('other_screen_bottom')
        errors = []

        screen_screen_intake = None
        try:
            screen_screen_intake = ScreenIntake.objects.get(code='SCREEN')
        except Exception as e:
            errors.append('Configuration error: Screen Intake for Screen does not exist, please contact the administrator.')
        
        if screen_screen_intake:
            if screen_intake == screen_screen_intake and not screen_type:
                self.add_error('screen_type', 'This field is required if Intake is a Screen.')

            if screen_intake == screen_screen_intake and not screen_material:
                self.add_error('screen_material', 'This field is required if Intake is a Screen.')

            if screen_intake == screen_screen_intake and not screen_opening:
                self.add_error('screen_opening', 'This field is required if Intake is a Screen.')

            if screen_intake == screen_screen_intake and not screen_bottom:
                self.add_error('screen_bottom', 'This field is required if Intake is a Screen.')

        try:
            if screen_material == ScreenMaterial.objects.get(code='OTHER') and not other_screen_material:
                self.add_error('other_screen_material', 'This field is required.')
        except Exception as e:
            errors.append('Configuration error: Other Screen Material does not exist, please contact the administrator.')
        
        try:
            if screen_bottom == ScreenBottom.objects.get(code='OTHER') and not other_screen_bottom:
                self.add_error('other_screen_bottom', 'This field is required.')
        except Exception as e:
            errors.append('Configuration error: Other Screen Bottom does not exist, please contact the administrator.')


        if len(errors) > 0:
            raise forms.ValidationError(errors)        

        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['screen_intake', 'screen_type', 'screen_material', 'other_screen_material', 'screen_opening', 'screen_bottom', 'other_screen_bottom']



class ScreenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        self.helper.render_required_fields = True
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            HTML('<tr valign="top">'),
            HTML('<td width="60">'),
            'screen_from',
            HTML('</td>'),
            HTML('<td width="60">'),
            'screen_to',
            HTML('</td>'),
            HTML('<td width="70">'),
            'internal_diameter',
            HTML('</td>'),
            HTML('<td width="200">'),
            'assembly_type',
            HTML('</td>'),
            HTML('<td width="60">'),
            'slot_size',
            HTML('</td><td width="75">&nbsp;{% if form.instance.pk %}{{ form.DELETE }}{% endif %}</td>'),
            HTML('</tr>'),
        )
        super(ScreenForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ScreenForm, self).clean()

        screen_from = cleaned_data.get('screen_from')
        screen_to = cleaned_data.get('screen_to')
        errors = []

        if screen_from and screen_to and screen_to < screen_from:
            errors.append('To must be greater than or equal to From.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)        

        return cleaned_data

    class Meta:
        model = Screen
        fields = ['screen_from', 'screen_to', 'internal_diameter', 'assembly_type', 'slot_size']



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



class ActivitySubmissionDevelopmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Well Development',
                Div(
                    Div('development_method', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('development_hours', 'hrs'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div('development_notes', css_class='col-md-6'),
                    css_class='row',
                ),
            )
        )
        super(ActivitySubmissionDevelopmentForm, self).__init__(*args, **kwargs)
   
    class Meta:
        model = ActivitySubmission
        fields = ['development_method', 'development_hours', 'development_notes']



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



class ActivitySubmissionWaterQualityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Water Quality',
                Div(
                    Div('water_quality_characteristics', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div('water_quality_colour', css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div('water_quality_odour', css_class='col-md-3'),
                    css_class='row',
                ),
            )
        )

        super(ActivitySubmissionWaterQualityForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ActivitySubmission
        fields = ['water_quality_characteristics', 'water_quality_colour', 'water_quality_odour']
        widgets = {'water_quality_characteristics': forms.CheckboxSelectMultiple}



class WellCompletionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                'Well Completion Details',
                Div(
                    Div(AppendedText('total_depth_drilled', 'ft'), css_class='col-md-3'),
                    Div(AppendedText('finished_well_depth', 'ft (bgl)'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('final_casing_stick_up', 'in'), css_class='col-md-3'),
                    Div(AppendedText('bedrock_depth', 'ft (bgl)'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('static_water_level', 'ft (btoc)'), css_class='col-md-3'),
                    Div(AppendedText('well_yield', 'USgpm'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div(AppendedText('artestian_flow', 'USgpm'), css_class='col-md-3'),
                    Div(AppendedText('artestian_pressure', 'ft'), css_class='col-md-3'),
                    css_class='row',
                ),
                Div(
                    Div('well_cap_type', css_class='col-md-3'),
                    Div(InlineRadios('well_disinfected'), css_class='col-md-3'),
                    css_class='row',
                ),
            )
        )
        super(WellCompletionForm, self).__init__(*args, **kwargs)
        # Make fields required on the form even though they are not required in the DB due to legacy data issues
        # TODO - check admin or staff user and don't make these fields required
        self.fields['total_depth_drilled'].required = True
        self.fields['finished_well_depth'].required = True
        self.fields['final_casing_stick_up'].required = True

    def clean(self):
        cleaned_data = super(WellCompletionForm, self).clean()
        
        total_depth_drilled = cleaned_data.get('total_depth_drilled') 
        finished_well_depth = cleaned_data.get('finished_well_depth') 
        errors = []

        if total_depth_drilled and finished_well_depth and total_depth_drilled < finished_well_depth:
            errors.append('Finished Well Depth can\'t be greater than Total Depth Drilled.')

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['total_depth_drilled', 'finished_well_depth', 'final_casing_stick_up', 'bedrock_depth', 'static_water_level', 'well_yield', 'artestian_flow', 'artestian_pressure', 'well_cap_type', 'well_disinfected']
        widgets = {'well_disinfected': forms.RadioSelect}



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



#WellCompletionDataFormSet = inlineformset_factory(ActivitySubmission, WellCompletionData, max_num=1, can_delete=False)
ActivitySubmissionLithologyFormSet = inlineformset_factory(ActivitySubmission, LithologyDescription, form=LithologyForm, fk_name='activity_submission', can_delete=False, extra=10)
ActivitySubmissionCasingFormSet = inlineformset_factory(ActivitySubmission, Casing, form=CasingForm, fk_name='activity_submission', can_delete=False, extra=5)
ActivitySubmissionLinerPerforationFormSet = inlineformset_factory(ActivitySubmission, LinerPerforation, form=LinerPerforationForm, fk_name='activity_submission', can_delete=False, extra=5)
ActivitySubmissionScreenFormSet = inlineformset_factory(ActivitySubmission, Screen, form=ScreenForm, fk_name='activity_submission', can_delete=False, extra=5)
ProductionDataFormSet = inlineformset_factory(ActivitySubmission, ProductionData, form=ProductionDataForm, fk_name='activity_submission', can_delete=True, min_num=1, max_num=1)
