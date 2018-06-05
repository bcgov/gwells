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
# Halt conditions, verbosity and field separator
#
set -euo pipefail
IFS=$'\n\t'
echo "Running Post-Deploy tasks..."
export PGPASSWORD=$DATABASE_PASSWORD
cd $APP_ROOT
echo ". Creating additional DB objects (e.g. spatial indices, stored procedures)"
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
	\i scripts/database/scripts/wellsearch/post-deploy.sql
	\i scripts/database/scripts/wellsearch/wells_replication_stored_functions.sql
EOF
set -x

# $DB_REPLICATE can be one of "None" | "Subset" | "Full"
# NOTE: TODO clearing and reloading of code tables to be independent of
#       db_replicate and only part of code migration (and python load ...)
#       is this the same as fixtures???  don't think so
if [ "$DB_REPLICATE" = "Subset" -o "$DB_REPLICATE" = "Full" ]
then
	# NOTE: this will clear out Registries app tables too, since the ProvinceStateCode table
	#       is also a parent table of Registries tables
	cd $APP_ROOT/app
	python manage.py flush --noinput
	python manage.py loaddata gwells/fixtures/codetables.ProvinceStateCode.json gwells/fixtures/codetables.json registries/fixtures/codetables.json

	echo ". Running DB Replication from Legacy Database, as per DB_REPLICATION flag"
    cd $APP_ROOT/app/scripts/
    ./db-replicate.sh
else
    echo ". Skipping DB Replication from Legacy Database, as per DB_REPLICATION flag"
fi

echo ". Running python-related post-deploy tasks."
cd $APP_ROOT/app
(
	set +e;
	python manage.py post-deploy
)

echo "Completed Post-Deploy tasks."
