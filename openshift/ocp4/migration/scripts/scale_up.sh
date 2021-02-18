#!/bin/bash
# This script scales up the gwells application on Silver
# add --revert to end (after test/prod) to scale back to 2 on Pathfinder.
# i.e. ./scale_up.sh [test/prod] --revert

ENVIRONMENT=${ENVIRONMENT:-$1}
. ./params.sh "$ENVIRONMENT"
. ./require_silver_auth.sh

set -euo pipefail

if echo $* | grep -e "--revert" -q
then
	# revert to 2 replicas
    echo "Scaling down to 0 replicas on Silver ($NAMESPACE4 ; env: $POD_SUFFIX)"

    oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE4" scale "dc/gwells-$POD_SUFFIX" --replicas=0
    oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE4" scale "dc/pgtileserv-$POD_SUFFIX" --replicas=0

    echo "Scaled to 0 replicas"

else
    echo "Scaling up on Silver ($NAMESPACE4 ; env: $POD_SUFFIX)"

    oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE4" scale "dc/gwells-$POD_SUFFIX" --replicas=2
    oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE4" scale "dc/pgtileserv-$POD_SUFFIX" --replicas=1

    REPLICAS=$(oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE4" get dc "gwells-$POD_SUFFIX" -o go-template="{{.status.readyReplicas}}")
    while [ "$REPLICAS" != 2 ]
    do
        echo "Waiting for GWELLS to scale up..."
        sleep 3
        REPLICAS=$(oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE4" get dc "gwells-$POD_SUFFIX" -o go-template="{{.status.readyReplicas}}")
    done
    echo "Successfully scaled up (current replicas: ${REPLICAS})"
fi
