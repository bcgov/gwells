--  Run this script as gwells owner (e.g. psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER)
\echo 'Copying GWELLS static code tables from deployed image CSV files'

--PROVINCE_STATE
\echo '... loading province_state_code code table.'
\copy province_state_code (province_state_code,description,display_order,create_date,update_date,create_user,update_user) from 'province_state_code.csv' with header delimiter ',' CSV ;

\echo 'Finshed copy of GWELLS static code tables.'
