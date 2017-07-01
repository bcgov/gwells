/* Delete all rows from Submission Ready tables */

truncate gwells_activity_submission restart identity cascade;
truncate gwells_driller             restart identity cascade;
truncate gwells_drilling_company    restart identity cascade;
truncate gwells_drilling_method     restart identity cascade;
truncate gwells_ground_elevation_method restart identity cascade;
truncate gwells_intended_water_use  restart identity cascade;
truncate gwells_land_district       restart identity cascade;
truncate gwells_ltsa_owner          restart identity cascade;
truncate gwells_province_state      restart identity cascade;
truncate gwells_well                restart identity cascade;
truncate gwells_well_activity_type  restart identity cascade;
truncate gwells_well_class          restart identity cascade;
truncate gwells_well_subclass       restart identity cascade;
truncate gwells_well_yield_unit     restart identity cascade;

/* Delete all rows from temporary transformation tables */
truncate xform_gwells_land_district    restart identity cascade;
truncate xform_gwells_well             restart identity cascade;
truncate xform_gwells_driller          restart identity cascade;
truncate xform_gwells_drilling_company restart identity cascade;
