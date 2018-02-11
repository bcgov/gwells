\echo 'Starting to clear tables procedure...'

-- Reset tables
TRUNCATE TABLE gwells_well,gwells_intended_water_use,gwells_well_class,
  province_state_code,gwells_drilling_method,decommission_method_code,
  gwells_lithology_colour,gwells_lithology_hardness,gwells_land_district,
  gwells_lithology_material,gwells_lithology_description_code,
  gwells_liner_material,gwells_surface_seal_material,gwells_surface_seal_method,
  gwells_surface_seal_method,gwells_surface_seal_material,casing_material_code,
  gwells_yield_estimation_method,gwells_screen_assembly_type,development_method_code,
  gwells_well_yield_unit,gwells_ground_elevation_method,gwells_well_status,
  gwells_licenced_status,gwells_screen_intake_method,drilling_company,
  gwells_screen_type,gwells_screen_material,gwells_screen_opening,gwells_screen_bottom,
  gwells_observation_well_status CASCADE;

\echo 'Finished clearing tables.'