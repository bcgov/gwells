#!/bin/bash
# We need to login to ocp3. Ask for auth token
read -r -p "Enter OCP3 auth token: " AUTH_TOKEN
oc --kubeconfig=/tmp/KUBECONFIG login https://console.pathfinder.gov.bc.ca:8443 --token="$AUTH_TOKEN"

NAMESPACE='moe-gwells-test'
GWELLS_DB_POD=$(oc --kubeconfig=/tmp/KUBECONFIG get pods -n "$NAMESPACE" | grep gwells-pg12-staging | head -1 | awk '{print $1}')
echo "------------------------------------------------------------------------------"
echo "Found pod $GWELLS_DB_POD on $NAMESPACE"
echo "Starting database dump..."
echo "------------------------------------------------------------------------------"

# On ocp3 - dump db
DB_DUMPFILE="/tmp/gwells-prod-db-latest"
SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- bash -c "pg_dump -Fc gwells > $DB_DUMPFILE"
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Dump took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Starting to copy dumpfile from ocp3 to this pod's volume..."
echo "------------------------------------------------------------------------------"


# On ocp4 - copy file from ocp3
mkdir /tmp/backup
SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIG rsync -n "$NAMESPACE" "$GWELLS_DB_POD":"$DB_DUMPFILE" /tmp/backup/
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Rsync took $((duration / 60)) minutes and $((duration % 60)) seconds."

# delete dump from source
echo "Cleanup - deleting dump from ocp3"
echo "------------------------------------------------------------------------------"

oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- rm -f $DB_DUMPFILE