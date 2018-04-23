--  @Registries
--  Run this script as gwells owner (e.g. psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f data-load-static-codes.sql)
\echo 'Registry - Copying static code tables from deployed image CSV files'

--Registry Activity Type
\echo '... loading registries_activity_code table'
\copy registries_activity_code (registries_activity_code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_activity_code.csv' with header delimiter ',' CSV ;

--Registry Activity Subtype
\echo '... loading registry_subactivity_code table'
\copy registries_subactivity_code (registries_subactivity_code,registries_activity_code,description,display_order,create_date,update_date,create_user,update_user,effective_date,expired_date) from 'registries_subactivity_code.csv' with header delimiter ',' CSV ;

--Registry Well Class
\echo '... loading registry_well_class_code table'
\copy registries_well_class_code (registries_well_class_code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_well_class_code.csv' with header delimiter ',' CSV ;

--Registry Well Class / Subactivity Mapping
\echo '... loading registries_well_qualification table'
\copy registries_well_qualification (registries_well_qualification_guid,registries_subactivity_code,registries_well_class_code,display_order,create_date,update_date,create_user,update_user) from 'registries_well_qualification.csv' with header delimiter ',' CSV ;

--Registry Status Code
\echo '... loading registry_status_code table'
\copy registries_status_code (registries_status_code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_status_code.csv' with header delimiter ',' CSV ;

--Registry Application Status Code
\echo '... loading registry_application_status_code table'
\copy registries_application_status_code (registries_application_status_code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_application_status_code.csv' with header delimiter ',' CSV ;

--Registry Removal Reasons Code
\echo '... loading registries_removal_reason_code table'
\copy registries_removal_reason_code (registries_removal_reason_code,description,display_order,create_date,update_date,create_user,update_user) from 'registries_removal_reason_code.csv' with header delimiter ',' CSV ;

\echo '... loading registries_certifying_authority_code table'
\copy registries_certifying_authority_code (create_user,create_date,update_user,update_date,cert_auth_code,description,effective_date,expired_date) from 'registries_certifying_authority_code.csv' with header delimiter ',' CSV ;

\echo '... loading registries_accredited_certificate_code table'
\copy registries_accredited_certificate_code (create_user,create_date,update_user,update_date,acc_cert_guid,name,description,effective_date,expired_date,cert_auth_code,registries_activity_code) from 'registries_accredited_certificate_code.csv' with header delimiter ',' CSV ;

\echo 'Registry - Finshed copy of static code tables.'

--Registries Test Data 
\echo 'Registries - Loading test data, based upon April 2018 Well Driller Register'

\echo '... skipping Registration Action Tracking_Driller'
--\copy xform_registries_action_tracking_driller (id,guid,registered_ind,date_app_received,company_name,name,town_region, date_gone_for_review,app_approval_date,date_approval_letter_card_sent,app_denial_date,comments,date_denial_letter_sent,date_removed_from_register,reviewed_ind) from 'RegistrationActionTracking_Driller.csv' with header delimiter ',' CSV ;

\echo '... skipping Registration Action Tracking_Pump Installer'
--\copy xform_registries_action_tracking_pump_installer (id,registered_ind,date_app_received,company_name,name,town_region, date_gone_for_review,app_approval_date,date_approval_letter_card_sent,app_denial_date,comments,date_denial_letter_sent,date_removed_from_register) from 'RegistrationActionTracking_Pump_Installer.csv' with header delimiter ',' CSV ;

\echo '... loading well_drillers_reg'
\copy xform_registries_drillers_reg (name,lastname,firstname,welldrillerregno,registrationdate,companyname,companyaddress,companycity,companyprov,companypostalcode,companyphone,companyfax,companyemail,certificatenumber,classofwelldriller,typeofcertificate,qualifiedtodrill,drilleridentifiedpreference,moeregion,file_number,cell_phone,notes,website) from 'well_drillers_reg.csv' with header delimiter ',' CSV ;

\echo '... loading pump_installers_reg'
\copy xform_registries_pump_installers_reg (name,lastname,firstname,wellpumpinstallerregno,registrationdate,companyname,companyaddress,companycity,companyprov,companypostalcode,companyphone,companyfax,companyemail,classofwellpumpinstaller,typeofcertificate,classofpump,sizeofpump,moeregion,file_number,cell_phone,notes,website) from 'pump_install_reg.csv' with header delimiter ',' CSV ;

\echo '... skipping Removed From Registry'
--\copy xform_registries_removed_from (name,lastname,firstname,registrationnumber,registrationdate,companyname,companyaddress,companycity,companyprov,companypostalcode,companyphone,companyfax,companyemail,classofwelldriller,reason,removed_from_registry) from 'RemovedFromRegistry.csv' with header delimiter ',' CSV ;

\echo 'Registries - Finshed loading of test data.'
