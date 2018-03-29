-- @Registries

\echo 'Starting to clear Registries app tables procedure (code tables only) ...'
\echo '... leaving xform_registries_* tables as we are storing PII on gitHub'

-- Reset tables
-- TRUNCATE TABLE registries_activity_code, registries_qualification_code, 
-- registries_status_code, registries_application_status_code, 
-- registries_removal_reason_code CASCADE;


-- Reset Test Data
truncate registries_organization, registries_person cascade;
 
\echo 'Finished clearing Registries tables (code tables only).'