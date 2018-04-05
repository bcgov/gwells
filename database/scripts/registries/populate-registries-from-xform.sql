-- Treat as one-off (manually) as this is just test data
--
-- export PGPASSWORD=$DATABASE_PASSWORD
--
-- psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f populate-registries-from-xform.sql


-- Companies
INSERT INTO registries_organization (
 create_user
,create_date
,update_user
,update_date
,effective_date
,expired_date
,org_guid
,name
,street_address
,city
,postal_code
,main_tel
,fax_tel
,website_url
,province_state_code
) SELECT
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'1970-01-01 00:00:00-08'
,null
,reg_guid -- should actually be gen_random_uuid() 
,companyname
,companyaddress
,companycity
,companypostalcode
,substring(companyphone from 1 for 15)
,substring(companyfax from 1 for 15)
,null
,CASE companyprov
  WHEN 'YK' THEN 'YT'
  WHEN null THEN 'BC'
  ELSE companyprov
 END AS province_state_code
from xform_registries_drillers_reg xform
where companyname is not null;

INSERT INTO registries_organization (
 create_user
,create_date
,update_user
,update_date
,effective_date
,expired_date
,org_guid
,name
,street_address
,city
,postal_code
,main_tel
,fax_tel
,website_url
,province_state_code
) SELECT
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'1970-01-01 00:00:00-08'
,null
,reg_guid -- should actually be gen_random_uuid() 
,companyname
,companyaddress
,companycity
,companypostalcode
,substring(companyphone from 1 for 15)
,substring(companyfax from 1 for 15)
,null
,CASE companyprov
  WHEN 'YK' THEN 'YT'
  WHEN null THEN 'BC'
  ELSE companyprov
 END AS province_state_code
from xform_registries_pump_installers_reg xform
where companyname is not null
and   companyname <> 'R. Ayre Enterprises'; -- bad data in companyprov (special char?)


-- Persons 
INSERT INTO registries_person (
 first_name
,surname
,effective_date
,expired_date
,person_guid
,create_user
,create_date
,update_user
,update_date
)
SELECT
 firstname
,lastname
,'1970-01-01 00:00:00-08'
,null
,reg_guid
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
from xform_registries_drillers_reg xform;

INSERT INTO registries_contact_detail (
 create_user
,create_date
,update_user
,update_date
,effective_date
,expired_date
,contact_detail_guid
,contact_tel
,contact_email
,person_guid
) SELECT 
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
,'1970-01-01 00:00:00-08'
,null
,gen_random_uuid()
,cellphone
,companyemail
,reg_guid
from xform_registries_drillers_reg xform;


INSERT INTO registries_person (
 first_name
,surname
,effective_date
,expired_date
,person_guid
,create_user
,create_date
,update_user
,update_date
)
SELECT
 firstname
,lastname
,'1970-01-01 00:00:00-08'
,null
,reg_guid
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
from xform_registries_pump_installers_reg xform;

INSERT INTO registries_contact_detail (
 create_user
,create_date
,update_user
,update_date
,effective_date
,expired_date
,contact_detail_guid
,contact_tel
,contact_email
,person_guid
) SELECT 
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
,'1970-01-01 00:00:00-08'
,null
,gen_random_uuid()
,null -- Why no cellphone in pump installers?
,companyemail
,reg_guid
from xform_registries_pump_installers_reg xform;



-- Driller Register (Active)
INSERT INTO registries_register (
 create_user
,create_date
,update_user
,update_date
,register_guid
,registration_no
,registration_date
,register_removal_date
,person_id
,registries_removal_reason_code
,registries_activity_code
,registries_status_code
)
SELECT
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
,gen_random_uuid()
,welldrillerregno
,registrationdate
,null
,reg_guid
,null
,'DRILL'
,'ACTIVE'
 from xform_registries_drillers_reg
 ;


-- Pump Installer Register (Active)
INSERT INTO registries_register (
 create_user
,create_date
,update_user
,update_date
,register_guid
,registration_no
,registration_date
,register_removal_date
,person_id
,registries_removal_reason_code
,registries_activity_code
,registries_status_code
)
SELECT
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
,gen_random_uuid()
,wellpumpinstallerregno
,registrationdate
,null
,reg_guid
,null
,'PUMP'
,'ACTIVE'
 from xform_registries_pump_installers_reg xform
 ;
