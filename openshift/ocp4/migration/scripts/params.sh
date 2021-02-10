#!/bin/bash

# ---------------------------------------------------------------------------------
# Set variables and get authentication
# ---------------------------------------------------------------------------------

# get params
ENVIRONMENT=${ENVIRONMENT:-$1}

# Ask what environment we're migrating
if [[ -z "$ENVIRONMENT" ]]; then
  read -r -p 'Namespace [test/prod]: ' ENVIRONMENT
fi

# Pathfinder namespace
NAMESPACE="moe-gwells-$ENVIRONMENT"

# Silver namespace
NAMESPACE4="26e83e-$ENVIRONMENT"

# Pod suffix i.e. gwells-staging, gwells-production
POD_SUFFIX='staging'
if [ "$ENVIRONMENT" == 'prod' ]; then
  POD_SUFFIX='production'
fi

