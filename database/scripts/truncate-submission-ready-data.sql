/* Delete all rows from Submission Ready tables */

truncate gwells_activity_submission restart identity cascade;
truncate gwells_bedrock_material restart identity cascade;
truncate gwells_bedrock_material_descriptor restart identity cascade;
truncate gwells_casing restart identity cascade;
truncate gwells_casing_material restart identity cascade;
truncate gwells_casing_type restart identity cascade;
truncate gwells_driller             restart identity cascade;
truncate gwells_drilling_company    restart identity cascade;
truncate gwells_drilling_method     restart identity cascade;
truncate gwells_ground_elevation_method restart identity cascade;
truncate gwells_intended_water_use  restart identity cascade;
truncate gwells_land_district       restart identity cascade;
truncate gwells_lithology_colour restart identity cascade;
truncate gwells_lithology_hardness restart identity cascade;
truncate gwells_lithology_moisture restart identity cascade;
truncate gwells_lithology_structure restart identity cascade;
truncate gwells_ltsa_owner          restart identity cascade;
truncate gwells_province_state      restart identity cascade;
truncate gwells_surface_seal_material restart identity cascade;
truncate gwells_surface_seal_method restart identity cascade;
truncate gwells_surficial_material restart identity cascade;
truncate gwells_well                restart identity cascade;
truncate gwells_well_activity_type  restart identity cascade;
truncate gwells_well_class          restart identity cascade;
truncate gwells_well_subclass       restart identity cascade;
truncate gwells_well_yield_unit     restart identity cascade;

truncate gwells_screen_type               restart identity cascade;   
truncate gwells_screen_intake             restart identity cascade;
truncate gwells_screen_opening            restart identity cascade;
truncate gwells_screen_bottom             restart identity cascade;
truncate gwells_screen_material           restart identity cascade;
truncate gwells_liner_material            restart identity cascade;
truncate gwells_filter_pack_material      restart identity cascade;
truncate gwells_filter_pack_material_size restart identity cascade;

truncate gwells_screen_assembly_type     restart identity cascade;
truncate gwells_development_method       restart identity cascade;
truncate gwells_yield_estimation_method  restart identity cascade;

/* Drop all temporary transformation tables */
drop table xform_gwells_land_district cascade;
drop table xform_gwells_well             cascade;
drop table xform_gwells_driller          cascade;
drop table xform_gwells_drilling_company cascade;
drop table xform_gwells_surface_seal_material cascade;
drop table xform_gwells_surface_seal_method cascade;
/* drop table xform_gwells_backfill_type cascade; */
