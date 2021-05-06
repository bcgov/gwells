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

# Ask if this is a test run or not
if [[ -z "$ASK_RUN" ]]; then
 read -r -p 'Is this a test run? [Y/n]: ' ASK_RUN
fi

TEST_RUN=1
if [[ "$ASK_RUN" =~ ^[Nn]$ ]]; then
  echo "Confirm that this migration is NOT a test run."
  echo "It will scale down pathfinder, scale up silver, and activate the proxy."
  read -r -p "Type PROCEED to confirm and proceed: " CONFIRM

  if [[ "$CONFIRM" == 'PROCEED' ]]; then
    TEST_RUN=0
  fi
fi