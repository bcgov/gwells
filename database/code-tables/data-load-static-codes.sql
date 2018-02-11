--  Run this script as gwells owner (e.g. psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER)
\echo 'Copying static code tables from deployed image CSV files'

--INTENDED USE
\echo '... loading gwells_intended_water_use code table'
\copy gwells_intended_water_use (intended_water_use_guid,code,description,is_hidden,sort_order,create_date,update_date,create_user,update_user) from 'gwells_intended_water_use.csv' with header delimiter ',' CSV ;

--CLASS
\echo '... loading gwells_gwells_well_class code table'
\copy gwells_well_class (well_class_guid,code,description,is_hidden,sort_order,create_date,update_date,create_user,update_user) from 'gwells_well_class.csv' with header delimiter ',' CSV ;

--SUBCLASS
\echo '... loading gwells_gwells_well_subclass code table'
\copy gwells_well_subclass (well_subclass_guid,code,description,is_hidden,sort_order,well_class_guid,create_date,update_date,create_user,update_user) from 'gwells_well_subclass.csv' with header delimiter ',' CSV ;

--PROVINCE_STATE
\echo '... loading gwells_province_state_code code table'
\copy province_state_code (province_state_guid,code,description,sort_order,create_date,update_date,create_user,update_user) from 'province_state_code.csv' with header delimiter ',' CSV ;

--YIELD UNIT
\echo '... loading gwells_gwells_well_yield_unit code table'
\copy gwells_well_yield_unit (well_yield_unit_guid,code,description,sort_order,create_date,update_date,create_user,update_user) from 'gwells_well_yield_unit.csv' with header delimiter ',' CSV ;

--DRILLING METHOD
\echo '... loading gwells_drilling_method_code code table'
\copy drilling_method_code (drilling_method_guid,code,description,is_hidden,sort_order,create_date,update_date,create_user,update_user) from 'drilling_method_code.csv' with header delimiter ',' CSV ;

--GROUND ELEVATION
\echo '... loading gwells_gwells_ground_elevation_method code table'
\copy gwells_ground_elevation_method (ground_elevation_method_guid,code,description,is_hidden,sort_order,create_date,update_date,create_user,update_user) from 'gwells_ground_elevation_method.csv' with header delimiter ',' CSV ;

--STATUS
\echo '... loading gwells_well_status code table'
\copy gwells_well_status (well_status_guid,code,description,is_hidden,sort_order,create_date,update_date,create_user,update_user) from 'gwells_well_status.csv' with header delimiter ',' CSV ;

--LICENCE
\echo '... loading gwells_licenced_status code table'
\copy gwells_licenced_status (licenced_status_guid,code,description,is_hidden,sort_order,create_date,update_date,create_user,update_user) from 'gwells_licenced_status.csv' with header delimiter ',' CSV ;

--DRILLING COMPANY
\echo '... loading drilling_company code table'
\copy drilling_company (create_user,create_date,update_user,update_date,drilling_company_guid,drilling_company_code,name,is_hidden) from 'drilling_company.csv' with header delimiter ',' CSV ;

--SCREEN INTAKE METHOD
\echo '... loading gwells_screen_intake_method code table'
\copy gwells_screen_intake_method (create_user,create_date,update_user,update_date,screen_intake_method_guid,screen_intake_code,description,status_flag,is_hidden,sort_order) from 'gwells_screen_intake_method.csv' with header delimiter ',' CSV ;

--SCREEN TYPE
\echo '... loading gwells_screen_type code table'
\copy gwells_screen_type (create_user,create_date,update_user,update_date,screen_type_guid,screen_type_code,description,is_hidden,sort_order) from 'gwells_screen_type.csv' with header delimiter ',' CSV ;


--SCREEN MATERIAL
\echo '... loading gwells_screen_material code table'
\copy gwells_screen_material (create_user,create_date,update_user,update_date,screen_material_guid,screen_material_code,description,is_hidden,sort_order) from 'gwells_screen_material.csv' with header delimiter ',' CSV ;

--SCREEN OPENING
\echo '... loading gwells_screen_opening code table'
\copy gwells_screen_opening (create_user,create_date,update_user,update_date,screen_opening_guid,screen_opening_code,description,is_hidden,sort_order) from 'gwells_screen_opening.csv' with header delimiter ',' CSV ;

--SCREEN BOTTOM
\echo '... loading gwells_screen_bottom code table'
\copy gwells_screen_bottom (create_user,create_date,update_user,update_date,screen_bottom_guid,screen_bottom_code,description,is_hidden,sort_order) from 'gwells_screen_bottom.csv' with header delimiter ',' CSV ;

