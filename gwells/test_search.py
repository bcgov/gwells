from django.test import TestCase
from .models import ProvinceState, Well, WellActivityType, WellClass, DrillingCompany, Driller
from .search import Search
import datetime

class SearchTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        prov = ProvinceState.objects.create(sort_order=1)
        prov.save()

        #activity_type = WellActivityType.objects.create(sort_order=1)
        #activity_type.save()

        well_class = WellClass.objects.create(sort_order=1)
        well_class.save()

        #c = DrillingCompany.objects.create()
        #c.save()

        #d = Driller.objects.create(drilling_company=c)


        w = Well.objects.create(well_class=well_class, owner_province_state=prov)
        w.identification_plate_number = 123
        w.street_address = '123 Main St.'
        w.legal_plan = '7789'
        w.owner_full_name = 'John Smith'
        w.save()

        w2 = Well.objects.create(well_class=well_class, owner_province_state=prov)
        w2.identification_plate_number = 3456332
        w2.street_address = '555 Government Street'
        w2.legal_district_lot = '789'
        w2.owner_full_name = 'Jane Doe'
        w2.save()

        w3 = Well.objects.create(well_class=well_class, owner_province_state=prov)
        w3.identification_plate_number = 1
        w3.street_address = '200 Main Street'
        w3.pid = 54321
        w3.owner_full_name = 'Joe Smith'
        w3.save()



    def test_well_search_well_number(self):
   	    wells = Search.well_search('1', '', '', '')
   	    self.assertEqual(wells.count(), 2)



    def test_well_search_address(self):
   	    wells = Search.well_search('', 'gov', '', '')
   	    self.assertEqual(wells.count(), 1)



    def test_well_search_legal(self):
   	    wells = Search.well_search('', '', '78', '')
   	    self.assertEqual(wells.count(), 2)



    #def test_well_search_legal_pid(self):
    #    """ Check that pid can be found when searching with leading zeros
    #        even though field is stored as an integer
    #    """
    #    wells = Search.well_search('', '', '000054321', '')
    #    self.assertEqual(wells.count(), 1)



    def test_well_search_owner(self):
   	    wells = Search.well_search('', '', '', 'smi')
   	    self.assertEqual(wells.count(), 2)



    def test_well_search_well_number_owner(self):
   	    wells = Search.well_search('123', '', '', 'john')
   	    self.assertEqual(wells.count(), 1)



    def test_well_search_params_named_positional(self):
        named = Search.well_search(addr='gov')
        positional = Search.well_search('', 'gov', '', '')
        self.assertEqual(named.count(), positional.count())



    def test_well_search_empty_string_params(self):
        wells = Search.well_search('', '', '', '')
        self.assertIsNone(wells)



    def test_well_search_none_params(self):
        wells = Search.well_search(None, None, None, None)
        self.assertIsNone(wells)


