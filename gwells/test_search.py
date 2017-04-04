from django.test import TestCase
#from unittest import mock
from .models import WellOwner, ProvinceState, Well 
from .search import Search

class SearchTestCase(TestCase):
    def setUp(self):
        #well_owner = mock.Mock(spec=WellOwner)
        #well_owner._state = mock.Mock()

        prov = ProvinceState.objects.create(sort_order=1)

        owner = WellOwner.objects.create(province_state_id=prov)
        owner.name = 'John Smith'

        w = Well.objects.create(well_owner_id=owner)
        w.identification_plate_number = 123
        w.well_tag_number = 456
        w.street_address = '123 Main St.'

        w = Well.objects.create(well_owner_id=owner)
        w.identification_plate_number = 3456332
        w.well_tag_number = 890
        w.street_address = '555 Government Street'

    def test_well_search(self):
   	    wells = Search.well_search('123', '', '', '')
   	    self.assertEqual(wells.count(), 1)