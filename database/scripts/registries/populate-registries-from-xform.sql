-- Treat as one-off (manually) as this is just test data
--
-- export PGPASSWORD=$DATABASE_PASSWORD
--
-- psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f populate-registries-from-xform.sql


-- Companies from Driller Registry
INSERT INTO registries_organization (
 name
,create_user
,create_date
,update_user
,update_date
,effective_date
,expired_date
,org_guid
,street_address
,city
,postal_code
,main_tel
,fax_tel
,website_url
,province_state_code
) SELECT
 distinct on (companyname) companyname
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'::timestamp
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'::timestamp
,'1970-01-01 00:00:00-08'::timestamp
,null::timestamp
,gen_random_uuid()
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

-- Companies from Pump Installer Registry
INSERT INTO registries_organization (
 name
,create_user
,create_date
,update_user
,update_date
,effective_date
,expired_date
,org_guid
,street_address
,city
,postal_code
,main_tel
,fax_tel
,website_url
,province_state_code
) SELECT
 distinct on (companyname) companyname
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'::timestamp
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'::timestamp
,'1970-01-01 00:00:00-08'::timestamp
,null::timestamp
,gen_random_uuid()
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
and companyname not in (
SELECT name from registries_organization)
and   companyname <> 'R. Ayre Enterprises'; -- bad data in companyprov (special char?)

-- Companies from drillers/pump-installers that have been removed
INSERT INTO registries_organization (
 name
,create_user
,create_date
,update_user
,update_date
,effective_date
,expired_date
,org_guid
,street_address
,city
,postal_code
,main_tel
,fax_tel
,website_url
,province_state_code
) SELECT
 distinct on (companyname) companyname
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'::timestamp
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'::timestamp
,'1970-01-01 00:00:00-08'::timestamp
,null::timestamp
,gen_random_uuid()
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
from xform_registries_removed_from xform
where companyname is not null
and companyname not in (
SELECT name from registries_organization);

-- Drillers
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

-- Attach companies for whom the drillers work
UPDATE registries_person per
SET organization_id = org.org_guid
FROM registries_organization org,
    xform_registries_drillers_reg xform
WHERE org.name = xform.companyname
and org.street_address = xform.companyaddress
and org.city           = xform.companycity
and per.person_guid = xform.reg_guid;

-- Driller Contact details
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

-- Pump Installers
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
from xform_registries_pump_installers_reg xform
where not exists (
    select 1 from registries_person existing
     where xform.firstname = existing.first_name and xform.lastname = existing.surname
);
-- What about same name but different people?  With different contact details?


-- Attach companies for whom the pump installers work
UPDATE registries_person per
SET organization_id = org.org_guid
FROM registries_organization org,
    xform_registries_pump_installers_reg xform
WHERE org.name = xform.companyname
and org.street_address = xform.companyaddress
and org.city           = xform.companycity
and per.person_guid = xform.reg_guid
-- And not already attached to a company
and per.organization_id is null;

-- Pump Installer Contact details
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
from xform_registries_pump_installers_reg xform
-- for whom not already in contact details due to Driller entry above
where not exists (
    select 1 from registries_person existing
     where xform.firstname = existing.first_name and xform.lastname = existing.surname
);


-- Drillers/Pump Installers that were once on Register but since removed
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
,removed_guid
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
from xform_registries_removed_from xform
where not exists (
    select 1 from registries_person existing
     where xform.firstname = existing.first_name and xform.lastname = existing.surname
);


-- Attach companies for whom the Removed Driller/Pump Installer used to work
UPDATE registries_person per
SET organization_id = org.org_guid
FROM registries_organization org,
    xform_registries_removed_from xform
WHERE org.name = xform.companyname
and org.street_address = xform.companyaddress
and org.city           = xform.companycity
and per.person_guid = xform.removed_guid
-- And not already attached to a company
and per.organization_id is null;

-- TODO NOTE we need to redo Data Model so that a Person can have multiple Contact Details, 
-- and can indeed work for more than one company at a time (e.g. Pump Installer & Driller )
-- so Person --< Relationship (PUMP, DRILLER) >- Organizatino


-- Contact details of the Removed Driller/Pump Installer
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
,null -- TODO why no cellphone?
,companyemail
,removed_guid
from xform_registries_removed_from xform
where companyemail is not null
-- for whom not already in contact details due to Driller or Pump Installer entries above
and not exists (
    select 1 from registries_person existing
     where xform.firstname = existing.first_name and xform.lastname = existing.surname
);
-- TODO Why no  entries above, when 'not exists' is inserted?

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
,person_guid
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
 -- TODO we may need a guid on Access side to keep it  straight , on all tables

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
,person_guid
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
,xform.wellpumpinstallerregno
,xform.registrationdate
,null
,per.person_guid
,null
,'PUMP'
,'ACTIVE'
from        xform_registries_pump_installers_reg xform
inner join  registries_person per
on xform.firstname = per.first_name
and   xform.lastname = per.surname
;
-- TODO Cannot use reg_guid as this PERSON may have been
--      entered as driller


-- Driller/Pump Installer (Removed)
INSERT INTO registries_register (
 create_user
,create_date
,update_user
,update_date
,register_guid
,registration_no
,registration_date
,register_removal_date
,person_guid
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
,xform.registrationnumber
,xform.registrationdate::date
,removed_from_registry
,per.person_guid
,'NLACT' -- xform.reason
,CASE substring(xform.registrationnumber from 1 for 2)
  WHEN 'WP' THEN 'PUMP'
  WHEN 'WD' THEN 'DRILL'
  ELSE 'DRILL'
 END AS registries_activity_code
,'REMOVED'
from        xform_registries_removed_from xform
inner join  registries_person per
on    xform.firstname = per.first_name
and   xform.lastname = per.surname
;

-- Applications from Well Drillers (ultimately successful)
INSERT INTO registries_application (
 create_user
,create_date
,update_user
,update_date
,application_guid
,file_no
,over19_ind
,registrar_notes
,reason_denied
,primary_certificate_no
,acc_cert_guid
,register_guid
,registries_subactivity_code
)
SELECT
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
,gen_random_uuid()
,file_no
,over19_ind
,registrar_notes
,reason_denied
,primary_certificate_no
,acc_cert_guid
,reg.register_guid
,registries_subactivity_code
FROM


SELECT register_guid, person_guid
from registries_register reg,
     xform_registries_action_tracking_driller
WHERE 
AND reg.registries_status_code = 'ACTIVE'


SELECT register_guid, person_id
from registries_register reg,
     registries_person per
WHERE per.person_guid = reg.person_guid;
AND reg.registries_status_code = 'ACTIVE'


