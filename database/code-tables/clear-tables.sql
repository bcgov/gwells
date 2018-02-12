\echo 'Starting to clear tables procedure...'

-- Reset tables
TRUNCATE TABLE gwells_well,intended_water_use_code,gwells_well_class,
  province_state_code,drilling_method_code,decommission_method_code,
  lithology_colour_code,lithology_hardness_code,land_district_code,
  gwells_lithology_material,gwells_lithology_description_code,
  liner_material_code,gwells_surface_seal_material,gwells_surface_seal_method,
  gwells_surface_seal_method,gwells_surface_seal_material,casing_material_code,
  gwells_yield_estimation_method,gwells_screen_assembly_type,development_method_code,
  gwells_well_yield_unit,ground_elevation_method_code,gwells_well_status,
  licenced_status_code,gwells_screen_intake_method,drilling_company,
  gwells_screen_type,gwells_screen_material,gwells_screen_opening,gwells_screen_bottom,
  gwells_observation_well_status CASCADE;

\echo 'Finished clearing tables.'