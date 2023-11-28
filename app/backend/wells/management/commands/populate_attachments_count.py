from django.core.management.base import BaseCommand
from wells.models import WellAttachment, Well
from django.db.models import Count
from wells.constants import WELL_TAGS
from gwells.documents import MinioClient
from collections import defaultdict
import logging

class Command(BaseCommand):
    help = 'Iterate through well tags and appropriately update file counts'
    # Class Constants
    BATCH_SIZE = 100
    CLIENT = MinioClient(disable_private=False)

    def __init__(self):
        self.formatted_well_tags = self.format_well_tags()
        self.logger = logging.getLogger(__name__)
        super().__init__()
    
    def populate_wells_with_attachment_table(self):
        """Summary:
            Iterates existing well objects and creates entry in Attachments table if one doesn't already exist
        """
        # Batch processing: Set a limit for fetching wells without attachments
        batch_size = 100
        offset = 0

        while True:
            well_tag_numbers_without_attachment = (
                Well.objects
                .annotate(attachment_count=Count('wellattachment'))
                .filter(attachment_count=0)
                .values_list('well_tag_number', flat=True)[offset:offset + batch_size]
            )

            if not well_tag_numbers_without_attachment:
                break

            well_attachments_to_create = []

            # Iterate through each tag number and create WellAttachment instances
            for tag_number in well_tag_numbers_without_attachment:
                well_instance = Well.objects.get(well_tag_number=tag_number)
                well_attachment_instance = WellAttachment(well_tag_number=well_instance)
                well_attachments_to_create.append(well_attachment_instance)

            # Bulk create for the current batch
            WellAttachment.objects.bulk_create(well_attachments_to_create)

            # Move to the next batch
            offset += batch_size

            
    def format_well_tags(self):
        """Summary:
            Formats well tags at the start to reduce runtime of functions
        Returns:
            Array: formatted WELL_TAGS
        """
        return [tag['value'].replace(" ", "_").lower() for tag in WELL_TAGS]

            
    def get_well_tags(self, offset):
        """Summary:
        Gets and returns up to 100 well tag numbers to reduce memory load of function

        Args:
            offset (Number): Offset to reduce memory consumption in call

        Returns:
            Array: well tag numbers of batch
        """
        return (
            Well.objects
            .values('well_tag_number')[offset: offset + self.BATCH_SIZE]
            .values_list('well_tag_number', flat=True)
        )

    
    def get_or_create_entry(self, well_tag_number):
        if WellAttachment.objects.filter(well_tag_number=well_tag_number).exists():
            return WellAttachment.objects.get(well_tag_number=well_tag_number)
        else:
            well = Well.objects.get(well_tag_number=well_tag_number)
            return WellAttachment.objects.create(well_tag_number=well)
                   
    def process_well_tag(self, well_tag_number):
        """Summary:
            Queries for files related to a well tag and updates the counted values in the WellAttachments table
        """
        response = self.CLIENT.get_documents(int(well_tag_number), resource="well", include_private=True)
        hash_map = defaultdict(int)
        for doc in response['public']:
            split_file = doc["name"].split("_")
            if len(split_file) <= 3:
                value = split_file[1].replace(" ", "_").lower()
                if "." in value:
                    value = value.split(".")[0]
            else:
                value = split_file[1].lower() + "_" + split_file[2].lower()
            hash_map[value] = (hash_map[value] or 0) + 1
        for doc in response['private']:
            split_file = doc["name"].split("_")
            if len(split_file) <= 3:
                value = split_file[1].replace(" ", "_").lower()
            else:
                value = split_file[1].lower() + "_" + split_file[2].lower()
            hash_map[value] = (hash_map[value] or 0) + 1
        
        if hash_map:
            try:
                well_attachment_entry = self.get_or_create_entry(well_tag_number)
                for key, value in hash_map.items():
                    if "well_record" in key:
                        setattr(well_attachment_entry, 'well_construction', value)
                    elif key in self.formatted_well_tags:
                        setattr(well_attachment_entry, key, value)
                    else:
                        self.logger.info("Invalid file type for well %s: %s", well_tag_number, key)
                well_attachment_entry.save()
            except Exception as e:
                self.logger.error(e)
        
        
    def handle(self, *args, **options):
        """Summary:  
            Function to iterate through Minio buckets in order to get the sum of all files relating to a well,
            updates WellAttachment entry corresponding to well tag number
        """
        offset = 0
        self.populate_wells_with_attachment_table()
        while True:
            well_tag_numbers = self.get_well_tags(offset)
            if not well_tag_numbers: # No tags left to iterate
                break
            for well_tag_number in well_tag_numbers:
                self.process_well_tag(well_tag_number)    
            offset += self.BATCH_SIZE
