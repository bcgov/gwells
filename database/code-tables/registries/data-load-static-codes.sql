--  @Registries
--  Run this script as gwells owner (e.g. psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f data-load-static-codes.sql)
\echo 'Registry - Copying static code tables from deployed image CSV files'

--Registry Activity Type
\echo '... loading registries_activity_code table'
\copy registries_activity_code (registries_activity_guid,code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_activity_code.csv' with header delimiter ',' CSV ;

--Registry Activity Subtype
\echo '... loading registry_subactivity_code table'
\copy registries_subactivity_code (registries_subactivity_guid,registries_activity_guid,code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_subactivity_code.csv' with header delimiter ',' CSV ;

--Registry Qualification Type
\echo '... loading registry_qualification code table'
\copy registries_qualification_code (registries_qualification_guid,registries_subactivity_guid,code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_qualification_code.csv' with header delimiter ',' CSV ;

--Registry Status Code
\echo '... loading registry_status_code code table'
\copy registries_status_code (registries_status_guid,code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_status_code.csv' with header delimiter ',' CSV ;

--Registry Application Status Code
\echo '... loading registry_application_status_code code table'
\copy registries_application_status_code (registries_application_status_guid,code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_application_status_code.csv' with header delimiter ',' CSV ;

--Registry Removal Reasons Code
\echo '... loading registry_removal_reason_code code table'
\copy registries_removal_reason_code (registries_removal_reason_guid,code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_removal_reason_code.csv' with header delimiter ',' CSV ;

\echo 'Registry - Finshed copy of static code tables.'

--Registries Test Data 
\echo 'Registries - Loading test data, based upon January 2018 Well Driller Register'

\echo '... loading Registration Action Tracking_Driller'
\copy xform_registries_action_tracking_driller (id,registered_ind,date_app_received,company_name,name,town_region, date_gone_for_review,app_approval_date,date_approval_letter_card_sent,app_denial_date,comments,date_denial_letter_sent,date_removed_from_register) from 'RegistrationActionTracking_Driller.sanitized.csv' with header delimiter ',' CSV ;

\echo '... loading Registration Action Tracking_Pump Installer'
\copy xform_registries_action_tracking_pump_installer (id,registered_ind,date_app_received,company_name,name,town_region, date_gone_for_review,app_approval_date,date_approval_letter_card_sent,app_denial_date,comments,date_denial_letter_sent,date_removed_from_register) from 'RegistrationActionTracking_Pump_Installer.sanitized.csv' with header delimiter ',' CSV ;

\echo '... loading well_drillers_reg'
\copy xform_registries_drillers_reg (name,lastname,firstname,welldrillerregno,registrationdate,companyname,companyaddress,companycity,companyprov,companypostalcode,companyphone,companyfax,companyemail,certificatenumber,classofwelldriller,typeofcertificate,qualifiedtodrill,drilleridentifiedpreference,moeregion,file_number,cellphone,notes) from 'well_drillers_reg.sanitized.csv' with header delimiter ',' CSV ;

\echo '... loading pump_installers_reg'
\copy xform_registries_pump_installers_reg (name,lastname,firstname,wellpumpinstallerregno,registrationdate,companyname,companyaddress,companycity,companyprov,companypostalcode,companyphone,companyfax,companyemail,classofwellpumpinstaller,typeofcertificate,classofpump,sizeofpump,typeofpumpequipment,moeregion,file_number,notes) from 'pump_install_reg.sanitized.csv' with header delimiter ',' CSV ;

\echo '... loading Removed From Registry'
\copy xform_registries_removed_from (name,lastname,firstname,registrationnumber,registrationdate,companyname,companyaddress,companycity,companyprov,companypostalcode,companyphone,companyfax,companyemail,classofwelldriller,reason,removed_from_registry) from 'RemovedFromRegistry.sanitized.csv' with header delimiter ',' CSV ;

\echo 'Registries - Finshed loading of test data.'
