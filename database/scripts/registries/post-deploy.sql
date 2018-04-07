ALTER TABLE registries_activity_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE registries_subactivity_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE registries_well_class_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE registries_well_qualification ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE registries_status_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE registries_application_status_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE registries_removal_reason_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;


-- Thu  1 Mar 20:00:30 2018 GW Django doesn't support multi-column PK's
--
--  May need to enforce but on (effective_date, expiry_date) range
-- 
-- ALTER TABLE registries_well_qualification DROP CONSTRAINT IF EXISTS registries_well_qualification CASCADE;
-- ALTER TABLE registries_well_qualification ADD CONSTRAINT registries_well_qualification UNIQUE (well_class, subactivity);



/* Additional updates to DB stucture, as Python's model.py has limited abilities to do this */
DROP VIEW IF EXISTS registries_well_driller_register;
DROP VIEW IF EXISTS registries_pump_installer_register;

DROP VIEW IF EXISTS registries_v_person;

-- GWELLS people in our system, with or without contact details
CREATE OR REPLACE VIEW v_person AS
SELECT 
 per.first_name          AS first_name       
,per.surname             AS surname          
,con.contact_tel         AS contact_tel        
,con.contact_email       AS contact_email      
,per.create_user         AS per_create_user      
,per.create_date         AS per_create_date      
,per.update_user         AS per_update_user      
,per.update_date         AS per_update_date      
,per.person_guid         AS per_person_guid      
,per.effective_date      AS per_effective_date   
,per.expired_date        AS per_expired_date     
,per.organization_guid   AS per_organization_guid
,con.create_user         AS con_create_user        
,con.create_date         AS con_create_date        
,con.update_user         AS con_update_user        
,con.update_date         AS con_update_date        
,con.contact_detail_guid AS con_contact_detail_guid
,con.effective_date      AS con_effective_date     
,con.expired_date        AS con_expired_date       
FROM registries_person per
LEFT JOIN registries_contact_detail con 
ON per.person_guid = con.person_guid
;

--CREATE OR REPLACE VIEW registries_well_driller_register AS
--SELECT 
-- reg.registration_no
--,reg.registration_date
--,status.code   as status_code
--,reg.register_removal_date
--,removal.code  as register_removal_reason
--,act.code as activity_code
--,appl.file_no
--,appl.over19_ind
--,appl.registrar_notes 
--,appl.reason_denied 
--,per.first_name
--,per.surname
--,contact.contact_tel
--,contact.contact_email
--,org.name           AS org_name
--,org.street_address
--,org.city
--,org.province_state_code AS prov_state_code 
--,org.postal_code           
--,org.main_tel              
--,org.fax_tel               
--,org.website_url           
---- Remainder are PK, FK, Audit columns (usually hidden from user)
--,reg.register_guid            
--,reg.create_user AS reg_create_user                 
--,reg.create_date AS reg_create_date
--,reg.update_user AS reg_update_user
--,reg.update_date AS reg_update_date
--,status.registries_status_guid
--,status.create_user AS status_create_user                 
--,status.create_date AS status_create_date
--,status.update_user AS status_update_user
--,status.update_date AS status_update_date
--,appl.application_guid
--,appl.create_user AS appl_create_user
--,appl.create_date AS appl_create_date
--,appl.update_user AS appl_update_user
--,appl.update_date AS appl_update_date
--,removal.registries_removal_reason_guid
--,removal.create_user AS removal_create_user
--,removal.create_date AS removal_create_date
--,removal.update_user AS removal_update_user
--,removal.update_date AS removal_update_date
--,act.registries_activity_guid 
--,act.create_user AS act_create_user
--,act.create_date AS act_create_date
--,act.update_user AS act_update_user
--,act.update_date AS act_update_date
--,per.person_guid
--,per.create_user AS per_create_user
--,per.create_date AS per_create_date
--,per.update_user AS per_update_user
--,per.update_date AS per_update_date
--,contact.contact_at_guid 
--,contact.effective_date AS contact_effective_date
--,contact.expired_date   AS contact_expired_date
--,contact.create_user AS contact_create_user
--,contact.create_date AS contact_create_date
----,contact.update_user AS contact_update_user
----,contact.update_date AS contact_update_date
----,org.org_guid  
----,org.create_user AS org_create_user          
----,org.create_date AS org_create_date          
----,org.update_user AS org_update_user          
----,org.update_date AS org_update_date 
----FROM registries_register reg
----INNER JOIN registries_application appl
----  ON appl.application_guid = reg.application_guid
----INNER JOIN registries_status_code status
----  ON reg.registries_status_guid = status.registries_status_guid
----INNER JOIN registries_activity_code act 
----  ON reg.registries_activity_guid = act.registries_activity_guid
----LEFT JOIN registries_person per
--  ON per.person_guid = appl.person_guid
--INNER JOIN registries_contact_detail contact
--  ON per.person_guid = contact.person_guid
--INNER JOIN registries_organization org
--  ON org.org_guid = contact.org_guid
--LEFT JOIN registries_removal_reason_code removal
--  ON removal.registries_removal_reason_guid = reg.registries_removal_reason_guid
--WHERE act.code = 'DRILL';       
--
--COMMENT ON  VIEW registries_driller_register  IS 'Placeholder view comment.';
