from django import forms
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Submit, Hidden, HTML, Field
from crispy_forms.bootstrap import FormActions, AppendedText
from django.forms.models import inlineformset_factory
from .search import Search
from .models import ActivitySubmission, WellActivityType
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
    

    @property
    def helper(self):
        helper = FormHelper()
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
                Hidden('dir', 'asc')
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

        if not well and not addr and not legal and not owner:
            raise forms.ValidationError(
                "At least 1 search field is required."
            )



    def process(self):
        well_results = None
        
        well = self.cleaned_data.get('well')
        addr = self.cleaned_data.get('addr')
        legal = self.cleaned_data.get('legal')
        owner = self.cleaned_data.get('owner')
        
        well_results = Search.well_search(well, addr, legal, owner)

            
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

        try:
            bc = ProvinceState.objects.get(code='BC')
            self.initial['owner_province_state'] = bc
            self.fields['owner_province_state'].empty_label = None
        except Exception as e:
            pass
    
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
                    css_class='row',
                ),
                Div(
                    Div(HTML('<label for="units">Measurement units for data entry</label><br /><input type="radio" name="units" value="Imperial" checked /> Imperial<br /><input type="radio" name="units" value="Metric" disabled /> Metric<br /><br />'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div('well_class', css_class='col-md-4'),
                    Div(Div('well_subclass', id='divSubclass'), Div('intended_water_use', id='divIntendedWaterUse'), css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('identification_plate_number', css_class='col-md-3'),
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
            #self.fields['well_activity_type'].widget = forms.RadioSelect(attrs={'id': 'value'})
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
        work_start_date = cleaned_data.get('work_start_date')
        work_end_date = cleaned_data.get('work_end_date')

        if work_start_date and work_end_date:
            if work_end_date < work_start_date:
                raise forms.ValidationError('Work End Date cannot be earlier than Work Start Date.')
        return cleaned_data

    class Meta:
        model = ActivitySubmission
        fields = ['well_activity_type', 'well_class', 'well_subclass', 'intended_water_use', 'identification_plate_number', 'driller_responsible', 'driller_name', 'consultant_name', 'consultant_company', 'work_start_date', 'work_end_date']
        help_texts = {'work_start_date': "yyyy-mm-dd", 'work_end_date': "yyyy-mm-dd",}



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
        legal_district_lot = cleaned_data.get('legal_district_lot')
        legal_block = cleaned_data.get('legal_block')
        legal_section = cleaned_data.get('legal_section')
        legal_township = cleaned_data.get('legal_township')
        legal_range = cleaned_data.get('legal_range')
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
                'Geographic Coordinates and Method of Drilling',
                Div(
                    Div(HTML('To determine coordinates using a Global Positioning System (GPS), set the datum to the North American Datum of 1983 (NAD 83), the current ministry standard for mapping.<br /><br />'), css_class='col-md-12'),
                    css_class='row',
                ),
                Div(
                    Div(
                        Div(
                            Div(AppendedText('latitude', 'decimal degrees'), css_class='col-md-5'),
                            Div(AppendedText('longitude', 'decimal degrees'), css_class='col-md-5'),
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
                            Div(HTML('<div id="div_id_gps-latitude_dms" class="form-group"> <label for="id_gps-latitude_d" class="control-label ">Latitude</label> <div class="controls "> <div class="input-group"> <input class="numberinput form-control" id="id_gps-latitude_d" name="gps-latitude_d" step="1" type="number" /> <span class="input-group-addon">deg</span> <input class="numberinput form-control" id="id_gps-latitude_m" name="gps-latitude_m" step="1" type="number" /> <span class="input-group-addon">min</span> <input class="numberinput form-control" id="id_gps-latitude_s" name="gps-latitude_s" step="0.01" type="number" /> <span class="input-group-addon">sec</span> </div> </div> </div>'), css_class='col-md-6'),
                            Div(HTML('<div id="div_id_gps-longitude_dms" class="form-group"> <label for="id_gps-longitude_d" class="control-label ">Longitude</label> <div class="controls "> <div class="input-group"> <input class="numberinput form-control" id="id_gps-longitude_d" name="gps-longitude_d" step="1" type="number" /> <span class="input-group-addon">deg</span> <input class="numberinput form-control" id="id_gps-longitude_m" name="gps-longitude_m" step="1" type="number" /> <span class="input-group-addon">min</span> <input class="numberinput form-control" id="id_gps-longitude_s" name="gps-longitude_s" step="0.01" type="number" /> <span class="input-group-addon">sec</span> </div> </div> </div>'), css_class='col-md-6'),
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
                            Div(HTML('<div id="div_id_gps-zone" class="form-group"> <label for="id_gps-zone" class="control-label ">Zone</label> <div class="controls "> <select class="select form-control" id="id_gps-zone" name="gps-zone"><option value="" selected="selected">---------</option></select> </div> </div>'), css_class='col-md-4'),
                            Div(HTML('<div id="div_id_gps-utm_easting" class="form-group"> <label for="id_gps-utm_easting" class="control-label ">UTM Easting</label> <div class="controls "> <div class="input-group"> <input class="numberinput form-control" id="id_gps-utm_easting" name="gps-utm_easting" step="0.01" type="number" /> <span class="input-group-addon">m</span> </div> </div> </div>'), css_class='col-md-4'),
                            Div(HTML('<div id="div_id_gps-utm_northing" class="form-group"> <label for="id_gps-utm_northing" class="control-label ">UTM Northing</label> <div class="controls "> <div class="input-group"> <input class="numberinput form-control" id="id_gps-utm_northing" name="gps-utm_northing" step="0.01" type="number" /> <span class="input-group-addon">m</span> </div> </div> </div>'), css_class='col-md-4'),
                            css_class='row',
                        ),
                        css_class='col-md-8',
                    ),
                    Div(
                        Div(
                            Div(HTML('<button type="button">Map It!</button>'), css_class='col-md-4', onclick='placeNewWellMarker()'),
                            Div(HTML('<button type="button">Clear Map</button>'), css_class='col', onclick='removeNewWellMarker()'),
                            css_class='row',
                        ),
                        Div(HTML('<div id="add-map"></div>')),
                        css_class='col-md-4',
                    ),
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
                    Div(AppendedText('ground_elevation', 'ft (asl)'), css_class='col-md-2'),
                    Div('ground_elevation_method', css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('drilling_method', css_class='col-md-3'),
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
    
    class Meta:
        model = ActivitySubmission
        fields = ['latitude', 'longitude', 'ground_elevation', 'ground_elevation_method', 'drilling_method', 'other_drilling_method', 'orientation_vertical']
        #help_texts = {'latitude': 'decimal degrees', 'longitude': 'decimal degrees',}
        widgets = {'orientation_vertical': forms.RadioSelect}


#WellCompletionDataFormSet = inlineformset_factory(ActivitySubmission, WellCompletionData, max_num=1, can_delete=False)
#LithologyFormSet = inlineformset_factory(ActivitySubmission, Lithology, extra=5)