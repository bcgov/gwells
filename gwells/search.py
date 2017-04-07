from django.db.models import Q
from functools import reduce
import operator
from .models import Well

class Search():
    def well_search(well, addr, legal, owner):
        well_results = None
        
       
        q_list = []

        if well:
            q_list.append(Q(identification_plate_number=well))
            q_list.append(Q(well_tag_number=well))

        if addr:
            q_list.append(Q(street_address__icontains=addr))

        if legal:
            q_list.append(Q(lot_number__icontains=legal))
            q_list.append(Q(legal_plan__icontains=legal))
            q_list.append(Q(legal_district_lot__icontains=legal))
            q_list.append(Q(pid__icontains=legal))

        if owner:
            q_list.append(Q(well_owner__full_name__icontains=owner))

        if len(q_list) > 0:
            well_results = Well.objects.filter(reduce(operator.or_, q_list)).order_by('well_tag_number', 'id')
                
        return well_results