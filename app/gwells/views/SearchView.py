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

from django.views import generic
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import JsonResponse
import json
from gwells.forms import SearchForm
from gwells.models import LandDistrictCode
from gwells.models import Survey


class SearchView(generic.DetailView):

    @staticmethod
    def get_surveys_for_context():
        surveys = Survey.objects.order_by('create_date')
        page = 's'
        return surveys, page

    @staticmethod
    def common_well_search(request):
        """
            Returns json and array data for a well search.  Used by both the map and text search.
        """
        well_results = None
        well_results_json = '[]'

        form = SearchForm(request.GET)
        if form.is_valid():
            well_results = form.process()

        if well_results and not len(well_results) > SearchForm.WELL_RESULTS_LIMIT:
            well_results_json = json.dumps(
                [well.as_dict() for well in well_results],
                cls=DjangoJSONEncoder)

        return form, well_results, well_results_json

    @staticmethod
    def well_search(request):
        """
            Text search.
        """
        well_results = None
        well_results_overflow = None
        well_results_json = '[]'
        form = None
        lat_long_box = '{}'

        if request.method == 'GET' and 'well' in request.GET:
            # The lat_long_box is returned as a JSON string regardless of the validity of the form,
            # provided the request has both a start_lat_long and an end_lat_long
            if 'start_lat_long' in request.GET and 'end_lat_long' in request.GET:
                start_lat_long = request.GET['start_lat_long']
                end_lat_long = request.GET['end_lat_long']
                lat_long_box = json.dumps(
                    {'startCorner': start_lat_long, 'endCorner': end_lat_long},
                    cls=DjangoJSONEncoder)
            form, well_results, well_results_json = SearchView.common_well_search(request)
        else:
            form = SearchForm()

        if well_results:
            if len(well_results) > SearchForm.WELL_RESULTS_LIMIT:
                well_results_overflow = ('Query returned more than %d wells. Please refine your search or '
                                         'select a smaller area to look for wells in.'
                                         % SearchForm.WELL_RESULTS_LIMIT)
                well_results = None
            else:
                well_results_json = json.dumps(
                    [well.as_dict() for well in well_results],
                    cls=DjangoJSONEncoder)

        # create an object that will be used to render the names for land districts.
        land_districts = {}
        all_land_districts = LandDistrictCode.objects.all()
        for land_district in all_land_districts:
            land_districts[land_district.land_district_code] = land_district.name

        surveys, page = SearchView.get_surveys_for_context()

        return render(request, 'gwells/search.html', {
            'form': form, 'well_list': well_results,
            'too_many_wells': well_results_overflow,
            'wells_json': well_results_json,
            'lat_long_box': lat_long_box,
            'land_districts': land_districts,
            'surveys': surveys,
            'page': page})

    @staticmethod
    def map_well_search(request):
        """
            Map search.
        """
        well_results = None
        well_results_json = '[]'
        form = None
        if (request.method == 'GET' and 'start_lat_long' in request.GET and 'end_lat_long' in request.GET):
            form, well_results, well_results_json = SearchView.common_well_search(request)

        return JsonResponse(well_results_json, safe=False)
