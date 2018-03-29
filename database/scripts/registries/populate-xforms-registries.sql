-- @Registries
--
-- Registries app (Well Driller, Pump Installer)
--   

\echo 'Creating Registries app tables...'

DROP TABLE IF EXISTS xform_registries_action_tracking_driller;
CREATE unlogged TABLE IF NOT EXISTS xform_registries_action_tracking_driller (
 trk_guid uuid DEFAULT gen_random_uuid()
,id integer
,registered_ind character varying(20)
,date_app_received date
,company_name character varying(80)
,name character varying(80)
,town_region character varying(80)
,date_gone_for_review date
,app_approval_date date
,date_approval_letter_card_sent date
,app_denial_date date
,comments character varying(200)
,date_denial_letter_sent date
,date_removed_from_register date
);

DROP TABLE IF EXISTS xform_registries_action_tracking_pump_installer;
CREATE unlogged TABLE IF NOT EXISTS xform_registries_action_tracking_pump_installer (
 trk_guid uuid DEFAULT gen_random_uuid()
,id integer
,registered_ind character varying(20)
,date_app_received date
,company_name character varying(80)
,name character varying(80)
,town_region character varying(80)
,date_gone_for_review date
,app_approval_date date
,date_approval_letter_card_sent date
,app_denial_date date
,comments character varying(200)
,date_denial_letter_sent date
,date_removed_from_register date
);

DROP TABLE IF EXISTS xform_registries_drillers_reg;
CREATE unlogged TABLE IF NOT EXISTS xform_registries_drillers_reg ( 
 reg_guid uuid DEFAULT gen_random_uuid()
,Name character varying(100)
,LastName character varying(20)
,FirstName character varying(20)
-- ,BirthDate character varying(20)
,Welldrillerregno character varying(20)
,Registrationdate date
,CompanyName character varying(100)
,CompanyAddress character varying(100)
,CompanyCity character varying(20)
,CompanyProv character varying(20)
,CompanyPostalCode character varying(20)
,CompanyPhone  character varying(20)
,CompanyFax character varying(50)
,CompanyEmail  character varying(50)
,CertificateNumber character varying(50)
,ClassofWellDriller  character varying(100) -- IGNORE for now
,TypeofCertificate  character varying(100)
--gwells=> select typeofcertificate, count(*) from public.xform_registries_drillers_reg group by typeofcertificate;
--           typeofcertificate            | count 
----------------------------------------+-------
-- n/a                                    |    96
-- Ground Water Drilling Technician, CGWA |     2
-- Water Well Driller, Prov. Of BC        |    29
--(3 rows)
,QualifiedToDrill character varying(100)
,DrillerIdentifiedPreference character varying(100)
,MoERegion  character varying(100) -- IGNORE obsolete
,File_Number  character varying(50)
,CellPhone character varying(20)
,Notes character varying(200)
 );  

DROP TABLE IF EXISTS xform_registries_pump_installers_reg;
CREATE unlogged TABLE IF NOT EXISTS xform_registries_pump_installers_reg ( 
 reg_guid uuid DEFAULT gen_random_uuid()
,Name character varying(100)
,LastName character varying(20)
,FirstName character varying(20)
,BirthDate character varying(20)
,Wellpumpinstallerregno character varying(20)
,Registrationdate date
,CompanyName character varying(100)
,CompanyAddress character varying(100)
,CompanyCity character varying(20)
,CompanyProv character varying(20)
,CompanyPostalCode character varying(20)
,CompanyPhone  character varying(20)
,CompanyFax character varying(50)
,CompanyEmail  character varying(50)
,ClassofWellPumpInstaller character varying(100) -- IGNORE for now
,TypeofCertificate  character varying(100)
,ClassofPump  character varying(50)
,SizeofPump  character varying(50)
,TypeofPumpEquipment  character varying(20) -- IGNORE no data
,MoERegion  character varying(100) -- IGNORE obsolete
,File_Number  character varying(50)
,Notes character varying(200)
 );  

DROP TABLE IF EXISTS xform_registries_removed_from;
CREATE unlogged TABLE IF NOT EXISTS xform_registries_removed_from ( 
 removed_guid uuid DEFAULT gen_random_uuid()
,Name character varying(100)
,LastName character varying(20)
,FirstName character varying(20)
-- ,BirthDate character varying(20)
,RegistrationNumber character varying(20)
,Registrationdate character varying(20) -- should be date
,CompanyName character varying(100)
,CompanyAddress character varying(100)
,CompanyCity character varying(20)
,CompanyProv character varying(20)
,CompanyPostalCode character varying(20)
,CompanyPhone  character varying(20)
,CompanyFax character varying(50)
,CompanyEmail  character varying(50)
,ClassofWellDriller  character varying(50)
,Reason character varying(50)
,Removed_from_Registry date
 );  


\echo 'Finished creating Registries app tables...'