--SCREEN ASSEMBLY
\echo '... loading gwells_screen_assembly_type code table'
\copy gwells_screen_assembly_type (create_user,create_date,update_user,update_date,screen_assembly_type_guid,screen_assembly_type_code,description,is_hidden,sort_order) from 'gwells_screen_assembly_type.csv' with header delimiter ',' CSV ;

--DEVELOPMENT METHOD
\echo '... loading development_method_code code table'
\copy development_method_code (create_user,create_date,update_user,update_date,development_method_guid,development_method_code,description,is_hidden,sort_order ) from 'development_method_code.csv' with header delimiter ',' CSV ;

--ESTIMATION METHOD
\echo '... loading gwells_yield_estimation_method code table'
\copy gwells_yield_estimation_method (create_user,create_date,update_user,update_date,yield_estimation_method_guid,yield_estimation_method_code,description,is_hidden,sort_order) from 'gwells_yield_estimation_method.csv' with header delimiter ',' CSV ;

--CASING MATERIAL
\echo '... loading casing_material_code code table'
\copy casing_material_code (create_user,create_date,update_user,update_date,casing_material_guid,casing_material_code,description,is_hidden,sort_order ) from 'casing_material_code.csv' with header delimiter ',' CSV ;

--SURFACE SEAL METHOD
\echo '... loading gwells_surface_seal_method code table'
\copy gwells_surface_seal_method (create_user,create_date,update_user,update_date,surface_seal_method_guid,surface_seal_method_code,description,is_hidden,sort_order ) from 'gwells_surface_seal_method.csv' with header delimiter ',' CSV ;

--SURFACE SEAL MATERIAL
\echo '... loading gwells_surface_seal_material table'
\copy gwells_surface_seal_material (create_user,create_date,update_user,update_date,surface_seal_material_guid,surface_seal_material_code,description,is_hidden,sort_order ) from 'gwells_surface_seal_material.csv' with header delimiter ',' CSV ;

--LINER MATERIAL
\echo '... loading gwells_liner_material code table'
\copy gwells_liner_material (create_user,create_date,update_user,update_date,liner_material_guid,liner_material_code,description,is_hidden,sort_order) from 'gwells_liner_material.csv' with header delimiter ',' CSV ;

--LITHOLOGY COLOUR
\echo '... loading gwells_lithology_colour code table'
\copy gwells_lithology_colour (create_user,create_date,update_user,update_date,lithology_colour_guid,code,description,is_hidden,sort_order) from 'gwells_lithology_colour.csv' with header delimiter ',' CSV ;

--LITHOLOGY HARDNESS
\echo '... loading gwells_lithology_hardness code table'
\copy gwells_lithology_hardness (lithology_hardness_guid,code,description,is_hidden,sort_order,create_date,update_date,create_user,update_user) from 'gwells_lithology_hardness.csv' with header delimiter ',' CSV ;

--LAND DISTRICT
\echo '... loading gwells_land_district code table'
\copy gwells_land_district (create_user,create_date,update_user,update_date,land_district_guid,code,name,sort_order) from 'gwells_land_district.csv' with header delimiter ',' CSV ;

--LITHOLOGY MATERIAL
\echo '... loading gwells_lithology_material code table'
\copy gwells_lithology_material (create_user,create_date,update_user,update_date,lithology_material_guid,code,description,sort_order,status_flag) from 'gwells_lithology_material.csv' with header delimiter ',' CSV ;

--LITHOLOGY DESCRIPTION
\echo '... loading gwells_lithology_description_code code table'
\copy gwells_lithology_description_code (create_user,create_date,update_user,update_date,lithology_description_code_guid,code,description,sort_order) from 'gwells_lithology_description_code.csv' with header delimiter ',' CSV ;

--DECOMMISSION METHOD
\echo '... loading decommission_method_code code table'
\copy decommission_method_code (create_user,create_date,update_user,update_date,code,description,status_flag,sort_order,decommission_method_guid) from 'decommission_method_code.csv' with header delimiter ',' CSV ;

--OBSERVATION WELL STATUS
\echo '... loading gwells_observation_well_status code table'
\copy gwells_observation_well_status (create_user,create_date,update_user,update_date,observation_well_status_guid,code,description,is_hidden,sort_order) from 'gwells_observation_well_status.csv' with header delimiter ',' CSV ;

\echo 'Finshed copy of static code tables.'
