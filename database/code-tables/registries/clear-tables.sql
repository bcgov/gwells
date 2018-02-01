\echo 'Starting to clear Registries app tables procedure...'

-- Reset tables
TRUNCATE TABLE registries_activity_code, registries_qualification_code, 
registries_status_code, registries_application_status_code, 
registries_removal_reason_code CASCADE;
 
TRUNCATE TABLE xform_registries_action_tracking_driller, xform_registries_drillers_reg, xform_registries_removed_from cascade

\echo 'Finished clearing Registries tables.'