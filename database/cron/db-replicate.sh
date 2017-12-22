#!/bin/sh
#
# Mon Nov  6 15:03:49 2017 GW Shell script run by 'oc exec' on OpenShift
#   initiated by Jenkins job, which connects to the application server
#   pod (gwells-nn-xxxxx which is STATUS = 'Running'):
#      oc exec gwells-nnn-xxxx $VIRTUAL_ENV/src/database/cron/db-replicate.sh
#
#   This deploy is triggered only on the PROD envionments  (moe-gwells-prod)
#
#   Example: oc exec gwells-97-69b7z /opt/app-root/src/database/cron/db-replicate.sh
#
export PGPASSWORD=$DATABASE_PASSWORD

cd /opt/app-root/src/database/code-tables/
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
\i clear-tables.sql
vacuum;
\i data-load-static-codes.sql
EOF

# FILTER is applied in /opt/app-root/src/database/scripts/populate-xform-gwells-well.sql
# at the end of the SQL WHERE clause
if [ "$LIMIT_ROWS_DB_REPLICATION" = "True" ]
then
  echo ". Limiting rows replicated from Legacy Database, per LIMIT_ROWS_DB_REPLICATION flag"
  FILTER="AND wells.well_tag_number between 100001 and 113567 " 
else
  echo ". All rows replicated from Legacy Database"
  FILTER=""
fi

# Separating into three steps, to avoid DB error
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -v xform_filter="$FILTER" << EOF
\set AUTOCOMMIT off
\ir ../scripts/create-xform-gwells-well-ETL-table.sql
\ir ../scripts/populate-xform-gwells-well.sql
\ir ../scripts/migrate_bcgs.sql
\ir ../scripts/populate-gwells-well-from-xform.sql
COMMIT;
EOF

psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
\set AUTOCOMMIT off
\ir ../scripts/migrate_screens.sql
\ir ../scripts/migrate_production_data.sql
COMMIT;
EOF

psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
\set AUTOCOMMIT off
\ir ../scripts/migrate_casings.sql
\ir ../scripts/migrate_perforations.sql
\ir ../scripts/migrate_aquifer_wells.sql
COMMIT;
EOF


psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
\set AUTOCOMMIT off
\ir ../scripts/migrate_lithology_descriptions.sql
DROP TABLE IF EXISTS xform_gwells_well;
COMMIT;
EOF

exit 0
