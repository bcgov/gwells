\echo 'Starting to clear tables procedure...'

-- Reset tables
\echo '... clearing gwells_well data table'
TRUNCATE TABLE gwells_well CASCADE;
\echo '... clearing gwells_intended_water_use data table'
TRUNCATE TABLE gwells_intended_water_use CASCADE;
\echo '... clearing gwells_well_class data table'
TRUNCATE TABLE gwells_well_class CASCADE;
\echo '... clearing gwells_province_state data table'
TRUNCATE TABLE gwells_province_state CASCADE;
\echo '... clearing gwells_drilling_method data table'
TRUNCATE TABLE gwells_drilling_method CASCADE;
\echo '...clearing gwells_decommission_method'
TRUNCATE TABLE gwells_decommission_method CASCADE;
\echo '... clearing gwells_lithology_colour data table'
TRUNCATE TABLE gwells_lithology_colour CASCADE;
\echo '... clearing gwells_lithology_hardness data table'
TRUNCATE TABLE gwells_lithology_hardness CASCADE;
\echo '... clearing gwells_land_district data table'
TRUNCATE TABLE gwells_land_district CASCADE;
\echo '...clearing gwells_lithology_material'
TRUNCATE TABLE gwells_lithology_material CASCADE;
\echo '...clearing gwells_lithology_description_code'
TRUNCATE TABLE gwells_lithology_description_code CASCADE;
\echo '...clearing gwells_liner_material'
TRUNCATE TABLE gwells_liner_material CASCADE;
\echo '...clearing gwells_surface_seal_material'
TRUNCATE TABLE gwells_surface_seal_material CASCADE;
\echo '...clearing gwells_surface_seal_method'
TRUNCATE TABLE gwells_surface_seal_method CASCADE;
\echo '...clearing gwells_surface_seal_method'
TRUNCATE TABLE gwells_surface_seal_method CASCADE;
\echo '...clearing gwells_surface_seal_material'
TRUNCATE TABLE gwells_surface_seal_material CASCADE;
\echo '... clearing gwells_casing_material'
TRUNCATE TABLE gwells_casing_material CASCADE;
\echo '... clearing gwells_yield_estimation_method'
TRUNCATE TABLE gwells_yield_estimation_method CASCADE;
\echo '... clearing gwells_screen_assembly_type'
TRUNCATE TABLE gwells_screen_assembly_type CASCADE;
\echo '... clearing gwells_development_method'
TRUNCATE TABLE gwells_development_method CASCADE;

\echo '... clearing gwells_well_yield_unit data table'
TRUNCATE TABLE gwells_well_yield_unit CASCADE;
\echo '... clearing gwells_ground_elevation_method data table'
TRUNCATE TABLE gwells_ground_elevation_method CASCADE;
\echo '... clearing gwells_well_status data table'
TRUNCATE TABLE gwells_well_status CASCADE;
\echo '... clearing gwells_licenced_status data table'
TRUNCATE TABLE gwells_licenced_status CASCADE;
\echo '... clearing gwells_screen_intake_method'
TRUNCATE TABLE gwells_screen_intake_method CASCADE;
\echo '... clearing gwells_drilling_company data table'
TRUNCATE TABLE gwells_drilling_company CASCADE;
\echo '... clearing gwells_screen_type'
TRUNCATE TABLE gwells_screen_type CASCADE;
\echo '... clearing gwells_screen_material'
TRUNCATE TABLE gwells_screen_material CASCADE;
\echo '... clearing gwells_screen_opening'
TRUNCATE TABLE gwells_screen_opening CASCADE;
\echo '... clearing gwells_screen_bottom'
TRUNCATE TABLE gwells_screen_bottom CASCADE;
\echo '... clearing gwells_observation_well_status'
TRUNCATE TABLE gwells_observation_well_status CASCADE;

/*
\echo '... clearing gwells_activity_submission data table'
TRUNCATE TABLE gwells_activity_submission CASCADE;
\echo '... clearing gwells_screen data table'
TRUNCATE TABLE gwells_screen CASCADE;
\echo '... clearing gwells_lithology_description data table'
TRUNCATE TABLE gwells_lithology_description;
\echo '... clearing gwells_casing data table'
TRUNCATE TABLE gwells_casing;
\echo '... clearing gwells_well_subclass data table'
TRUNCATE TABLE gwells_well_subclass CASCADE;
\echo '... clearing gwells_production_data'
TRUNCATE TABLE gwells_production_data CASCADE;
\echo '... clearing gwells_casing'
TRUNCATE TABLE gwells_casing CASCADE;
\echo '...clearing gwells_perforation'
TRUNCATE TABLE gwells_perforation CASCADE;
*/

\echo 'Finished clearing tables.'
