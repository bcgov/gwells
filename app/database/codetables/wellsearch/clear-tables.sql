\echo 'Starting to clear tables procedure...'

-- Reset tables
TRUNCATE TABLE well,intended_water_use_code,well_class_code,
  drilling_method_code,decommission_method_code,
  lithology_colour_code,lithology_hardness_code,land_district_code,
  lithology_material_code,lithology_description_code,
  liner_material_code,surface_seal_material_code,surface_seal_method_code,
  surface_seal_method_code,surface_seal_material_code,casing_material_code,
  yield_estimation_method_code,screen_assembly_type_code,development_method_code,
  well_yield_unit_code,ground_elevation_method_code,well_status_code,
  licenced_status_code,screen_intake_method_code,drilling_company,
  screen_type_code,screen_material_code,screen_opening_code,screen_bottom_code,
  obs_well_status_code CASCADE;
  
-- TRUNCATE TABLE province_state_code CASCADE;

\echo 'Finished clearing tables.'

/* NOTE that 'real' content data tables are:

activity_submission
activity_submission_water_quality
aquifer_well
bcgs_number
casing
driller
drilling_company
ltsa_owner
perforation
production_data
registries_contact_detail
registries_organization
registries_person
registries_register
registries_register_note
registries_well_qualification
screen
water_quality_characteristic
well

*/