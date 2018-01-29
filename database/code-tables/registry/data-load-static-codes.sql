--  Run this script as gwells owner (e.g. psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f data-load-static-codes.sql)
\echo 'Registry - Copying static code tables from deployed image CSV files'

--Registry Activity Type
\echo '... loading registry_activity_type code table'
\copy registry_activity_type (registry_activity_type_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registry_activity_type.csv' with header delimiter ',' CSV ;

--Registry Activity Subtype
\echo '... loading registry_activity_subtype code table'
\copy registry_activity_subtype (registry_activity_subtype_guid,registry_activity_type_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registry_activity_subtype.csv' with header delimiter ',' CSV ;

--Registry Qualification Type
\echo '... loading registry_qualification code table'
\copy registry_qualification (registry_qualification_guid,registry_activity_subtype_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registry_qualification_type.csv' with header delimiter ',' CSV ;

--Registry Status Code
\echo '... loading registry_status_code code table'
\copy registry_status_code (registry_status_code_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registration_status_code.csv' with header delimiter ',' CSV ;

--Registry Application Status Code
\echo '... loading registry_application_status_code code table'
\copy registry_application_status_code (registry_application_status_code_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registry_application_status_code.csv' with header delimiter ',' CSV ;

--Registry Removal Reasons Code
\echo '... loading registry_removal_reason_code code table'
\copy registry_removal_reason_code (registry_removal_reason_guid,code,description,is_hidden,sort_order,when_created,when_updated,who_created,who_updated) from 'registration_removal_reason_code.csv' with header delimiter ',' CSV ;


\echo 'Registry - Finshed copy of static code tables.'

-- To clear the above tables:
-- 
-- truncate registry_activity_type cascade;
-- truncate registry_qualification cascade;
-- truncate registry_status_code cascade;
-- truncate registry_application_status_code cascade;
-- truncate registry_removal_reason_code cascade;
--
