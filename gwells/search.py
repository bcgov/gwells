from django.db.models import Q
from functools import reduce
import operator
from django.db.models import DecimalField
from .custom_transforms import AbsoluteValue
DecimalField.register_lookup(AbsoluteValue)
from .models import Well

class Search():
    def well_search(well='', addr='', legal='', owner='', lat_long_box=None):
        """
        Search for wells

        :param well: the identification plate number or well tag number
        :param addr: part of the street address or site area of the well
        :param legal: part of the legal plan, legal district lot or pid
        :param owner: part of the owner's full name
        :returns: QuerySet of Well objects or None if no matching records found.
        """
        well_results = None
        query_limit = 1000

        q_list = []

        if well:
            q_list.append(Q(identification_plate_number=well) | Q(well_tag_number=well))

        if addr:
            q_list.append(Q(street_address__icontains=addr) | Q(city__icontains=addr))

        if legal:
            pid = legal.lstrip('0')
            q_list.append(Q(legal_plan__icontains=legal) |
                          Q(legal_district_lot__icontains=legal) | Q(legal_pid=pid))

        if owner:
            q_list.append(Q(owner_full_name__icontains=owner))

        if lat_long_box is not None and lat_long_box['start_corner'] and lat_long_box['end_corner']:
            delimiter = ','
            start_corner = lat_long_box['start_corner'].split(delimiter)
            end_corner = lat_long_box['end_corner'].split(delimiter)

            # The minimum and maximum latitude values are as expected
            max_lat = max(start_corner[0], end_corner[0])
            min_lat = min(start_corner[0], end_corner[0])

            # We must compare the absolute values of the minimum and maximum longitude values,
            # since users often erronneously enter positive longitudes for BC.
            max_long = max(abs(float(start_corner[1])), abs(float(end_corner[1])))
            min_long = min(abs(float(start_corner[1])), abs(float(end_corner[1])))

            q_list.append(Q(latitude__abs__gt=min_lat) & Q(latitude__abs__lt=max_lat)
                          & Q(longitude__abs__gt=min_long) & Q(longitude__abs__lt=max_long))

        if q_list:
            well_results = Well.objects.distinct().filter(
                reduce(operator.and_, q_list)).order_by('well_tag_number', 'created')[:query_limit]

        return well_results
