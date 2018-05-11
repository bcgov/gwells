#!/bin/sh
#
# Fri Feb  9 08:46:56 2018 GW Shell script to copy down legacy Oracle tables via
# via the Oracle Foreign Data Wrapper on the postgres Pod.  This script runs
# on a local developer workstation, calling renote 'oc exec' commands
#
# NOTE: You need to be logged in with a token, via:
#       https://console.pathfinder.gov.bc.ca:8443/oauth/token/request
#
# Running on postgres database pod, as DB root access not enabled on gwells application pod

oc project moe-gwells-test
podname=$(oc get pods -n moe-gwells-test | grep postgresql | grep Running | head -n 1 | awk '{print $1}')
oc exec ${podname} -n moe-gwells-test -- /bin/bash -c 'psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER << EOF
drop schema if exists xfer_wells cascade;create schema xfer_wells;
CREATE TABLE xfer_wells.gw_aquifer_attrs AS SELECT * FROM wells.gw_aquifer_attrs;
CREATE TABLE xfer_wells.gw_aquifer_attrs_old AS SELECT * FROM wells.gw_aquifer_attrs_old;
CREATE TABLE xfer_wells.gw_aquifer_wells AS SELECT * FROM wells.gw_aquifer_wells;
CREATE TABLE xfer_wells.gw_casing_material_codes AS SELECT * FROM wells.gw_casing_material_codes;
CREATE TABLE xfer_wells.gw_class_of_well_codes AS SELECT * FROM wells.gw_class_of_well_codes;
CREATE TABLE xfer_wells.gw_class_subclass_xrefs AS SELECT * FROM wells.gw_class_subclass_xrefs;
CREATE TABLE xfer_wells.gw_closure_method_codes AS SELECT * FROM wells.gw_closure_method_codes;
CREATE TABLE xfer_wells.gw_development_method_cds AS SELECT * FROM wells.gw_development_method_cds;
CREATE TABLE xfer_wells.gw_drilling_method_codes AS SELECT * FROM wells.gw_drilling_method_codes;
CREATE TABLE xfer_wells.gw_filter_pack_material_cds AS SELECT * FROM wells.gw_filter_pack_material_cds;
CREATE TABLE xfer_wells.gw_filter_pack_size_codes AS SELECT * FROM wells.gw_filter_pack_size_codes;
CREATE TABLE xfer_wells.gw_ground_elevaton_mthd_cds AS SELECT * FROM wells.gw_ground_elevaton_mthd_cds;
CREATE TABLE xfer_wells.gw_liner_material_codes AS SELECT * FROM wells.gw_liner_material_codes;
CREATE TABLE xfer_wells.gw_nts_mapsheets AS SELECT * FROM wells.gw_nts_mapsheets;
CREATE TABLE xfer_wells.gw_orientation_of_well_cds AS SELECT * FROM wells.gw_orientation_of_well_cds;
CREATE TABLE xfer_wells.gw_province_state_codes AS SELECT * FROM wells.gw_province_state_codes;
CREATE TABLE xfer_wells.gw_relative_hardness_codes AS SELECT * FROM wells.gw_relative_hardness_codes;
CREATE TABLE xfer_wells.gw_screen_assembly_type_cds AS SELECT * FROM wells.gw_screen_assembly_type_cds;
CREATE TABLE xfer_wells.gw_screen_bottom_codes AS SELECT * FROM wells.gw_screen_bottom_codes;
CREATE TABLE xfer_wells.gw_screen_intake_codes AS SELECT * FROM wells.gw_screen_intake_codes;
CREATE TABLE xfer_wells.gw_screen_material_codes AS SELECT * FROM wells.gw_screen_material_codes;
CREATE TABLE xfer_wells.gw_screen_opening_codes AS SELECT * FROM wells.gw_screen_opening_codes;
CREATE TABLE xfer_wells.gw_screen_type_codes AS SELECT * FROM wells.gw_screen_type_codes;
CREATE TABLE xfer_wells.gw_status_of_well_codes AS SELECT * FROM wells.gw_status_of_well_codes;
CREATE TABLE xfer_wells.gw_subclass_of_well_codes AS SELECT * FROM wells.gw_subclass_of_well_codes;
CREATE TABLE xfer_wells.gw_surface_seal_materil_cds AS SELECT * FROM wells.gw_surface_seal_materil_cds;
CREATE TABLE xfer_wells.gw_surface_seal_method_cds AS SELECT * FROM wells.gw_surface_seal_method_cds;
CREATE TABLE xfer_wells.gw_utm_zone_codes AS SELECT * FROM wells.gw_utm_zone_codes;
CREATE TABLE xfer_wells.gw_water_qual_chrctrstc_cds AS SELECT * FROM wells.gw_water_qual_chrctrstc_cds;
CREATE TABLE xfer_wells.gw_well_water_quality_xrefs AS SELECT * FROM wells.gw_well_water_quality_xrefs;
CREATE TABLE xfer_wells.gw_yield_estimated_mthd_cds AS SELECT * FROM wells.gw_yield_estimated_mthd_cds;
CREATE TABLE xfer_wells.wells_acceptance_status_code AS SELECT * FROM wells.wells_acceptance_status_code;
CREATE TABLE xfer_wells.wells_aquifer_lithology_codes AS SELECT * FROM wells.wells_aquifer_lithology_codes;
CREATE TABLE xfer_wells.wells_aquifer_subtype_codes AS SELECT * FROM wells.wells_aquifer_subtype_codes;
CREATE TABLE xfer_wells.wells_bcgs_numbers AS SELECT * FROM wells.wells_bcgs_numbers;
CREATE TABLE xfer_wells.wells_casings AS SELECT * FROM wells.wells_casings;
CREATE TABLE xfer_wells.wells_constant AS SELECT * FROM wells.wells_constant;
CREATE TABLE xfer_wells.wells_constr_method_codes AS SELECT * FROM wells.wells_constr_method_codes;
CREATE TABLE xfer_wells.wells_driller_codes AS SELECT * FROM wells.wells_driller_codes;
CREATE TABLE xfer_wells.wells_errors AS SELECT * FROM wells.wells_errors;
CREATE TABLE xfer_wells.wells_ground_water_authrzation AS SELECT * FROM wells.wells_ground_water_authrzation;
CREATE TABLE xfer_wells.wells_legal_land_dist_codes AS SELECT * FROM wells.wells_legal_land_dist_codes;
CREATE TABLE xfer_wells.wells_lith_description_codes AS SELECT * FROM wells.wells_lith_description_codes;
CREATE TABLE xfer_wells.wells_lithology_colour_codes AS SELECT * FROM wells.wells_lithology_colour_codes;
CREATE TABLE xfer_wells.wells_lithology_descriptions AS SELECT * FROM wells.wells_lithology_descriptions;
CREATE TABLE xfer_wells.wells_lithology_material_codes AS SELECT * FROM wells.wells_lithology_material_codes;
CREATE TABLE xfer_wells.wells_location_accuracy_code AS SELECT * FROM wells.wells_location_accuracy_code;
CREATE TABLE xfer_wells.wells_owners AS SELECT * FROM wells.wells_owners;
CREATE TABLE xfer_wells.wells_perforations AS SELECT * FROM wells.wells_perforations;
CREATE TABLE xfer_wells.wells_production_data AS SELECT * FROM wells.wells_production_data;
CREATE TABLE xfer_wells.wells_screens AS SELECT * FROM wells.wells_screens;
CREATE TABLE xfer_wells.wells_sequences AS SELECT * FROM wells.wells_sequences;
CREATE TABLE xfer_wells.wells_temp_access AS SELECT * FROM wells.wells_temp_access;
CREATE TABLE xfer_wells.wells_temp_access_lithology AS SELECT * FROM wells.wells_temp_access_lithology;
CREATE TABLE xfer_wells.wells_use_codes AS SELECT * FROM wells.wells_use_codes;
CREATE TABLE xfer_wells.wells_utm_description AS SELECT * FROM wells.wells_utm_description;
CREATE TABLE xfer_wells.wells_utm_scale_codes AS SELECT * FROM wells.wells_utm_scale_codes;
CREATE TABLE xfer_wells.wells_watershed_codes AS SELECT * FROM wells.wells_watershed_codes;
CREATE TABLE xfer_wells.wells_well_licence AS SELECT * FROM wells.wells_well_licence;
CREATE TABLE xfer_wells.wells_wells AS SELECT * FROM wells.wells_wells;
CREATE TABLE xfer_wells.wells_yield_unit_codes AS SELECT * FROM wells.wells_yield_unit_codes;
EOF'

