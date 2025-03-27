from django.core.management.base import BaseCommand
from wells.models import PumpingTestDescriptionCode
from collections import defaultdict
import json

class Command(BaseCommand):
  help = "Update values in the pumping_test_description_code table"
  
  def update_pumping_test_description_codes(self):
    pumping_test_description_codes = open("wells/migrations/pumping_test_description_codes.json")
    pumping_codes = json.load(pumping_test_description_codes)
    for entry in pumping_codes:
      PumpingTestDescriptionCode.objects.update_or_create(pk=entry["pk"], defaults=entry["fields"])

  def handle(self, *args, **options):
    self.update_pumping_test_description_codes()
    print("update_pumping_test_description_codes.py completed successfully")
