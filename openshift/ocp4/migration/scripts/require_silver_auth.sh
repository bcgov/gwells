#!/bin/bash
KUBECONFIGSILVER=/tmp/KUBECONFIGSILVER
if [ ! -f "$KUBECONFIGSILVER" ]; then
  read -r -p "Enter Silver auth token: " AUTH_TOKEN
  oc --kubeconfig="$KUBECONFIGSILVER" login --token="$AUTH_TOKEN" --server=https://api.silver.devops.gov.bc.ca:6443
fi