oc exec ${podname} -n moe-gwells-test -- /bin/bash -c 'mkdir -p /tmp/xfer;pg_dump -d $POSTGRESQL_DATABASE -Fc --no-privileges -no-tablespaces --schema=xfer_wells > /tmp/xfer/wells-legacy.$(date +"%m_%d_%Y").dmp'
oc exec ${podname} -n moe-gwells-test -- /bin/bash -c 'psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c "DROP SCHEMA xfer_wells cascade;"'


# Running on postgres database pod, as DB root access not enabled on gwells application pod
mkdir -p ~/tmp/xfer
oc rsync ${podname}:/tmp/xfer ~/tmp

# NOTE
#   psql -U postgres << EOF
# > drop database if exists wells;
# > create database wells;
# > drop user if exists wells;
# > create user wells;
# > alter user wells with encrypted password 'wells';
# > grant all privileges on database wells to wells;
# > \connect wells
# > create schema wells;
# > grant usage on schema wells to wells;
# > grant all privileges on schema wells to wells;
# > alter user wells set search_path to wells;
# > EOF

# Reset target schema on the local DB, to hold objects from pg_restore
psql -d wells -U wells << EOF
DROP SCHEMA IF EXISTS xfer_wells CASCADE;
EOF

pg_restore -d wells --v --no-owner --no-privileges -U wells ~/tmp/xfer/wells-legacy.$(date +"%m_%d_%Y").dmp

