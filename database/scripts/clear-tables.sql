DROP FUNCTION IF EXISTS clear_tables();

CREATE OR REPLACE FUNCTION clear_tables() RETURNS void AS $$
BEGIN

raise notice 'Starting clear_tables() procedure...';

-- Reset tables
raise notice '... clearing gwells.lithology_description data table';
delete from gwells.lithology_description;
raise notice '... clearing gwells.activity_submission data table';
delete from gwells.activity_submission;
raise notice '... clearing gwells.well data table';
delete from gwells.well;

raise notice '... clearing gwells.intended_water_use data table';
delete from gwells.intended_water_use;
raise notice '... clearing gwells.well_subclass data table';
delete from gwells.well_subclass;
raise notice '... clearing gwells.well_class data table';
delete from gwells.well_class;

raise notice '... clearing gwells.province_state data table';
delete from gwells.province_state;
raise notice '... clearing gwells.well_yield_unit data table';
delete from gwells.well_yield_unit;
raise notice '... clearing gwells.drilling_method data table';
delete from gwells.drilling_method;
raise notice '... clearing gwells.ground_elevation_method data table';
delete from gwells.ground_elevation_method;
raise notice '... clearing gwells.land_district data table';
delete from gwells.land_district;
raise notice '... clearing gwells.well_status data table';
delete from gwells.well_status;
raise notice '... clearing gwells.licensed_status data table';
delete from gwells.licensed_status;

raise notice 'Finished clear_tables() procedure.';
END;
$$ LANGUAGE plpgsql;
