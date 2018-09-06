/* Additional updates to DB stucture, as Python's model.py has limited abilities to do this */
DROP INDEX IF EXISTS well_latlong CASCADE;
CREATE INDEX well_latlong ON well (latitude, longitude);

DROP INDEX IF EXISTS bcgs_number_idx CASCADE;
CREATE INDEX bcgs_number_idx ON bcgs_number (bcgs_number);

COMMENT ON TABLE activity_submission               IS 'Placeholder table comment.';
COMMENT ON TABLE activity_submission_water_quality IS 'Placeholder table comment.';
COMMENT ON TABLE aquifer_well                      IS 'Placeholder table comment.';
COMMENT ON TABLE bcgs_number                       IS 'Placeholder table comment.';
COMMENT ON TABLE bedrock_material_code                  IS 'Placeholder table comment.';
COMMENT ON TABLE bedrock_material_descriptor_code       IS 'Placeholder table comment.';
COMMENT ON TABLE casing                            IS 'Placeholder table comment.';
COMMENT ON TABLE casing_material_code                   IS 'Placeholder table comment.';
COMMENT ON TABLE casing_code                       IS 'Placeholder table comment.';
COMMENT ON TABLE decommission_method_code               IS 'Placeholder table comment.';
COMMENT ON TABLE development_method_code                IS 'Placeholder table comment.';
COMMENT ON TABLE drilling_company                  IS 'Placeholder table comment.';
COMMENT ON TABLE drilling_method_code                   IS 'Placeholder table comment.';
COMMENT ON TABLE filter_pack_material_code              IS 'Placeholder table comment.';
COMMENT ON TABLE filter_pack_material_size_code         IS 'Placeholder table comment.';
COMMENT ON TABLE ground_elevation_method_code           IS 'Placeholder table comment.';
COMMENT ON TABLE intended_water_use_code                IS 'Placeholder table comment.';
COMMENT ON TABLE land_district_code                     IS 'Placeholder table comment.';
COMMENT ON TABLE licenced_status_code                   IS 'Placeholder table comment.';
COMMENT ON TABLE liner_material_code                    IS 'Placeholder table comment.';
COMMENT ON TABLE liner_perforation                 IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_colour_code                  IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_description             IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_description_code        IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_hardness_code                IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_material_code                IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_moisture_code                IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_structure_code               IS 'Placeholder table comment.';
COMMENT ON TABLE ltsa_owner                        IS 'Placeholder table comment.';
COMMENT ON TABLE perforation                       IS 'Placeholder table comment.';
COMMENT ON TABLE production_data                   IS 'Placeholder table comment.';
COMMENT ON TABLE province_state_code                    IS 'Placeholder table comment.';
COMMENT ON TABLE screen                            IS 'Placeholder table comment.';
COMMENT ON TABLE screen_assembly_type_code              IS 'Placeholder table comment.';
COMMENT ON TABLE screen_bottom_code                     IS 'Placeholder table comment.';
COMMENT ON TABLE screen_intake_method_code              IS 'Placeholder table comment.';
COMMENT ON TABLE screen_material_code                   IS 'Placeholder table comment.';
COMMENT ON TABLE screen_opening_code                    IS 'Placeholder table comment.';
COMMENT ON TABLE screen_type_code                       IS 'Placeholder table comment.';
COMMENT ON TABLE surface_seal_material_code             IS 'Placeholder table comment.';
COMMENT ON TABLE surface_seal_method_code               IS 'Placeholder table comment.';
COMMENT ON TABLE surficial_material_code                IS 'Placeholder table comment.';
COMMENT ON TABLE water_quality_characteristic      IS 'Placeholder table comment.';
COMMENT ON TABLE well                              IS 'Placeholder table comment.';
COMMENT ON TABLE well_activity_code                IS 'Placeholder table comment.';
COMMENT ON TABLE well_class_code                        IS 'Placeholder table comment.';
COMMENT ON TABLE well_status_code                       IS 'Placeholder table comment.';
COMMENT ON TABLE well_subclass_code                     IS 'Placeholder table comment.';
COMMENT ON TABLE well_water_quality                IS 'Placeholder table comment.';
COMMENT ON TABLE well_yield_unit_code                   IS 'Placeholder table comment.';
COMMENT ON TABLE yield_estimation_method_code           IS 'Placeholder table comment.';


ALTER TABLE bedrock_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE bedrock_material_descriptor_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE casing_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE casing_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE decommission_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE development_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE drilling_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE filter_pack_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE filter_pack_material_size_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE ground_elevation_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE intended_water_use_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE land_district_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE licenced_status_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE liner_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_colour_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_description_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_hardness_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_moisture_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_structure_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE obs_well_status_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;

