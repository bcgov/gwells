--  Run this script as gwells owner (e.g. psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER)
\echo 'Copying WellSearch static code tables from deployed image CSV files'

--INTENDED USE
\echo '... loading intended_water_use_code code table'
\copy intended_water_use_code (intended_water_use_code,description,display_order,create_date,update_date,create_user,update_user) from 'intended_water_use_code.csv' with header delimiter ',' CSV ;

--CLASS
\echo '... loading well_class_code code table'
\copy well_class_code (well_class_code,description,display_order,create_date,update_date,create_user,update_user) from 'well_class_code.csv' with header delimiter ',' CSV ;

--SUBCLASS
\echo '... loading well_subclass_code code table'
\copy well_subclass_code (well_subclass_guid,well_subclass_code,description,display_order,well_class_code,create_date,update_date,create_user,update_user) from 'well_subclass_code.csv' with header delimiter ',' CSV ;

--YIELD UNIT
\echo '... loading well_yield_unit_code code table'
\copy well_yield_unit_code (well_yield_unit_code,description,display_order,create_date,update_date,create_user,update_user) from 'well_yield_unit_code.csv' with header delimiter ',' CSV ;

--DRILLING METHOD
\echo '... loading drilling_method_code code table'
\copy drilling_method_code (drilling_method_code,description,display_order,create_date,update_date,create_user,update_user) from 'drilling_method_code.csv' with header delimiter ',' CSV ;

--GROUND ELEVATION
\echo '... loading ground_elevation_method_code code table'
\copy ground_elevation_method_code (ground_elevation_method_code,description,display_order,create_date,update_date,create_user,update_user) from 'ground_elevation_method_code.csv' with header delimiter ',' CSV ;

--STATUS
\echo '... loading well_status_code code table'
\copy well_status_code (well_status_code,description,display_order,create_date,update_date,create_user,update_user) from 'well_status_code.csv' with header delimiter ',' CSV ;

--LICENCE
\echo '... loading licenced_status_code code table'
\copy licenced_status_code (licenced_status_code,description,display_order,create_date,update_date,create_user,update_user) from 'licenced_status_code.csv' with header delimiter ',' CSV ;

--DRILLING COMPANY
\echo '... loading drilling_company code table'
\copy drilling_company (create_user,create_date,update_user,update_date,drilling_company_guid,drilling_company_code,name) from 'drilling_company.csv' with header delimiter ',' CSV ;

--SCREEN INTAKE METHOD
\echo '... loading screen_intake_method_code code table'
\copy screen_intake_method_code (create_user,create_date,update_user,update_date,screen_intake_code,description,display_order) from 'screen_intake_method_code.csv' with header delimiter ',' CSV ;

--SCREEN TYPE
\echo '... loading screen_type_code code table'
\copy screen_type_code (create_user,create_date,update_user,update_date,screen_type_code,description,display_order) from 'screen_type_code.csv' with header delimiter ',' CSV ;

--SCREEN MATERIAL
\echo '... loading screen_material_code code table'
\copy screen_material_code (create_user,create_date,update_user,update_date,screen_material_code,description,display_order) from 'screen_material_code.csv' with header delimiter ',' CSV ;

--SCREEN OPENING
\echo '... loading screen_opening_code code table'
\copy screen_opening_code (create_user,create_date,update_user,update_date,screen_opening_code,description,display_order) from 'screen_opening_code.csv' with header delimiter ',' CSV ;

--SCREEN BOTTOM
\echo '... loading screen_bottom_code code table'
\copy screen_bottom_code (create_user,create_date,update_user,update_date,screen_bottom_code,description,display_order) from 'screen_bottom_code.csv' with header delimiter ',' CSV ;

--SCREEN ASSEMBLY
\echo '... loading screen_assembly_type_code code table'
\copy screen_assembly_type_code (create_user,create_date,update_user,update_date,screen_assembly_type_code,description,display_order) from 'screen_assembly_type_code.csv' with header delimiter ',' CSV ;

