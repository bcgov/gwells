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
import re


def get_fk_description(obj, field, value):
    """
    Returns a human readable representation (name, description etc.) for a foreign key id

    Checks for presence of a 'name' or 'description' field on the related object. If not present,
    defaults back to the object's id (e.g. the guid)

    obj: an instance of a Version object (django-reversion)
    field: name of a foreign key field
    value: the value of the foreign key field (an id for a related model instance)
    """

    related_object = None

    try:
        related_object = obj.revision.version_set.get(object_id=value)
    except:
        # unable to find related object matching foreign key
        # this can occur if related record wasn't logged along with the edited record
        return value

    # return the 'description' or 'name' field, if available
    return related_object.field_dict.get('description') or related_object.field_dict.get('name') or value


def generate_history_diff(collection, identifier=None):
    """
    Returns a list of revisions for a record, showing fields that changed in each revision.

    collection: a list of Version objects (django-reversion)
    identifier: optional description of the object being edited (e.g. 'Geoexchange Driller Application')

    returns a list:
        [{
            diff: {},
            prev: {},
            user: string,
            date: date
        }]

    """
    history_diff = []

    for i in range(len(collection)):
        changed = False
        cur_ver = collection[i]
        cur = collection[i].field_dict
        prev = None

        if i < (len(collection) - 1):
            prev_ver = collection[i+1]
            prev = collection[i+1].field_dict

        item = {
            "diff": {},
            "prev": {},
            "user": cur['update_user'] or cur['create_user'],
            "date": cur['update_date'] or cur['create_date']
        }

        if identifier:
            item["name"] = identifier

        # Check if revision is the first one (initial version of record)
        if prev is None:
            item['created'] = True
            history_diff.append(item)

        else:
            for key, value in prev.items():
                # loop through the previous record and add changed fields to the 'diff' dict
                # leave out update/create stamps
                if (cur[key] != value and
                        key != "update_date" and
                        key != "update_user" and
                        key != "create_date" and
                        key != "create_user"):

                    if re.match('[\w]+_id$', key):
                        # key looks like a foreign key field

                        # strip trailing _id from field name
                        key_stripped = re.sub('_id$', '', key)

                        # try to generate a human readable string
                        item['diff'][key_stripped] = get_fk_description(
                            cur_ver, key, cur[key])
                        item['prev'][key_stripped] = get_fk_description(
                            prev_ver, key, value)

                    else:
                        item['diff'][key] = cur[key]
                        item['prev'][key] = value

                    changed = True
            if changed:
                history_diff.append(item)

    return history_diff
