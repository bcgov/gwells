#!/bin/bash
echo "Remember to install newman (npm install -g newman) and set GWELLS_API_TEST_USER,"
echo "GWELLS_API_TEST_PASSWORD and GWELLS_API_BASE_URL"
newman run ./registries_api_tests.json --global-var test_user=$GWELLS_API_TEST_USER --global-var test_password=$GWELLS_API_TEST_PASSWORD --global-var base_url=$GWELLS_API_BASE_URL
