#!/bin/bash

# Usage:
# - Set env variables (choose any username and password):
#   GWELLS_API_BASE_URL:   URL for testing (API tests will make requests here)
# - Install newman:
#     npm install -g newman
# - Run script:
#     ./local_wells_search.sh

# Load ENVs to environment if not already present
if [ -z "$GWELLS_API_TEST_USER" ] && [ -f "./.envrc" ]; then
  source ./.envrc
  set -e
fi

ENV_VARS=(
    "GWELLS_API_BASE_URL"
)

echo "Running local_wells.sh"

for env_var in ${ENV_VARS[@]}
do
    if [ -z ${!env_var+x} ]; then
        echo "$env_var is unset"
        exit
    fi
done

echo "Remember to install newman (npm install -g newman) and set GWELLS_API_BASE_URL."
newman run ./wells_search_api_tests.json --global-var base_url=$GWELLS_API_BASE_URL
newman run ./wells_search_v2_api_tests.json --global-var base_url=$GWELLS_API_BASE_URL
