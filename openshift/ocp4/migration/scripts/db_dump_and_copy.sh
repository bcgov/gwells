#!/bin/bash
# Usage: ./db_dump_and_copy.sh [test/prod]

# This script dumps the old database and copies it to the migrator-cli's volume

# Get variables from previous scripts or params
ENVIRONMENT=${ENVIRONMENT:-$1}
. ./params.sh "$ENVIRONMENT"
. ./require_pathfinder_auth.sh

# Start dump and copy
GWELLS_DB_POD=$(oc --kubeconfig="$KUBECONFIG" get pods -n "$NAMESPACE" | grep "gwells-pg12-$POD_SUFFIX" | head -1 | awk '{print $1}')
echo "------------------------------------------------------------------------------"
echo "Found pod $GWELLS_DB_POD on $NAMESPACE"
echo "Starting database dump..."
echo "------------------------------------------------------------------------------"

# On Pathfinder - dump db
DB_DUMPFILE="/tmp/gwells-$ENVIRONMENT-db-latest"
SECONDS=0
oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- bash -c "pg_dump -Fc gwells > $DB_DUMPFILE"
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Dump took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Starting to copy dumpfile from Pathfinder to this pod's volume..."
echo "------------------------------------------------------------------------------"


# On ocp4 - copy file from Pathfinder
mkdir -p /tmp/backup
SECONDS=0
oc --kubeconfig="$KUBECONFIG" rsync -n "$NAMESPACE" "$GWELLS_DB_POD":"$DB_DUMPFILE" /tmp/backup/
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Rsync took $((duration / 60)) minutes and $((duration % 60)) seconds."

# delete dump from source
echo "Cleanup - deleting dump from Pathfinder"
echo "------------------------------------------------------------------------------"

oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- rm -f "$DB_DUMPFILE"

# Scale down the pathfinder database DC
#oc --kubeconfig="$KUBECONFIG" -n "$NAMESPACE" scale --replicas=0 "dc/gwells-pg12-$POD_SUFFIX"
