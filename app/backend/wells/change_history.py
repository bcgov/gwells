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

from gwells.models.bulk import BulkWellAquiferCorrelationHistory
from wells.models import ActivitySubmission, FieldsProvided
from wells.serializers import (
    CasingSummarySerializer,
    ScreenSerializer,
    LinerPerforationSerializer,
    DecommissionDescriptionSerializer,
    LithologyDescriptionSummarySerializer
)
from wells.stack import MANY_TO_MANY_LOOKUP, merge_series
from submissions.models import WELL_ACTIVITY_CODE_LEGACY, WELL_ACTIVITY_CODE_STAFF_EDIT
from aquifers.models import VerticalAquiferExtentsHistory

# Fields to skip when we are looping through the list of FieldsProvided for each submission.
# activity_submission = the field reference foreignkey to the submission
# well_activity_type = the code string for the kind of submission causes
#                      (https://apps.nrs.gov.bc.ca/int/jira/browse/WATER-784)
FIELDS_TO_IGNORE = ('activity_submission', 'well_activity_type')
KEY_VALUE_LOOKUP = {
    'well_publication_status': 'well_publication_status_code',
    'boundary_effect': 'description',
    'well_disinfected_status': 'description',
    'well_orientation_status': 'description',
    'drive_shoe_status': 'description',
    'owner_province_state': 'province_state_code',
    'well_class': 'description',
    'well_subclass': 'description',
    'intended_water_use': 'description',
    'land_district': 'name',
    'coordinate_acquisition_code': 'description',
    'aquifer_lithology': 'description',
    'well_yield_unit': 'well_yield_unit_code',
    'surface_seal_material': 'description',
    'surface_seal_method': 'description',
    'liner_material': 'code',
    'screen_intake_method': 'description',
    'screen_type': 'description',
    'screen_material': 'description',
    'screen_opening': 'description',
    'screen_bottom': 'description',
    'filter_pack_material': 'description',
    'filter_pack_material_size': 'description',
    'decommission_method': 'description',
    'company_of_person_responsible': 'name',
    'yield_estimation_method': 'description',
    'ground_elevation_method': 'description',
    'observation_well_status': 'obs_well_status_code',
    'well_status': 'well_status_code'
}
COMPOUND_KEY_VALUE_LOOKUP = {
    'aquifer': ['aquifer_id', 'aquifer_name'],
    'person_responsible': ['surname', 'first_name'],
}
FOREIGN_KEY_SERIALIZER_LOOKUP = {
    'casing_set': CasingSummarySerializer,
    'screen_set': ScreenSerializer,
    'linerperforation_set': LinerPerforationSerializer,
    'decommission_description_set': DecommissionDescriptionSerializer,
    'lithologydescription_set': LithologyDescriptionSummarySerializer
}
ALL_SUBMISSION_FOREIGN_KEY = [
    "well_activity_type",
    "well_status",
    "well_publication_status",
    "well_class",
    "well_subclass",
    "intended_water_use",
    "person_responsible",
    "company_of_person_responsible",
    "owner_province_state",
    "land_district",
    "coordinate_acquisition_code",
    "ground_elevation_method",
    "well_orientation_status",
    "surface_seal_material",
    "surface_seal_method",
    "liner_material",
    "screen_intake_method",
    "screen_type",
    "screen_material",
    "screen_opening",
    "screen_bottom",
    "filter_pack_material",
    "filter_pack_material_size",
    "well_disinfected_status",
    "well_yield_unit",
    "observation_well_status",
    "aquifer",
    "decommission_method",
    "boundary_effect",
    "aquifer_lithology",
    "yield_estimation_method",
]
ALL_SUBMISSION_MANY_TO_MANY_RELATIONS = [
    # models.ManyToManyField()
    "development_methods",
    "water_quality_characteristics",
    "drilling_methods",
    # Reverse Foreign keys to a submission
    "lithologydescription_set",
    "linerperforation_set",
    "casing_set",
    "screen_set",
    "decommission_description_set",
]

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
    all_submissions = ActivitySubmission.objects \
        .select_related(*ALL_SUBMISSION_FOREIGN_KEY) \
        .prefetch_related(*ALL_SUBMISSION_MANY_TO_MANY_RELATIONS) \
        .filter(well_id=well_tag_number) \
        .order_by('filing_number') \
        .all()

    submissions = []
    for submission in all_submissions:
        if submission.well_activity_type_id == WELL_ACTIVITY_CODE_LEGACY:
            # Always make sure the legacy record is frist
            submissions.insert(0, submission)
        else:
            submissions.append(submission)

    all_fields = FieldsProvided._meta.get_fields()
    all_fields_list = [field.name for field in all_fields if field.name not in FIELDS_TO_IGNORE]

    # store field that change and their value to compare to
    previous_changes = {}

    # Loop through all submission for a well to build the history
    history = []
    for submission in submissions:
        history_item = []

        # Get the list of changed fields for this submission. Only STAFF_EDITs will have
        # FieldsProvided. For everything else use the entire list of fields.
        fields_provided = FieldsProvided.objects.filter(activity_submission=submission.filing_number).first()
        if fields_provided is not None:
            field_names = [key for key, value in model_to_dict(fields_provided).items() if value and key not in FIELDS_TO_IGNORE]
        else:
            field_names = all_fields_list

        is_staff_edit = submission.well_activity_type_id == WELL_ACTIVITY_CODE_STAFF_EDIT

        for field_name in field_names:
            # Clean and transform history values
            prev_value = previous_changes.get(field_name, None)
            cur_value = clean_attrs(submission, field_name, prev_value)

            # We need to skip this field for non-staff-edits as any None value. A None means that
            # this field was not altered as part of the CON, ALT, DEC submission. We don't want to
            # overwrite the previous_changes with this None as it would imply that a non-staff-edit
            # set an existing value to None.
            if not is_staff_edit and cur_value is None:
                continue

            previous_changes[field_name] = cur_value

            # skip this if it is the same as the previous value (for some reason)
            if cur_value == prev_value:
                continue

            item = {
                "diff": cur_value,
                "prev": prev_value,
                "type": field_name,
                "action": action_type(cur_value, prev_value),
                "user": submission.create_user,
                "date": submission.create_date
            }

            history_item.append(item)

        # only add this item to the history list if it has changes
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


