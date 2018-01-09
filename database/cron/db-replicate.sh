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

if [ "$DB_REPLICATE" = "Subset" ]
then
	echo "... Limiting replication to a subset of Legacy Database, per DB_REPLICATE flag"
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -c 'SELECT gwells_populate_xform(true);'
elif [ "$DB_REPLICATE" = "Full" ]
then
  	echo "... All rows replicated from Legacy Database"
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -c 'SELECT gwells_populate_xform(false);'
else 	
  	echo "... ERROR Unrecognized DB_REPLICATE option - XFORM table is empty."
  	exit 1
fi

psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
	\set AUTOCOMMIT off
	\echo '... clearing gwells_bcgs_number'
	TRUNCATE TABLE gwells_bcgs_number CASCADE;	
	SELECT gwells_migrate_bcgs();
	COMMIT;	
EOF

# Breaking out the long transaction into parts for performance reasons
# Thu Dec 28 15:17:55 2017 GW Until we merge into one DB stored function gwells_replicate(boolean), add
#                             new migrates here and to ./database/scripts/full_db_replication.sql
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
	\set AUTOCOMMIT off
	SELECT gwells_populate_well();	
	SELECT gwells_migrate_screens();
	SELECT gwells_migrate_production();
	SELECT gwells_migrate_casings();
	SELECT gwells_migrate_perforations();
	SELECT gwells_migrate_aquifers();
	SELECT gwells_migrate_lithology();
	DROP TABLE IF EXISTS xform_gwells_well;
	COMMIT;
EOF

exit 0
