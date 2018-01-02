#!/bin/sh
#
# Mon Nov  6 15:03:49 2017 GW Shell script run by 'oc exec' on OpenShift
#   initiated by Jenkins job, which connects to the application server 
#   pod (gwells-nn-xxxxx which is STATUS = 'Running'):
#      oc exec gwells-nnn-xxxx $VIRTUAL_ENV/src/database/cron/post-deploy.sh
#
#   This deploy is triggered on all three envionments (moe-gwells-dev,
#   moe-gwells-test, moe-gwells-prod)
#
#   Example: oc exec gwells-97-69b7z /opt/app-root/src/database/cron/post-deploy.sh
#
echo "Running Post-Deploy tasks..."
export PGPASSWORD=$DATABASE_PASSWORD
cd /opt/app-root/src/database/scripts/
echo ". Creating additional DB objects (e.g. spatial indices, stored functions)"
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
	\i post-deploy.sql
	\i populate-xform-gwells-well.sql
	\i migrate_bcgs.sql
	\i populate-gwells-well-from-xform.sql
	\i migrate_screens.sql
	\i migrate_production_data.sql
	\i migrate_casings.sql	
	\i migrate_perforations.sql
	\i migrate_aquifer_wells.sql	
	\i migrate_lithology_descriptions.sql
	\i full_db_replication.sql
EOF

# $DB_REPLICATE can be one of "None" | "Subset" | "Full" 
if [ "$DB_REPLICATE" = "Subset" -o "$DB_REPLICATE" = "Full" ]
then
	# COPY statements in data-load-static-codes.sql requuire to be in this directory
	cd /opt/app-root/src/database/code-tables/

	# Refresh Code lookup tables, including the gwells_well table
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
	\i clear-tables.sql
	\i data-load-static-codes.sql
EOF
	echo ". Running DB Replication from Legacy Database, as per DB_REPLICATION flag"
    cd /opt/app-root/src/database/cron/
    ./db-replicate.sh
else
    echo ". Skipping DB Replication from Legacy Database, as per DB_REPLICATION flag"
fi 

echo "Completed Post-Deploy tasks."
