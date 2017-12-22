#!/bin/sh
#
# Fri Dec 22 12:04:09 2017 GW Shell script run by 'Pre Lifecycle Hook' on OpenShift
#   which connects to the application container (gwells-app).
#
#   This pre-deploy is triggered on all three envionments (moe-gwells-dev,
#   moe-gwells-test, moe-gwells-prod)
#
#   Example: oc exec gwells-97-69b7z /opt/app-root/src/database/cron/pre-deploy.sh
#
echo "Running Pre-Deploy tasks..."
echo ". Disabling DB connections"
export PGPASSWORD=$POSTGRESQL_ADMIN_PASSWORD
psql -h $DATABASE_SERVICE_NAME -U postgres -c "ALTER DATABASE $DATABASE_NAME WITH ALLOW_CONNECTIONS false;"
sleep 5

echo "Completed Pre-Deploy tasks."
