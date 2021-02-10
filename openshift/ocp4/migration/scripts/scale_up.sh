#!/bin/bash
set -euo pipefail

ENVIRONMENT=${ENVIRONMENT:-$1}
. ./params.sh "$ENVIRONMENT"
. ./require_silver_auth.sh

if echo $* | grep -e "--revert" -q
then
	# revert to 2 replicas
    echo "Scaling down to 0 replicas on Silver ($NAMESPACE ; env: $POD_SUFFIX)"

    oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE" scale "dc/gwells-$POD_SUFFIX" --replicas=0
    echo "Scaled to 0 replicas"

else
    echo "Scaling up on Silver ($NAMESPACE ; env: $POD_SUFFIX)"

    oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE" scale "dc/gwells-$POD_SUFFIX" --replicas=2

    REPLICAS=$(oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE" get dc "gwells-$POD_SUFFIX" -o go-template="{{.status.readyReplicas}}")
    while [ "$REPLICAS" != 2 ]
    do
        echo "Waiting for GWELLS to scale up..."
        sleep 3
        REPLICAS=$(oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE" get dc "gwells-$POD_SUFFIX" -o go-template="{{.status.readyReplicas}}")
    done
    echo "Successfully scaled up (current replicas: ${REPLICAS})"
fi
