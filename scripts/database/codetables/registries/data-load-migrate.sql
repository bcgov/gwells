--  @Registries
--  Run this script as gwells owner (e.g. psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f data-load-static-codes.sql)


--Registries Migrated Data 
\echo 'Registries - Loading test data, based upon May 2018 Well Driller Register'

\echo '... skipping Registration Action Tracking_Driller'
--\copy xform_registries_action_tracking_driller (id,guid,registered_ind,date_app_received,company_name,name,town_region, date_gone_for_review,app_approval_date,date_approval_letter_card_sent,app_denial_date,comments,date_denial_letter_sent,date_removed_from_register,reviewed_ind) from 'RegistrationActionTracking_Driller.csv' with header delimiter ',' CSV ;

\echo '... skipping Registration Action Tracking_Pump Installer'
--\copy xform_registries_action_tracking_pump_installer (id,registered_ind,date_app_received,company_name,name,town_region, date_gone_for_review,app_approval_date,date_approval_letter_card_sent,app_denial_date,comments,date_denial_letter_sent,date_removed_from_register) from 'RegistrationActionTracking_Pump_Installer.csv' with header delimiter ',' CSV ;

\echo '... loading well_drillers_reg'
\copy xform_registries_drillers_reg (name,lastname,firstname,welldrillerregno,registrationdate,companyname,companyaddress,companycity,companyprov,companypostalcode,companyphone,companyfax,companyemail,certificatenumber,classofwelldriller,typeofcertificate,qualifiedtodrill,drilleridentifiedpreference,moeregion,file_number,cell_phone,notes,website) from 'well_drillers_reg.csv' with header delimiter ',' CSV ;

\echo '... loading pump_installers_reg'
\copy xform_registries_pump_installers_reg (name,lastname,firstname,wellpumpinstallerregno,registrationdate,companyname,companyaddress,companycity,companyprov,companypostalcode,companyphone,companyfax,companyemail,classofwellpumpinstaller,typeofcertificate,classofpump,sizeofpump,moeregion,file_number,cell_phone,notes,website) from 'pump_install_reg.csv' with header delimiter ',' CSV ;

\echo '... skipping Removed From Registry (pending data cleanup)'
-- \copy xform_registries_removed_from (name,lastname,firstname,registrationnumber,registrationdate,companyname,companyaddress,companycity,companyprov,companypostalcode,companyphone,companyfax,companyemail,classofwelldriller,reason,removed_from_registry) from 'removed_from_registry.csv' with header delimiter ',' CSV ;

\echo 'Registries - Finshed loading of migrated data.'
