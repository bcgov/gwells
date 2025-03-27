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
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.db.models import Count

from aquifers.models import Aquifer


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Updates aquifers if the demand (L,M,H) value has changed
    """

    def add_arguments(self, parser):
        parser.add_argument('-a', '--aquifer', help='aquifer number to update demand')

    @transaction.atomic
    def handle(self, *_args, **options):
        qs = Aquifer.objects.all()

        # optionally only update the one aquifer
        if options['aquifer']:
            qs = qs.filter(pk=options['aquifer'])

        qs = qs.annotate(num_correlated_wells=Count('well'))

        count = 0

        for aquifer in qs:
            aquifer_id = aquifer.aquifer_id
            before_demand = aquifer.demand_id
            try:
                changed = update_aquifer_demand(aquifer)

                if changed:
                    count += 1
                    logger.info("Changing aquifer %s demand from %s to %s",
                                aquifer_id, before_demand, aquifer.demand_id)
                else:
                    logger.debug("No changes to aquifer %s demand stays at %s",
                                aquifer_id, aquifer.demand_id)
            except:
                logger.exception("Failed to compute demand for aquifer %d", aquifer_id)
                raise
        logger.info("Updated %d aquifers", count)

def update_aquifer_demand(aquifer, num_correlated_wells=None):
    """
    Updates the demand of an aquifer
    """
    if num_correlated_wells is None:
        num_correlated_wells = aquifer.num_correlated_wells

    if num_correlated_wells is None:
        raise Exception("update_aquifer_demand() called with num_correlated_wells = None")

    # Use aquifer geom.area as the area column only has one decimal place of precision and some
    # aquifers (e.g. 778) are so small that they will return `Decimal(0.0)`.
    if not aquifer.geom:
        return False

    area = aquifer.geom.area / 1_000_000 # convert to km²
    demand = aquifer_demand(area, num_correlated_wells)

    if demand != aquifer.demand_id:
        aquifer.demand_id = demand
        aquifer.save()
        return True
    return False

def aquifer_demand(aquifer_area_sqkm, num_correlated_wells):
    """
    Calculates the aquifer demand
    """
    if aquifer_area_sqkm is None or num_correlated_wells == 0:
        return 'L'

    num_wells_per_km_sq = num_correlated_wells / aquifer_area_sqkm
    if num_wells_per_km_sq <= 4:
        return 'L'
    elif num_wells_per_km_sq > 20:
        return 'H'
    else:
        return 'M'
