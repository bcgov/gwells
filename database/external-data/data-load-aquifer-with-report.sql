\echo '... loading gwells_aquifer_has table'

CREATE TABLE IF NOT EXISTS gwells_aquifer_has_report( --Create temp table with aquifers that have reports
  aquifer_id     integer
);

\copy gwells_aquifer_has_report (aquifer_id) from './AquiferWithDescription.csv' with header delimiter ',' CSV

UPDATE gwells_aquifer_well
SET aquifer_has_report = True
FROM gwells_aquifer_has_report
WHERE gwells_aquifer_well.aquifer_id = gwells_aquifer_has_report.aquifer_id;

UPDATE gwells_aquifer_well
SET aquifer_has_report = False
WHERE aquifer_has_report IS NULL;

DROP TABLE IF EXISTS gwells_aquifer_has_report;
