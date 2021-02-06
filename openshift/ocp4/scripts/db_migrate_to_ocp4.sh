#!/bin/bash
# TODO: Clean this script up! It works, but you still need to do manual oc logins

# ------------------------- start of copy script ---------------------
oc --kubeconfig=/tmp/KUBECONFIG login https://console.pathfinder.gov.bc.ca:8443 --token=<MY_OCP3_AUTH_TOKEN>

NAMESPACE='moe-gwells-test'
GWELLS_DB_POD=$(oc --kubeconfig=/tmp/KUBECONFIG get pods -n "$NAMESPACE" | grep gwells-pg12-staging | head -1 | awk '{print $1}')

#oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- date
#oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- ls -alh /tmp/

#DB_DUMPFILE="/tmp/gwells-prod-db-$(date +%Y%m%d%H%M%S)"
DB_DUMPFILE="/tmp/gwells-prod-db-latest"
SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- bash -c "pg_dump -Fc gwells > $DB_DUMPFILE"
duration=$SECONDS
echo "Dump took $((duration / 60)) minutes and $((duration % 60)) seconds."

#oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- ls -alh "$DB_DUMPFILE"
#SECONDS=0
#oc --kubeconfig=/tmp/KUBECONFIG cp -n "$NAMESPACE" "$GWELLS_DB_POD":"$DB_DUMPFILE" $DB_DUMPFILE
#duration=$SECONDS
#echo "Copy took $((duration / 60)) minutes and $((duration % 60)) seconds."

SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIG rsync -n "$NAMESPACE" "$GWELLS_DB_POD":"$DB_DUMPFILE" /tmp/
duration=$SECONDS
echo "Rsync took $((duration / 60)) minutes and $((duration % 60)) seconds."

mkdir backup
mv $DB_DUMPFILE /tmp/backup/
DB_DUMPFILE="/tmp/backup/gwells-prod-db-latest"

# delete dump from source
oc --kubeconfig=/tmp/KUBECONFIG exec -n "$NAMESPACE" "$GWELLS_DB_POD" -- rm -f $DB_DUMPFILE
# ------------------------- end of copy script ---------------------


# ------------------------- start of copy from migrator-cli vol to db pod vol (both on ocp4) ---------------------
# oc login to silver
oc --kubeconfig=/tmp/KUBECONFIGSILVER login --token=<MY_AUTH_TOKEN> --server=https://api.silver.devops.gov.bc.ca:6443
# end login

NAMESPACE4=26e83e-test
GWELLS4_DB_POD=$(oc --kubeconfig=/tmp/KUBECONFIGSILVER get pods -n "$NAMESPACE4" | grep gwells-pg12-staging | grep Running | head -1 | awk '{print $1}')

#oc --kubeconfig=/tmp/KUBECONFIGSILVER exec -n "$NAMESPACE4" "$GWELLS_DB_POD" -- ls -alh /pgdata/backup/
SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIGSILVER -n "$NAMESPACE4" rsync /tmp/backup/ "$GWELLS4_DB_POD":/pgdata/backup/ -c postgresql
duration=$SECONDS
echo "Copy took $((duration / 60)) minutes and $((duration % 60)) seconds."
# ------------------------- end of copy to db pod ---------------------

# ------------------------- start of delete script ---------------------

# ------------------------- end of copy script ---------------------

# ------------------------- db load ---------------------------
# NOTE: Remove -v if you don't want to see the progress
PG_DUMPFILE="/pgdata/backup/gwells-prod-db-latest"
SECONDS=0
oc --kubeconfig=/tmp/KUBECONFIGSILVER exec -n "$NAMESPACE4" "$GWELLS4_DB_POD" -c postgresql -- bash -c "pg_restore -c -d gwells $PG_DUMPFILE"
duration=$SECONDS
echo "Reload took $((duration / 60)) minutes and $((duration % 60)) seconds."

# -------------------------end of load ---------------------------