#!/bin/bash

# ---------------------------------------------------------------------------------
# Set variables and get authentication
# ---------------------------------------------------------------------------------
# Ask what environment we're migrating
read -r -p 'Namespace [test/prod] :' ENVIRONMENT

# We need to login to Pathfinder. Ask for auth token
read -r -p "Enter Pathfinder auth token: " AUTH_TOKEN
oc --kubeconfig=/tmp/KUBECONFIG login https://console.pathfinder.gov.bc.ca:8443 --token="$AUTH_TOKEN"

# We need to login to Silver. Ask for auth token
read -r -p "Enter Silver auth token: " AUTH_TOKEN
oc --kubeconfig=/tmp/KUBECONFIGSILVER login --token="$AUTH_TOKEN" --server=https://api.silver.devops.gov.bc.ca:6443



# Pod names
POD_NAME='staging'
if [ "$ENVIRONMENT" == 'prod' ]; then
  POD_NAME='production'
fi

# Pathfinder namespace
NAMESPACE="moe-gwells-$ENVIRONMENT"

# Silver namespace
NAMESPACE4="26e83e-$ENVIRONMENT"

# ---------------------------------------------------------------------------------
# Start database migration
# ---------------------------------------------------------------------------------
. ./migrate_database.sh

. ./migrate_minio.sh