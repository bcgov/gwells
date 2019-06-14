import re
from deepdiff import DeepDiff
from django.contrib.gis.geos import GEOSGeometry
from django.forms.models import model_to_dict
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
from wells.models import (
    ActivitySubmission,
    FieldsProvided)

def get_well_history_old(well):
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


def get_well_history(well):
    submissions = ActivitySubmission.objects.filter(well=well.well_tag_number).order_by('-create_date')
    legacy_record = submissions.filter(well_activity_type='LEGACY').first()
    history = []

    for submission in submissions:
        history_item = []
        if submission.well_activity_type.code == 'LEGACY':
            continue
        fields_provided = FieldsProvided.objects.filter(activity_submission=submission.filing_number).first()
        fields_provided_dict = model_to_dict(fields_provided)
        for key, value in fields_provided_dict.items():
            if value and key != 'activity_submission':
                submission_value = getattr(submission, key)
                legacy_value = getattr(legacy_record, key)

                if submission_value is None and legacy_value is None:
                    continue

                item = {
                    "diff": clean_attrs(submission_value, key),
                    "prev": clean_attrs(legacy_value, key),
                    "type": key,
                    "action": '',
                    "user": submission.update_user,
                    "date": submission.update_date
                }
                if item['diff'] != item['prev']:
                    history_item.append(item)

                # update stacked legacy_record for next comparison loop
                if hasattr(legacy_value, 'instance'):
                    legacy_value.set(submission_value.all())
                else:
                    setattr(legacy_record, key, submission_value)

        if history_item:
            history.append(history_item)

    # history_diff = sorted(history_diff, key=lambda x: x['date'], reverse=True)

    well_history = {
        'diff': history,
        'create_user': well.create_user,
        'create_date': well.create_date
    }

    return well_history


def clean_attrs(obj, key):
    if obj is None:
        return None

    # convert geo point type to string
    if isinstance(obj, GEOSGeometry):
        round5 = (round(obj[0], 5), round(obj[1], 5))
        return ', '.join(map(str, round5))

    if key in KEY_VALUE_LOOKUP:
        return getattr(obj, KEY_VALUE_LOOKUP[key])

    # convert querysets to raw array objects
    if hasattr(obj, 'instance'):
        if isinstance(obj.instance._meta.get_field(key), (ManyToOneRel, ManyToManyRel)):
            converted = []
            for q in obj.all().values():
                converted.append(q)
            return converted

    # return original object if no type checks caught
    return obj


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

KEY_VALUE_LOOKUP = {
    'well_publication_status': 'well_publication_status_code',
    'boundary_effect': 'boundary_effect_code',
    'well_disinfected_status': 'well_disinfected_code',
    'drive_shoe_status': 'drive_shoe_code',
    'owner_province_state': 'province_state_code',
    'well_class': 'well_class_code',
    'well_subclass': 'well_subclass_guid',
    'intended_water_use': 'intended_water_use_code',
    'land_district': 'land_district_code',
    'coordinate_acquisition_code': 'code',
    'aquifer_lithology': 'aquifer_lithology_code',
    'well_yield_unit': 'well_yield_unit_code',
    'surface_seal_material': 'surface_seal_material_code',
    'surface_seal_method': 'surface_seal_method_code',
    'liner_material': 'code',
    'screen_intake_method': 'screen_intake_code',
    'screen_type': 'screen_type_code',
    'screen_material': 'screen_material_code',
    'screen_opening': 'screen_opening_code',
    'screen_bottom': 'screen_bottom_code',
    'filter_pack_material': 'filter_pack_material_code',
    'filter_pack_material_size': 'filter_pack_material_size_code',
    'decommission_method': 'decommission_method_code',
    'aquifer': 'aquifer_id',
    'person_responsible': 'person_guid',
    'company_of_person_responsible': 'org_guid',
    'aquifer_lithology': 'aquifer_lithology_code',
    'yield_estimation_method': 'yield_estimation_method_code',
    'ground_elevation_method': 'ground_elevation_method_code',
    'observation_well_status': 'obs_well_status_code',
    'well_status': 'well_status_code'
}