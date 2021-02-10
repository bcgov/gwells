#!/bin/bash

# Get variables from previous scripts or params
NAMESPACE=${NAMESPACE:-$1}
POD_SUFFIX=${POD_SUFFIX:-$2}
KUBECONFIG=${KUBECONFIG:-'/tmp/KUBECONFIG'}

if [[ -z "$NAMESPACE" ]]; then
  echo "Namespace not set, exiting... (input param1 moe-gwells-[test/prod])"
  exit 1
fi

if [[ -z "$POD_SUFFIX" ]]; then
  echo "Pod suffix not set, exiting... (input param2 [staging/prod])"
  exit 1
fi

if [ ! -f "$KUBECONFIG" ]; then
  read -r -p "Enter Pathfinder auth token: " AUTH_TOKEN
  oc --kubeconfig="$KUBECONFIG" login https://console.pathfinder.gov.bc.ca:8443 --token="$AUTH_TOKEN"
fi

# Start dump and copy
GWELLS_DB_POD=$(oc --kubeconfig="$KUBECONFIG" get pods -n "$NAMESPACE" | grep "gwells-pg12-$POD_SUFFIX" | head -1 | awk '{print $1}')
echo "------------------------------------------------------------------------------"
echo "Found pod $GWELLS_DB_POD on $NAMESPACE"
echo "Starting database dump..."
echo "------------------------------------------------------------------------------"

# On Pathfinder - dump db
DB_DUMPFILE="/tmp/gwells-$NAMESPACE-db-latest"
SECONDS=0
oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- bash -c "pg_dump -Fc gwells > $DB_DUMPFILE"
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Dump took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Starting to copy dumpfile from Pathfinder to this pod's volume..."
echo "------------------------------------------------------------------------------"


# On ocp4 - copy file from Pathfinder
mkdir /tmp/backup
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
oc --kubeconfig="$KUBECONFIG" -n "$NAMESPACE" scale --replicas=0 dc/gwells-pg12-production
