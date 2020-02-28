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
from decimal import Decimal

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.gis.geos import Point

from aquifers.models import Aquifer, VerticalAquiferExtent
from wells.models import Well
from gwells.models.bulk import BulkWellAquiferCorrelationHistory, BulkVerticalAquiferExtentsHistory
from gwells.permissions import (
    HasBulkWellAquiferCorrelationUploadRole,
    HasBulkVerticalAquiferExtentsUploadRole
)


logger = logging.getLogger(__name__)


class BulkWellAquiferCorrelation(APIView):
    """
    Changes multiple aquifers well correlations all at once
    """
    permission_classes = (HasBulkWellAquiferCorrelationUploadRole, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.change_log = []
        self.create_date = timezone.now()

    @swagger_auto_schema(auto_schema=None)
    @transaction.atomic
    def post(self, request, **kwargs):
        aquifers = request.data
        unknown_aquifers = []
        unknown_wells = []
        changes = {}
        wells_to_update = []

        # check for a ?commit querystring parameter for this /bulk API
        # this flag will actually perform the bulk_update() on the DB
        # without it will just check for errors and return the changes
        # that would have been made
        update_db = 'commit' in request.GET

        for aquifer in aquifers:
            aquifer_id = int(aquifer['aquiferId'])
            well_tag_numbers = aquifer['wellTagNumbers']

            # capture errors about any unknown aquifers
            aquifer = Aquifer.objects.filter(pk=aquifer_id).first()
            if aquifer is None:
                unknown_aquifers.append(aquifer_id)

            wells = Well.objects.filter(well_tag_number__in=well_tag_numbers)
            if len(wells) != len(well_tag_numbers):
                db_well_tag_numbers = [well.well_tag_number for well in wells]
                # capture errors about any unknown wells
                for well_id in list(set(well_tag_numbers) - set(db_well_tag_numbers)):
                    unknown_wells.append(well_id)

            # now figure out what has changed for each well
            for well in wells:
                well_tag_number = well.well_tag_number
                existing_aquifer_id = well.aquifer.aquifer_id if well.aquifer else None

                # No existing aquifer for this well? Must be a new correlation
                if existing_aquifer_id is None:
                    self.append_to_change_log(well_tag_number, aquifer_id, None)
                    change = {
                        'action': 'new',
                        'aquiferId': aquifer_id
                    }
                    wells_to_update.append(well)
                elif existing_aquifer_id != aquifer_id: # existing ids don't match - must be a change
                    self.append_to_change_log(well_tag_number, aquifer_id, existing_aquifer_id)
                    change = {
                        'action': 'update',
                        'existingAquiferId': existing_aquifer_id,
                        'newAquiferId': aquifer_id
                    }
                    wells_to_update.append(well)
                else: # all other cases must mean this well is unchanged
                    change = {
                        'action': 'same'
                    }

                if change:
                    changes[well_tag_number] = change

            if update_db:
                # change all well's to point to the new aquifer
                for well in wells:
                    well.aquifer = aquifer

        # if there are any unknown aquifers or wells then we want to return errors
        if len(unknown_aquifers) > 0 or len(unknown_wells) > 0:
            return self.return_errors(unknown_aquifers, unknown_wells, changes)

        if update_db: # no errors then updated the DB (if ?commit is passed in)
            self.update_wells(wells_to_update)

        # no errors then we return the changes that were (or could be) performed
        http_status = status.HTTP_200_OK if update_db else status.HTTP_202_ACCEPTED
        return JsonResponse(changes, status=http_status)

    def return_errors(self, unknown_aquifers, unknown_wells, changes):
        # roll back the transaction as the bulk_update could have run for one
        # aquifer but errored on another. Best to abort the whole thing and warn the user
        transaction.set_rollback(True)

        errors = {
            'unknownAquifers': unknown_aquifers,
            'unknownWells': unknown_wells,
            'changes': changes # always return the list of changes even if there are unknowns
        }

        return JsonResponse(errors, status=status.HTTP_400_BAD_REQUEST)

    def update_wells(self, wells):
        logger.info("Bulk updating %d wells", len(wells))
        # bulk update using efficient SQL for any well aquifer correlations that have changed
        Well.objects.bulk_update(wells, ['aquifer'])
        # save the BulkWellAquiferCorrelation records
        BulkWellAquiferCorrelationHistory.objects.bulk_create(self.change_log)

    def append_to_change_log(self, well_tag_number, to_aquifer_id, from_aquifer_id):
        bulk_history_item = BulkWellAquiferCorrelationHistory(
            well_id=well_tag_number,
            update_to_aquifer_id=to_aquifer_id,
            update_from_aquifer_id=from_aquifer_id,
            create_user=self.request.user.profile.username,
            create_date=self.create_date
        )
        self.change_log.append(bulk_history_item)


class BulkVerticalAquiferExtents(APIView):
    """
    Changes multiple vertical aquifer extents all at once
    """
    permission_classes = (HasBulkVerticalAquiferExtentsUploadRole, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conflicts = []
        self.change_log = []
        self.create_date = timezone.now()
        self.unknown_well_tag_numbers = set()
        self.unknown_aquifer_ids = set()

    @swagger_auto_schema(auto_schema=None)
    @transaction.atomic
    def post(self, request, **kwargs):
        vertical_aquifer_extents = request.data

        new_vae_models = []

        # check for a ?commit querystring parameter for this /bulk API
        # this flag will actually perform the bulk_update() on the DB
        # without it will just check for errors and return the changes
        # that would have been made
        update_db = 'commit' in request.GET

        incoming_vae_data = self.as_wells(vertical_aquifer_extents)

        incoming_well_tag_numbers = incoming_vae_data.keys()
        existing_wells = self.lookupExistingWells(incoming_well_tag_numbers)

        incoming_aquifer_ids = set(row['aquiferId'] for row in vertical_aquifer_extents)
        existing_aquifers = self.lookupExistingAquifers(incoming_aquifer_ids)

        if len(self.unknown_well_tag_numbers) > 0 or len(self.unknown_aquifer_ids) > 0:
            return self.return_errors()

        for well_tag_number, data in incoming_vae_data.items():
            well = existing_wells[well_tag_number]

            existing_data = VerticalAquiferExtent.objects \
                .filter(well_id=well_tag_number) \
                .order_by('start')[:]
            existing_aquifer_ids = [item.aquifer_id for item in existing_data]
            extents = [{'start': item.start, 'end': item.end} for item in existing_data]

            max_depth = float('-inf')
            data.sort(key=lambda item: item['fromDepth'])
            for vae in data:
                aquifer_id = vae['aquiferId']
                from_depth = Decimal(format(vae['fromDepth'], '.2f')) if vae['fromDepth'] is not None else None
                to_depth = Decimal(format(vae['toDepth'], '.2f')) if vae['toDepth'] is not None else Decimal('Infinity')

                if aquifer_id in existing_aquifer_ids:
                    self.addConflict(vae, 'Aquifer %s already defined for well' % aquifer_id)
                    continue
                if from_depth < 0:
                    self.addConflict(vae, 'From depth can not be less then zero')
                    continue
                if to_depth < 0:
                    self.addConflict(vae, 'To depth can not be less then zero')
                    continue
                if to_depth < from_depth:
                    self.addConflict(vae, 'From depth must be below to depth')
                    continue

                aquifer = existing_aquifers[aquifer_id]

                if self.checkExtentOverlaps(from_depth, to_depth, extents):
                    self.addConflict(vae, 'Overlaps with an existing vertical aquifer extent')
                    continue

                if from_depth < max_depth:
                    self.addConflict(vae, 'Overlaps with another vertical aquifer extent in the CSV')
                    continue
                max_depth = to_depth

                if update_db:
                    vae_model = self.buildVerticalAquiferExtentModel(well, aquifer, from_depth, to_depth)
                    new_vae_models.append(vae_model)
                    self.append_to_history_log(vae_model)

        # if there are any unknown aquifers or wells then we want to return errors
        if len(self.conflicts) > 0:
            return self.return_errors()

        if update_db: # no errors then updated the DB (if ?commit is passed in)
            self.create_vertical_aquifer_extents(new_vae_models)

        # no errors then we return the changes that were (or could be) performed
        http_status = status.HTTP_200_OK if update_db else status.HTTP_202_ACCEPTED
        return Response({}, status=http_status)

    def as_wells(self, vertical_aquifer_extents):
        wells = {}
        for record in vertical_aquifer_extents:
            wells.setdefault(record['wellTagNumber'], []).append(record)
        return wells

    def lookupExistingWells(self, well_tag_numbers):
        wells = Well.objects.filter(pk__in=well_tag_numbers)
        keyed_wells = {well.well_tag_number: well for well in wells}
        known_well_tag_numbers = set(keyed_wells.keys())

        self.unknown_well_tag_numbers = well_tag_numbers - known_well_tag_numbers

        return keyed_wells

    def lookupExistingAquifers(self, aquifer_ids):
        aquifers = Aquifer.objects.filter(pk__in=aquifer_ids)
        keyed_aquifers = {aquifer.aquifer_id: aquifer for aquifer in aquifers}
        known_aquifer_ids = set(keyed_aquifers.keys())

        self.unknown_aquifer_ids = aquifer_ids - known_aquifer_ids

        return keyed_aquifers

    def addConflict(self, data, msg):
        self.conflicts.append({
            **data,
            'message': msg,
        })

    def buildVerticalAquiferExtentModel(self, well, aquifer, from_depth, to_depth):
        if well.geom:
            longitude = well.geom.x
            latitude = well.geom.y

        point = Point(-abs(float(longitude)), float(latitude), srid=4326)

        return VerticalAquiferExtent(
            well=well,
            aquifer=aquifer,
            geom=point,
            start=from_depth,
            end=to_depth
        )

    def checkExtentOverlaps(self, from_depth, to_depth, existing_extents):
        if len(existing_extents) == 0:
            return False

        max_depth = float('-inf')
        for extent in existing_extents:
            start = extent['start']
            end = extent['end'] if extent['end'] is not None else Decimal('Infinity')
            if from_depth >= max_depth and to_depth <= start:
                return False
            max_depth = end
        return True

    def return_errors(self):
        # roll back the transaction as the bulk_update could have run for one
        # aquifer but errored on another. Best to abort the whole thing and warn the user
        transaction.set_rollback(True)
        errors = {
            'unknownAquifers': self.unknown_aquifer_ids,
            'unknownWells': self.unknown_well_tag_numbers,
            'conflicts': self.conflicts
        }
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def create_vertical_aquifer_extents(self, models):
        logger.info("Bulk updating %d VerticalAquiferExtents", len(models))
        # bulk update using efficient SQL for any well aquifer correlations that have changed
        VerticalAquiferExtent.objects.bulk_create(models)
        # save the BulkWellAquiferCorrelation records
        BulkWellAquiferCorrelationHistory.objects.bulk_create(self.change_log)

    def append_to_history_log(self, model):
        bulk_history_item = BulkVerticalAquiferExtentsHistory(
            well=model.well,
            aquifer=model.aquifer,
            geom=model.geom,
            start=model.start,
            end=model.end,
            create_user=self.request.user.profile.username,
            create_date=self.create_date
        )
        self.change_log.append(bulk_history_item)
