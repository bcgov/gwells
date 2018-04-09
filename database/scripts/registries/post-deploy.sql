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




-- Well Class and Qualifications 
DROP VIEW IF EXISTS vw_well_class;
CREATE OR REPLACE VIEW vw_well_class AS
SELECT 
 subact.registries_activity_code   AS activity_code   
,subact.description                AS subactivity                
,class.description               AS well_class               
---- Remainder are PK, FK, Audit columns (usually hidden from user)
,class.create_user               AS class_create_user               
,class.create_date               AS class_create_date               
,class.update_user               AS class_update_user               
,class.update_date               AS class_update_date               
,class.registries_well_class_code AS class_registries_well_class_code
,class.display_order             AS class_display_order             
,class.effective_date            AS class_effective_date            
,class.expired_date              AS class_expired_date              
,subact.registries_subactivity_code AS subact_registries_subactivity_code
,subact.display_order              AS subact_display_order              
,subact.create_user                AS subact_create_user                
,subact.create_date                AS subact_create_date                
,subact.update_user                AS subact_update_user                
,subact.update_date                AS subact_update_date                
,subact.effective_date             AS subact_effective_date             
,subact.expired_date               AS subact_expired_date               
FROM registries_well_qualification qual 
INNER JOIN registries_well_class_code class
ON qual.registries_well_class_code = class.registries_well_class_code
INNER JOIN registries_subactivity_code subact
ON qual.registries_subactivity_code = subact.registries_subactivity_code
;



-- GWELLS people in our system, with or without contact details
DROP VIEW IF EXISTS vw_person;
CREATE OR REPLACE VIEW vw_person AS
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
---- Remainder are PK, FK, Audit columns (usually hidden from user)
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

-- People and the Company for which they work
DROP VIEW IF EXISTS vw_person_org;
CREATE OR REPLACE VIEW vw_person_org AS
SELECT 
 per.first_name          AS first_name       
,per.surname             AS surname          
,con.contact_tel         AS contact_tel        
,con.contact_email       AS contact_email      
,org.name                AS org_name               
,org.street_address      AS org_street_address     
,org.city                AS org_city               
,org.postal_code         AS org_postal_code        
,org.main_tel            AS org_main_tel           
,org.fax_tel             AS org_fax_tel            
,org.website_url         AS org_website_url        
,org.province_state_code AS org_province_state_code
---- Remainder are PK, FK, Audit columns (usually hidden from user)
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
,org.create_user         AS org_create_user        
,org.create_date         AS org_create_date        
,org.update_user         AS org_update_user        
,org.update_date         AS org_update_date        
,org.org_guid            AS org_org_guid           
,org.effective_date      AS org_effective_date     
,org.expired_date        AS org_expired_date       
FROM registries_person per
LEFT JOIN registries_contact_detail con 
ON per.person_guid = con.person_guid
LEFT JOIN registries_organization org
ON per.organization_guid = org.org_guid
;

-- "ACTIVE" Well Drillers on the Registry
DROP VIEW IF EXISTS vw_well_driller_reg;
CREATE OR REPLACE VIEW vw_well_driller_reg AS
SELECT 
 per.first_name          AS first_name       
,per.surname             AS surname          
,con.contact_tel         AS contact_tel        
,con.contact_email       AS contact_email      
,org.name                AS org_name               
,org.street_address      AS org_street_address     
,org.city                AS org_city               
,org.postal_code         AS org_postal_code        
,org.main_tel            AS org_main_tel           
,org.fax_tel             AS org_fax_tel            
,org.website_url         AS org_website_url        
,org.province_state_code AS org_province_state_code
,reg.registration_no               AS reg_registration_no               
,reg.registration_date             AS reg_registration_date             
,reg.registries_activity_code      AS reg_registries_activity_code      
,reg.registries_status_code        AS reg_registries_status_code        
-- Not relevant as only ACTIVE Drillers
-- ,reg.register_removal_date         AS reg_register_removal_date         
-- ,reg.person_guid                   AS reg_person_guid                   
-- ,reg.registries_removal_reason_code AS reg_registries_removal_reason_code
---- Remainder are PK, FK, Audit columns (usually hidden from user)
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
,org.create_user         AS org_create_user        
,org.create_date         AS org_create_date        
,org.update_user         AS org_update_user        
,org.update_date         AS org_update_date        
,org.org_guid            AS org_org_guid           
,org.effective_date      AS org_effective_date     
,org.expired_date        AS org_expired_date       
,reg.create_user         AS reg_create_user                   
,reg.create_date         AS reg_create_date                   
,reg.update_user         AS reg_update_user                   
,reg.update_date         AS reg_update_date                   
,reg.register_guid       AS reg_register_guid                 
FROM registries_person per
LEFT JOIN registries_contact_detail con 
ON per.person_guid = con.person_guid
LEFT JOIN registries_organization org
ON per.organization_guid = org.org_guid
INNER JOIN  registries_register reg
ON per.person_guid = reg.person_guid
WHERE reg.registries_activity_code = 'DRILL'
AND   reg.registries_status_code = 'ACTIVE'
;

