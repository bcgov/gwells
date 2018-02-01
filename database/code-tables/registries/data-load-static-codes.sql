--  @Registries
--  Run this script as gwells owner (e.g. psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f data-load-static-codes.sql)
\echo 'Registry - Copying static code tables from deployed image CSV files'

--Registry Activity Type
\echo '... loading registries_activity_code table'
\copy registries_activity_code (registries_activity_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registries_activity_code.csv' with header delimiter ',' CSV ;

--Registry Activity Subtype
\echo '... loading registry_subactivity_code table'
\copy registries_subactivity_code (registries_subactivity_guid,registries_activity_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registries_subactivity_code.csv' with header delimiter ',' CSV ;

--Registry Qualification Type
\echo '... loading registry_qualification code table'
\copy registries_qualification_code (registries_qualification_guid,registries_subactivity_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registries_qualification_code.csv' with header delimiter ',' CSV ;

--Registry Status Code
\echo '... loading registry_status_code code table'
\copy registries_status_code (registries_status_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registries_status_code.csv' with header delimiter ',' CSV ;

--Registry Application Status Code
\echo '... loading registry_application_status_code code table'
\copy registries_application_status_code (registries_application_status_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registries_application_status_code.csv' with header delimiter ',' CSV ;

--Registry Removal Reasons Code
\echo '... loading registry_removal_reason_code code table'
\copy registries_removal_reason_code (registries_removal_reason_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registries_removal_reason_code.csv' with header delimiter ',' CSV ;

\echo 'Registry - Finshed copy of static code tables.'

--Registries Test Data 
\echo 'Registries - Loading test data, based upon January 2018 Well Driller Register'

\echo '... loading Registration Action Tracking_Driller'
\copy xform_registries_action_tracking_driller from 'Registration Action Tracking_Driller.sanitized.csv' with header delimiter ',' CSV ;

\echo '... loading well_drillers_reg'
\copy xform_registries_drillers_reg from 'well_drillers_reg.sanitized.csv' with header delimiter ',' CSV ;

\echo '... loading Removed From Registry'
\copy xform_registries_removed_from from 'Removed From Registry.sanitized.csv' with header delimiter ',' CSV ;

\echo 'Registries - Finshed loading of test data.'