COMMENT ON COLUMN registries_accredited_certificate_code.name IS 'Certifications that are recognized by British Columbia for the purposes of registering an individual as a well pump installer or well driller.  E.g. GEOTECH, ';
COMMENT ON COLUMN registries_organization.email IS 'The email address for a company, this is different from the email for the individual who is a registered driller or pump installer.  ';
COMMENT ON COLUMN registries_organization.city IS 'City used for mailing address for the company.';
COMMENT ON COLUMN registries_organization.website_url IS 'The web address associated with the company';
COMMENT ON COLUMN registries_organization.street_address IS 'Street address used for mailing address for the company.';
COMMENT ON COLUMN registries_organization.name IS 'Company''s Doing Business As name.' ;
COMMENT ON COLUMN registries_organization.main_tel IS 'Telephone number used to contact the company';
COMMENT ON COLUMN registries_organization.fax_tel IS 'Fax number used to contact the company';
COMMENT ON COLUMN registries_organization.postal_code IS 'Postal code used for mailing address for the company';
COMMENT ON COLUMN registries_organization.province_state_code IS 'Province or state used for the mailing address for the company';
COMMENT ON COLUMN registries_organization_note.note IS 'Internal note used for the purposes of conducting business with the company.';
COMMENT ON COLUMN registries_person.first_name IS 'Legal first name of the well driller or well pump installer who has applied and/or is registered with the province.';
COMMENT ON COLUMN registries_person.contact_tel IS 'Land line area code and 7 digit phone number provided by the well driller or well pump installer where they can be contacted.' ;
COMMENT ON COLUMN registries_person.contact_cell IS 'Cell phone area code and 7 digit number provided by the well driller or well pump installer where they can be contacted.';
COMMENT ON COLUMN registries_person.surname IS 'Legal last name of the well driller or well pump installer who has applied and/or is registered with the province.';
COMMENT ON COLUMN registries_person.well_driller_orcs_no IS 'Well driller''s unique filing number used in the BC government Operational Records Classification Systems (ORCS) filing system.  E.g --------- [Explain how the number is info rich]  Each person has an ORCS number when a file is started with their correspondence, usually with the application for being registered.';
COMMENT ON COLUMN registries_person.contact_email IS 'Email address for the well driller or well pump installer.';
COMMENT ON COLUMN registries_person.pump_installer_orcs_no IS 'Well pump installer''s unique filing number used in the BC government Operational Records Classification Systems (ORCS) filing system.  E.g --------- [Explain how the number is info rich]  Each person has an ORCS number when a file is started with their correspondence, usually with the application for being registered.  Each person can have a unique ORCS number as a well pump installer and as a well driller.';
COMMENT ON COLUMN registries_person_note.note IS 'Internal note used for the purposes of conducting business with an applicant.';
COMMENT ON COLUMN registries_proof_of_age_code.registries_proof_of_age_code IS 'List of valid options for what documentation the ministry staff reviewed to verify the applicants age to be over 19.  I.e. Drivers Licence, Birth Certificate, Passport.';
COMMENT ON COLUMN registries_register.registration_no IS 'Unique number assigned to the well driller or well pump instaler upon registration.  Format used: [certification type] yymmdd[sequence]  where [sequence] is two digits starting with 01 for the first person registered in alphabetical order for that day, and [certification type] would be ''WD'' well driller and ''WPI'' for well pump installer.  E.g. WD 18031001';
COMMENT ON COLUMN registries_removal_reason_code.registries_removal_reason_code IS 'Reason why a well driller or well pump installer was removed from the registry.  I.e NMEET, FAILTM, NLACT';
COMMENT ON COLUMN registries_removal_reason_code.description IS 'Description of code e.g NMEET = Fails to meet a requirement for registration.';



-- Tue 13 Feb 22:36:42 2018 GW Disabled for now until after CodeWithUs Sprint
-- ALTER TABLE province_state_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;

ALTER TABLE screen_assembly_type_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE screen_bottom_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE screen_intake_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE screen_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE screen_opening_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE screen_type_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE surface_seal_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE surface_seal_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE surficial_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE well_activity_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE well_class_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE well_status_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE well_subclass_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE well_yield_unit_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE yield_estimation_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;

-- Thu  1 Mar 20:00:30 2018 GW Django doesn't support multi-column PK's
ALTER TABLE well_subclass_code DROP CONSTRAINT IF EXISTS well_subclass_code_uk CASCADE;
ALTER TABLE well_subclass_code ADD CONSTRAINT well_subclass_code_uk UNIQUE (well_class_code, well_subclass_code);
