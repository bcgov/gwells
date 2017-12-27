/* Additional updaates to DB stucture, as Python's model.py has limited abilities to do this */
DROP INDEX IF EXISTS gwells_well_latlong CASCADE;
CREATE INDEX gwells_well_latlong ON gwells_well (latitude, longitude);

COMMENT ON TABLE gwells_activity_submission               IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_activity_submission_water_quality IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_aquifer_well                      IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_bcgs_number                       IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_bedrock_material                  IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_bedrock_material_descriptor       IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_casing                            IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_casing_material                   IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_casing_type                       IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_decommission_method               IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_development_method                IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_driller                           IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_drilling_company                  IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_drilling_method                   IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_filter_pack_material              IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_filter_pack_material_size         IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_ground_elevation_method           IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_intended_water_use                IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_land_district                     IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_licenced_status                   IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_liner_material                    IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_liner_perforation                 IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_lithology_colour                  IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_lithology_description             IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_lithology_description_code        IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_lithology_hardness                IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_lithology_material                IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_lithology_moisture                IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_lithology_structure               IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_ltsa_owner                        IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_perforation                       IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_production_data                   IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_province_state                    IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_screen                            IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_screen_assembly_type              IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_screen_bottom                     IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_screen_intake_method              IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_screen_material                   IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_screen_opening                    IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_screen_type                       IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_surface_seal_material             IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_surface_seal_method               IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_surficial_material                IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_water_quality_characteristic      IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_well                              IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_well_activity_type                IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_well_class                        IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_well_status                       IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_well_subclass                     IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_well_water_quality                IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_well_yield_unit                   IS 'Placeholder table comment.';
COMMENT ON TABLE gwells_yield_estimation_method           IS 'Placeholder table comment.';


/* COMMENT ON FUNCTION my_function (timestamp) IS 'Returns Roman Numeral'; */
