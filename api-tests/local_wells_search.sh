#!/bin/bash

# Usage:
# - Set env variables (choose any username and password):
#   GWELLS_API_BASE_URL:   URL for testing (API tests will make requests here)
# - Install newman:
#     npm install -g newman
# - Run script:
#     ./local_wells_search.sh

if [ -z $GWELLS_API_BASE_URL ]; then
    echo "GWELLS_API_BASE_URL is unset"
    exit
fi

echo "Remember to install newman (npm install -g newman) and set GWELLS_API_BASE_URL."
newman run ./wells_search_api_tests.json --global-var base_url=$GWELLS_API_BASE_URL
