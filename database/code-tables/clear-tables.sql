\echo 'Starting to clear tables procedure...'

-- Reset tables
TRUNCATE TABLE gwells_well,intended_water_use_code,well_class_code,
  province_state_code,drilling_method_code,decommission_method_code,
  lithology_colour_code,lithology_hardness_code,land_district_code,
  lithology_material_code,gwells_lithology_description_code,
  liner_material_code,surface_seal_material_code,surface_seal_method_code,
  surface_seal_method_code,surface_seal_material_code,casing_material_code,
  gwells_yield_estimation_method,screen_assembly_type_code,development_method_code,
  gwells_well_yield_unit,ground_elevation_method_code,gwells_well_status,
  licenced_status_code,screen_intake_method_code,drilling_company,
  screen_type_code,screen_material_code,screen_opening_code,screen_bottom_code,
  obs_well_status_code CASCADE;

\echo 'Finished clearing tables.'