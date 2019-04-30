import re
from deepdiff import DeepDiff


def get_well_history(well):
    # query records in history for this model.
    all_history = [obj for obj in well.history.all().order_by(
        '-revision__date_created')]

    revisions = [r.revision for r in all_history]

    history = {
        'well': [],
        'liner': [],
        'casing': [],
        'screen': [],
        'lithology description': [],
        'decommission description': []
    }

    for revision in revisions:
        time = revision.date_created.timestamp().__int__()
        temp_history = {
            'well': [],
            'liner': [],
            'casing': [],
            'screen': [],
            'lithology description': [],
            'decommission description': []
        }
        for version in revision.version_set.all():
            content_name = version.content_type.name
            temp_history[content_name].append(version.field_dict)
        for temp_key, temp_val in temp_history.items():
            if temp_val:
                history[temp_key].append({'time': time, 'data': temp_val})

    history_diff = []

    for key, value in history.items():
        for i in range(len(value)):
            if key == 'well':
                if i == len(value) - 1:
                    break
                diff = DeepDiff(value[i + 1]['data'], value[i]['data'], verbose_level=1, view='tree')
            else:
                if i == len(value) - 1:
                    diff = DeepDiff(None, value[i]['data'], verbose_level=1, view='tree')
                else:
                    if value[i + 1]['data'].__len__() == value[i]['data'].__len__():
                        diff = DeepDiff(value[i + 1]['data'], value[i]['data'], verbose_level=1, view='tree')
                    else:
                        diff = DeepDiff(value[i + 1]['data'], value[i]['data'], verbose_level=1,
                                        view='tree', ignore_order=True, report_repetition=True)

            if diff != {}:
                user = ''
                try:
                    user = value[i]['data'][0]['update_user'] or value[i]['data'][0]['create_user']
                except:
                    pass

                item = {
                    "diff": {},
                    "prev": {},
                    "type": key.title(),
                    "action": '',
                    "user": user,
                    "date": value[i]['time']
                }

                for tk, tree in diff.items():
                    item['action'] = action_map(tk)  # values_changed, iterable_item_added, iterable_item_removed
                    for limb in tree.items:
                        if keep_key(limb.path()):
                            path = format_path(limb.path())
                            t2 = [] if str(limb.t2) == 'not present' else limb.t2
                            t1 = [] if str(limb.t1) == 'not present' else limb.t1
                            if type(t2) == dict:
                                t2 = [t2]
                            if type(t1) == dict:
                                t1 = [t1]
                            item['diff'][path] = t2
                            item['prev'][path] = t1
                        else:
                            pass

                if item['diff'] != {}:
                    history_diff.append(item)

    history_diff = sorted(history_diff, key=lambda x: x['date'], reverse=True)

    return history_diff


def format_path(path):
    path = re.sub(r"^root.[0-9]].'", '', path)
    path = re.sub(r"']", '', path)
    path = re.sub(r"_", ' ', path)
    return path.title()


def action_map(action):

    if action == 'iterable_item_added':
        return 'Added'
    elif action == 'iterable_item_removed':
        return 'Removed'
    elif action == 'values_changed':
        return 'Changed'
    elif action == 'type_changes':
        return 'Created'
    else:
        return action


def keep_key(key):

    return key != "root[0]['update_date']" and key != "root[0]['update_user']" \
        and key != "root[0]['create_user']" and key != "root[0]['expiry_date']" \
        and key != "root[0]['create_date']" and key != "root[0]['liner_perforation_guid'].int"  \
        and key != "root[0]['lithology_description_guid'].int" and key != "root[0]['casing_guid'].int" \
        and key != "root[0]['decommission_description_guid'].int" and key != "root[0]['screen_guid'].int" \
        and key != "root[1]['update_date']" and key != "root[1]['update_user']" \
        and key != "root[1]['create_user']" and key != "root[1]['expiry_date']" \
        and key != "root[1]['create_date']" and key != "root[1]['liner_perforation_guid'].int" \
        and key != "root[1]['lithology_description_guid'].int" and key != "root[1]['casing_guid'].int" \
        and key != "root[1]['decommission_description_guid'].int" and key != "root[1]['screen_guid'].int"