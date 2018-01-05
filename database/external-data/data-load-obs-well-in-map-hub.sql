\echo '... loading gwells_available_obswell table'

CREATE TABLE IF NOT EXISTS gwells_available_obswell( --Create temp table with obswells that are in maphub
  obswellcode     character varying(3)
);

\copy gwells_available_obswell (obswellcode) from './featuresActiveReduced.csv' with header delimiter ',' CSV
\copy gwells_available_obswell (obswellcode) from './featuresInactiveReduced.csv' with header delimiter ',' CSV

UPDATE gwells_well
SET observation_well_in_map_hub = True
FROM gwells_available_obswell
WHERE observation_well_number = obswellcode;

UPDATE gwells_well
SET observation_well_in_map_hub = False
WHERE observation_well_in_map_hub IS NULL;

DROP TABLE IF EXISTS gwells_available_obswell;
