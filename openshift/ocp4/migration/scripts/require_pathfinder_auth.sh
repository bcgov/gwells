#!/bin/bash
KUBECONFIG=/tmp/KUBECONFIG
if [ ! -f "$KUBECONFIG" ]; then
  read -r -p "Enter Pathfinder auth token: " AUTH_TOKEN
  oc --kubeconfig="$KUBECONFIG" login https://console.pathfinder.gov.bc.ca:8443 --token="$AUTH_TOKEN"
fi