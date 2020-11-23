#!/bin/sh
# pre-deploy hook that runs migrations for GWELLS app.

set -xeuo pipefail

APP_SOURCE_DIR=$APP_ROOT

while true
do 
        # wait here for database to be available
        psql -qtAX -c 'select 1' && break
        sleep 10
done

echo ls $APP_ROOT


cd $APP_SOURCE_DIR/src/backend/
python manage.py migrate
