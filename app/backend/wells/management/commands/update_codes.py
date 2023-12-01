from django.core.management import call_command
from django.core.management.base import BaseCommand
import os, fnmatch

class Command(BaseCommand):
  file_pattern = 'update_*_codes.py'
  folder_path = './wells/management/commands'
  help = f'Run all commands using the {file_pattern} format'
  
  
  def handle(self, *args, **options):
    matching_files = []
    for file_name in os.listdir(self.folder_path):
        if fnmatch.fnmatch(file_name, self.file_pattern):
            matching_files.append(file_name)
    print(len(matching_files), "files found")
    for file_path in matching_files:
      call_command(file_path.replace(".py",""))
    print("update_codes has completed successfully")
