-- @Aquifers
--
-- Aquifers app (Aquifers, and associations to Wells, and Hydraulic Properties from tests on
-- the aquifer at the point of the well)
--   
-- Loading the temporary mapping of wells <-> aquifers is done via
--   cd app/database/scripts/aquifers/
--   psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER << EOF
--   \copy xform_aquifers FROM 'xforms-aquifers.csv' HEADER DELIMITER ',' CSV
--   EOF
--
-- Output should be: COPY 1195
--
--
\echo 'Creating Aquifers app tables...'

DROP TABLE IF EXISTS xform_aquifers;
CREATE unlogged TABLE IF NOT EXISTS xform_aquifers (
 aquifer_id integer
,mapping_year integer
);

\echo 'Finished creating Aquifers app tables...'

