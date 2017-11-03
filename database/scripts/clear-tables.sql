DROP FUNCTION IF EXISTS clear_tables();

CREATE OR REPLACE FUNCTION clear_tables() RETURNS void AS $$
BEGIN

raise notice 'Starting clear_tables() procedure...';

-- Reset tables
raise notice '... clearing gwells_lithology_description data table';
DELETE FROM gwells_lithology_description;

raise notice '... clearing gwells_activity_submission data table';
DELETE FROM gwells_activity_submission;

raise notice '... clearing gwells_well data table';
DELETE FROM gwells_well;

raise notice '... clearing gwells_intended_water_use data table';
DELETE FROM gwells_intended_water_use;

raise notice '... clearing gwells_well_subclass data table';
DELETE FROM gwells_well_subclass;

raise notice '... clearing gwells_well_class data table';
DELETE FROM gwells_well_class;

raise notice '... clearing gwells_province_state data table';
DELETE FROM gwells_province_state;

raise notice '... clearing gwells_well_yield_unit data table';
DELETE FROM gwells_well_yield_unit;

raise notice '... clearing gwells_drilling_method data table';
DELETE FROM gwells_drilling_method;

raise notice '... clearing gwells_ground_elevation_method data table';
DELETE FROM gwells_ground_elevation_method;

raise notice '... clearing gwells_land_district data table';
DELETE FROM gwells_land_district;

raise notice '... clearing gwells_well_status data table';
DELETE FROM gwells_well_status;

raise notice '... clearing gwells_licenced_status data table';
DELETE FROM gwells_licenced_status;

raise notice 'Finished clear_tables() procedure.';
END;
$$ LANGUAGE plpgsql;
