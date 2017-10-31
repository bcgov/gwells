DROP FUNCTION IF EXISTS copy_remote_code_tables();

CREATE OR REPLACE FUNCTION copy_remote_code_tables() RETURNS void AS $$
BEGIN

raise notice 'Starting copy_remote_code_tables() procedure...';

-- Get static code tables from GitHub
raise notice '... importing gwells_intended_water_use code table';
copy gwells_intended_water_use (intended_water_use_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_intended_water_use.csv -O - -q' header delimiter ',' CSV ;

raise notice '... importing gwells_class code table';
copy gwells_well_class (well_class_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_well_class.csv -O - -q' header delimiter ',' CSV ;

raise notice '... importing gwells_subclass code table';
copy gwells_well_subclass (well_subclass_guid,code,description,is_hidden,sort_order,well_class_guid,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_well_subclass.csv -O - -q' header delimiter ',' CSV ;

raise notice '... importing gwells_province_state code table';
copy gwells_province_state (province_state_guid,code,description,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_province_state.csv -O - -q' header delimiter ',' CSV ;

raise notice '... importing gwells_well_yield_unit code table';
copy gwells_well_yield_unit (well_yield_unit_guid,code,description,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_well_yield_unit.csv -O - -q' header delimiter ',' CSV ;

raise notice '... importing gwells_drilling_method code table';
copy gwells_drilling_method (drilling_method_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_drilling_method.csv -O - -q' header delimiter ',' CSV ;

raise notice '... importing gwells_ground_elevation_method code table';
copy gwells_ground_elevation_method (ground_elevation_method_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_ground_elevation_method.csv -O - -q' header delimiter ',' CSV ;

raise notice '... importing gwells_well_status code table';
copy gwells_well_status (well_status_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_well_status.csv -O - -q' header delimiter ',' CSV ;

raise notice '... importing gwells_licensed_status code table';
copy gwells_licensed_status (well_licensed_status_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from program 'wget https://raw.githubusercontent.com/bcgov/gwells/master/database/code-tables/gwells_licensed_status.csv -O - -q' header delimiter ',' CSV ;

raise notice '... importing gwells_land_district data table';
INSERT INTO gwells_land_district (
  land_district_guid,code,name,sort_order,when_created,when_updated,who_created,who_updated)
SELECT
  gen_random_uuid(),LEGAL_LAND_DISTRICT_CODE,LEGAL_LAND_DISTRICT_NAME,SORT_ORDER,WHEN_CREATED,
  coalesce(WHEN_UPDATED,WHEN_CREATED),WHO_CREATED ,coalesce(WHO_UPDATED,WHO_CREATED) -- STATUS_FLAG
FROM WELLS.WELLS_LEGAL_LAND_DIST_CODES
ORDER BY LEGAL_LAND_DISTRICT_CODE ASC;


raise notice 'Finished copy_remote_code_tables() procedure.';
END;
$$ LANGUAGE plpgsql;
