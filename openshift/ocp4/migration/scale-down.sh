#!/bin/bash

NAMESPACE="moe-gwells-$1"
ENV_NAME="staging"

if [ "$1" == 'prod' ]; then
    ENV_NAME='prod'
fi
echo
echo "Scaling down on Pathfinder ($NAMESPACE ; env: $ENV_NAME)"
echo
oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" scale "dc/gwells-$ENV_NAME" --replicas=0
REPLICAS=$(oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" get dc "gwells-$ENV_NAME" -o go-template="{{.status.replicas}}")
while [ "$REPLICAS" != 0 ]
do
    echo "Waiting for GWELLS to scale down (current replicas: ${REPLICAS})"
    sleep 1
    REPLICAS=$(oc --kubeconfig=/tmp/KUBECONFIG -n "$NAMESPACE" get dc gwells-$ENV_NAME -o go-template="{{.status.replicas}}")
done
echo "Successfully scaled down (current replicas: ${REPLICAS})"  

