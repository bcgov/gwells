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
	\i db_replicate.sql
EOF

# $DB_REPLICATE can be one of "None" | "Subset" | "Full"
if [ "$DB_REPLICATE" = "Subset" -o "$DB_REPLICATE" = "Full" ]
then
	# \copy statements in data-load-static-codes.sql required to be in this directory
	cd /opt/app-root/src/database/code-tables/

	# Refresh Code lookup tables, including the well table
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
	\i clear-tables.sql
	\i data-load-static-codes.sql
EOF

	echo ". Running DB Replication from Legacy Database, as per DB_REPLICATION flag"
    cd /opt/app-root/src/database/cron/
    ./db-replicate.sh


	# \copy statements in data-load-static-codes.sql required to be in this directory
# Wed 28 Mar 19:50:16 2018 GW Commented out this section to avoid overwrite of
#                             one-off Registries replication (from MS Access source)
#	cd ../code-tables/registries/

	# @Registries
	# Temporary setup of Registries (Well Driller only) as part of Code With Us
	# ,including Test Data loaded into the Registries (Driller) tables
#	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
#	\ir ../../scripts/registries/post-deploy.sql
#	\i clear-tables.sql
#	\ir ../../scripts/registries/initialize-xforms-registries.sql
#	\i data-load-static-codes.sql
#	\ir ../../scripts/registries/populate-registries-from-xform.sql
#EOF
else
    echo ". Skipping DB Replication from Legacy Database, as per DB_REPLICATION flag"
fi

# libpython3.5m.so.rh-python35-1.0 => /opt/rh/rh-python35/root/usr/lib64/libpython3.5m.so.rh-python35-1.0 (0x00007f845927b000)

echo $LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64/

cd /opt/app-root/src/
python manage.py post-deploy

echo "Completed Post-Deploy tasks."
