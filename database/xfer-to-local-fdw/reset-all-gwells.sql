
 -- DANGER DANGER
 -- SQL Script that is run as part of 'resetting' the application model.py
 -- 1. all /migrations/000*.py should be removed first from the local file system
 -- 2. after this script is run, then 'python manage.py makemigrations xxx' should be run
 -- 
 -- psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -f reset-all-gwells.sql
 -- 
 drop table if exists auth_group                               cascade;
 drop table if exists auth_group_permissions                   cascade;
 drop table if exists auth_permission                          cascade;
 drop table if exists auth_user                                cascade;
 drop table if exists auth_user_groups                         cascade;
 drop table if exists auth_user_user_permissions               cascade;
 drop table if exists bossoidc_keycloak                        cascade;
 drop table if exists django_admin_log                         cascade;
 drop table if exists django_content_type                      cascade;
 drop table if exists django_migrations                        cascade;
 drop table if exists django_session                           cascade;
 drop table if exists gwells_activity_submission               cascade;
 drop table if exists gwells_activity_submission_water_quality cascade;
 drop table if exists gwells_aquifer_well                      cascade;
 drop table if exists gwells_bcgs_number                       cascade;
 drop table if exists gwells_bedrock_material                  cascade;
 drop table if exists gwells_bedrock_material_descriptor       cascade;
 drop table if exists gwells_casing                            cascade;
 drop table if exists gwells_casing_material                   cascade;
 drop table if exists casing_code                       cascade;
 drop table if exists gwells_decommission_method               cascade;
 drop table if exists gwells_development_method                cascade;
 drop table if exists gwells_driller                           cascade;
 drop table if exists gwells_drilling_company                  cascade;
 drop table if exists gwells_drilling_method                   cascade;
 drop table if exists gwells_filter_pack_material              cascade;
 drop table if exists gwells_filter_pack_material_size         cascade;
 drop table if exists gwells_ground_elevation_method           cascade;
 drop table if exists gwells_intended_water_use                cascade;
 drop table if exists gwells_land_district                     cascade;
 drop table if exists gwells_licenced_status                   cascade;
 drop table if exists gwells_liner_material                    cascade;
 drop table if exists gwells_liner_perforation                 cascade;
 drop table if exists gwells_lithology_colour                  cascade;
 drop table if exists gwells_lithology_description             cascade;
 drop table if exists gwells_lithology_description_code        cascade;
 drop table if exists gwells_lithology_hardness                cascade;
 drop table if exists gwells_lithology_material                cascade;
 drop table if exists gwells_lithology_moisture                cascade;
 drop table if exists gwells_lithology_structure               cascade;
 drop table if exists gwells_ltsa_owner                        cascade;
 drop table if exists gwells_observation_well_status           cascade;
 drop table if exists gwells_perforation                       cascade;
 drop table if exists gwells_production_data                   cascade;
 drop table if exists gwells_province_state                    cascade;
 drop table if exists gwells_screen                            cascade;
 drop table if exists gwells_screen_assembly_type              cascade;
 drop table if exists gwells_screen_bottom                     cascade;
 drop table if exists gwells_screen_intake_method              cascade;
 drop table if exists gwells_screen_material                   cascade;
 drop table if exists gwells_screen_opening                    cascade;
 drop table if exists gwells_screen_type                       cascade;
 drop table if exists gwells_surface_seal_material             cascade;
 drop table if exists gwells_surface_seal_method               cascade;
 drop table if exists gwells_surficial_material                cascade;
 drop table if exists gwells_water_quality_characteristic      cascade;
 drop table if exists gwells_well                              cascade;
 drop table if exists gwells_well_activity_type                cascade;
 drop table if exists gwells_well_class                        cascade;
 drop table if exists gwells_well_status                       cascade;
 drop table if exists gwells_well_subclass                     cascade;
 drop table if exists gwells_well_water_quality                cascade;
 drop table if exists gwells_well_yield_unit                   cascade;
 drop table if exists gwells_user                              cascade;
 drop table if exists gwells_user_groups                       cascade;

 drop table if exists gwells_user_user_permissions             cascade;

 drop table if exists gwells_yield_estimation_method           cascade;
 drop table if exists registries_activity_code                 cascade;
 drop table if exists registries_application                   cascade;
 drop table if exists registries_application_status            cascade;
 drop table if exists registries_application_status_code       cascade;
 drop table if exists registries_classification_applied_for    cascade;
 drop table if exists registries_contact_at                    cascade;
 drop table if exists registries_organization                  cascade;
 drop table if exists registries_person                        cascade;
 drop table if exists registries_qualification_code            cascade;
 drop table if exists registries_register                      cascade;
 drop table if exists registries_removal_reason_code           cascade;
 drop table if exists registries_status_code                   cascade;
 drop table if exists registries_subactivity_code              cascade;
 drop table if exists xform_registries_action_tracking_driller cascade;
 drop table if exists xform_registries_drillers_reg            cascade;
 drop table if exists xform_registries_removed_from            cascade;
