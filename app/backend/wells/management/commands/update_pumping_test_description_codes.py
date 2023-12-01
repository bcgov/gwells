from django.core.management.base import BaseCommand
from wells.models import PumpingTestDescriptionCode
from collections import defaultdict
import json

class Command(BaseCommand):
  
  def __init__(self):
    pass
  
  def update_pumping_test_description_codes(self):
    pumping_test_description_codes = open("wells/migrations/pumping_test_description_codes.json")
    pumping_codes = json.load(pumping_test_description_codes)
    for entry in pumping_codes:
      print(entry['fields']['description'])
      PumpingTestDescriptionCode.objects.update_or_create(pk=entry["pk"], defaults=entry["fields"])
    

  def handle(self, *args, **options):
    self.update_pumping_test_description_codes()
