#!/bin/bash
# 
# Usage:
# - Set env variables (choose any username and password):
#     export GWELLS_API_BASE_URL="http://localhost:8000/gwells/registries"
#     export GWELLS_API_TEST_USER="testuser"
#     export GWELLS_API_TEST_PASSWORD="secret"
#     export GWELLS_API_TEST_AUTH_SERVER=""
#     export GWELLS_API_TEST_CLIENT_ID=""
#     export GWELLS_API_TEST_CLIENT_SECRET"""
# - Create Django test user (requires env variables from previous step):
#     python manage.py createtestuser
# - Install newman:
#     npm install -g newman
# - Run script:
#     ./local_newman.sh


ENV_VARS=(
    "GWELLS_API_TEST_USER"
    "GWELLS_API_TEST_PASSWORD"
    "GWELLS_API_BASE_URL"
    "GWELLS_API_TEST_AUTH_SERVER"
    "GWELLS_API_TEST_CLIENT_ID"
    "GWELLS_API_TEST_CLIENT_SECRET"
)

for env_var in ${ENV_VARS[@]}
do
    if [ -z ${!env_var+x} ]; then 
        echo "$env_var is unset"
        exit
    fi
done

echo "Remember to install newman (npm install -g newman) and set GWELLS_API_TEST_USER,"
echo "GWELLS_API_TEST_PASSWORD, GWELLS_API_BASE_URL and Keycloak credentials"
newman run ./registries_api_tests.json --global-var test_user=$GWELLS_API_TEST_USER --global-var test_password=$GWELLS_API_TEST_PASSWORD --global-var base_url=$GWELLS_API_BASE_URL --global-var auth_server=$GWELLS_API_TEST_AUTH_SERVER --global-var client_id=$GWELLS_API_TEST_CLIENT_ID --global-var client_secret=$GWELLS_API_TEST_CLIENT_SECRET
