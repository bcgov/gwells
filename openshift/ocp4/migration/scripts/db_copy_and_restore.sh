#!/bin/bash
# This script copies the dump from the migrator-cli volume to the db volume and restores the database using pg_restore

# Get variables from previous scripts or params
ENVIRONMENT=${ENVIRONMENT:-$1}
. ./params.sh "$ENVIRONMENT"
. ./require_silver_auth.sh

# Start copy to db pod and restore
GWELLS4_DB_POD=$(oc --kubeconfig="$KUBECONFIGSILVER" get pods -n "$NAMESPACE4" | grep "gwells-pg12-$POD_SUFFIX" | grep Running | head -1 | awk '{print $1}')

echo "------------------------------------------------------------------------------"
echo "Found pod $GWELLS4_DB_POD on $NAMESPACE4"
echo "Starting copy to db pod..."
echo "------------------------------------------------------------------------------"

# Copy to db pod
SECONDS=0
oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE4" rsync /tmp/backup/ "$GWELLS4_DB_POD":/pgdata/backup/ -c postgresql
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Copy took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Starting pg_reload..."
echo "------------------------------------------------------------------------------"


# Reload database
PG_DUMPFILE="/pgdata/backup/gwells-$ENVIRONMENT-db-latest"
SECONDS=0
oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "pg_restore -c -d gwells $PG_DUMPFILE"
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Reload took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Migration done. Please check the database."
echo "------------------------------------------------------------------------------"