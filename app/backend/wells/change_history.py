import re
from deepdiff import DeepDiff
from django.contrib.gis.geos import GEOSGeometry


def get_well_history(well):
    # query records in history for this model.
    all_history = [obj for obj in well.history.all().order_by(
        '-revision__date_created')]

    # get all revisions associated with the well
    revisions = [r.revision for r in all_history]

    # create our containers for sorted well edits
    history = {
        'well': [],
        'liner': [],
        'liner perforation': [],
        'casing': [],
        'screen': [],
        'lithology description': [],
        'decommission description': []
    }

    # loop through each revision associated with the well and insert the field dictionaries into the containers
    for revision in revisions:
        time = revision.date_created.timestamp().__int__()
        edit_user = ''
        temp_history = {
            'well': [],
            'liner': [],
            'liner perforation': [],
            'casing': [],
            'screen': [],
            'lithology description': [],
            'decommission description': []
        }
        for version in revision.version_set.all():
            content_name = version.content_type.name
            if content_name == 'well':
                try:
                    edit_user = version.field_dict['update_user'] or version.field_dict['create_user']
                except:
                    pass
            try:
                if isinstance(version.field_dict['geom'], GEOSGeometry):
                    version.field_dict['geom'] = ', '.join(map(str, version.field_dict['geom'].coords))
            except:
                pass
            temp_history[content_name].append(version.field_dict)
        for temp_key, temp_val in temp_history.items():
            if temp_val:
                history[temp_key].append({'time': time, 'data': temp_val, 'user': edit_user})

    history_diff = []

    # loop through our grouped field dictionary objects and deep diff them to create our diffed history
    for key, value in history.items():
        for i in range(len(value)):
            if i == len(value) - 1:
                diff = DeepDiff(None, value[i]['data'], verbose_level=1, view='tree')
            else:
                if value[i + 1]['data'].__len__() == value[i]['data'].__len__():
                    diff = DeepDiff(value[i + 1]['data'], value[i]['data'], verbose_level=1, view='tree')
                else:
                    diff = DeepDiff(value[i + 1]['data'], value[i]['data'], verbose_level=1,
                                    view='tree', ignore_order=True, report_repetition=True)

            if diff != {}:
                # create our item object which will contain the formatted data sent back to the client
                item = {
                    "diff": {},
                    "prev": {},
                    "type": key.title(),
                    "action": '',
                    "user": value[i]['user'],
                    "date": value[i]['time']
                }

                # loop through version edit history and add changes/values to the item object
                for tk, tree in diff.items():
                    item['action'] = 'Edited'
                    for limb in tree.items:
                        if keep_key(limb.path()):
                            path = format_path(limb.path())
                            t2 = [] if str(limb.t2) == 'not present' else limb.t2
                            t1 = [] if str(limb.t1) == 'not present' else limb.t1
                            if type(t2) == dict:
                                t2 = [t2]
                            if type(t1) == dict:
                                t1 = [t1]
                            try:
                                if isinstance(t2[0]['geom'], GEOSGeometry):
                                    t2[0]['geom'] = ', '.join(map(str, t2[0]['geom'].coords))
                            except:
                                pass
                            try:
                                if isinstance(t1[0]['geom'], GEOSGeometry):
                                    t1[0]['geom'] = ', '.join(map(str, t1[0]['geom'].coords))
                            except:
                                pass
                            item['diff'][path] = t2
                            item['prev'][path] = t1
                        else:
                            pass

                if item['diff'] != {}:
                    history_diff.append(item)

    # sort our diffed edit objects by timestamp
    history_diff = sorted(history_diff, key=lambda x: x['date'], reverse=True)

    well_history = {
        'diff': history_diff,
        'create_user': well.create_user,
        'create_date': well.create_date
    }

    return well_history


# Removes the deep diff root/node nomenclature from our key names
def format_path(path):
    path = re.sub(r"^root.[0-9]].'", '', path)
    path = re.sub(r"']", '', path)
    path = re.sub(r"_", ' ', path)
    return path.title()


# Ignores keys which we do not want to be flagged as diffable
def keep_key(key):

    return key not in \
       [
            "root[0]['update_date']", "root[0]['update_user']", "root[0]['create_user']", "root[0]['expiry_date']",
            "root[0]['create_date']", "root[0]['liner_perforation_guid'].int",
            "root[0]['lithology_description_guid'].int", "root[0]['casing_guid'].int",
            "root[0]['decommission_description_guid'].int", "root[0]['screen_guid'].int",
            "root[0]['company_of_person_responsible_id'].int", "root[0]['person_responsible_id'].int",
            "root[1]['update_date']", "root[1]['update_user']", "root[1]['create_user']", "root[1]['expiry_date']",
            "root[1]['create_date']", "root[1]['liner_perforation_guid'].int",
            "root[1]['lithology_description_guid'].int", "root[1]['casing_guid'].int",
            "root[1]['decommission_description_guid'].int", "root[1]['screen_guid'].int",
            "root[1]['company_of_person_responsible_id'].int", "root[1]['person_responsible_id'].int"
       ]
