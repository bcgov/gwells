#!/bin/sh
#
# Mon Nov  6 15:03:49 2017 GW Shell script run by 'oc exec' on OpenShift
#   initiated by Jenkins job, which connects to the application server
#   pod (gwells-nn-xxxxx which is STATUS = 'Running'):
#      oc exec gwells-nnn-xxxx $VIRTUAL_ENV/src/database/cron/db-replicate.sh
#
#   This deploy is triggered only on the PROD envionments (moe-gwells-prod), or
#   on local Developer workstations (unit testing).
#
#   Example: oc exec gwells-97-69b7z /opt/app-root/src/database/cron/db-replicate.sh
#
#   If run on local Developer workstation, ensure that you have Environment variables set
#   for $DATABASE_SERVICE_NAME, $DATABASE_PASSWORD, $DATABASE_NAME, $DATABASE_USER,
#   $DB_REPLICATE (None|Subset|Full)
#
#   Example: ./db-replicate.sh
#    
export PGPASSWORD=$DATABASE_PASSWORD


# TODO GW - replace below, leveraging new IN boolean parameter for gwells_db_replicate()
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
#                             new migrate steps here and to ./database/scripts/db_replicate.sql
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
	\set AUTOCOMMIT off
	TRUNCATE TABLE gwells_well CASCADE;
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
