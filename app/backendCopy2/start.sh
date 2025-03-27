#! /usr/bin/env sh
# adapted from https://github.com/tiangolo/uvicorn-gunicorn-docker
set -e

export APP_MODULE=${APP_MODULE:-"main:wally_api"}

if [ -f /app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
elif [ -f /app/backend/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/backend/gunicorn_conf.py
else
    DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
fi
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}

# Let the DB start
# python /app/api/db/wait_for_db.py

# Load fixture data for dev environments
# if [ "$WALLY_ENV" = "DEV" ]; then
#     echo "Loading Fixtures"
#     python /app/api/initial_data.py
# fi

echo "$GUNICORN_CONF" "$APP_MODULE"

# Start Gunicorn
exec gunicorn -k uvicorn.workers.UvicornWorker -c "$GUNICORN_CONF" "$APP_MODULE"
