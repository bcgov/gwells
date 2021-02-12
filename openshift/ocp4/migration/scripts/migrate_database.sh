#!/bin/bash
# Usage: ./db_dump_and_copy.sh

# Run the database migration scripts

. ./db_dump_and_copy.sh
ls -alh /tmp/backup

echo "------------------------------------------------------------------------------"
echo "Copy from Pathfinder successful. Copying to the db pod and restoring the database..."
echo "------------------------------------------------------------------------------"

. ./db_copy_and_restore.sh
