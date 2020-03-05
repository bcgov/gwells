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
from django.contrib.gis.geos import GEOSGeometry
from django.forms.models import model_to_dict

from wells.models import (ActivitySubmission, FieldsProvided)
from wells.serializers import CasingSummarySerializer, ScreenSerializer, LinerPerforationSerializer, \
    DecommissionDescriptionSerializer, LithologyDescriptionSummarySerializer
from submissions.serializers import WellStaffEditSubmissionSerializer
from submissions.models import WELL_ACTIVITY_CODE_LEGACY
from wells.stack import KEY_VALUE_LOOKUP, MANY_TO_MANY_LOOKUP
from gwells.models.bulk import BulkWellAquiferCorrelationHistory
from aquifers.models import VerticalAquiferExtentsHistory

# Fields to skip when we are looping through the list of FieldsProvided for each submission.
# activity_submission = the field reference foreignkey to the submission
# well_activity_type = the code string for the kind of submission causes https://apps.nrs.gov.bc.ca/int/jira/browse/WATER-784
FIELDS_TO_IGNORE = ('activity_submission', 'well_activity_type')


def get_well_history(well):
    well_history = {
        'history': None,
        'create_user': well.create_user,
        'create_date': well.create_date
    }

    well_tag_number = well.well_tag_number

    history = []
    history += get_well_submission_history(well_tag_number)
    history += get_well_aquifer_correlation_history(well_tag_number)
    history += get_vertical_aquifer_extents_history(well_tag_number)

    history.sort(key=get_history_date, reverse=True)

    well_history['history'] = history

    return well_history

def get_well_submission_history(well_tag_number):
    submissions = ActivitySubmission.objects \
        .filter(well_id=well_tag_number) \
        .order_by('filing_number')
    legacy_record = submissions.filter(well_activity_type=WELL_ACTIVITY_CODE_LEGACY).first()

    legacy_copy = None
    # We use a copy of the legacy record as our composite stacker
    if legacy_record:
        legacy_copy = WellStaffEditSubmissionSerializer(legacy_record).data

    history = []
    for submission in submissions: # Loop through all submission for a well to build the history
        if submission.well_activity_type.code == WELL_ACTIVITY_CODE_LEGACY:
            continue

        fields_provided = FieldsProvided.objects.filter(activity_submission=submission.filing_number).first()
        if fields_provided is None:
            continue

        history_item = []
        fields_provided_dict = model_to_dict(fields_provided)
        for key, value in fields_provided_dict.items():
            if not value or key in FIELDS_TO_IGNORE: # skip some of the fields
                continue

            # clean and transform our history values
            submission_value = clean_attrs(getattr(submission, key), key)
            legacy_value = clean_attrs(legacy_copy.get(key, None), key) if legacy_copy else None

            if submission_value is None and legacy_value is None:
                continue

            item = {
                "diff": submission_value,
                "prev": legacy_value,
                "type": key,
                "action": action_type(submission_value, legacy_value),
                "user": submission.update_user,
                "date": submission.update_date
            }

            if item['diff'] != item['prev']:
                history_item.append(item)

            if legacy_copy:
                legacy_copy[key] = item['diff']  # update the composite each loop

        if len(history_item) > 0:
            history.append(history_item)
    return history

def get_well_aquifer_correlation_history(well_tag_number):
    bulk_well_aquifer_correlation_history = BulkWellAquiferCorrelationHistory.objects \
        .filter(well_id=well_tag_number) \
        .order_by('create_date')

    history = []
    for bulk_history_item in bulk_well_aquifer_correlation_history:
        to_aquifer_id = bulk_history_item.update_to_aquifer.aquifer_id
        from_aquifer_id = None
        if bulk_history_item.update_from_aquifer:
            from_aquifer_id = bulk_history_item.update_from_aquifer.aquifer_id

        item = {
            "diff": to_aquifer_id,
            "prev": from_aquifer_id,
            "type": 'aquifer',
            "action": 'Added' if bulk_history_item.update_from_aquifer is None else 'Updated',
            "user": bulk_history_item.create_user,
            "date": bulk_history_item.create_date
        }

        history.append([item])
    return history

def get_vertical_aquifer_extents_history(well_tag_number):
    clean_keys = ['aquifer_id', 'start', 'end', 'create_date', 'create_user']

    vertical_aquifer_extents_history = VerticalAquiferExtentsHistory.objects \
        .filter(well_tag_number=well_tag_number) \
        .order_by('create_date', 'start') \
        .values()

    if len(vertical_aquifer_extents_history) == 0:
        return []

    index = -1
    create_date = None
    grouped_history = []
    # loop through batches of history items grouping by all the ones with the same create_date
    for history_item in vertical_aquifer_extents_history:
        if history_item['create_date'] != create_date:
            index += 1
            create_date = history_item['create_date']
            grouped_history.append({
                'user': history_item['create_user'],
                'date': create_date,
                'extents': []
            })
        # append to the list of extents in this group
        grouped_history[index]['extents'].append(history_item)

    history = []
    prev = None
    for history_item in grouped_history:
        diff = []
        # cleans diff dict (removes geom, create_user, update_user, etc)
        for extent in history_item['extents']:
            diff.append({k:v for k, v in extent.items() if k in clean_keys})
        item = {
            "diff": diff,
            "prev": prev,
            "type": 'vertical_aquifer_extents',
            "action": 'Added' if prev is None else 'Updated',
            "user": history_item['user'],
            "date": history_item['date']
        }
        prev = diff

        history.append([item])
    return history


def get_history_date(history_items):
    if len(history_items) > 0:
        return history_items[0]['date']
    return None

# transforms data between different relatioship types
def clean_attrs(obj, key):
    if obj is None or obj is [] or obj is '':
        return None

    # Geo Point lookup
    elif isinstance(obj, GEOSGeometry):  # convert geo point type to string
        round5 = (round(obj[0], 5), round(obj[1], 5))
        return ', '.join(map(str, round5))

    # Key Value lookup
    elif key in KEY_VALUE_LOOKUP:
        if type(obj) == str:
            return obj
        else:
            return getattr(obj, KEY_VALUE_LOOKUP[key], None)

    # Foreign Key lookup
    elif key in FOREIGN_KEY_SERIALIZER_LOOKUP:
        if hasattr(obj, 'instance'):
            Serializer = FOREIGN_KEY_SERIALIZER_LOOKUP[key]
            return Serializer(obj, many=True).data
        else:
            return obj

    # Many To Many lookup
    elif key in MANY_TO_MANY_LOOKUP:
        converted = []
        if hasattr(obj, 'instance'):
            for item in obj.all():
                converted.append({'code': getattr(item, MANY_TO_MANY_LOOKUP[key], None)})
        else:
            for item in obj:
                converted.append(item)
        return converted if len(converted) > 0 else None

    # return original object if no type checks caught
    return obj


def action_type(diff, prev):
    empty_diff = diff is None or diff is [] or diff is ''
    empty_prev = prev is None or prev is [] or prev is ''
    if empty_diff:
        return 'Removed'
    elif not empty_diff and empty_prev:
        return 'Added'
    elif not empty_diff and not empty_prev:
        return 'Updated'
    else:
        return 'Edited'


FOREIGN_KEY_SERIALIZER_LOOKUP = {
    'casing_set': CasingSummarySerializer,
    'screen_set': ScreenSerializer,
    'linerperforation_set': LinerPerforationSerializer,
    'decommission_description_set': DecommissionDescriptionSerializer,
    'lithologydescription_set': LithologyDescriptionSummarySerializer
}
