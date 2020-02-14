import logging

from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone

from aquifers.permissions import HasAquiferEditRole
from aquifers.models import Aquifer
from wells.models import Well
from gwells.models.bulk import BulkWellAquiferCorrelationHistory

logger = logging.getLogger(__name__)

class BulkWellAquiferCorrelation(APIView):
    """
    Changes multiple aquifers well correlations all at once
    """
    permission_classes = (HasAquiferEditRole, )

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