# Empty out FDW home schema
psql -d wells -U wells << EOF
DROP TABLE IF EXISTS wells.gw_aquifer_attrs               CASCADE;
DROP TABLE IF EXISTS wells.gw_aquifer_attrs_old           CASCADE;
DROP TABLE IF EXISTS wells.gw_aquifer_wells               CASCADE;
DROP TABLE IF EXISTS wells.gw_casing_material_codes       CASCADE;
DROP TABLE IF EXISTS wells.gw_class_of_well_codes         CASCADE;
DROP TABLE IF EXISTS wells.gw_class_subclass_xrefs        CASCADE;
DROP TABLE IF EXISTS wells.gw_closure_method_codes        CASCADE;
DROP TABLE IF EXISTS wells.gw_development_method_cds      CASCADE;
DROP TABLE IF EXISTS wells.gw_drilling_method_codes       CASCADE;
DROP TABLE IF EXISTS wells.gw_filter_pack_material_cds    CASCADE;
DROP TABLE IF EXISTS wells.gw_filter_pack_size_codes      CASCADE;
DROP TABLE IF EXISTS wells.gw_ground_elevaton_mthd_cds    CASCADE;
DROP TABLE IF EXISTS wells.gw_liner_material_codes        CASCADE;
DROP TABLE IF EXISTS wells.gw_nts_mapsheets               CASCADE;
DROP TABLE IF EXISTS wells.gw_orientation_of_well_cds     CASCADE;
DROP TABLE IF EXISTS wells.gw_province_state_codes        CASCADE;
DROP TABLE IF EXISTS wells.gw_relative_hardness_codes     CASCADE;
DROP TABLE IF EXISTS wells.gw_screen_assembly_type_cds    CASCADE;
DROP TABLE IF EXISTS wells.gw_screen_bottom_codes         CASCADE;
DROP TABLE IF EXISTS wells.gw_screen_intake_codes         CASCADE;
DROP TABLE IF EXISTS wells.gw_screen_material_codes       CASCADE;
DROP TABLE IF EXISTS wells.gw_screen_opening_codes        CASCADE;
DROP TABLE IF EXISTS wells.gw_screen_type_codes           CASCADE;
DROP TABLE IF EXISTS wells.gw_status_of_well_codes        CASCADE;
DROP TABLE IF EXISTS wells.gw_subclass_of_well_codes      CASCADE;
DROP TABLE IF EXISTS wells.gw_surface_seal_materil_cds    CASCADE;
DROP TABLE IF EXISTS wells.gw_surface_seal_method_cds     CASCADE;
DROP TABLE IF EXISTS wells.gw_utm_zone_codes              CASCADE;
DROP TABLE IF EXISTS wells.gw_water_qual_chrctrstc_cds    CASCADE;
DROP TABLE IF EXISTS wells.gw_well_water_quality_xrefs    CASCADE;
DROP TABLE IF EXISTS wells.gw_yield_estimated_mthd_cds    CASCADE;
DROP TABLE IF EXISTS wells.wells_acceptance_status_code   CASCADE;
DROP TABLE IF EXISTS wells.wells_aquifer_lithology_codes  CASCADE;
DROP TABLE IF EXISTS wells.wells_aquifer_subtype_codes    CASCADE;
DROP TABLE IF EXISTS wells.wells_bcgs_numbers             CASCADE;
DROP TABLE IF EXISTS wells.wells_casings                  CASCADE;
DROP TABLE IF EXISTS wells.wells_constant                 CASCADE;
DROP TABLE IF EXISTS wells.wells_constr_method_codes      CASCADE;
DROP TABLE IF EXISTS wells.wells_driller_codes            CASCADE;
DROP TABLE IF EXISTS wells.wells_errors                   CASCADE;
DROP TABLE IF EXISTS wells.wells_ground_water_authrzation CASCADE;
DROP TABLE IF EXISTS wells.wells_legal_land_dist_codes    CASCADE;
DROP TABLE IF EXISTS wells.wells_lith_description_codes   CASCADE;
DROP TABLE IF EXISTS wells.wells_lithology_colour_codes   CASCADE;
DROP TABLE IF EXISTS wells.wells_lithology_descriptions   CASCADE;
DROP TABLE IF EXISTS wells.wells_lithology_material_codes CASCADE;
DROP TABLE IF EXISTS wells.wells_location_accuracy_code   CASCADE;
DROP TABLE IF EXISTS wells.wells_owners                   CASCADE;
DROP TABLE IF EXISTS wells.wells_perforations             CASCADE;
DROP TABLE IF EXISTS wells.wells_production_data          CASCADE;
DROP TABLE IF EXISTS wells.wells_screens                  CASCADE;
DROP TABLE IF EXISTS wells.wells_sequences                CASCADE;
DROP TABLE IF EXISTS wells.wells_temp_access              CASCADE;
DROP TABLE IF EXISTS wells.wells_temp_access_lithology    CASCADE;
DROP TABLE IF EXISTS wells.wells_use_codes                CASCADE;
DROP TABLE IF EXISTS wells.wells_utm_description          CASCADE;
DROP TABLE IF EXISTS wells.wells_utm_scale_codes          CASCADE;
DROP TABLE IF EXISTS wells.wells_watershed_codes          CASCADE;
DROP TABLE IF EXISTS wells.wells_well_licence             CASCADE;
DROP TABLE IF EXISTS wells.wells_wells                    CASCADE;
DROP TABLE IF EXISTS wells.wells_yield_unit_codes         CASCADE;
EOF


