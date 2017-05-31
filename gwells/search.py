from django.db.models import Q
from functools import reduce
import operator
from .models import ActivitySubmission

class Search():
    def well_search(well='', addr='', legal='', owner=''):
        """
        Search for wells

        :param well: the identification plate number or well tag number
        :param addr: part of the street address or site area of the well
        :param legal: part of the legal plan, legal district lot or pid
        :param owner: part of the owner's full name
        :returns: QuerySet of Well objects or None if no matching records found.
        """
        well_results = None
        
       
        q_list = []

        if well:
            q_list.append(Q(identification_plate_number=well) | Q(well_tag_number=well))

        if addr:
            q_list.append(Q(street_address__icontains=addr) | Q(city__icontains=addr))

        if legal:
            pid = legal.lstrip('0')
            q_list.append(Q(legal_plan__icontains=legal) | Q(legal_district_lot__icontains=legal) | Q(legal_pid=pid))

        if owner:
            q_list.append(Q(owner_full_name__icontains=owner))

        if len(q_list) > 0:
            well_results = ActivitySubmission.objects.distinct().filter(reduce(operator.and_, q_list)).order_by('well_tag_number', 'created')
                
        return well_results