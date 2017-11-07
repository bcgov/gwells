\echo 'Starting clear_tables() procedure...'

-- Reset tables
\echo '... clearing gwells_lithology_description data table'
DELETE FROM gwells_lithology_description;

\echo '... clearing gwells_activity_submission data table'
DELETE FROM gwells_activity_submission;

\echo '... clearing gwells_well data table'
DELETE FROM gwells_well;

\echo '... clearing gwells_intended_water_use data table'
DELETE FROM gwells_intended_water_use;

\echo '... clearing gwells_well_subclass data table'
DELETE FROM gwells_well_subclass;

\echo '... clearing gwells_well_class data table'
DELETE FROM gwells_well_class;

\echo '... clearing gwells_province_state data table'
DELETE FROM gwells_province_state;

\echo '... clearing gwells_well_yield_unit data table'
DELETE FROM gwells_well_yield_unit;

\echo '... clearing gwells_drilling_method data table'
DELETE FROM gwells_drilling_method;

\echo '... clearing gwells_ground_elevation_method data table'
DELETE FROM gwells_ground_elevation_method;

\echo '... clearing gwells_land_district data table'
DELETE FROM gwells_land_district;

\echo '... clearing gwells_well_status data table'
DELETE FROM gwells_well_status;

\echo '... clearing gwells_licenced_status data table'
DELETE FROM gwells_licenced_status;

\echo '... clearing gwells_drilling_company data table'
DELETE FROM gwells_drilling_company;

\echo '... clearing gwells_screen_intake_method'
DELETE FROM gwells_screen_intake_method;

\echo '... clearing gwells_screen_type'
DELETE FROM gwells_screen_type;

\echo '... clearing gwells_screen_material'
DELETE FROM gwells_screen_material;

\echo '... clearing gwells_screen_opening'
DELETE FROM gwells_screen_opening;

\echo '... clearing gwells_screen_bottom'
DELETE FROM gwells_screen_bottom;

\echo 'Finished clear_tables() procedure.'
