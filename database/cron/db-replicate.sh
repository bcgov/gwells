#!/bin/sh
#
# Mon Nov  6 15:03:49 2017 GW Shell script run by 'oc exec' on OpenShift
#   initiated by Jenkins job, which connects to the application server 
#   pod (gwells-nn-xxxxx which is STATUS = 'Running'):
#      oc exec gwells-nnn-xxxx $VIRTUAL_ENV/src/database/cron/db-replicate.sh
#
#   This deploy is triggered only on the PROD envionments  (moe-gwells-prod)
#
#   Example: oc exec gwells-97-69b7z /opt/app-root/src/database/cron/db-replicate.sh
#
export PGPASSWORD=$DATABASE_PASSWORD           
cd /opt/app-root/src/database/code-tables/ 
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  -c 'select gwells_setup_replicate();'               
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  -c 'vacuum;'               
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  -f data-load-static-codes.sql
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  -c 'select gwells_replicate();'              