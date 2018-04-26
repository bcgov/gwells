-- Treat as one-off (manually) as this is just test data
--
-- export PGPASSWORD=$DATABASE_PASSWORD
--
-- psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f populate-registries-from-xform.sql

-- Companies from Driller Registry (140)
\echo 'Inserting Companies from Driller Registry'
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

-- Companies from Pump Installer Registry 177
\echo 'Inserting Companies from Pump Installer Registry'
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
SELECT name from registries_organization);

-- Companies from drillers/pump-installers that have been removed
/*
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
*/

-- Drillers 285
\echo 'Inserting People from Driller Registry'
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

-- Driller Contact details 285
\echo '...Updating people, attaching contact details from Driller Registry'
INSERT INTO registries_contact_detail (
 create_user
,create_date
,update_user
,update_date
,effective_date
,expired_date
,contact_detail_guid
,contact_cell
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
,cell_phone
,null
,companyemail
,reg_guid
from xform_registries_drillers_reg xform;

-- Pump Installers 259  (61 of the 320 are already in the Register as Well Drillers)
\echo 'Inserting People from Pump Installer Registry'
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

-- Pump Installer Contact details 259  (61 of the 320 already have Contact Details as Well Drillers)
\echo '...Updating people, attaching contact details from Pump Installers'
INSERT INTO registries_contact_detail (
 create_user
,create_date
,update_user
,update_date
,effective_date
,expired_date
,contact_detail_guid
,contact_cell
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
,cell_phone
,null
,companyemail
,reg_guid
from xform_registries_pump_installers_reg xform
-- for whom not already in contact details due to Driller entry above
where not exists (
    select 1 from registries_person existing inner join registries_contact_detail contact
    on existing.person_guid = contact.person_guid
    where xform.firstname = existing.first_name and xform.lastname = existing.surname
);


-- Drillers/Pump Installers that were once on Register but since removed
/*
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
*/

-- Attach companies for whom the Removed Driller/Pump Installer used to work
/*
UPDATE registries_person per
SET organization_guid = org.org_guid
FROM registries_organization org,
    xform_registries_removed_from xform
WHERE org.name = xform.companyname
and org.street_address = xform.companyaddress
and org.city           = xform.companycity
and per.person_guid = xform.removed_guid
-- And not already attached to a company
and per.organization_guid is null;
*/

-- TODO NOTE we need to redo Data Model so that a Person can have multiple Contact Details, 
-- and can indeed work for more than one company at a time (e.g. Pump Installer & Driller )
-- so Person --< Relationship (PUMP, DRILLER) >- Organizatino


-- Contact details of the Removed Driller/Pump Installer
/*
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
*/
-- TODO Why no  entries above, when 'not exists' is inserted?

-- Driller Register (Active) 285
\echo 'Inserting Entries into Driller Registry'
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
 from xform_registries_drillers_reg;

-- Attach companies for whom the drillers work 285
\echo '...Updating Register, attaching companies from Driller Registry'
UPDATE registries_register reg
SET organization_guid = org.org_guid
FROM registries_organization org,
    xform_registries_drillers_reg xform,
    registries_person per
WHERE org.name = xform.companyname
and org.street_address = xform.companyaddress
and org.city           = xform.companycity
and per.person_guid    = reg.person_guid
and xform.firstname = per.first_name
and xform.lastname = per.surname
-- And not already attached to a company
and reg.organization_guid is null;


-- Pump Installer Register (Active) 320
\echo 'Inserting Entries into Pump Installer Registry'
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
and   xform.lastname = per.surname;

-- TODO Cannot use reg_guid as this PERSON may have been
--      entered as driller

 
-- Attach companies for whom the pump installers work 320
\echo '...Updating Register, attaching companies from Pump Installer Registry'
UPDATE registries_register reg
SET organization_guid = org.org_guid
FROM registries_organization org,
    xform_registries_pump_installers_reg xform,
    registries_person per
WHERE org.name = xform.companyname
and org.street_address = xform.companyaddress
and org.city           = xform.companycity
and per.person_guid    = reg.person_guid
and xform.firstname = per.first_name
and xform.lastname = per.surname
-- And not already attached to a company
and reg.organization_guid is null;

-- Driller/Pump Installer (Removed)
/*
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
and   xform.lastname = per.surname;
*/


-- Applications from pre-2016-FEB-29 2016 Well Drillers, who were
-- grandfathered in 257
\echo 'Inserting "Fake" Applications for pre-2016-FEB-29 grandfathered Well Drillers (WATER)'
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
,xform.file_number
,TRUE
,CONCAT_WS('. ',xform.notes,'Registered prior to 2016-FEB-29, assigned all Driller Classes and qualified to drill ')
,null
,COALESCE(xform.certificatenumber, 'N/A')
, (SELECT acc_cert_guid
    from registries_accredited_certificate_code
    where name = 'Grand-parent'
    and  registries_activity_code = 'DRILL'
   )
,reg.register_guid
,'WATER'
from registries_register reg,
     xform_registries_drillers_reg xform,
     registries_person per
WHERE per.person_guid = reg.person_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'DRILL'
and xform.reg_guid = per.person_guid
and xform.registrationdate <=  '2016-02-29'
and xform.name = concat(per.surname, ', ', per.first_name);

-- Pseudo-Applications from "Water Well" Well Drillers, who were
-- grandfathered in  257
\echo '... Approved entries'
INSERT INTO registries_application_status (
 create_user
,create_date
,update_user
,update_date
,application_status_guid
,notified_date
,effective_date
,expired_date
,application_guid
,registries_application_status_code
)
SELECT
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,gen_random_uuid()
,xform.registrationdate -- default in this case
,xform.registrationdate -- default in this case
,null -- still Registered 
,app.application_guid
,'A'
from registries_register reg,
     registries_person per,
     registries_application app,
     xform_registries_drillers_reg xform
WHERE per.person_guid = reg.person_guid
AND   app.register_guid = reg.register_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'DRILL'
and app.registries_subactivity_code = 'WATER'
and xform.registrationdate <=  '2016-02-29'
and xform.name = concat(per.surname, ', ', per.first_name)
;

-- 257
\echo 'Inserting "Fake" Applications for pre-2016-FEB-29 grandfathered Well Drillers (GEOTECH)'
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
,xform.file_number
,TRUE
,xform.notes
,null
,COALESCE(xform.certificatenumber, 'N/A')
, (SELECT acc_cert_guid
    from registries_accredited_certificate_code
    where name = 'Grand-parent'
    and  registries_activity_code = 'DRILL'
   )
,reg.register_guid
,'GEOTECH'
from registries_register reg,
     xform_registries_drillers_reg xform,
     registries_person per
WHERE per.person_guid = reg.person_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'DRILL'
and xform.reg_guid = per.person_guid
and xform.registrationdate <=  '2016-02-29'
and xform.name = concat(per.surname, ', ', per.first_name);

-- 257
\echo '... Approved entries'
INSERT INTO registries_application_status (
 create_user
,create_date
,update_user
,update_date
,application_status_guid
,notified_date
,effective_date
,expired_date
,application_guid
,registries_application_status_code
)
SELECT
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,gen_random_uuid()
,xform.registrationdate -- default in this case
,xform.registrationdate -- default in this case
,null -- still Registered 
,app.application_guid
,'A'
from registries_register reg,
     registries_person per,
     registries_application app,
     xform_registries_drillers_reg xform
WHERE per.person_guid = reg.person_guid
AND   app.register_guid = reg.register_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'DRILL'
and app.registries_subactivity_code = 'GEOTECH'
and xform.registrationdate <=  '2016-02-29'
and xform.name = concat(per.surname, ', ', per.first_name)
;

-- 257
\echo 'Inserting "Fake" Applications for pre-2016-FEB-29 grandfathered Well Drillers (GEOXCHG)'
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
,xform.file_number
,TRUE
,xform.notes
,null
,COALESCE(xform.certificatenumber, 'N/A')
, (SELECT acc_cert_guid
    from registries_accredited_certificate_code
    where name = 'Grand-parent'
    and  registries_activity_code = 'DRILL'
   )
,reg.register_guid
,'GEOXCHG'
from registries_register reg,
     xform_registries_drillers_reg xform,
     registries_person per
WHERE per.person_guid = reg.person_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'DRILL'
and xform.reg_guid = per.person_guid
and xform.registrationdate <=  '2016-02-29'
and xform.name = concat(per.surname, ', ', per.first_name);

\echo '... Approved entries'
INSERT INTO registries_application_status (
 create_user
,create_date
,update_user
,update_date
,application_status_guid
,notified_date
,effective_date
,expired_date
,application_guid
,registries_application_status_code
)
SELECT
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,gen_random_uuid()
,xform.registrationdate -- default in this case
,xform.registrationdate -- default in this case
,null -- still Registered 
,app.application_guid
,'A'
from registries_register reg,
     registries_person per,
     registries_application app,
     xform_registries_drillers_reg xform
WHERE per.person_guid = reg.person_guid
AND   app.register_guid = reg.register_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'DRILL'
and app.registries_subactivity_code = 'GEOXCHG'
and xform.registrationdate <=  '2016-02-29'
and xform.name = concat(per.surname, ', ', per.first_name)
;


-- 320 
\echo 'Inserting "Fake" Applications for Pump Installers (PUMPINST)'
\echo '.. to be fixed manually post-migration or via a '
\echo '.. subsequent re-migration after data cleanup in'
\echo '.. the source MS Access tables.'
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
,xform.file_number
,TRUE
,CONCAT_WS('. ',xform.notes,'Pseudo-Applications until ACTION_TRACKING tables are fixed. ')
,null
,'N/A' -- why no cert #?
, (SELECT acc_cert_guid
    from registries_accredited_certificate_code
    where name = 'Grand-parent'
    and  registries_activity_code = 'PUMP'
   )
,reg.register_guid
,'PUMPINST'
from registries_register reg,
     xform_registries_pump_installers_reg xform,
     registries_person per
WHERE per.person_guid = reg.person_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'PUMP'
-- and xform.reg_guid = per.person_guid CANNOT use this as the person_guid came
-- from previous well-driller creation
and xform.firstname = per.first_name
and xform.lastname = per.surname;

-- 320
\echo '... Approved entries for Pump Installers '
INSERT INTO registries_application_status (
 create_user
,create_date
,update_user
,update_date
,application_status_guid
,notified_date
,effective_date
,expired_date
,application_guid
,registries_application_status_code
)
SELECT
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,gen_random_uuid()
,xform.registrationdate -- default in this case
,xform.registrationdate -- default in this case
,null -- still Registered 
,app.application_guid
,'A'
from registries_register reg,
     registries_person per,
     registries_application app,
     xform_registries_pump_installers_reg xform
WHERE per.person_guid = reg.person_guid
AND   app.register_guid = reg.register_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'PUMP'
and xform.firstname = per.first_name
and xform.lastname = per.surname;
;




-- Historical Statuses for Applications from "Water Well" Well Drillers (ultimately successful)
--
-- CANNOT do below as the same person appears on register many times
-- and I cannot link to the same person w/o a key.  But I for now can use
-- xform_registries_drillers_reg.reg_guid being the same as registries_person.person_guid

/*
INSERT INTO registries_application_status (
 create_user
,create_date
,update_user
,update_date
,application_status_guid
,notified_date
,effective_date
,expired_date
,application_guid
,registries_application_status_code
)
SELECT
 'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,gen_random_uuid()
,null -- N/A for recipt of application
,trk.date_app_received
,trk.app_approval_date
,app.application_guid
,'P'
from registries_register reg,
     xform_registries_action_tracking_driller trk,
     registries_person per,
     registries_application app
WHERE per.person_guid = reg.person_guid
AND   app.register_guid = reg.register_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'DRILL'
and app.registries_subactivity_code = 'WATER'
and trim(both from trk.name) = concat(per.surname, ', ', per.first_name)
and trk.date_app_received is not null
and trk.app_approval_date is not null;

*/

-- Applications from "Geoexchange" Well Drillers (ultimately successful)
/*
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
,xform.file_number
,TRUE
,xform.notes
,null
,xform.certificatenumber
, (SELECT acc_cert_guid
    from registries_accredited_certificate_code
    where name = 'Geoexchange Driller Certificate'
   )
,reg.register_guid
,'GEOXCHG'
from registries_register reg,
     xform_registries_drillers_reg xform,
     xform_registries_action_tracking_driller trk,
     registries_person per
WHERE per.person_guid = reg.person_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'DRILL'
and xform.reg_guid = per.person_guid
and xform.classofwelldriller like '%Geoexchange%'
and trim(both from trk.name) = concat(per.surname, ', ', per.first_name)
and xform.name = concat(per.surname, ', ', per.first_name);
*/

-- Applications from "Geotechnical" Well Drillers (ultimately successful)
/*
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
,xform.file_number
,TRUE
,xform.notes
,null
,xform.certificatenumber
, (SELECT acc_cert_guid
    from registries_accredited_certificate_code
    where name = 'Geotechnical/Environmental Driller Certificate'
   )
,reg.register_guid
,'GEOTECH'
from registries_register reg,
     xform_registries_drillers_reg xform,
     xform_registries_action_tracking_driller trk,
     registries_person per
WHERE per.person_guid = reg.person_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'DRILL'
and xform.reg_guid = per.person_guid
and xform.classofwelldriller like '%Geotechnical%'
and trim(both from trk.name) = concat(per.surname, ', ', per.first_name)
and xform.name = concat(per.surname, ', ', per.first_name);
*/

-- Applications from Pump Installers (ultimately successful)
/*
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
,xform.file_number
,TRUE
,xform.notes
,null
,xform.wellpumpinstallerregno
,CASE 
  WHEN typeofcertificate like '%Ontario%' THEN '88d5d0aa-d2aa-450a-9708-a911dce42f7f'::uuid 
  WHEN typeofcertificate like '%CGWA%'    THEN '1886daa8-e799-49f0-9034-33d02bad543d'::uuid 
  WHEN typeofcertificate like '%BC%'      THEN '7bf968aa-c6e0-4f57-b4f4-58723214de80'::uuid 
  ELSE 'a53d3f1e-65eb-46b7-8999-e662d654df77'::uuid
 END AS acc_cert_guid
,reg.register_guid
,'PUMPINST'
from registries_register reg,
     xform_registries_pump_installers_reg xform,
     xform_registries_action_tracking_pump_installer trk,
     registries_person per
WHERE per.person_guid = reg.person_guid
AND reg.registries_status_code = 'ACTIVE'
and reg.registries_activity_code = 'PUMP'
and xform.reg_guid = per.person_guid
and trim(both from trk.name) = concat(per.surname, ', ', per.first_name)
and xform.name = concat(per.surname, ', ', per.first_name);
*/
