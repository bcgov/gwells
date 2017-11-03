#!/bin/sh
export PGPASSWORD=$DATABASE_PASSWORD           
cd $VIRTUAL_ENV/src/database/code-tables/ 
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  -c 'select gwells_setup_replicate();'               
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  -c 'vacuum;'               
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  -f data-load-static-codes.sql
psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER  -c 'select gwells_replicate();'              