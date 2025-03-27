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
import json

from django.contrib.gis.geos import GEOSGeometry

from aquifers.models import Aquifer, VerticalAquiferExtentsHistory

FIELDS_TO_IGNORE = (
    'create_user',
    'create_date',
    'update_user',
    'update_date',
    'geom_simplified',
    'well',
    'activitysubmission',
    'resources',
    'verticalaquiferextent',
    'update_to_aquifer_set',
    'update_from_aquifer_set',
    'history',
)
KEY_VALUE_LOOKUP = {
    'material': 'description',
    'subtype': 'description',
    'vulnerability': 'description',
    'productivity': 'description',
    'demand': 'description',
    'known_water_use': 'description',
    'quality_concern': 'description',
}

def get_aquifer_history_diff(aquifer):
    """
    Returns a list of revisions for an aquifer, showing fields that changed in each revision.

    aquifer: a Django Aquifer model

    returns a list:
        [{
            diff: {},
            prev: {},
            user: string,
            date: date
        }]
    """

    history = []
    history += get_aquifer_reversion_history(aquifer)
    history += get_vertical_aquifer_extents_history(aquifer)

    history.sort(key=get_history_date, reverse=True)

    return history

def get_aquifer_reversion_history(aquifer):
    """
    Returns a list of history items for an aquifer from django-revision Version history records.

    returns a list:
        [{
            diff: {},
            prev: {},
            user: string,
            date: date
        }]
    """

    # pylint: disable=protected-access

    history_name = f'Aquifer {aquifer.aquifer_id}'

    reversion_history = aquifer.history.all().order_by('revision__date_created')

    all_fields = Aquifer._meta.get_fields()
    field_names = [field.name for field in all_fields if field.name not in FIELDS_TO_IGNORE]

    # store field that change and their value to compare to
    aquifer_composite = {}

    init_ver_obj = reversion_history[0]._object_version.object

    # build initial aquifer created entry
    history = [
        {
            'diff': {},
            'prev': {},
            'user': init_ver_obj.create_user,
            'date': init_ver_obj.create_date,
            'name': history_name,
            'created': True,
        }
    ]

    # Loop through all revisions for an aquifer to build the history
    for i, ver in enumerate(reversion_history):
        obj = ver._object_version.object
        diff = {}
        prev = {}

        for field_name in field_names:
            # Clean and transform history values
            prev_value = aquifer_composite.get(field_name, None)
            cur_value = clean_attrs(obj, field_name, ver)

            aquifer_composite[field_name] = cur_value

            # record a diff if cur_value and prev_value are not equal
            if cur_value != prev_value:
                diff[field_name] = cur_value
                prev[field_name] = prev_value

        item = {
            'diff': diff,
            'prev': prev,
            'name': history_name,
            'user': obj.update_user or obj.create_user,
            'date': obj.update_date or obj.create_date
        }

        if i > 0 and len(diff) > 0: # skip initial creation diff and empty diffs
            history.append(item)
    return history


def get_vertical_aquifer_extents_history(aquifer):
    """
    Returns a list of this aquifer's vertical extent history changes.

    returns a list:
        [{
            diff: {},
            prev: {},
            user: string,
            date: date
        }]
    """

    clean_keys = ['well_tag_number', 'start', 'end']

    vertical_aquifer_extents_history = VerticalAquiferExtentsHistory.objects \
        .filter(aquifer_id=aquifer.aquifer_id) \
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
    prev = {}
    for history_item in grouped_history:
        extents = []
        # cleans diff dict (removes geom, create_user, update_user, etc)
        for extent in history_item['extents']:
            extents.append({k:v for k, v in extent.items() if k in clean_keys})
        diff = {'extents': extents}
        item = {
            'diff': diff,
            'prev': prev,
            'name': f'Aquifer {aquifer.aquifer_id}\'s Vertical Extents',
            'user': history_item['user'],
            'date': history_item['date']
        }
        prev = diff

        history.append(item)
    return history


def get_history_date(history_item):
    """
    Returns the date of a history item
    """
    return history_item['date']


def clean_attrs(obj, key, ver):
    """
    Returns the value of a Reversion Version item
    """
    if obj is None:
        return None

    # For geom we need to deserialize the stored JSON text from the DB. This is because of an
    # error that is thrown because of an incompatibility between legacy Polygon versioned data
    # and the updated DB MultiPolygon.
    if key == 'geom':
        return json.loads(ver.serialized_data)[0]['fields'].get('geom')

    # get the value from the object
    val = getattr(obj, key, None)
    if val is None:
        return None

    # Key Value lookup
    if key in KEY_VALUE_LOOKUP:
        return getattr(val, KEY_VALUE_LOOKUP[key], None)

    # return original value if no type checks caught
    return val
