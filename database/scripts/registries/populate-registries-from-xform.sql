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






NOTE: classofwelldriller seems to be certificate# or 'grand-parent'
 - there is one record with " 00023-WW-02; GWDT-2002-092"
   I should 'substring just text b/f the semicolon'


create registries_register (type DRILL)
  - for xform_registries_action_tracking_driller.Registered = Yes 
  - for xform_registries_action_tracking_driller.Registered = Removed


/*
DROP FUNCTION IF EXISTS gwells_populate_well();

CREATE OR REPLACE FUNCTION gwells_populate_well() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
  raise notice '... importing xform into the gwells_well table';

  INSERT INTO gwells_well (
    well_tag_number                    ,
    well_guid                          ,
    owner_full_name                    ,
    owner_mailing_address              ,
    owner_city                         ,
    owner_postal_code                  ,
    street_address                     ,
    city                               ,
    legal_lot                          ,
    legal_plan                         ,
    legal_district_lot                 ,
    legal_block                        ,
    legal_section                      ,
    legal_township                     ,
    legal_range                        ,
    land_district_guid                 ,
    legal_pid                          ,
    well_location_description          ,
    identification_plate_number        ,
    diameter                           ,
    total_depth_drilled                ,
    finished_well_depth                ,
    static_water_level                 ,
    well_cap_type                      ,
    well_disinfected                   ,
    well_yield                         ,
    intended_water_use_guid            ,
    province_state_guid                ,
    well_class_guid                    ,
    well_subclass_guid                 ,
    well_yield_unit_guid               ,
    latitude                           ,
    longitude                          ,
    ground_elevation                   ,
    well_orientation                   ,
    other_drilling_method              ,
    drilling_method_guid               ,
    ground_elevation_method_guid       ,
    when_created                       ,
    when_updated                       ,
    who_created                        ,
    who_updated                        ,
    surface_seal_length                ,
    surface_seal_thickness             ,
    surface_seal_method_guid           ,
    surface_seal_material_guid         ,
    backfill_type                      ,
    backfill_depth                     ,
    liner_material_guid                ,
    well_status_guid                   ,
    observation_well_number            ,
    observation_well_status_guid       ,
    licenced_status_guid               ,
    other_screen_bottom                ,
    other_screen_material              ,
    development_notes                  ,
    water_quality_colour               ,
    water_quality_odour                ,
    alternative_specs_submitted        ,
    construction_start_date            ,
    construction_end_date              ,
    alteration_start_date              ,
    alteration_end_date                ,
    decommission_start_date            ,
    decommission_end_date              ,
    drilling_company_guid              ,
    final_casing_stick_up              ,
    artesian_flow                      ,
    artesian_pressure                  ,
    bedrock_depth                      ,
    water_supply_system_name           ,
    water_supply_system_well_name      ,
    well_identification_plate_attached ,
    ems                                ,
    screen_intake_method_guid          ,
    screen_type_guid                   ,
    screen_material_guid               ,
    screen_opening_guid                ,
    screen_bottom_guid                 ,
    utm_zone_code                      ,
    utm_northing                       ,
    utm_easting                        ,
    utm_accuracy_code                  ,
    bcgs_id                            ,
    development_method_guid            ,
    development_hours                  ,
    decommission_reason                ,
    decommission_method_guid           ,
    sealant_material                   ,
    backfill_material                  ,
    decommission_details               ,
    comments
    )
  SELECT
  	xform.well_tag_number                          ,
  	gen_random_uuid()                              ,
  	COALESCE(xform.owner_full_name,' ')            ,
  	COALESCE(xform.owner_mailing_address, ' ')     ,
  	COALESCE(xform.owner_city, ' ')                ,
  	COALESCE(xform.owner_postal_code , ' ')        ,
  	COALESCE(xform.street_address    , ' ')        ,
  	COALESCE(xform.city              , ' ')        ,
  	COALESCE(xform.legal_lot         , ' ')        ,
  	COALESCE(xform.legal_plan        , ' ')        ,
  	COALESCE(xform.legal_district_lot, ' ')        ,
  	COALESCE(xform.legal_block       , ' ')        ,
  	COALESCE(xform.legal_section     , ' ')        ,
  	COALESCE(xform.legal_township    , ' ')        ,
  	COALESCE(xform.legal_range       , ' ')        ,
    xform.land_district_guid                       ,
  	xform.legal_pid                                ,
  	COALESCE(xform.well_location_description,' ')  ,
  	xform.identification_plate_number              ,
  	COALESCE(xform.diameter, ' ')                  ,
  	xform.total_depth_drilled                      ,
  	xform.finished_well_depth                      ,
    xform.static_water_level                       ,
    xform.well_cap_type                            ,
    xform.well_disinfected                         ,
  	xform.well_yield                               ,
  	xform.intended_water_use_guid                  ,
  	xform.province_state_guid                      ,
  	xform.well_class_guid                          ,
  	xform.well_subclass_guid                       ,
  	xform.well_yield_unit_guid                     ,
  	xform.latitude                                 ,
  	xform.longitude                                ,
  	xform.ground_elevation                         ,
  	xform.well_orientation                         ,
  	NULL                                           ,
  	xform.drilling_method_guid                     ,
  	xform.ground_elevation_method_guid             ,
  	xform.when_created                             ,
  	xform.when_updated                             ,
  	xform.who_created                              ,
  	xform.who_updated                              ,
  	xform.surface_seal_length                      ,
  	xform.surface_seal_thickness                   ,
  	xform.surface_seal_method_guid                 ,
    xform.surface_seal_material_guid               ,
    xform.backfill_type                            ,
    xform.backfill_depth                           ,
    xform.liner_material_guid                      ,
  	xform.well_status_guid                         ,
    xform.observation_well_number                  ,
    xform.observation_well_status_guid             ,
  	xform.licenced_status_guid                     ,
  	''                                             ,
  	''                                             ,
  	''                                             ,
  	''                                             ,
  	''                                             ,
  	false                                          ,
  	xform.construction_start_date                  ,
  	xform.construction_end_date                    ,
  	xform.alteration_start_date                    ,
  	xform.alteration_end_date                      ,
  	xform.decommission_start_date                  ,
  	xform.decommission_end_date                    ,
  	xform.drilling_company_guid                    ,
    xform.final_casing_stick_up                    ,
    xform.artesian_flow                            ,
    xform.artesian_pressure                        ,
    xform.bedrock_depth                            ,
    xform.water_supply_system_name                 ,
    xform.water_supply_system_well_name            ,
    xform.well_identification_plate_attached       ,
    xform.ems                                      ,
    xform.screen_intake_method_guid                ,
    xform.screen_type_guid                         ,
    xform.screen_material_guid                     ,
    xform.screen_opening_guid                      ,
    xform.screen_bottom_guid                       ,
    xform.utm_zone_code                            ,
    xform.utm_northing                             ,
    xform.utm_easting                              ,
    xform.utm_accuracy_code                        ,
  	xform.bcgs_id                                  ,
    xform.development_method_guid                  ,
    xform.development_duration                     ,
    xform.decommission_reason                      ,
    xform.decommission_method_guid                 ,
    xform.sealant_material                         ,
    xform.backfill_material                        ,
    xform.decommission_details                     ,
    xform.comments
  FROM xform_gwells_well xform;

  raise notice '...xform data imported into the gwells_well table';
  SELECT count(*) from gwells_well into row_count;
  raise notice '% rows loaded into the gwells_well table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION gwells_populate_well () IS 'Transfer from local XFORM ETL table into gwells_well.';
*/
