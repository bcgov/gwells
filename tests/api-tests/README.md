# API Tests

The API tests use [Newman](https://www.npmjs.com/package/newman) to run the tests that are created in [Postman](https://www.getpostman.com).

You can install Newman as a global dependency with `npm i -g newman@4.6.1` (This is the version currently used by Jenkins.)

## Jenkings Dev vs Staging tests

There is a soft difference regarding what test suites get run and where 
The tests defined [wells_search_api_tests.json](./wells_search_api_tests.json) and [wells_search_api_tests.json](wells_search_api_tests.json) are scoped to only be running in the `dev` namespace. 

It's worth noting that when exporting from Jenkins, the filenames are named after the collection and not as the file you imported. Due to the difference in data sets between environments, these tests will fail in staging if named incorrectly.

## Running your tests locally
Running the tests through the following methods will load all the necessary environment variables locally into your terminal shell. These values don't persist outside of your shell. These commands will run **all** tests.

1. Have your Docker images running.
2. In your .envrc file, you need to populate the `GWELLS_API_TEST_CLIENT_SECRET` secret. This is obtainable from OpenShift under `[-tools]` -> `Secrets` -> `apitest-secrets`.
    - Optionally you can populate the `GWELLS_API_TEST_USER` and `GWELLS_API_TEST_PASSWORD` keys using OpenShift secrets or your own IDIR.
        - If these two fields are not populated, the terminal will prompt for input.
3. Run one of the following commands to run all the test suites:
    - From **api-tests**: `./run_local_all.sh`
    - From **root**: `make api-tests-local`
        - add the argument `TEST_FILE="your filename"` to run only one test suite

> <span style="color: red">Do not commit these secrets (even accidentally!).</span> 

## Creating New Tests

### Developing Tests

* Develop your API Tests in Postman
* Export the collection (this results in a json file)
* Create an accompanying Bash script
* The pipeline will run your tests and report back in Jenkins

### Bash Scripts

When you're developing new Postman collections, please create an accompanying bash script to run them easily! This will help with loading in env variables, running all test suites at once, and reducing errors.

> When creating your bash script, use the file structure `local_*.sh` This will ensure your tests are picked up by the `local_run_all.sh` script

Add this section of script to the top of your new bash script. It will check if the `GWELLS_API_TEST_USER` Environment variable is present, if it is not it will load in all the environment variables to your terminal from the `.envrc` file. This helps to make all tests run standalone while reducing the setup.

```bash
# Load ENVs to environment if not already present
if [ -z "$GWELLS_API_TEST_USER" ] && [ -f "./.envrc" ]; then
  source ./.envrc
  set -e
fi
```

You can also ensure that all necessary environment variables are loaded before running the test suites by adding: 

```bash
ENV_VARS=(
    # ...All Envs needed for your tests
)

for env_var in ${ENV_VARS[@]}
do
    if [ -z ${!env_var+x} ]; then 
        echo "$env_var is unset"
        exit
    fi
done
```
