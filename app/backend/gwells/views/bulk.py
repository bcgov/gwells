import logging

from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from django.http import JsonResponse

from aquifers.permissions import HasAquiferEditRole
from aquifers.models import Aquifer
from wells.models import Well
from gwells.models.bulk import BulkHistory

logger = logging.getLogger(__name__)

class BulkWellAquiferCorrelation(APIView):
    """
    Changes multiple aquifers well correlations all at once
    """
    permission_classes = (HasAquiferEditRole, )

    @swagger_auto_schema(auto_schema=None)
    @transaction.atomic
    def post(self, request, **kwargs):
        aquifers = request.data
        unknown_aquifers = []
        unknown_wells = []
        changes = {}
        patch_log = []
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
                    patch_log.append({
                        'op': 'add',
                        'path': '/well/%d/aquifer' % well_tag_number,
                        'value': aquifer_id
                    })
                    change = {
                        'action': 'new',
                        'aquiferId': aquifer_id
                    }
                    wells_to_update.append(well)
                elif existing_aquifer_id != aquifer_id: # existing ids dont' match must be a change
                    # record a JSON patch 'test' with the existing aquifer_id
                    patch_log.append({
                        'op': 'test',
                        'path': '/well/%d/aquifer' % well_tag_number,
                        'value': existing_aquifer_id
                    })
                    # record the change to the new aquifer_id
                    patch_log.append({
                        'op': 'replace',
                        'path': '/well/%d/aquifer' % well_tag_number,
                        'value': aquifer_id
                    })
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
        elif update_db: # no errors then updated the DB (if ?commit is passed in)
            self.update_wells(wells_to_update, patch_log)

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
            'changes': changes # always return the list of changes even if there are unknown wells and/or aquifers
        }

        return JsonResponse(errors, status=status.HTTP_400_BAD_REQUEST)

    def update_wells(self, wells, patch_log):
        logger.info("Bulk updating %d wells", len(wells))
        # bulk update using efficient SQL for any well aquifer correlations that have changed
        Well.objects.bulk_update(wells, ['aquifer'])
        # save a record in BulkHistory to record the list of changes to the DB in JSON Patch format
        BulkHistory.objects.create(
            operation_name='well-aquifer-correlation',
            record=patch_log,
            create_user=self.request.user.profile.username
        )
