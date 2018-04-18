-- @Registries

\echo 'Starting to clear Registries app tables procedure (code tables only) ...'
\echo '... leaving xform_registries_* tables as we are storing PII on gitHub'

-- Reset lookup tables tables

truncate table registries_application_status          cascade;
truncate table registries_well_qualification cascade;
truncate table registries_register cascade;
truncate table registries_application_status_code     cascade;
truncate table registries_status_code cascade;
truncate table registries_application                 cascade;
truncate table registries_contact_detail              cascade;
truncate table registries_person cascade;
truncate table registries_organization cascade;
truncate table registries_accredited_certificate_code cascade;
truncate table registries_activity_code               cascade;
truncate table registries_removal_reason_code cascade;
truncate table registries_subactivity_code cascade;
truncate table registries_certifying_authority_code   cascade;
truncate table registries_well_class_code cascade;

-- Reset Test Data
truncate registries_organization, registries_person cascade;
 
\echo 'Finished clearing Registries tables (code tables only).'