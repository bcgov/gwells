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
#   If run on local Developer workstation, ensure that you have Environment variables set
#   for $DATABASE_SERVICE_NAME, $DATABASE_PASSWORD, $DATABASE_NAME, $DATABASE_USER
#
#   Optionally, set $DB_REPLICATE (None|Subset|Full).
#
#   Example: ./post-deploy.sh
#    
echo "Running Post-Deploy tasks..."
export PGPASSWORD=$DATABASE_PASSWORD
cd /opt/app-root/src/database/scripts/
echo ". Creating additional DB objects (e.g. spatial indices, stored functions)"
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
	\i post-deploy.sql
	\i populate-xform-gwells-well.sql
	\i replicate_bcgs.sql
	\i populate-gwells-well-from-xform.sql
	\i replicate_screens.sql
	\i replicate_production_data.sql
	\i replicate_casings.sql
	\i replicate_perforations.sql
	\i replicate_aquifer_wells.sql
	\i replicate_lithology_descriptions.sql
	\i full_db_replication.sql
	\i db_replicate.sql
EOF
# TODO delete the "\i full_db_replication.sql" once db_replicate.sql is tested
# and the Jenkins job is reconfigured from:
# 'psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c "SELECT gwells_full_replicate();"'
#
# to:
# 'psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c "SELECT gwells_db_replicate(false);"'
#
# https://jenkins-moe-gwells-tools.pathfinder.gov.bc.ca/job/gwells-prod-db-scripts/configure

# $DB_REPLICATE can be one of "None" | "Subset" | "Full"
if [ "$DB_REPLICATE" = "Subset" -o "$DB_REPLICATE" = "Full" ]
then
	# \copy statements in data-load-static-codes.sql required to be in this directory
	cd /opt/app-root/src/database/code-tables/

	# Refresh Code lookup tables, including the gwells_well table
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
	\i clear-tables.sql
	\i data-load-static-codes.sql
EOF

	echo ". Running DB Replication from Legacy Database, as per DB_REPLICATION flag"
    cd ../cron/
    ./db-replicate.sh

else
    echo ". Skipping DB Replication from Legacy Database, as per DB_REPLICATION flag"
fi

echo "Completed Post-Deploy tasks."
