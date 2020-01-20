from django.contrib.gis.geos import GEOSGeometry
from django.forms.models import model_to_dict

from wells.models import (ActivitySubmission, FieldsProvided)
from wells.serializers import CasingSummarySerializer, ScreenSerializer, LinerPerforationSerializer, \
    DecommissionDescriptionSerializer, LithologyDescriptionSummarySerializer
from submissions.serializers import WellStaffEditSubmissionSerializer
from wells.stack import KEY_VALUE_LOOKUP, MANY_TO_MANY_LOOKUP
from submissions.models import WELL_ACTIVITY_CODE_LEGACY

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

    submissions = ActivitySubmission.objects.filter(well=well.well_tag_number).order_by('filing_number')
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

    well_history['history'] = history[::-1]  # we reverse the list to put newest edits at the top

    return well_history


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
