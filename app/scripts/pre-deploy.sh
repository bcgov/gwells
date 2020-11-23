#!/bin/sh
# pre-deploy hook that runs migrations for GWELLS app.

set -xeuo pipefail

while true
do 
        # wait here for database to be available
        psql -qtAX -c 'select 1' && break
        sleep 10
done

cd /app/backend/
python manage.py migrate
