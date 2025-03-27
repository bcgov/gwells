from django.core.management.base import BaseCommand
from wells.models import AnalysisMethodCode
from collections import defaultdict
import json

class Command(BaseCommand):
  help = "Update values in the analysis_method_code table"
  def update_analysis_method_codes(self):
    analysis_method_codes = open("wells/migrations/analysis_method_codes.json")
    analysis_codes = json.load(analysis_method_codes)
    for entry in analysis_codes:
      AnalysisMethodCode.objects.update_or_create(pk=entry["pk"], defaults=entry["fields"])
    
  def handle(self, *args, **options):
    self.update_analysis_method_codes()
    print("update_analysis_method_codes.py completed successfully")
