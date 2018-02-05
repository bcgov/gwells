-- Treat as one-off (manually) as this is just test data
--
-- export PGPASSWORD=$DATABASE_PASSWORD
--
-- psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f populate-registries-from-xform.sql

-- Preload with known organizations that act as Certificate Authorities
INSERT INTO registries_organization (              
 name                  
,street_address        
,city                  
,postal_code           
,main_tel              
,fax_tel               
,website_url           
,certificate_authority 
,province_state_guid
,org_guid   
,who_created  
,when_created 
,who_updated  
,when_updated 
) SELECT
 'CGWA'
,null
,null
,null
,null
,null
,'https://www.bcgwa.org/'
,true
,(select prov.province_state_guid from gwells_province_state prov where prov.code = 'BC')
,'d76775a3-650d-44cb-a3b7-5faf8558f29d'::uuid
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
;

INSERT INTO registries_organization (              
 name                  
,street_address        
,city                  
,postal_code           
,main_tel              
,fax_tel               
,website_url           
,certificate_authority 
,province_state_guid
,org_guid   
,who_created  
,when_created 
,who_updated  
,when_updated 
) SELECT
 'Province of B.C.'
,null
,null
,null
,null
,null
,'https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/laws-rules/groundwater-protection-regulation'
,true
,(select prov.province_state_guid from gwells_province_state prov where prov.code = 'BC')
,'d3dfedd0-59b3-41cd-a40c-6e35b236a3d6'::uuid
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
;

INSERT INTO registries_organization (              
 name                  
,certificate_authority 
,org_guid   
,who_created  
,when_created 
,who_updated  
,when_updated 
) SELECT
 distinct on (trim (both from company_name)) company_name
,false
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
from xform_registries_action_tracking_driller
where company_name is not null
order by trim (both from company_name);


UPDATE registries_organization org SET 
(street_address        
,city                  
,postal_code           
,main_tel              
,fax_tel               
,province_state_guid
) = (SELECT 
 companyaddress
,companycity
,companypostalcode
,companyphone
,companyfax
,prov.province_state_guid
from xform_registries_drillers_reg xform
    ,gwells_province_state prov
where xform.companyname = org.name
and   prov.code = xform.companyprov
LIMIT 1
)
WHERE org.certificate_authority is false;


-- May need distinct on (first_name || surname )
SELECT COUNT(*), firstname, lastname
FROM   xform_registries_drillers_reg xform
group by firstname, lastname
having count(*) > 1;

