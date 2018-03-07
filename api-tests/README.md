# API Tests

The API tests use [Newman](https://www.npmjs.com/package/newman) to run the tests that are created in [Postman](https://www.getpostman.com).

* Develop your API Tests in Postman
* Export the collection (this results in a json file)
* Update the runnewman.sh to point to your json file
* The pipeline will run your tests and report back in Jenkins

Please note that the API tests use 2 environment variables for user and password:
* GWELLS_API_TEST_USER
* GWELLS_API_TEST_PASSWORD

They are both populated from the apitest-secrets secret.
This user/pw has been created in our dev database.

