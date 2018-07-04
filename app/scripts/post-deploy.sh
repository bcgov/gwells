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
#
# Halt conditions, verbosity and field separator
#
set -xeuo pipefail
IFS=$'\n\t'


# Create additional DB objects (e.g. spatial indices, stored procedures)
#
echo "Post-Deploy: SQL imports"
cd $APP_ROOT/src/database/scripts/wellsearch/
export PGPASSWORD=$DATABASE_PASSWORD

(
	set +x;
	psql -X --set ON_ERROR_STOP=on -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER << EOF
		\i post-deploy.sql
		\i wells_replication_stored_functions.sql
EOF || (
		echo "psql failed while trying to run this sql script" 1>&2
		exit $?
	)
)


# Python related portion of post-deploy
#
echo "Post-Deploy: Python tasks"
cd $APP_ROOT/src/
python manage.py post-deploy


# Success!
#
echo "Post-Deploy: completed successfully"