INSERT INTO registries_person (              
 first_name                  
,surname        
,person_guid                             
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT 
 (regexp_split_to_array(name,', '))[2]
,(regexp_split_to_array(name,', '))[1]
,xform_trk.trk_guid
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
from xform_registries_action_tracking_driller xform_trk;

INSERT INTO registries_contact_at (              
 contact_tel    
,contact_email  
,effective_date 
,expired_date   
,org_guid       
,person_guid                               
,contact_at_guid
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT trim (both from xform.companyphone)
,trim (both from xform.companyemail)
,'1900-01-01 00:00:00-08' 
,null
,org.org_guid
,per.person_guid
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from xform_registries_drillers_reg xform
inner join registries_person per
  on (per.surname    = xform.lastname and
      per.first_name = xform.firstname)
inner join registries_organization org
  on org.name = xform.companyname;

INSERT INTO registries_application (              
 file_no         
,over19_ind      
,registrar_notes 
,reason_denied   
,person_guid     
,application_guid 
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT
 null
,true
,trim (both from xform_trk.comments)
,null
,xform_trk.trk_guid
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from xform_registries_action_tracking_driller xform_trk;

-- 'DRILL', 'GEOXCHG'
INSERT INTO registries_classification_applied_for (              
 primary_certificate_no         
,certifying_org_guid                       
,application_guid               
,registries_subactivity_guid    
,classification_applied_for_guid
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT
 'LEGACY'
,CASE
   WHEN xform_reg.typeofcertificate like '%CGWA' 
     THEN 'd76775a3-650d-44cb-a3b7-5faf8558f29d'::uuid
   WHEN xform_reg.typeofcertificate like '%Prov. Of BC'
     THEN 'd3dfedd0-59b3-41cd-a40c-6e35b236a3d6'::uuid
 ELSE null
 END  
,appl.application_guid
,(select subact.registries_subactivity_guid
  from registries_subactivity_code subact, registries_activity_code act
  where act.registries_activity_guid = subact.registries_activity_guid
  and   act.code = 'DRILL'
  and   subact.code = 'GEOXCHG'
 )
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from registries_application appl
    ,registries_person per
    ,xform_registries_drillers_reg xform_reg
where per.person_guid = appl.person_guid
and  (per.surname    = xform_reg.lastname and
      per.first_name = xform_reg.firstname)
and   xform_reg.classofwell LIKE '%Geothermal%';

-- 'DRILL', 'GEOTECH'
INSERT INTO registries_classification_applied_for (              
 primary_certificate_no         
,certifying_org_guid                       
,application_guid               
,registries_subactivity_guid    
,classification_applied_for_guid
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT
 'LEGACY'
,CASE
   WHEN xform_reg.typeofcertificate like '%CGWA' 
     THEN 'd76775a3-650d-44cb-a3b7-5faf8558f29d'::uuid
   WHEN xform_reg.typeofcertificate like '%Prov. Of BC'
     THEN 'd3dfedd0-59b3-41cd-a40c-6e35b236a3d6'::uuid
 ELSE null
 END  
,appl.application_guid
,(select subact.registries_subactivity_guid
  from registries_subactivity_code subact, registries_activity_code act
  where act.registries_activity_guid = subact.registries_activity_guid
  and   act.code = 'DRILL'
  and   subact.code = 'GEOTECH'
 )
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from registries_application appl
    ,registries_person per
    ,xform_registries_drillers_reg xform_reg
where per.person_guid = appl.person_guid
and  (per.surname    = xform_reg.lastname and
      per.first_name = xform_reg.firstname)
and   xform_reg.classofwell LIKE '%Geotechnical%';


-- 'DRILL', 'WATER'
INSERT INTO registries_classification_applied_for (              
 primary_certificate_no         
,certifying_org_guid                       
,application_guid               
,registries_subactivity_guid    
,classification_applied_for_guid
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT
 'LEGACY'
,CASE
   WHEN xform_reg.typeofcertificate like '%CGWA' 
     THEN 'd76775a3-650d-44cb-a3b7-5faf8558f29d'::uuid
   WHEN xform_reg.typeofcertificate like '%Prov. Of BC'
     THEN 'd3dfedd0-59b3-41cd-a40c-6e35b236a3d6'::uuid
 ELSE null
 END  
,appl.application_guid
,(select subact.registries_subactivity_guid
  from registries_subactivity_code subact, registries_activity_code act
  where act.registries_activity_guid = subact.registries_activity_guid
  and   act.code = 'DRILL'
  and   subact.code = 'WATER'
 )
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from registries_application appl
    ,registries_person per
    ,xform_registries_drillers_reg xform_reg
where per.person_guid = appl.person_guid
and  (per.surname    = xform_reg.lastname and
      per.first_name = xform_reg.firstname)
and   xform_reg.classofwell LIKE '%Water Well%';

-- Pending of Applications Subsequently Approved
INSERT INTO registries_application_status (
 notified_date                     
,effective_date                    
,expired_date                      
,application_guid                  
,registries_application_status_guid
,application_status_guid           
,who_created                       
,when_created                      
,who_updated                       
,when_updated 
)
SELECT
 null -- N/A for Pending
,xform_trk.date_app_received
,coalesce(xform_trk.app_approval_date,xform_trk.date_app_received)
,appl.application_guid
,(select status_code.registries_application_status_guid
 from registries_application_status_code status_code
 where status_code.code = 'P')
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from xform_registries_action_tracking_driller xform_trk
  ,registries_application appl
where lower(xform_trk.registered_ind) = 'yes'
and   appl.person_guid = xform_trk.trk_guid -- we explicitly set this above
and   xform_trk.date_app_received is not null
and   xform_trk.app_denial_date is null -- Ignore bad data
;

-- Approval of Applications  
INSERT INTO registries_application_status (
 notified_date                     
,effective_date                    
,expired_date                      
,application_guid                  
,registries_application_status_guid
,application_status_guid           
,who_created                       
,when_created                      
,who_updated                       
,when_updated 
)
SELECT
 xform_trk.date_approval_letter_card_sent
,coalesce(xform_trk.app_approval_date,xform_trk.date_app_received)
,null
,appl.application_guid
,(select status_code.registries_application_status_guid
 from registries_application_status_code status_code
 where status_code.code = 'A')
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from xform_registries_action_tracking_driller xform_trk
  ,registries_application appl
where lower(xform_trk.registered_ind) = 'yes'
and appl.person_guid = xform_trk.trk_guid -- we explicitly set this above
and   xform_trk.app_approval_date is not null
and   xform_trk.app_denial_date is null -- Ignore bad data
;

-- Pending of Applications Subsequently Denied
INSERT INTO registries_application_status (
 notified_date                     
,effective_date                    
,expired_date                      
,application_guid                  
,registries_application_status_guid
,application_status_guid           
,who_created                       
,when_created                      
,who_updated                       
,when_updated 
)
SELECT
 null -- N/A for Pending
,xform_trk.date_app_received
,coalesce(xform_trk.app_denial_date,xform_trk.date_app_received)
,appl.application_guid
,(select status_code.registries_application_status_guid
 from registries_application_status_code status_code
 where status_code.code = 'P')
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from xform_registries_action_tracking_driller xform_trk
  ,registries_application appl
where appl.person_guid = xform_trk.trk_guid -- we explicitly set this above
and   lower(xform_trk.registered_ind) = 'no'
and   xform_trk.date_app_received is not null
and   xform_trk.app_approval_date is null -- Ignore bad data
;


-- Denial (not Approved) of Applications, including implicit denial since
-- app_denial_date / date_denial_letter_sent may be null
INSERT INTO registries_application_status (
 notified_date                     
,effective_date                    
,expired_date                      
,application_guid                  
,registries_application_status_guid
,application_status_guid           
,who_created                       
,when_created                      
,who_updated                       
,when_updated 
)
SELECT
 xform_trk.date_denial_letter_sent
,coalesce(xform_trk.app_denial_date,xform_trk.date_app_received)
,null
,appl.application_guid
,(select status_code.registries_application_status_guid
 from registries_application_status_code status_code
 where status_code.code = 'NA')
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from xform_registries_action_tracking_driller xform_trk
  ,registries_application appl
where appl.person_guid = xform_trk.trk_guid -- we explicitly set this above
and   lower(xform_trk.registered_ind) = 'no'
and   xform_trk.date_app_received is not null
and   xform_trk.app_approval_date is null -- Ignore bad data
;

-- NOTE: To view statuses in 'time order'
-- select per.person_guid, per.first_name, per.surname, 
-- code.description, status.effective_date, status.expired_date
-- from   registries_application_status status, registries_application_status_code code
--       ,registries_application appl, registries_person per
-- where  status.registries_application_status_guid = code.registries_application_status_guid
-- and    appl.application_guid = status.application_guid
-- and    appl.person_guid = per.person_guid
-- order by per.person_guid, status.effective_date, code.sort_order;


-- Insert "Fake" applications for Drillers subsequently removed from Well Driller Register
-- Pending
INSERT INTO registries_application_status (
 notified_date                     
,effective_date                    
,expired_date                      
,application_guid                  
,registries_application_status_guid
,application_status_guid           
,who_created                       
,when_created                      
,who_updated                       
,when_updated 
)
SELECT
 null -- N/A for Pending
,coalesce(xform_trk.date_app_received
         ,xform_trk.app_approval_date
         ,xform_trk.date_gone_for_review)
,coalesce(xform_trk.date_app_received
         ,xform_trk.app_approval_date
         ,xform_trk.date_gone_for_review)
,appl.application_guid
,(select status_code.registries_application_status_guid
 from registries_application_status_code status_code
 where status_code.code = 'P')
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from xform_registries_action_tracking_driller xform_trk
  ,registries_application appl
where lower(xform_trk.registered_ind) = 'removed'
and   appl.person_guid = xform_trk.trk_guid -- we explicitly set this above
;

-- "Fake" Approval 
INSERT INTO registries_application_status (
 notified_date                     
,effective_date                    
,expired_date                      
,application_guid                  
,registries_application_status_guid
,application_status_guid           
,who_created                       
,when_created                      
,who_updated                       
,when_updated 
)
SELECT
 null -- N/A for Pending
,coalesce(xform_trk.date_app_received
         ,xform_trk.app_approval_date
         ,xform_trk.date_gone_for_review)
,coalesce(xform_trk.app_approval_date
         ,xform_trk.date_app_received
         ,xform_trk.date_gone_for_review)
,appl.application_guid
,(select status_code.registries_application_status_guid
 from registries_application_status_code status_code
 where status_code.code = 'A')
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from xform_registries_action_tracking_driller xform_trk
  ,registries_application appl
where lower(xform_trk.registered_ind) = 'removed'
and   appl.person_guid = xform_trk.trk_guid -- we explicitly set this above
;

-- Drillers whose applications were Approved but not Removed
INSERT INTO registries_register (
 registration_no                
,registration_date              
,register_removal_date          
,registries_removal_reason_guid 
,registries_activity_guid       
,application_guid               
,registries_status_guid         
,register_guid                  
,who_created                       
,when_created                      
,who_updated                       
,when_updated 
)
SELECT
 xform_reg.welldrillerregno
,xform_reg.registrationdate
,null        
,null
,(select registries_activity_guid from registries_activity_code where code='DRILL')
,appl.application_guid               
,(select registries_status_guid from registries_status_code where code='ACTIVE')
,gen_random_uuid()   
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
 from xform_registries_action_tracking_driller xform_trk
     ,registries_application appl
     ,registries_person per
     ,xform_registries_drillers_reg xform_reg
    where lower(xform_trk.registered_ind) = 'yes'
    and appl.person_guid = xform_trk.trk_guid -- we explicitly set this above
    and per.person_guid = appl.person_guid
    and  xform_trk.app_approval_date is not null
    and (xform_reg.lastname  = per.surname and
         xform_reg.firstname = per.first_name)
    and  xform_trk.app_denial_date is null -- Ignore bad data 
;


-- Drillers grandfathered in (without applications) and not in Tracking spreadsheet
INSERT INTO registries_person (              
 first_name                  
,surname        
,person_guid                             
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT 
 xform_reg.firstname
,xform_reg.lastname
,xform_reg.reg_guid 
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
from xform_registries_drillers_reg xform_reg
where not exists (
  select 1
  from registries_person per
  where per.surname   = xform_reg.lastname
  and   per.first_name = xform_reg.firstname);

-- May need distinct on (first_name || surname )
SELECT COUNT(*), firstname, lastname
FROM   xform_registries_drillers_reg xform
group by firstname, lastname
having count(*) > 1;



INSERT INTO registries_organization (              
 name 
,street_address        
,city                  
,postal_code           
,main_tel              
,fax_tel  
,website_url
,certificate_authority 
,province_state_guid
,org_guid   
,who_created  
,when_created 
,who_updated  
,when_updated 
) SELECT
 distinct on (trim (both from companyname)) companyname
,companyaddress
,companycity
,companypostalcode
,companyphone
,companyfax
,null
,false
,prov.province_state_guid
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08' 
from xform_registries_drillers_reg xform_reg
left join gwells_province_state prov
on prov.code = xform_reg.companyprov
where xform_reg.companyname is not null
and not exists (
  select 1
  from registries_person per
  where per.surname   = xform_reg.lastname
  and   per.first_name = xform_reg.firstname);


INSERT INTO registries_contact_at (              
 contact_tel    
,contact_email  
,effective_date 
,expired_date   
,org_guid       
,person_guid                               
,contact_at_guid
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT trim (both from xform_reg.companyphone)
,trim (both from xform_reg.companyemail)
,'1900-01-01 00:00:00-08' 
,null
,org.org_guid
,per.person_guid
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from registries_person per
    ,xform_registries_drillers_reg xform_reg
    ,registries_organization org
where per.person_guid = xform_reg.reg_guid
and xform_reg.companyname is not null
and org.name = xform_reg.companyname;

-- "Fake" Application to represent grand-fathered web drillers
INSERT INTO registries_application (              
 file_no         
,over19_ind      
,registrar_notes 
,reason_denied   
,person_guid     
,application_guid 
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT
 xform_reg.file_number
,true
,'System-created application for grandfathered driller.'
,null
,xform_reg.reg_guid -- we explicitly set this above
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from registries_person per
    ,xform_registries_drillers_reg xform_reg
    ,registries_organization org
where per.person_guid = xform_reg.reg_guid
and xform_reg.companyname is not null
and org.name = xform_reg.companyname;


-- "Fake" Applications to represent grand-fathered web drillers

-- 'DRILL', 'GEOXCHG'
INSERT INTO registries_classification_applied_for (              
 primary_certificate_no         
,certifying_org_guid                       
,application_guid               
,registries_subactivity_guid    
,classification_applied_for_guid
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT
 xform_reg.classofwelldriller
,CASE
   WHEN xform_reg.typeofcertificate like '%CGWA' 
     THEN 'd76775a3-650d-44cb-a3b7-5faf8558f29d'::uuid
   WHEN xform_reg.typeofcertificate like '%Prov. Of BC'
     THEN 'd3dfedd0-59b3-41cd-a40c-6e35b236a3d6'::uuid
 ELSE null
 END  
,appl.application_guid
,(select subact.registries_subactivity_guid
  from registries_subactivity_code subact, registries_activity_code act
  where act.registries_activity_guid = subact.registries_activity_guid
  and   act.code = 'DRILL'
  and   subact.code = 'GEOXCHG'
 )
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from registries_application appl
    ,xform_registries_drillers_reg xform_reg
where xform_reg.reg_guid = appl.person_guid
and xform_reg.companyname is not null
and   xform_reg.classofwell LIKE '%Geothermal%';


-- 'DRILL', 'GEOTECH'
INSERT INTO registries_classification_applied_for (              
 primary_certificate_no         
,certifying_org_guid                       
,application_guid               
,registries_subactivity_guid    
,classification_applied_for_guid
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT
 xform_reg.classofwelldriller
,CASE
   WHEN xform_reg.typeofcertificate like '%CGWA' 
     THEN 'd76775a3-650d-44cb-a3b7-5faf8558f29d'::uuid
   WHEN xform_reg.typeofcertificate like '%Prov. Of BC'
     THEN 'd3dfedd0-59b3-41cd-a40c-6e35b236a3d6'::uuid
 ELSE null
 END  
,appl.application_guid
,(select subact.registries_subactivity_guid
  from registries_subactivity_code subact, registries_activity_code act
  where act.registries_activity_guid = subact.registries_activity_guid
  and   act.code = 'DRILL'
  and   subact.code = 'GEOTECH'
 )
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from registries_application appl
    ,xform_registries_drillers_reg xform_reg
where xform_reg.reg_guid = appl.person_guid
and xform_reg.companyname is not null
and   xform_reg.classofwell LIKE '%Geotechnical%';

-- 'DRILL', 'WATER'
INSERT INTO registries_classification_applied_for (              
 primary_certificate_no         
,certifying_org_guid                       
,application_guid               
,registries_subactivity_guid    
,classification_applied_for_guid
,who_created  
,when_created 
,who_updated  
,when_updated 
)
SELECT
 xform_reg.classofwelldriller
,CASE
   WHEN xform_reg.typeofcertificate like '%CGWA' 
     THEN 'd76775a3-650d-44cb-a3b7-5faf8558f29d'::uuid
   WHEN xform_reg.typeofcertificate like '%Prov. Of BC'
     THEN 'd3dfedd0-59b3-41cd-a40c-6e35b236a3d6'::uuid
 ELSE null
 END  
,appl.application_guid
,(select subact.registries_subactivity_guid
  from registries_subactivity_code subact, registries_activity_code act
  where act.registries_activity_guid = subact.registries_activity_guid
  and   act.code = 'DRILL'
  and   subact.code = 'WATER'
 )
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from registries_application appl
    ,xform_registries_drillers_reg xform_reg
where xform_reg.reg_guid = appl.person_guid
and xform_reg.companyname is not null
and   xform_reg.classofwell LIKE '%Water Well%';

-- Fake Approvals
INSERT INTO registries_application_status (
 notified_date                     
,effective_date                    
,expired_date                      
,application_guid                  
,registries_application_status_guid
,application_status_guid           
,who_created                       
,when_created                      
,who_updated                       
,when_updated 
)
SELECT
 null
,xform_reg.registrationdate
,null
,appl.application_guid
,(select status_code.registries_application_status_guid
 from registries_application_status_code status_code
 where status_code.code = 'A')
,gen_random_uuid()
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
,'DATALOAD_USER'
,'2018-01-01 00:00:00-08'
from registries_person per
    ,xform_registries_drillers_reg xform_reg
    ,registries_organization org
    ,registries_application appl
where per.person_guid = xform_reg.reg_guid
and xform_reg.companyname is not null
and org.name = xform_reg.companyname
and appl.person_guid = xform_reg.reg_guid -- we explicitly set this above;
;

-- create registries_register (type DRILL)
--  for xform_registries_action_tracking_driller.Registered = Removed
--  similar to 'fake' applications, and statuses

