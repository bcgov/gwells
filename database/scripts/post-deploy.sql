/* Additional updaates to DB stucture, as Python's model.py has limited abilities to do this */
DROP INDEX IF EXISTS gwells_well_latlong CASCADE;
CREATE INDEX gwells_well_latlong ON gwells_well (latitude, longitude);

COMMENT ON TABLE gwells_activity_submission               IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_activity_submission_water_quality IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_aquifer_well                      IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_bcgs_number                       IS 'Placeholder table comment.';
COMMENT ON TABLE bedrock_material_code                  IS 'Placeholder table comment.';
COMMENT ON TABLE bedrock_material_descriptor_code       IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_casing                            IS 'Placeholder table comment.';
COMMENT ON TABLE casing_material_code                   IS 'Placeholder table comment.';
COMMENT ON TABLE casing_code                       IS 'Placeholder table comment.';
COMMENT ON TABLE decommission_method_code               IS 'Placeholder table comment.';
COMMENT ON TABLE development_method_code                IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_driller                           IS 'Placeholder table comment.';
COMMENT ON TABLE drilling_company                  IS 'Placeholder table comment.';
COMMENT ON TABLE drilling_method_code                   IS 'Placeholder table comment.';
COMMENT ON TABLE filter_pack_material_code              IS 'Placeholder table comment.';
COMMENT ON TABLE filter_pack_material_size_code         IS 'Placeholder table comment.';
COMMENT ON TABLE ground_elevation_method_code           IS 'Placeholder table comment.';
COMMENT ON TABLE intended_water_use_code                IS 'Placeholder table comment.';
COMMENT ON TABLE land_district_code                     IS 'Placeholder table comment.';
COMMENT ON TABLE licenced_status_code                   IS 'Placeholder table comment.';
COMMENT ON TABLE liner_material_code                    IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_liner_perforation                 IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_colour_code                  IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_lithology_description             IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_lithology_description_code        IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_hardness_code                IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_material_code                IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_moisture_code                IS 'Placeholder table comment.';
COMMENT ON TABLE lithology_structure_code               IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_ltsa_owner                        IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_perforation                       IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_production_data                   IS 'Placeholder table comment.';
COMMENT ON TABLE province_state_code                    IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_screen                            IS 'Placeholder table comment.';
COMMENT ON TABLE screen_assembly_type_code              IS 'Placeholder table comment.';
COMMENT ON TABLE screen_bottom_code                     IS 'Placeholder table comment.';
COMMENT ON TABLE screen_intake_method_code              IS 'Placeholder table comment.';
COMMENT ON TABLE screen_material_code                   IS 'Placeholder table comment.';
COMMENT ON TABLE screen_opening_code                    IS 'Placeholder table comment.';
COMMENT ON TABLE screen_type_code                       IS 'Placeholder table comment.';
COMMENT ON TABLE surface_seal_material_code             IS 'Placeholder table comment.';
COMMENT ON TABLE surface_seal_method_code               IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_surficial_material                IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_water_quality_characteristic      IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_well                              IS 'Placeholder table comment.';
COMMENT ON TABLE well_activity_code                IS 'Placeholder table comment.';
COMMENT ON TABLE well_class_code                        IS 'Placeholder table comment.';
COMMENT ON TABLE well_status_code                       IS 'Placeholder table comment.';
COMMENT ON TABLE well_subclass_code                     IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_well_water_quality                IS 'Placeholder table comment.';
COMMENT ON TABLE well_yield_unit_code                   IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_yield_estimation_method           IS 'Placeholder table comment.';