psql -d wells -U wells << EOF
ALTER TABLE xfer_wells.gw_aquifer_attrs SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_aquifer_attrs_old SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_aquifer_wells SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_casing_material_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_class_of_well_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_class_subclass_xrefs SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_closure_method_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_development_method_cds SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_drilling_method_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_filter_pack_material_cds SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_filter_pack_size_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_ground_elevaton_mthd_cds SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_liner_material_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_nts_mapsheets SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_orientation_of_well_cds SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_province_state_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_relative_hardness_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_screen_assembly_type_cds SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_screen_bottom_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_screen_intake_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_screen_material_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_screen_opening_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_screen_type_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_status_of_well_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_subclass_of_well_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_surface_seal_materil_cds SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_surface_seal_method_cds SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_utm_zone_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_water_qual_chrctrstc_cds SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_well_water_quality_xrefs SET SCHEMA wells;
ALTER TABLE xfer_wells.gw_yield_estimated_mthd_cds SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_acceptance_status_code SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_aquifer_lithology_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_aquifer_subtype_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_bcgs_numbers SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_casings SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_constant SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_constr_method_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_driller_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_errors SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_ground_water_authrzation SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_legal_land_dist_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_lith_description_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_lithology_colour_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_lithology_descriptions SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_lithology_material_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_location_accuracy_code SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_owners SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_perforations SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_production_data SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_screens SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_sequences SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_temp_access SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_temp_access_lithology SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_use_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_utm_description SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_utm_scale_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_watershed_codes SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_well_licence SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_wells SET SCHEMA wells;
ALTER TABLE xfer_wells.wells_yield_unit_codes SET SCHEMA wells;
CREATE UNIQUE INDEX well_tag_number_idx on wells_wells (well_tag_number);
EOF

# NOTE
# psql -d gwells -U postgres << EOF
# create extension if not exists postgres_fdw;
# drop server if exists wells cascade;
# create server wells foreign data wrapper postgres_fdw options (host 'localhost', dbname 'wells');
# drop user mapping if exists for public server wells;
# create user mapping for public server wells options (user 'wells', password 'wells');
# import foreign schema wells from server wells into wells;
# grant usage on schema wells to gwells;
# grant select on all tables in schema wells to public;
# grant usage on foreign server wells to gwells;
#  EOF

# To verify that the fdw is set up correctly and visible from gwells 
psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c "\d wells.*"


