#!/bin/bash
# We need to login to Pathfinder. Ask for auth token
read -r -p "Enter Pathfinder auth token: " AUTH_TOKEN
oc --kubeconfig=/tmp/KUBECONFIG login https://console.pathfinder.gov.bc.ca:8443 --token="$AUTH_TOKEN"

NAMESPACE="moe-gwells-$1"
POD_NAME='staging'
if [ "$1" == 'prod' ]; then
  POD_NAME='production'
fi

GWELLS_DB_POD=$(oc --kubeconfig=/tmp/KUBECONFIG get pods -n "$NAMESPACE" | grep "gwells-pg12-$POD_NAME" | head -1 | awk '{print $1}')
echo "------------------------------------------------------------------------------"
echo "Found pod $GWELLS_DB_POD on $NAMESPACE"
echo "Starting database dump..."
echo "------------------------------------------------------------------------------"

# On Pathfinder - dump db
DB_DUMPFILE="/tmp/gwells-$1-db-latest"
SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- bash -c "pg_dump -Fc gwells > $DB_DUMPFILE"
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Dump took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Starting to copy dumpfile from Pathfinder to this pod's volume..."
echo "------------------------------------------------------------------------------"


# On ocp4 - copy file from Pathfinder
mkdir /tmp/backup
SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIG rsync -n "$NAMESPACE" "$GWELLS_DB_POD":"$DB_DUMPFILE" /tmp/backup/
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Rsync took $((duration / 60)) minutes and $((duration % 60)) seconds."

# delete dump from source
echo "Cleanup - deleting dump from Pathfinder"
echo "------------------------------------------------------------------------------"

oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- rm -f "$DB_DUMPFILE"

# Scale down the pathfinder database DC
oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" scale --replicas=0 dc/gwells-pg12-production