# transforms data between different relationship types
def clean_attrs(obj, key, prev_val):
    if obj is None:
        return None

    val = getattr(obj, key, None)
    if val is None:
        return None

    # Geo Point lookup
    if isinstance(val, GEOSGeometry):  # convert geo point type to string
        round5 = (round(val[0], 5), round(val[1], 5))
        return ', '.join(map(str, round5))

    # string concatenated multiple key val lookups:
    if key in COMPOUND_KEY_VALUE_LOOKUP:
        attrs = [getattr(val, source, None) for source in COMPOUND_KEY_VALUE_LOOKUP[key]]
        return ', '.join(str(attr) for attr in attrs if attr is not None)

    # Key Value lookup
    if key in KEY_VALUE_LOOKUP:
        return getattr(val, KEY_VALUE_LOOKUP[key], None)

    # Foreign Key lookup
    if key in FOREIGN_KEY_SERIALIZER_LOOKUP:
        if hasattr(val, 'instance'):
            Serializer = FOREIGN_KEY_SERIALIZER_LOOKUP[key]
            data_set = Serializer(val, many=True).data
            if len(data_set) > 0:
                # Staff edits contain the entire series. For everything else we merge
                if obj.well_activity_type_id != WELL_ACTIVITY_CODE_STAFF_EDIT:
                    if isinstance(prev_val, list):
                        return merge_series(prev_val, data_set)
                return data_set
            return None
        return val

    # Many To Many lookup
    if key in MANY_TO_MANY_LOOKUP:
        converted = []
        if hasattr(val, 'instance'):
            for item in val.all():
                converted.append({'code': getattr(item, MANY_TO_MANY_LOOKUP[key], None)})
        else:
            for item in val:
                converted.append(item)
        return converted if len(converted) > 0 else None

    # return original value if no type checks caught
    return val


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
