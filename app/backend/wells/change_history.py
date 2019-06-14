from django.contrib.gis.geos import GEOSGeometry
from django.forms.models import model_to_dict
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
from django.db.models.fields.related import ManyToManyField
from wells.models import (ActivitySubmission, FieldsProvided)


def get_well_history(well):

    well_history = {
        'history': None,
        'create_user': well.create_user,
        'create_date': well.create_date
    }

    submissions = ActivitySubmission.objects.filter(well=well.well_tag_number).order_by('filing_number')
    legacy_record = submissions.earliest('filing_number')  # filter(well_activity_type='LEGACY').first()

    if legacy_record:
        legacy_copy = model_to_dict(legacy_record)  # We use a copy of the legacy record as our composite stacker
    else:
        return well_history  # Return empty history if a legacy record hasn't been created yet

    history = []
    for submission in submissions:
        history_item = []
        if submission.well_activity_type.code == 'LEGACY':
            continue
        fields_provided = FieldsProvided.objects.filter(activity_submission=submission.filing_number).first()
        fields_provided_dict = model_to_dict(fields_provided)
        for key, value in fields_provided_dict.items():
            if value and key != 'activity_submission':
                submission_value = clean_attrs(getattr(submission, key), key)
                legacy_value = clean_attrs(legacy_copy.get(key, None), key)

                if submission_value is None and legacy_value is None:
                    continue

                item = {
                    "diff": submission_value,
                    "prev": legacy_value,
                    "type": key,
                    "action": '',
                    "user": submission.update_user,
                    "date": submission.update_date
                }
                if item['diff'] != item['prev']:
                    history_item.append(item)

                legacy_copy[key] = item['diff']

        if history_item:
            history.append(history_item)

    well_history['history'] = history.sort()

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
        if isinstance(obj.instance._meta.get_field(key), (ManyToOneRel, ManyToManyRel, ManyToManyField)):
            converted = []
            for q in obj.all().values():
                converted.append(q)
            return converted if len(converted) > 0 else None

    # return original object if no type checks caught
    return obj


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