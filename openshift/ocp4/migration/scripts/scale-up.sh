#!/bin/bash

NAMESPACE="26e83e-$1"
ENV_NAME="staging"

if [ "$1" == 'prod' ]; then
    ENV_NAME='production'
fi

echo
echo "Scaling up on Silver ($NAMESPACE ; env: $ENV_NAME)"
echo

oc --kubeconfig=/tmp/KUBECONFIGSILVER -n "$NAMESPACE" scale "dc/gwells-$ENV_NAME" --replicas=2

REPLICAS=$(oc --kubeconfig=/tmp/KUBECONFIGSILVER -n "$NAMESPACE" get dc "gwells-$ENV_NAME" -o go-template="{{.status.readyReplicas}}")
while [ "$REPLICAS" != 2 ]
do
    echo "Waiting for GWELLS to scale up..."
    sleep 3
    REPLICAS=$(oc --kubeconfig=/tmp/KUBECONFIGSILVER -n "$NAMESPACE" get dc "gwells-$ENV_NAME" -o go-template="{{.status.readyReplicas}}")
done
echo "Successfully scaled up (current replicas: ${REPLICAS})"
