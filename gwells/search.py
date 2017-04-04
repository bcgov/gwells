from django.db.models import Q
from functools import reduce
import operator
from .models import Well

class Search():
    def well_search(well, addr, legal, owner):
        well_results = None
        
       
        q_list = []

        #if well:
        #    q_list.append(Q(identification_plate_number_icontains=well))
        #    q_list.append(Q(well_tag_number__icontains=well))

        if addr:
            q_list.append(Q(street_address__icontains=addr))

        if legal:
            q_list.append(Q(lot_number__icontains=legal))
            q_list.append(Q(legal_plan__icontains=legal))
            q_list.append(Q(legal_district_lot__icontains=legal))
            q_list.append(Q(pid__icontains=legal))

            #qset_owner = Q(well_owner_id__full_name__icontains=owner)
        if len(q_list) > 0:
            well_results = Well.objects.filter(reduce(operator.or_, q_list)).order_by('-id')
                

            #token_list = querydata.split(' ')

            #qset = Q(address_line__icontains=token_list[0])
            #qset_owner = Q(given_name__icontains=token_list[0]) | Q(surname__icontains=token_list[0])
            
            #for token in token_list[1:]:
            #    qset.add(Q(address_line__icontains=token), qset.connector)
            #    qset_owner.add((Q(given_name__icontains=token) | Q(surname__icontains=token)), qset_owner.connector)

            #well_results = Well.objects.select_related('well_owner_id').filter(qset).order_by('-id')
 

            #wellresults = Well.objects.annotate(
            #    search=SearchVector('address_line')
            #    ).filter(search=querydata)
            
        return well_results