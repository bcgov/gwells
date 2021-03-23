#!/bin/bash
# Usage: ./db_copy_and_restore.sh [test/prod]
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
oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "dropdb gwells"
oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "createdb --owner=\$PG_USER gwells"
oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "pg_restore -d gwells $PG_DUMPFILE"

# Do we need to change the db user? This reassigns the privileges of the old user to $PG_USER
read -r -p 'Do you need to change db user? [Y/n]: ' ASK_CHANGE

if [[ "$ASK_CHANGE" =~ ^[Yy]$ ]]; then
  read -r -p 'Enter old user: ' OLD_USER

  if [[ ${#OLD_USER} -gt 0 ]]; then
    echo "Changing user from $OLD_USER to \$PG_USER on pod"
    echo "Command is psql -U postgres -d gwells -c \"REASSIGN OWNED BY \\\"$OLD_USER\\\" TO \\\"\$PG_USER\\\"\""
    oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "psql -U postgres -d gwells -c \"REASSIGN OWNED BY \\\"$OLD_USER\\\" TO \\\"\$PG_USER\\\"\""
  fi
fi
#oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "pg_restore --no-owner --role=\$PG_USER -d gwells $PG_DUMPFILE"
#oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "psql -U postgres -d gwells -c \"GRANT USAGE ON SCHEMA postgis_ftw TO ftw_reader\""
#oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "psql -U postgres -d gwells -c \"ALTER DEFAULT PRIVILEGES IN SCHEMA postgis_ftw GRANT SELECT ON TABLES TO ftw_reader\""

duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Reload took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Database migration done. Please check the database."
echo "------------------------------------------------------------------------------"