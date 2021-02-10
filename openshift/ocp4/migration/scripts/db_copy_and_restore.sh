#!/bin/bash

# Get variables from previous scripts or params
NAMESPACE4=${NAMESPACE4:-$1}
POD_SUFFIX=${POD_SUFFIX:-$2}
KUBECONFIGSILVER=${KUBECONFIGSILVER:-'/tmp/KUBECONFIGSILVER'}

if [[ -z "$NAMESPACE4" ]]; then
  echo "Namespace not set, exiting... (input param1 26e83e-[test/prod])"
  exit 1
fi

if [[ -z "$POD_SUFFIX" ]]; then
  echo "Pod suffix not set, exiting... (input param2 [staging/prod])"
  exit 1
fi

if [ ! -f "$KUBECONFIGSILVER" ]; then
  read -r -p "Enter Silver auth token: " AUTH_TOKEN
  oc --kubeconfig="$KUBECONFIGSILVER" login --token="$AUTH_TOKEN" --server=https://api.silver.devops.gov.bc.ca:6443
fi

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
PG_DUMPFILE="/pgdata/backup/gwells-$1-db-latest"
SECONDS=0
oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "pg_restore -c -d gwells $PG_DUMPFILE"
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Reload took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Migration done. Please check the database."
echo "------------------------------------------------------------------------------"