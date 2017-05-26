from django.test import TestCase
from .models import WellOwner, ProvinceState, WellActivity, WellActivityType, ClassOfWell, SubclassOfWell, DrillingCompany, Driller
from .search import Search
import datetime

class SearchTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        prov = ProvinceState.objects.create(sort_order=1)
        prov.save()

        activity_type = WellActivityType.objects.create(sort_order=1)
        activity_type.save()

        class_of_well = ClassOfWell.objects.create(sort_order=1)
        class_of_well.save()

        c = DrillingCompany.objects.create()
        c.save()

        d = Driller.objects.create(drilling_company=c)


        w = WellActivity.objects.create(well_activity_type=activity_type, class_of_well=class_of_well, driller_responsible=d, activity_start_date=datetime.date.today(), activity_end_date = datetime.date.today())
        w.identification_plate_number = 123
        w.well_tag_number = 456
        w.street_address = '123 Main St.'
        w.legal_plan = '7789'
        w.save()

        w2 = WellActivity.objects.create(well_activity_type=activity_type, class_of_well=class_of_well, driller_responsible=d, activity_start_date=datetime.date.today(), activity_end_date = datetime.date.today())
        w2.identification_plate_number = 3456332
        w2.well_tag_number = 890
        w2.street_address = '555 Government Street'
        w2.legal_district_lot = '789'
        w2.save()

        w3 = WellActivity.objects.create(well_activity_type=activity_type, class_of_well=class_of_well, driller_responsible=d, activity_start_date=datetime.date.today(), activity_end_date = datetime.date.today())
        w3.identification_plate_number = 55555
        w3.well_tag_number = 123
        w3.street_address = '200 Main Street'
        w3.pid = 54321
        w3.save()

        owner = WellOwner.objects.create(province_state=prov, well_activity=w)
        owner.full_name = 'John Smith'
        owner.save()

        owner = WellOwner.objects.create(province_state=prov, well_activity=w)
        owner.full_name = 'John Doe'
        owner.save()

        owner = WellOwner.objects.create(province_state=prov, well_activity=w2)
        owner.full_name = 'Jane Doe'
        owner.save()

        owner = WellOwner.objects.create(province_state=prov, well_activity=w3)
        owner.full_name = 'Joe Smith'
        owner.save()



    def test_well_search_well_number(self):
   	    wells = Search.well_search('123', '', '', '')
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


