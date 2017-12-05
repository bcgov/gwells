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
export PGPASSWORD=$DATABASE_PASSWORD &&
cd /opt/app-root/src/database/code-tables/ &&

psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f clear-tables.sql &&

for table in $(psql -U postgres --tuples-only -c "SELECT schemaname || '.'
|| tablename FROM pg_tables WHERE tablename NOT IN ('pg_tablespace', 'pg_auth_members', 'pg_pltemplate', 'pg_shdescription', 'pg_shdescription', 'pg_replication_origin', 'pg_db_role_setting', 'pg_db_role_setting', 'pg_authid', 'pg_database', 'pg_shdepend', 'pg_shseclabel')") ;
do psql -U postgres -c "VACUUM ANALYZE $table"; done &&

psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f  data-load-static-codes.sql &&

sleep 30 &&

cd /opt/app-root/src/database/scripts/ &&

psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f create-xform-gwells-well-ETL-table.sql &&
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f populate-xform-gwells-well.sql &&
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f populate-gwells-well-from-xform.sql &&
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f migrate_screens.sql &&
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f migrate_production_data.sql &&
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f migrate_casings.sql &&
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f migrate_perforations.sql &&
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f migrate_aquifer_wells.sql &&
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -f migrate_lithology_descriptions.sql &&
exit 0
