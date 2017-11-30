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
echo ". Creating additional DB objects (e.g. spatial indices)"
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  -f post-deploy.sql

if [ "$ENABLE_DB_REPLICATION" = "True" ]
then
  echo ". Running DB Replication from Legacy Database, as per ENABLE_DB_REPLICATION flag"
  cd /opt/app-root/src/database/cron/
  ./db-replicate.sh
else
  echo ". Skipping DB Replication from Legacy Database, as per ENABLE_DB_REPLICATION flag"
fi 

echo "Completed Post-Deploy tasks."