--DEVELOPMENT METHOD
\echo '... loading development_method_code code table'
\copy development_method_code (create_user,create_date,update_user,update_date,development_method_code,description,display_order ) from 'development_method_code.csv' with header delimiter ',' CSV ;

--ESTIMATION METHOD
\echo '... loading yield_estimation_method_code code table'
\copy yield_estimation_method_code (create_user,create_date,update_user,update_date,yield_estimation_method_code,description,display_order) from 'yield_estimation_method_code.csv' with header delimiter ',' CSV ;

--CASING MATERIAL
\echo '... loading casing_material_code code table'
\copy casing_material_code (create_user,create_date,update_user,update_date,casing_material_code,description,display_order ) from 'casing_material_code.csv' with header delimiter ',' CSV ;

--SURFACE SEAL METHOD
\echo '... loading surface_seal_method_code code table'
\copy surface_seal_method_code (create_user,create_date,update_user,update_date,surface_seal_method_code,description,display_order ) from 'surface_seal_method_code.csv' with header delimiter ',' CSV ;

--SURFACE SEAL MATERIAL
\echo '... loading surface_seal_material_code table'
\copy surface_seal_material_code (create_user,create_date,update_user,update_date,surface_seal_material_code,description,display_order ) from 'surface_seal_material_code.csv' with header delimiter ',' CSV ;

--LINER MATERIAL
\echo '... loading liner_material_code code table'
\copy liner_material_code (create_user,create_date,update_user,update_date,liner_material_code,description,display_order) from 'liner_material_code.csv' with header delimiter ',' CSV ;

--LITHOLOGY COLOUR
\echo '... loading lithology_colour_code code table'
\copy lithology_colour_code (create_user,create_date,update_user,update_date,lithology_colour_code,description,display_order) from 'lithology_colour_code.csv' with header delimiter ',' CSV ;

--LITHOLOGY HARDNESS
\echo '... loading lithology_hardness_code code table'
\copy lithology_hardness_code (lithology_hardness_code,description,display_order,create_date,update_date,create_user,update_user) from 'lithology_hardness_code.csv' with header delimiter ',' CSV ;

--LAND DISTRICT
\echo '... loading land_district_code code table'
\copy land_district_code (create_user,create_date,update_user,update_date,land_district_code,name,display_order) from 'land_district_code.csv' with header delimiter ',' CSV ;

--LITHOLOGY MATERIAL
\echo '... loading lithology_material_code code table'
\copy lithology_material_code (create_user,create_date,update_user,update_date,lithology_material_code,description,display_order) from 'lithology_material_code.csv' with header delimiter ',' CSV ;

--LITHOLOGY DESCRIPTION
\echo '... loading lithology_description_code code table'
\copy lithology_description_code (create_user,create_date,update_user,update_date,lithology_description_code,description,display_order) from 'lithology_description_code.csv' with header delimiter ',' CSV ;

-- Thu 15 Feb 08:16:45 2018 GW Where is LITHOLOGY MOISTURE?

-- Thu 15 Feb 08:41:01 2018 GW Where is LITHOLOGY STRUCTURE?

-- Thu 15 Feb 09:40:03 2018 GW Where is SURFICIAL MATERIAL CODE?


--DECOMMISSION METHOD
\echo '... loading decommission_method_code code table'
\copy decommission_method_code (create_user,create_date,update_user,update_date,decommission_method_code,description,display_order) from 'decommission_method_code.csv' with header delimiter ',' CSV ;

--OBSERVATION WELL STATUS
\echo '... loading obs_well_status_code code table'
\copy obs_well_status_code (create_user,create_date,update_user,update_date,obs_well_status_code,description,display_order) from 'obs_well_status_code.csv' with header delimiter ',' CSV ;

-- BEDROCK STATUS (currently not used)
-- \echo '... loading bedrock_material_code code table'
-- \copy bedrock_material_code (bedrock_material_code,description,display_order,create_date,update_date,create_user,update_user) from 'bedrock_material_code.csv' with header delimiter ',' CSV ;


\echo 'Finshed copy of WellSearch static code tables.'