-- "ACTIVE" Pump Installers on the Registry
DROP VIEW IF EXISTS vw_pump_installer_reg;
CREATE OR REPLACE VIEW vw_pump_installer_reg AS
SELECT 
 per.first_name          AS first_name       
,per.surname             AS surname          
,con.contact_tel         AS contact_tel        
,con.contact_email       AS contact_email      
,org.name                AS org_name               
,org.street_address      AS org_street_address     
,org.city                AS org_city               
,org.postal_code         AS org_postal_code        
,org.main_tel            AS org_main_tel           
,org.fax_tel             AS org_fax_tel            
,org.website_url         AS org_website_url        
,org.province_state_code AS org_province_state_code
,reg.registration_no               AS reg_registration_no               
,reg.registration_date             AS reg_registration_date             
,reg.registries_activity_code      AS reg_registries_activity_code      
,reg.registries_status_code        AS reg_registries_status_code        
-- Not relevant as only ACTIVE Drillers
-- ,reg.register_removal_date         AS reg_register_removal_date         
-- ,reg.person_guid                   AS reg_person_guid                   
-- ,reg.registries_removal_reason_code AS reg_registries_removal_reason_code
---- Remainder are PK, FK, Audit columns (usually hidden from user)
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
,org.create_user         AS org_create_user        
,org.create_date         AS org_create_date        
,org.update_user         AS org_update_user        
,org.update_date         AS org_update_date        
,org.org_guid            AS org_org_guid           
,org.effective_date      AS org_effective_date     
,org.expired_date        AS org_expired_date       
,reg.create_user         AS reg_create_user                   
,reg.create_date         AS reg_create_date                   
,reg.update_user         AS reg_update_user                   
,reg.update_date         AS reg_update_date                   
,reg.register_guid       AS reg_register_guid                 
FROM registries_person per
LEFT JOIN registries_contact_detail con 
ON per.person_guid = con.person_guid
LEFT JOIN registries_organization org
ON per.organization_guid = org.org_guid
INNER JOIN  registries_register reg
ON per.person_guid = reg.person_guid
WHERE reg.registries_activity_code = 'PUMP'
AND   reg.registries_status_code = 'ACTIVE'
;


-- Accredited Certificates 
DROP VIEW IF EXISTS vw_accredited_certficate;
CREATE OR REPLACE VIEW vw_accredited_certficate AS
SELECT
 auth.cert_auth_code AS certifying_auth_code
,auth.description    AS certifying_auth_name   
,cert.name                    AS  name                    
,cert.description             AS  description             
---- Remainder are PK, FK, Audit columns (usually hidden from user)
,auth.create_user    AS auth_create_user   
,auth.create_date    AS auth_create_date   
,auth.update_user    AS auth_update_user   
,auth.update_date    AS auth_update_date   
,auth.effective_date AS auth_effective_date
,auth.expired_date   AS auth_expired_date  
,cert.create_user             AS  cert_create_user             
,cert.create_date             AS  cert_create_date             
,cert.update_user             AS  cert_update_user             
,cert.update_date             AS  cert_update_date             
,cert.acc_cert_guid           AS  cert_acc_cert_guid           
,cert.effective_date          AS  cert_effective_date          
,cert.expired_date            AS  cert_expired_date            
,cert.cert_auth_code          AS  cert_cert_auth_code          
,cert.registries_activity_code AS cert_registries_activity_code
FROM registries_accredited_certificate_code cert
INNER JOIN registries_certifying_authority_code auth
ON cert.cert_auth_code = auth.cert_auth_code;






