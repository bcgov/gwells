/* Delete all rows from Submission Ready tables */

truncate activity_submission restart identity cascade;
truncate bedrock_material restart identity cascade;
truncate bedrock_material_descriptor restart identity cascade;
truncate casing restart identity cascade;
truncate casing_material restart identity cascade;
truncate casing_type restart identity cascade;
truncate driller             restart identity cascade;
truncate drilling_company    restart identity cascade;
truncate drilling_method     restart identity cascade;
truncate ground_elevation_method restart identity cascade;
truncate intended_water_use  restart identity cascade;
truncate land_district       restart identity cascade;
truncate lithology_colour restart identity cascade;
truncate lithology_hardness restart identity cascade;
truncate lithology_moisture restart identity cascade;
truncate lithology_structure restart identity cascade;
truncate ltsa_owner          restart identity cascade;
truncate province_state      restart identity cascade;
truncate surface_seal_material restart identity cascade;
truncate surface_seal_method restart identity cascade;
truncate surficial_material restart identity cascade;
truncate well                restart identity cascade;
truncate well_activity_type  restart identity cascade;
truncate well_class          restart identity cascade;
truncate well_subclass       restart identity cascade;
truncate well_yield_unit     restart identity cascade;

truncate screen_type               restart identity cascade;   
truncate screen_intake             restart identity cascade;
truncate screen_opening            restart identity cascade;
truncate screen_bottom             restart identity cascade;
truncate screen_material           restart identity cascade;
truncate liner_material            restart identity cascade;
truncate filter_pack_material      restart identity cascade;
truncate filter_pack_material_size restart identity cascade;

truncate screen_assembly_type     restart identity cascade;
truncate development_method       restart identity cascade;
truncate yield_estimation_method  restart identity cascade;

/* Drop all temporary transformation tables */
drop table xform_gwells_land_district cascade;
drop table xform_gwells_well             cascade;
drop table xform_gwells_driller          cascade;
drop table xform_gwells_drilling_company cascade;
drop table xform_gwells_surface_seal_material cascade;
drop table xform_gwells_surface_seal_method cascade;
/* drop table xform_gwells_backfill_type cascade; */
