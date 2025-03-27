from django.core.management.base import BaseCommand
from aquifers.models import AquiferResourceSection
from collections import defaultdict
import json

class Command(BaseCommand):
  help = "Update values in the aquifer_resource_section_code table"
  def update_analysis_method_codes(self):
    codes_file = open("aquifers/migrations/aquifer_resource_sections.json")
    aquifer_resource_sections_codes = json.load(codes_file)
    for entry in aquifer_resource_sections_codes:
      AquiferResourceSection.objects.update_or_create(pk=entry["pk"], defaults=entry["fields"])
    
  def handle(self, *args, **options):
    self.update_analysis_method_codes()
    print("update_aquifer_resource_section_code.py completed successfully")
