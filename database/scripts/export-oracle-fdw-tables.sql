create table ora_wells_constr_method_codes as table wells.wells_constr_method_codes;
create table ora_wells_legal_land_dist_codes as table wells.wells_legal_land_dist_codes;
create table ora_wells_driller_codes as table wells.wells_driller_codes;
create table ora_wells_aquifer_lithology_codes as table wells.wells_aquifer_lithology_codes;
create table ora_wells_location_accuracy_code as table wells.wells_location_accuracy_code;
create table ora_wells_bcgs_numbers as table wells.wells_bcgs_numbers;
create table ora_wells_owners as table wells.wells_owners;
create table ora_wells_use_codes as table wells.wells_use_codes;
create table ora_wells_utm_scale_codes as table wells.wells_utm_scale_codes;create table ora_wells_acceptance_status_code as table wells.wells_acceptance_status_code;
create table ora_gw_closure_method_codes as table wells.gw_closure_method_codes;
create table ora_gw_subclass_of_well_codes as table wells.gw_subclass_of_well_codes;
create table ora_gw_class_of_well_codes as table wells.gw_class_of_well_codes;
create table ora_gw_class_subclass_xrefs as table wells.gw_class_subclass_xrefs;
create table ora_gw_drilling_method_codes as table wells.gw_drilling_method_codes;
create table ora_gw_development_method_cds as table wells.gw_development_method_cds;
create table ora_gw_filter_pack_material_cds as table wells.gw_filter_pack_material_cds;
create table ora_gw_filter_pack_size_codes as table wells.gw_filter_pack_size_codes;
create table ora_gw_ground_elevaton_mthd_cds as table wells.gw_ground_elevaton_mthd_cds;
create table ora_gw_liner_material_codes as table wells.gw_liner_material_codes;
create table ora_gw_orientation_of_well_cds as table wells.gw_orientation_of_well_cds;
create table ora_gw_screen_bottom_codes as table wells.gw_screen_bottom_codes;
create table ora_gw_screen_intake_codes as table wells.gw_screen_intake_codes;
create table ora_gw_screen_material_codes as table wells.gw_screen_material_codes;
create table ora_gw_screen_opening_codes as table wells.gw_screen_opening_codes;
create table ora_gw_surface_seal_materil_cds as table wells.gw_surface_seal_materil_cds;
create table ora_gw_surface_seal_method_cds as table wells.gw_surface_seal_method_cds;
create table ora_gw_screen_type_codes as table wells.gw_screen_type_codes;
create table ora_gw_status_of_well_codes as table wells.gw_status_of_well_codes;
create table ora_gw_utm_zone_codes as table wells.gw_utm_zone_codes;
create table ora_wells_watershed_codes as table wells.wells_watershed_codes;
create table ora_wells_yield_unit_codes as table wells.wells_yield_unit_codes;
create table ora_wells_screens as table wells.wells_screens;
create table ora_gw_aquifer_attrs as table wells.gw_aquifer_attrs;
create table ora_gw_aquifer_wells as table wells.gw_aquifer_wells;
create table ora_wells_casings as table wells.wells_casings;
create table ora_gw_aquifer_attrs_old as table wells.gw_aquifer_attrs_old;
create table ora_wells_production_data as table wells.wells_production_data;
create table ora_wells_well_licence as table wells.wells_well_licence;
create table ora_wells_perforations as table wells.wells_perforations;
create table ora_wells_sequences as table wells.wells_sequences;
create table ora_gw_water_qual_chrctrstc_cds as table wells.gw_water_qual_chrctrstc_cds;
create table ora_wells_temp_access as table wells.wells_temp_access;
create table ora_gw_yield_estimated_mthd_cds as table wells.gw_yield_estimated_mthd_cds;
create table ora_wells_lithology_colour_codes as table wells.wells_lithology_colour_codes;

-- See https://stackoverflow.com/questions/1347646/postgres-error-on-insert-error-invalid-byte-sequence-for-encoding-utf8-0x0
-- create table ora_wells_lithology_descriptions as table wells.wells_lithology_descriptions;

create table ora_wells_lithology_material_codes as table wells.wells_lithology_material_codes;
create table ora_gw_nts_mapsheets as table wells.gw_nts_mapsheets;

create table ora_gw_screen_assembly_type_cds as table wells.gw_screen_assembly_type_cds;
create table ora_gw_casing_material_codes as table wells.gw_casing_material_codes;
create table ora_gw_province_state_codes as table wells.gw_province_state_codes;
create table ora_gw_relative_hardness_codes as table wells.gw_relative_hardness_codes;

create table ora_gw_well_water_quality_xrefs as table wells.gw_well_water_quality_xrefs;
create table ora_wells_aquifer_subtype_codes as table wells.wells_aquifer_subtype_codes;
create table ora_wells_lith_description_codes as table wells.wells_lith_description_codes;
create table ora_wells_errors as table wells.wells_errors;
create table ora_wells_ground_water_authrzation as table wells.wells_ground_water_authrzation;
create table ora_wells_constant as table wells.wells_constant;

create table ora_wells_temp_access_lithology as table wells.wells_temp_access_lithology;
create table ora_wells_utm_description as table wells.wells_utm_description;
create table ora_wells_temp_access_contractors as table wells.wells_temp_access_contractors;
create table ora_wells_wells as table wells.wells_wells;

-- pg_dump -d gwells -U userGN0 -Fc --table=ora_*  --no-privileges --no-tablespaces > gwells-oracle.dmp 
