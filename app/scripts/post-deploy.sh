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
set +e
set -x
echo "Running Post-Deploy tasks..."
export PGPASSWORD=$DATABASE_PASSWORD
cd $APP_ROOT/src/database/scripts/wellsearch/
echo ". Creating additional DB objects (e.g. spatial indices, stored procedures)"
psql -X --set ON_ERROR_STOP=on -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
	\i post-deploy.sql
	\i wells_replication_stored_functions.sql
EOF


psql_exit_status=$?

if [ $psql_exit_status != 0 ]; then
    echo "psql failed while trying to run this sql script" 1>&2
    exit $psql_exit_status
fi



echo ". Running python-related post-deploy tasks."
cd $APP_ROOT/src/
set +e
python manage.py post-deploy
set -e

echo "Completed Post-Deploy tasks."
