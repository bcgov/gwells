#!/bin/bash
. ./dump_and_copy.sh
ls -alh /tmp/backup
echo "------------------------------------------------------------------------------"
echo "Copy from ocp3 successful. Copying to the db pod and restoring the database..."
echo "------------------------------------------------------------------------------"
. ./copy_and_load_db.sh
