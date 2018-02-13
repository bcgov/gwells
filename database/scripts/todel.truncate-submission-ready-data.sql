/* Delete all rows from Submission Ready tables */

TRUNCATE activity_submission RESTART IDENTITY CASCADE;
TRUNCATE bedrock_material RESTART IDENTITY CASCADE;
TRUNCATE bedrock_material_descriptor RESTART IDENTITY CASCADE;
TRUNCATE casing restart IDENTITY CASCADE;
TRUNCATE casing_material RESTART IDENTITY CASCADE;
TRUNCATE casing_code RESTART IDENTITY CASCADE;
TRUNCATE driller             RESTART IDENTITY CASCADE;
TRUNCATE drilling_company    RESTART IDENTITY CASCADE;
TRUNCATE drilling_method     RESTART IDENTITY CASCADE;
TRUNCATE ground_elevation_method RESTART IDENTITY CASCADE;
TRUNCATE intended_water_use  RESTART IDENTITY CASCADE;
TRUNCATE land_district       RESTART IDENTITY CASCADE;
TRUNCATE lithology_colour RESTART IDENTITY CASCADE;
TRUNCATE lithology_hardness RESTART IDENTITY CASCADE;
TRUNCATE lithology_moisture RESTART IDENTITY CASCADE;
TRUNCATE lithology_structure RESTART IDENTITY CASCADE;
TRUNCATE ltsa_owner          RESTART IDENTITY CASCADE;
TRUNCATE province_state      RESTART IDENTITY CASCADE;
TRUNCATE surface_seal_material restart identity cascade;
TRUNCATE surface_seal_method RESTART IDENTITY CASCADE;
TRUNCATE surficial_material  RESTART IDENTITY CASCADE;
TRUNCATE well                RESTART IDENTITY CASCADE;
TRUNCATE well_activity_type  RESTART IDENTITY CASCADE;
TRUNCATE well_class          RESTART IDENTITY CASCADE;
TRUNCATE well_subclass       RESTART IDENTITY CASCADE;
TRUNCATE well_yield_unit     RESTART IDENTITY CASCADE;

TRUNCATE screen_type               RESTART IDENTITY CASCADE;   
TRUNCATE screen_intake             RESTART IDENTITY CASCADE;
TRUNCATE screen_opening            RESTART IDENTITY CASCADE;
TRUNCATE screen_bottom             RESTART IDENTITY CASCADE;
TRUNCATE screen_material           RESTART IDENTITY CASCADE;
TRUNCATE liner_material            RESTART IDENTITY CASCADE;
TRUNCATE filter_pack_material      RESTART IDENTITY CASCADE;
TRUNCATE filter_pack_material_size RESTART IDENTITY CASCADE;

TRUNCATE screen_assembly_type     RESTART IDENTITY CASCADE;
TRUNCATE development_method       RESTART IDENTITY CASCADE;
TRUNCATE yield_estimation_method  RESTART IDENTITY CASCADE;

/* Drop all temporary transformation tables */
DROP TABLE IF EXISTS xform_land_district_code         CASCADE;
DROP TABLE IF EXISTS xform_gwells_well                  CASCADE;
DROP TABLE IF EXISTS xform_gwells_driller               CASCADE;
DROP TABLE IF EXISTS xform_gwells_drilling_company      CASCADE;
DROP TABLE IF EXISTS xform_surface_seal_material_code CASCADE;
DROP TABLE IF EXISTS xform_surface_seal_method_code   CASCADE;
/* drop table xform_gwells_backfill_type cascade; */
