#!/bin/bash

# ---------------------------------------------------------------------------------
# Set variables and get authentication
# ---------------------------------------------------------------------------------
# Ask what environment we're migrating
read -r -p 'Namespace [test/prod]: ' ENVIRONMENT

KUBECONFIG=/tmp/KUBECONFIG
KUBECONFIGSILVER=/tmp/KUBECONFIGSILVER

# We need to login to Pathfinder. Ask for auth token
read -r -p "Enter Pathfinder auth token: " AUTH_TOKEN
oc --kubeconfig="$KUBECONFIG" login https://console.pathfinder.gov.bc.ca:8443 --token="$AUTH_TOKEN"

# We need to login to Silver. Ask for auth token
read -r -p "Enter Silver auth token: " AUTH_TOKEN
oc --kubeconfig="$KUBECONFIGSILVER" login --token="$AUTH_TOKEN" --server=https://api.silver.devops.gov.bc.ca:6443


# Pod suffix i.e. gwells-staging, gwells-production
POD_SUFFIX='staging'
if [ "$ENVIRONMENT" == 'prod' ]; then
  POD_SUFFIX='production'
fi

# Pathfinder namespace
NAMESPACE="moe-gwells-$ENVIRONMENT"

# Silver namespace
NAMESPACE4="26e83e-$ENVIRONMENT"

# scale down

# ---------------------------------------------------------------------------------
# Migrate the database
# ---------------------------------------------------------------------------------
. ./migrate_database.sh "$ENVIRONMENT" "$POD_SUFFIX" "$NAMESPACE" "$NAMESPACE4"

# ---------------------------------------------------------------------------------
# Mirror minio data
# ---------------------------------------------------------------------------------
. ./migrate_minio.sh