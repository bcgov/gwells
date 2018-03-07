"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from .AuditModel import AuditModel
from .ActivitySubmission import ActivitySubmission
from .Well import Well
from .LithologyDescriptionCode import LithologyDescriptionCode
from .LithologyColourCode import LithologyColourCode
from .LithologyHardnessCode import LithologyHardnessCode
from .LithologyMaterialCode import LithologyMaterialCode
from .WellYieldUnitCode import WellYieldUnitCode
from .BedrockMaterialCode import BedrockMaterialCode
from .BedrockMaterialDescriptorCode import BedrockMaterialDescriptorCode
from .LithologyStructureCode import LithologyStructureCode
from .LithologyMoistureCode import LithologyMoistureCode
from .SurficialMaterialCode import SurficialMaterialCode

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class LithologyDescription(AuditModel):
    """
    Lithology information details
    """
    lithology_description_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True)
    well_tag_number = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    lithology_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='From', blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    lithology_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='To', blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    lithology_raw_data = models.CharField(max_length=250, blank=True, null=True, verbose_name='Raw Data')

    lithology_description = models.ForeignKey(LithologyDescriptionCode, db_column='lithology_description_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Description")
    lithology_colour = models.ForeignKey(LithologyColourCode, db_column='lithology_colour_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Colour')
    lithology_hardness = models.ForeignKey(LithologyHardnessCode, db_column='lithology_hardness_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Hardness')
    lithology_material = models.ForeignKey(LithologyMaterialCode, db_column='lithology_material_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Material")

    water_bearing_estimated_flow = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, verbose_name='Water Bearing Estimated Flow')
    water_bearing_estimated_flow_units = models.ForeignKey(WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Units')
    lithology_observation = models.CharField(max_length=250, blank=True, null=True, verbose_name='Observations')

    bedrock_material = models.ForeignKey(BedrockMaterialCode, db_column='bedrock_material_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Bedrock Material')
    bedrock_material_descriptor = models.ForeignKey(BedrockMaterialDescriptorCode, db_column='bedrock_material_descriptor_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Descriptor')
    lithology_structure = models.ForeignKey(LithologyStructureCode, db_column='lithology_structure_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Bedding')
    lithology_moisture = models.ForeignKey(LithologyMoistureCode, db_column='lithology_moisture_code', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Moisture')
    surficial_material = models.ForeignKey(SurficialMaterialCode, db_column='surficial_material_code', related_name='surficial_material_set', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Surficial Material')
    secondary_surficial_material = models.ForeignKey(SurficialMaterialCode, db_column='secondary_surficial_material_code', related_name='secondary_surficial_material_set', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Secondary Surficial Material')

    lithology_sequence_number = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_description'
        ordering=["lithology_sequence_number"]
    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.lithology_from, self.lithology_to)
        else:
            return 'well {} {} {}'.format(self.well, self.lithology_from, self.lithology_to)
