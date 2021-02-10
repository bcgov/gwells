#!/bin/bash
# add --revert to end (after test/prod) to scale back to 2 on Pathfinder.

set -euo pipefail

NAMESPACE="moe-gwells-$1"
ENV_NAME="staging"

if [ "$1" == 'prod' ]; then
    ENV_NAME='production'
fi


if echo $* | grep -e "--revert" -q
then
	# revert to 2 replicas
    echo "Scaling back to 2 replicas on Pathfinder ($NAMESPACE ; env: $ENV_NAME)"

    oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" scale "dc/gwells-$ENV_NAME" --replicas=2
    echo "Scaled to 2 replicas"

else
    echo "Scaling down on Pathfinder ($NAMESPACE ; env: $ENV_NAME)"
    oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" scale "dc/gwells-$ENV_NAME" --replicas=0
    REPLICAS=$(oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" get dc "gwells-$ENV_NAME" -o go-template="{{.status.replicas}}")
    while [ "$REPLICAS" != 0 ]
    do
        echo "Waiting for GWELLS to scale down (current replicas: ${REPLICAS})"
        sleep 1
        REPLICAS=$(oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" get dc gwells-$ENV_NAME -o go-template="{{.status.replicas}}")
    done
    echo "Successfully scaled down (current replicas: ${REPLICAS})"  
fi
