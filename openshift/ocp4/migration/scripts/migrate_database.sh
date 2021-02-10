#!/bin/bash

# Run the database migration scripts

# Get variables from previous scripts or params
ENVIRONMENT=${ENVIRONMENT:-$1}
POD_SUFFIX=${POD_SUFFIX:-$2}
NAMESPACE=${NAMESPACE:-$3}
NAMESPACE4=${NAMESPACE4:-$4}

if [[ -z "$ENVIRONMENT" ]]; then
  read -r -p 'Namespace [test/prod] :' ENVIRONMENT
fi

if [[ -z "$NAMESPACE" ]]; then
  NAMESPACE="moe-gwells-$ENVIRONMENT"
fi

if [[ -z "$NAMESPACE4" ]]; then
  NAMESPACE4="26e83e-$ENVIRONMENT"
fi

if [[ -z "$POD_SUFFIX" ]]; then
  POD_SUFFIX='staging'
  if [ "$ENVIRONMENT" == 'prod' ]; then
    POD_SUFFIX='production'
  fi
fi

. ./db_dump_and_copy.sh "$NAMESPACE" "$POD_SUFFIX"
ls -alh /tmp/backup

echo "------------------------------------------------------------------------------"
echo "Copy from Pathfinder successful. Copying to the db pod and restoring the database..."
echo "------------------------------------------------------------------------------"

. ./db_copy_and_restore.sh "$NAMESPACE4" "$POD_SUFFIX"
