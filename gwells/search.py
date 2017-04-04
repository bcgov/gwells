from django.db.models import Q
from .models import Well

class Search():
    def well_search(well, addr, legal, owner):
        well_results = None
        
       
        if (well is not None):
            qset_well = Q(identification_plate_number__icontains=well) | Q(well_tag_number__icontains=well)
            qset_addr = Q(street_address__icontains=addr)
            qset_legal = Q(lot_number__icontains=legal) | Q(legal_plan__icontains=legal) | Q(legal_district_lot__icontains=legal) | Q(pid__icontains=legal)
            qset_owner = Q(well_owner_id__full_name__icontains=owner)
            qset = qset_well | qset_addr | qset_legal | qset_owner

            #token_list = querydata.split(' ')

            #qset = Q(address_line__icontains=token_list[0])
            #qset_owner = Q(given_name__icontains=token_list[0]) | Q(surname__icontains=token_list[0])
            
            #for token in token_list[1:]:
            #    qset.add(Q(address_line__icontains=token), qset.connector)
            #    qset_owner.add((Q(given_name__icontains=token) | Q(surname__icontains=token)), qset_owner.connector)

            well_results = Well.objects.select_related('well_owner_id').filter(qset).order_by('-id')
 

            #wellresults = Well.objects.annotate(
            #    search=SearchVector('address_line')
            #    ).filter(search=querydata)
            
        return well_results