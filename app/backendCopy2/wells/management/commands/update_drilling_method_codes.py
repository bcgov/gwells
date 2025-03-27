from django.core.management.base import BaseCommand
from wells.models import DrillingMethodCode
from collections import defaultdict
import json

class Command(BaseCommand):
  help = "Update a value in the drilling_methods_code table"
  def update_drilling_method_codes(self):
    drilling_method_codes = open("gwells/fixtures/wellsearch-codetables.json")
    drilling_method_codes = json.load(drilling_method_codes)

    for item in drilling_method_codes:
        if item["model"] == "wells.drillingmethodcode":          
            DrillingMethodCode.objects.update_or_create(pk=item["pk"], defaults=item["fields"])
            
  def handle(self, *args, **options):
    self.update_drilling_method_codes()
    print("update_drilling_method_codes.py completed successfully")
