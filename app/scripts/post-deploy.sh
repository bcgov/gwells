#!/bin/sh
#
# Mon Nov  6 15:03:49 2017 GW Shell script run by 'oc exec' on OpenShift
#   initiated by Jenkins job, which connects to the application server
#   pod (gwells-nn-xxxxx which is STATUS = 'Running'):
#      oc exec gwells-nnn-xxxx $VIRTUAL_ENV/src/openshift/scripts/post-deploy.sh
#
#   This deploy is triggered on all three envionments (moe-gwells-dev,
#   moe-gwells-test, moe-gwells-prod)
#
#   Example: oc exec gwells-97-69b7z /opt/app-root/src/openshift/scripts/post-deploy.sh
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
cd /opt/app-root/src/
echo ". Creating additional DB objects (e.g. spatial indices, stored procedures)"
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
	\ir database/scripts/wellsearch/post-deploy.sql
	\ir database/scripts/wellsearch/wells_replication_stored_functions.sql
EOF

# $DB_REPLICATE can be one of "None" | "Subset" | "Full"
# NOTE: TODO clearing and reloading of code tables to be independent of
#       db_replicate and only part of code migration (and python load ...)
#       is this the same as fixtures???  don't think so
if [ "$DB_REPLICATE" = "Subset" -o "$DB_REPLICATE" = "Full" ]
then
	# \copy statements in data-load-static-codes.sql required to be in this directory
	# NOTE: this will clear out Registries app tables too
	cd /opt/app-root/src/database/codetables/gwells

	# Refresh Code lookup tables
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
	\i clear-tables.sql
	\i data-load-static-codes.sql
EOF

	# \copy statements in data-load-static-codes.sql required to be in this directory
	cd /opt/app-root/src/database/codetables/wellsearch

	# Refresh WellSearch Code lookup tables, including the well table
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
	\i clear-tables.sql
	\i data-load-static-codes.sql
EOF

	# \copy statements in data-load-static-codes.sql required to be in this directory
	cd /opt/app-root/src/database/codetables/registries

	# Refresh Registries app code lookup tables
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  << EOF
	\ir ../../scripts/registries/post-deploy.sql
	\i clear-tables.sql
	\ir ../../scripts/registries/initialize-xforms-registries.sql
	\i data-load-static-codes.sql
	\ir ../../scripts/registries/populate-registries-from-xform.sql
EOF

	echo ". Running DB Replication from Legacy Database, as per DB_REPLICATION flag"
    cd /opt/app-root/src/scripts/
    ./db-replicate.sh
else
    echo ". Skipping DB Replication from Legacy Database, as per DB_REPLICATION flag"
fi

echo ". Running python-related post-deploy tasks."
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64/
cd /opt/app-root/src/
python manage.py post-deploy

echo "Completed Post-Deploy tasks."
