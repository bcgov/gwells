#!/bin/bash

# Ask what environment we're migrating
#read -r -p 'Namespace [test/prod] :' ENVIRONMENT
if [[ -z "$NAMESPACE" ]]; then
  echo "Namespace not set, exiting..." 1>&2
  exit 1
fi

. ./db_dump_and_copy.sh
#. ./dump_and_copy.sh "$ENVIRONMENT"
ls -alh /tmp/backup

echo "------------------------------------------------------------------------------"
echo "Copy from Pathfinder successful. Copying to the db pod and restoring the database..."
echo "------------------------------------------------------------------------------"

. ./db_copy_and_restore.sh
#. ./copy_and_load_db.sh "$ENVIRONMENT"
