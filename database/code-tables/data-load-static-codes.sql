--  Run this script as gwells owner (e.g. psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER)
\echo 'Copying static code tables from deployed image CSV files'

--INTENDED USE
\echo '... loading gwells_intended_water_use code table'
\copy gwells_intended_water_use (intended_water_use_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_intended_water_use.csv' with header delimiter ',' CSV ;

--CLASS
\echo '... loading gwells_gwells_well_class code table'
\copy gwells_well_class (well_class_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_well_class.csv' with header delimiter ',' CSV ;

--SUBCLASS
\echo '... loading gwells_gwells_well_subclass code table'
\copy gwells_well_subclass (well_subclass_guid,code,description,is_hidden,sort_order,well_class_guid,when_created,when_updated,who_created,who_updated) from 'gwells_well_subclass.csv' with header delimiter ',' CSV ;

--PROVINCE_STATE
\echo '... loading gwells_gwells_province_state code table'
\copy gwells_province_state (province_state_guid,code,description,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_province_state.csv' with header delimiter ',' CSV ;

--YIELD UNIT
\echo '... loading gwells_gwells_well_yield_unit code table'
\copy gwells_well_yield_unit (well_yield_unit_guid,code,description,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_well_yield_unit.csv' with header delimiter ',' CSV ;

--DRILLING METHOD
\echo '... loading gwells_gwells_drilling_method code table'
\copy gwells_drilling_method (drilling_method_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_drilling_method.csv' with header delimiter ',' CSV ;

--GROUND ELEVATION
\echo '... loading gwells_gwells_ground_elevation_method code table'
\copy gwells_ground_elevation_method (ground_elevation_method_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_ground_elevation_method.csv' with header delimiter ',' CSV ;

--STATUS
\echo '... loading gwells_well_status code table'
\copy gwells_well_status (well_status_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_well_status.csv' with header delimiter ',' CSV ;

--LICENCE
\echo '... loading gwells_licenced_status code table'
\copy gwells_licenced_status (well_licenced_status_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'gwells_licenced_status.csv' with header delimiter ',' CSV ;

--DRILLING COMPANY
\echo '... loading gwells_drilling_company code table'
\copy gwells_drilling_company (who_created,when_created,who_updated,when_updated,drilling_company_guid,drilling_company_code,name,is_hidden) from 'gwells_drilling_company.csv' with header delimiter ',' CSV ;

--SCREEN INTAKE METHOD
\echo '... loading gwells_screen_intake_method code table'
\copy gwells_screen_intake_method (who_created,when_created,who_updated,when_updated,screen_intake_method_guid,screen_intake_code,description,status_flag,is_hidden,sort_order) from 'gwells_screen_intake_method.csv' with header delimiter ',' CSV ;

--SCREEN TYPE
\echo '... loading gwells_screen_type code table'
\copy gwells_screen_type (who_created,when_created,who_updated,when_updated,screen_type_guid,screen_type_code,description,is_hidden,sort_order) from 'gwells_screen_type.csv' with header delimiter ',' CSV ;


--SCREEN MATERIAL
\echo '... loading gwells_screen_material code table'
\copy gwells_screen_material (who_created,when_created,who_updated,when_updated,screen_material_guid,screen_material_code,description,is_hidden,sort_order) from 'gwells_screen_material.csv' with header delimiter ',' CSV ;

--SCREEN OPENING
\echo '... loading gwells_screen_opening code table'
\copy gwells_screen_opening (who_created,when_created,who_updated,when_updated,screen_opening_guid,screen_opening_code,description,is_hidden,sort_order) from 'gwells_screen_opening.csv' with header delimiter ',' CSV ;

--SCREEN BOTTOM
\echo '... loading gwells_screen_bottom code table'
\copy gwells_screen_bottom (who_created,when_created,who_updated,when_updated,screen_bottom_guid,screen_bottom_code,description,is_hidden,sort_order) from 'gwells_screen_bottom.csv' with header delimiter ',' CSV ;

--SCREEN ASSEMBLY
\echo '... loading gwells_screen_assembly_type code table'
\copy gwells_screen_assembly_type (who_created,when_created,who_updated,when_updated,screen_assembly_type_guid,screen_assembly_type_code,description,is_hidden,sort_order) from 'gwells_screen_assembly_type.csv' with header delimiter ',' CSV ;

--BCGS NUMBER
\echo '... loading gwells_bcgs_number code table'
\copy gwells_bcgs_number (who_created,when_created,who_updated,when_updated,bcgs_id,bcgs_number) from 'gwells_bcgs_number.csv' with header delimiter ',' CSV ;

--DEVELOPMENT METHOD
\echo '... loading gwells_development_method code table'
\copy gwells_development_method (who_created,when_created,who_updated,when_updated,development_method_guid,development_method_code,description,is_hidden,sort_order ) from 'gwells_development_method.csv' with header delimiter ',' CSV ;

--ESTIMATION METHOD
\echo '... loading gwells_yield_estimation_method code table'
\copy gwells_yield_estimation_method (who_created,when_created,who_updated,when_updated,yield_estimation_method_guid,yield_estimation_method_code,description,is_hidden,sort_order) from 'gwells_yield_estimation_method.csv' with header delimiter ',' CSV ;

--CASING MATERIAL
\echo '... loading gwells_casing_material code table'
\copy gwells_casing_material (who_created,when_created,who_updated,when_updated,casing_material_guid,casing_material_code,description,is_hidden,sort_order ) from 'gwells_casing_material.csv' with header delimiter ',' CSV ;

\echo 'Finshed copy of static code tables.'
