export GWELLS_API_BASE_URL="https://dlvrapps.nrs.gov.bc.ca/gwells/registries"
export GWELLS_API_TEST_USER="testuser"
export GWELLS_API_TEST_PASSWORD="testpassword"
newman run registries_api_tests.json --global-var base_url=$GWELLS_API_BASE_URL --global-var test_user=$GWELLS_API_TEST_USER --global-var test_password=$GWELLS_API_TEST_PASSWORD -r cli,junit,html;
