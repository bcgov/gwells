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
from django.db.models import Q
from functools import reduce
import operator
from .models import Well


class Search():
    def well_search(well='', addr='', legal='', owner='', lat_long_box=None, query_limit=1000):
        """
        Search for wells

        :param well: the identification plate number or well tag number
        :param addr: part of the street address or site area of the well
        :param legal: part of the legal plan, legal district lot or pid
        :param owner: part of the owner's full name
        :param lat_long_box: an object including 'start_corner' and 'end_corner',
            each a latitude-longitude pair describing extreme corners of an extent rectangle
            from within which the wells are to be selected
        :param query_limit: the number of wells the caller will display
        :returns: QuerySet of Well objects or None if no matching records found.
        """
        well_results = None
        q_list = []

        if well:
            q_list.append(Q(identification_plate_number=well) | Q(well_tag_number=well))

        if addr:
            q_list.append(Q(street_address__icontains=addr) | Q(city__icontains=addr))

        if legal:
            q_list.append(Q(legal_plan__icontains=legal) |
                          Q(legal_district_lot__icontains=legal) |
                          Q(legal_pid=legal))

        if owner:
            q_list.append(Q(owner_full_name__icontains=owner))

        # If there is a lat_long_box, then a user has drawn a box on the map
        #  to limit their query to within the box.
        if lat_long_box and lat_long_box['start_corner'] and lat_long_box['end_corner']:
            delimiter = ','
            start_corner = lat_long_box['start_corner'].split(delimiter)
            end_corner = lat_long_box['end_corner'].split(delimiter)

            # Casting to floats serves as last-minute sanitisation.
            start_lat = float(start_corner[0])
            start_long = float(start_corner[1])
            end_lat = float(end_corner[0])
            end_long = float(end_corner[1])

            # The minimum and maximum latitude values should behave as expected
            max_lat = max(start_lat, end_lat)
            min_lat = min(start_lat, end_lat)

            # We must compare the absolute values of the minimum and maximum longitude values,
            # since users may erronneously enter positive longitudes for BC.
            max_long = max(start_long, end_long)
            min_long = min(start_long, end_long)

            q_list.append(Q(latitude__gt=min_lat) & Q(latitude__lt=max_lat) &
                          Q(longitude__gt=min_long) & Q(longitude__lt=max_long))

        if q_list:
            # If there are too many results, we return one plus the query limit to engage post-query logic in
            # views.py
            well_results = Well.objects.only('well_tag_number', 'identification_plate_number',
                                             'owner_full_name', 'street_address', 'legal_lot', 'legal_plan',
                                             'legal_district_lot', 'land_district', 'legal_pid', 'diameter',
                                             'finished_well_depth', 'well_guid', 'latitude', 'longitude',
                                             'city').filter(
                reduce(operator.and_, q_list)).order_by('well_tag_number', 'create_date')[:query_limit+1]

        return well_results
