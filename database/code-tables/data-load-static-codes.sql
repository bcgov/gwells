--  Run this script as gwells owner (e.g. psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER)
\echo 'Copying static code tables from deployed image CSV files'	

\echo '... loading gwells_intended_water_use code table'	
\copy gwells_intended_water_use (intended_water_use_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_intended_water_use.csv' with header delimiter ',' CSV ; 
\echo '... loading gwells_gwells_well_class code table'
\copy gwells_well_class (well_class_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_well_class.csv' with header delimiter ',' CSV ; 
\echo '... loading gwells_gwells_well_subclass code table'
\copy gwells_well_subclass (well_subclass_guid,code,description,is_hidden,sort_order,well_class_guid,when_created,when_updated,who_created,who_updated) from 'gwells_well_subclass.csv' with header delimiter ',' CSV ; 
\echo '... loading gwells_gwells_province_state code table'
\copy gwells_province_state (province_state_guid,code,description,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_province_state.csv' with header delimiter ',' CSV ; 
\echo '... loading gwells_gwells_well_yield_unit code table'
\copy gwells_well_yield_unit (well_yield_unit_guid,code,description,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_well_yield_unit.csv' with header delimiter ',' CSV ; 
\echo '... loading gwells_gwells_drilling_method code table'
\copy gwells_drilling_method (drilling_method_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_drilling_method.csv' with header delimiter ',' CSV ; 
\echo '... loading gwells_gwells_ground_elevation_method code table'
\copy gwells_ground_elevation_method (ground_elevation_method_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_ground_elevation_method.csv' with header delimiter ',' CSV ; 
\echo '... loading gwells_well_status code table'
\copy gwells_well_status (well_status_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_well_status.csv' with header delimiter ',' CSV ; 
\echo '... loading gwells_licensed_status code table'
\copy gwells_licensed_status (well_licensed_status_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_licensed_status.csv' with header delimiter ',' CSV ; 

\echo 'Finshed copy of static code tables.'