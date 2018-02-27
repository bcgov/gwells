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

if [ "$DB_REPLICATE" = "Subset" ]
then
	echo "... Limiting replication to a subset of Legacy Database, per DB_REPLICATE flag"
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -c 'SELECT gwells_db_replicate(true);'
elif [ "$DB_REPLICATE" = "Full" ]
then
  	echo "... All rows replicated from Legacy Database"
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -c 'SELECT gwells_db_replicate(false);'
else 	
  	echo "... ERROR Unrecognized DB_REPLICATE option - XFORM table is now empty."
  	exit 1
fi

exit 0
