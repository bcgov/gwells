#!/bin/bash

# Ask what environment we're migrating
read -r -p 'Namespace [test/prod] :' ENVIRONMENT

. ./dump_and_copy.sh "$ENVIRONMENT"
ls -alh /tmp/backup

echo "------------------------------------------------------------------------------"
echo "Copy from Pathfinder successful. Copying to the db pod and restoring the database..."
echo "------------------------------------------------------------------------------"

. ./copy_and_load_db.sh "$ENVIRONMENT"
