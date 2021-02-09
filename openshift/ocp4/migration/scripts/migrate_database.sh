#!/bin/bash
read -r -p 'Namespace [test/prod] :' NAMESPACE
. ./dump_and_copy.sh "$NAMESPACE"
ls -alh /tmp/backup
echo "------------------------------------------------------------------------------"
echo "Copy from ocp3 successful. Copying to the db pod and restoring the database..."
echo "------------------------------------------------------------------------------"
. ./copy_and_load_db.sh "$NAMESPACE"
