#!/bin/bash

# We need to login to ocp4. Ask for auth token
read -r -p "Enter OCP4 auth token: " AUTH_TOKEN
oc --kubeconfig=/tmp/KUBECONFIGSILVER login --token="$AUTH_TOKEN" --server=https://api.silver.devops.gov.bc.ca:6443

NAMESPACE4="26e83e-$1"

POD_NAME='staging'
if [ "$1" == 'prod' ]; then
  POD_NAME='prod'
fi

GWELLS4_DB_POD=$(oc --kubeconfig=/tmp/KUBECONFIGSILVER get pods -n "$NAMESPACE4" | grep "gwells-pg12-$POD_NAME" | grep Running | head -1 | awk '{print $1}')

echo "------------------------------------------------------------------------------"
echo "Found pod $GWELLS4_DB_POD on $NAMESPACE4"
echo "Starting copy to db pod..."
echo "------------------------------------------------------------------------------"

# Copy to db pod
SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIGSILVER -n "$NAMESPACE4" rsync /tmp/backup/ "$GWELLS4_DB_POD":/pgdata/backup/ -c postgresql
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Copy took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Starting pg_reload..."
echo "------------------------------------------------------------------------------"


# Reload database
PG_DUMPFILE="/pgdata/backup/gwells-$1-db-latest"
SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIGSILVER exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "pg_restore -c -d gwells $PG_DUMPFILE"
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Reload took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Migration done. Please check the database."
echo "------------------------------------------------------------------------------"