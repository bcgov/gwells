/* Additional updates to DB stucture, as Python's model.py has limited abilities to do this */

DROP INDEX IF EXISTS bcgs_number_idx CASCADE;
CREATE INDEX bcgs_number_idx ON bcgs_number (bcgs_number);

COMMENT ON TABLE reversion_revision IS 'ASK DEVELOPERS to describe this table';
COMMENT ON TABLE reversion_version IS 'ASK DEVELOPERS to describe this table';
COMMENT ON TABLE xform_aquifers IS 'ASK DEVELOPERS TO DELETE THIS TABLE';


ALTER TABLE bedrock_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE bedrock_material_descriptor_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE casing_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE casing_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE decommission_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE development_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE drilling_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE filter_pack_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE filter_pack_material_size_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE ground_elevation_method_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE intended_water_use_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE land_district_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE licenced_status_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE liner_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_colour_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_description_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_hardness_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_material_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_moisture_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE lithology_structure_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;
ALTER TABLE obs_well_status_code ALTER COLUMN effective_date SET DEFAULT CURRENT_DATE;


COMMENT ON COLUMN reversion_revision.date_created IS 'Date and time (UTC) when the physical record was created in the database.';


-- Thu  1 Mar 20:00:30 2018 GW Django doesn't support multi-column PK's
ALTER TABLE well_subclass_code DROP CONSTRAINT IF EXISTS well_subclass_code_uk CASCADE;
ALTER TABLE well_subclass_code ADD CONSTRAINT well_subclass_code_uk UNIQUE (well_class_code, well_subclass_code);
