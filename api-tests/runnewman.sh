export GWELLS_API_BASE_URL="https://dlvrapps.nrs.gov.bc.ca/gwells/registries"
export GWELLS_API_TEST_USER="testuser"
export GWELLS_API_TEST_PASSWORD="testpassword"
newman run registries_api_tests.json --global-var base_url="https://dlvrapps.nrs.gov.bc.ca/gwells/registries" --global-var test_user="testuser" --global-var test_password="testpassword" -r cli,junit,html;
