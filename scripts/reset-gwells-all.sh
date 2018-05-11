# Fri Apr 13 12:55:03 2018
# SQL Script that is run as part of 'resetting' the application model.py.  The pipeline deployment automatically
# handles:
# 1. removal/addition of all /migrations/000*.py in all Django apps (via check-in to the repo)
# 2. execution of 'python manage.py migrate'  (via the Build Configuration's [Post-Commit Hook](https://console.pathfinder.gov.bc.ca:8443/console/project/moe-gwells-tools/edit/builds/gwells-developer))
#
# ./reset-gwells-all.sh 
#

# Halt conditions, verbosity and field separator
#
set -euo pipefail
[ "${VERBOSE:-x}" != true ]|| set -x
IFS=$'\n\t'


# Receive project from parameter, default to dev
#
PROJECT=${1:-moe-gwells-dev}


# Show message if passed any params
#
if [ "${#}" -eq 0 ]
then
	echo
    echo "Part of resetting the application model.py."
    echo
	echo "Provide a project name."
	echo " './reset-gwells-all.sh <project_name>'"
	echo
	exit
fi


# Check login
#
if ( ! oc whoami )
then
    echo
    echo "Please obtain an OpenShift API token.  A window will open shortly."
    sleep 3
    open https://console.pathfinder.gov.bc.ca:8443/oauth/token/request
    exit
fi


# Check project availability
#
CHECK=$( oc projects | tr -d '*' | grep -v "Using project" | grep "${PROJECT}" | awk '{ print $1 }' || echo )
if [ "${PROJECT}" != "${CHECK}" ]
then
	echo
	echo "Unable to access project ${PROJECT}"
	echo
	exit
fi


# Identify running GWells database pod under selected project
#
PODNAME=$(oc get pods -n ${PROJECT} | grep postgresql-[0-9] | grep Running | head -n 1 | awk '{print $1}')


# Drop tables
#
# Fri 20 Apr 10:26:57 2018 GW Excluded "province_state_code", as this impacts the
#                             Registries app.  As we move to a steady-state (in terms
#                             of lookup code tables, we will SKIP reloading them)
#
oc exec ${PODNAME} -n ${PROJECT} -- /bin/bash -c 'export PGPASSWORD=$POSTGRESQL_PASSWORD;psql -h $POSTGRESQL_SERVICE_HOST -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER  << EOF
drop table if exists activity_submission                             cascade;
drop table if exists activity_submission_water_quality               cascade;
drop table if exists aquifer_well                                    cascade;
drop table if exists auth_group                                      cascade;
drop table if exists auth_group_permissions                          cascade;
drop table if exists auth_permission                                 cascade;
drop table if exists auth_user                                       cascade;
drop table if exists auth_user_groups                                cascade;
drop table if exists auth_user_user_permissions                      cascade;
drop table if exists bcgs_number                                     cascade;
drop table if exists bedrock_material_code                           cascade;
drop table if exists bedrock_material_descriptor_code                cascade;
drop table if exists casing                                          cascade;
drop table if exists casing_code                                     cascade;
drop table if exists casing_material_code                            cascade;
drop table if exists decommission_method_code                        cascade;
drop table if exists development_method_code                         cascade;
drop table if exists django_admin_log                                cascade;
drop table if exists django_content_type                             cascade;
drop table if exists django_migrations                               cascade;
drop table if exists django_session                                  cascade;
drop table if exists driller                                         cascade;
drop table if exists drilling_company                                cascade;
drop table if exists drilling_method_code                            cascade;
drop table if exists filter_pack_material_code                       cascade;
drop table if exists filter_pack_material_size_code                  cascade;
drop table if exists ground_elevation_method_code                    cascade;
drop table if exists gwells_survey                                   cascade;
drop table if exists intended_water_use_code                         cascade;
drop table if exists land_district_code                              cascade;
drop table if exists licenced_status_code                            cascade;
drop table if exists liner_material_code                             cascade;
drop table if exists liner_perforation                               cascade;
drop table if exists lithology_colour_code                           cascade;
drop table if exists lithology_description                           cascade;
drop table if exists lithology_description_code                      cascade;
drop table if exists lithology_hardness_code                         cascade;
drop table if exists lithology_material_code                         cascade;
drop table if exists lithology_moisture_code                         cascade;
drop table if exists lithology_structure_code                        cascade;
drop table if exists ltsa_owner                                      cascade;
drop table if exists obs_well_status_code                            cascade;
drop table if exists online_survey                                   cascade;
drop table if exists perforation                                     cascade;
drop table if exists production_data                                 cascade;
drop table if exists profile                                         cascade;
drop table if exists registries_accredited_certificate               cascade;
drop table if exists registries_activity_code                        cascade;
drop table if exists registries_application                          cascade;
drop table if exists registries_application_status                   cascade;
drop table if exists registries_application_status_code              cascade;
drop table if exists registries_certifying_authority                 cascade;
drop table if exists registries_contact_detail                       cascade;
drop table if exists registries_organization                         cascade;
drop table if exists registries_person                               cascade;
drop table if exists registries_register                             cascade;
drop table if exists registries_removal_reason_code                  cascade;
drop table if exists registries_status_code                          cascade;
drop table if exists registries_subactivity_code                     cascade;
drop table if exists registries_well_class_code                      cascade;
drop table if exists registries_well_qualification                   cascade;
drop table if exists screen                                          cascade;
drop table if exists screen_assembly_type_code                       cascade;
drop table if exists screen_bottom_code                              cascade;
drop table if exists screen_intake_method_code                       cascade;
drop table if exists screen_material_code                            cascade;
drop table if exists screen_opening_code                             cascade;
drop table if exists screen_type_code                                cascade;
drop table if exists surface_seal_material_code                      cascade;
drop table if exists surface_seal_method_code                        cascade;
drop table if exists surficial_material_code                         cascade;
drop table if exists water_quality_characteristic                    cascade;
drop table if exists well                                            cascade;
drop table if exists well_activity_code                              cascade;
drop table if exists well_class_code                                 cascade;
drop table if exists well_status_code                                cascade;
drop table if exists well_subclass_code                              cascade;
drop table if exists well_water_quality                              cascade;
drop table if exists well_yield_unit_code                            cascade;
drop table if exists xform_registries_action_tracking_driller        cascade;
drop table if exists xform_registries_action_tracking_pump_installer cascade;
drop table if exists xform_registries_drillers_reg                   cascade;
drop table if exists xform_registries_pump_installers_reg            cascade;
drop table if exists xform_registries_removed_from                   cascade;
drop table if exists yield_estimation_method_code                    cascade;
drop table if exists province_state_code                             cascade;

drop table if exists registries_certifying_authority_code   cascade;
drop table if exists registries_accredited_certificate_code cascade;

drop table if exists registries_classification_applied_for cascade;
drop table if exists registries_contact_at                 cascade;
drop table if exists registries_contact_detail             cascade;
drop table if exists registries_organization               cascade;
drop table if exists registries_person                     cascade;
drop table if exists registries_qualification_code         cascade;
drop table if exists registries_register_note              cascade;
drop table if exists registries_person_note                cascade;
EOF
'
