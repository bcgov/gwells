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
import uuid
import datetime
import logging
import reversion
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from reversion.models import Version
from gwells.models import AuditModel

User = get_user_model()
logger = logging.getLogger(__name__)

@reversion.register()
class Aquifer(AuditModel):
    """
    An underground layer of water-bearing permeable rock, rock fractures or unconsolidated materials
    (gravel, sand, or silt), from which groundwater is extracted using a water well. 

    This table holds ONLY the aquifers to which we have associated one or more wells.  It is not
    the definitive source of all aquifers in the province. 

    """
    aquifer_id = models.PositiveIntegerField(
        primary_key=True, editable=False, verbose_name="Aquifer ID Number")
    aquifer_name = models.CharField(max_length=100)
    location_description = models.CharField(
        max_length=100, blank=True, verbose_name='Description of Location')

    """
    See https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/groundwater-wells/aquifers/aquifer-subtype-code-description

    gwells=# select distinct aquifer_subtype_code  from wells.gw_aquifer_attrs order by 1;
    aquifer_subtype_code
    ----------------------
    1a
    1b
    1c
    2
    3
    4a
    4b
    4c
    5a
    5b
    6a
    6b
    UNK
    (13 rows)

    """
    subtype_code = models.CharField(
        max_length=2, blank=True, verbose_name='Aquifer subtype')


    """

    aquifer_materials
    -------------------
    Bedrock
    Gravel
    Sand
    Sand and Gravel

    """
    material = models.CharField(
        max_length=100, blank=True, verbose_name='Aquifer Name')


    name = models.CharField(
        max_length=100, blank=True, verbose_name='Aquifer Name')


    """
    aquifer_ranking_value
    -----------------------
                        5
                        6
                        7
                        8
                        9
                        10
                        11
                        12
                        13
                        14
                        15
                        16
                        17
                        18
                        19
                        20

    """

    """
    gwells=# \edit
    demand
    ----------
    High
    Low
    Moderate

    """



    """
     productivity
    --------------
    High
    Low
    Moderate
    
    """

    """
     quality_concerns
    ------------------
    Isolated
    Local
    None
    Regional
    
    """

    """
    quantity_concerns
    -------------------
    Isolated
    Local
    None
    Regional
    """
"""
aquifer_id                  | integer                        | not null  | (key 'true')
 aquifer_subtype_code        | character varying(10)          | not null  |
 adjoining_mapsheet          | character varying(3)           |           |
 aquifer_classification      | character varying(30)          |           |
 aquifer_materials           | character varying(18)          |           |
 aquifer_ranking_value       | numeric(25,0)                  |           |
 demand                      | character varying(9)           |           |
 litho_stratographic_unit    | character varying(78)          |           |
 productivity                | character varying(12)          |           |
 quality_concerns            | character varying(40)          |           |
 quantity_concerns           | character varying(40)          |           |
 size_km2                    | numeric(12,1)                  |           |
 type_of_water_use           | character varying(21)          |           |
 vulnerability               | character varying(13)          |           |
 aquifer_description_rpt_ind | character varying(1)           | not null  |
 aquifer_statistics_rpt_ind  | character varying(1)           | not null  |


    aquifer_id = models.PositiveIntegerField(verbose_name="Aquifer Number", blank=True, null=True)

    well_tag_number = models.ForeignKey(Well, db_column='well_tag_number', to_field='well_tag_number',
                                        on_delete=models.CASCADE, blank=False, null=False)
"""
    history = GenericRelation(Version)

    class Meta:
        db_table = 'aquifer'
        verbose_name_plural = 'Aquifers'

    def __str__(self):
        return '%s - %s' % (
            self.aquifer_id,
            self.aquifer_name
        )

"""
    Hydraulic properties of the well, usually determined via tests.
"""
@reversion.register()
class HydraulicProperty(AuditModel):

    hydraulic_property_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well_tag_number = models.ForeignKey(Well, db_column='well_tag_number', to_field='well_tag_number',
                                        on_delete=models.CASCADE, blank=False, null=False)

    history = GenericRelation(Version)

   class Meta:
        db_table = 'hydraulic_property'
        verbose_name_plural = 'Hydraulic Properties'

    def __str__(self):
        return '%s' % (
            self.well_tag_number
        )