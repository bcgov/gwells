pipeline {
  environment {

    APP_NAME = "gwells"
    REPOSITORY = 'https://www.github.com/bcgov/gwells.git'

    // TOOLS_PROJECT is where images are built
    TOOLS_PROJECT = "moe-gwells-tools"

    // DEV_PROJECT is the project where individual development environments are spun up
    // for example: a pull request PR-999 will result in gwells-dev-pr-999.pathfinder.gov.bc.ca
    DEV_PROJECT = "moe-gwells-dev"
    DEV_SUFFIX = "dev"

    // TEST_PROJECT contains the test deployment. The test image is a candidate for promotion to prod.
    TEST_PROJECT = "moe-gwells-test"
    TEST_SUFFIX = "test-sth"

    // PROD_PROJECT is the prod deployment.
    // New production images can be deployed by tagging an existing "test" image as "prod".
    PROD_PROJECT = "moe-gwells-test"
    PROD_SUFFIX= "prod-test-sth"

    // PR_NUM is the pull request number e.g. 'pr-4'
    PR_NUM = "${env.JOB_BASE_NAME}".toLowerCase()
  }
  agent any
  stages {

    // the Start Pipeline stage will process and apply OpenShift build templates which will create
    // buildconfigs and an imagestream for built images.
    // each pull request gets its own buildconfig but all new builds are pushed to a single imagestream,
    // to be tagged with the pull request number.
    // e.g.:  gwells-app:pr-999
    stage('Start pipeline') {
      steps {
        script {
          abortAllPreviousBuildInProgress(currentBuild)
          openshift.withCluster() {
            openshift.withProject(TOOLS_PROJECT) {
              // create a new build config if one does not already exist
              echo "Applying build configuration..."
              def buildtemplate = openshift.process("-f",
                "openshift/backend.bc.json",
                "NAME_SUFFIX=-${DEV_SUFFIX}-${PR_NUM}",
                "ENV_NAME=${DEV_SUFFIX}",
                "APP_IMAGE_TAG=${PR_NUM}",
                "SOURCE_REPOSITORY_URL=${REPOSITORY}",
                "SOURCE_REPOSITORY_REF=pull/${CHANGE_ID}/head"
              )

              // database build/imagestream template
              def dbtemplate = openshift.process("-f",
                "openshift/postgresql.bc.json",
                "NAME_SUFFIX=-${DEV_SUFFIX}-${PR_NUM}",
                "ENV_NAME=${DEV_SUFFIX}"
              )

              // apply the template objects to create and/or modify objects in the dev environment
              openshift.apply(buildtemplate)
              openshift.apply(dbtemplate)
            }

            openshift.withProject(DEV_PROJECT) {
              // process templates. deployTemplate and deployDBTemplate will contain sets of model specs
              echo "Processing deployment config for pull request ${PR_NUM}"
              def deployTemplate = openshift.process("-f",
                "openshift/backend.dc.json",
                "NAME_SUFFIX=-${DEV_SUFFIX}-${PR_NUM}",
                "BUILD_ENV_NAME=${DEV_SUFFIX}",
                "ENV_NAME=${DEV_SUFFIX}",
                "HOST=${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}.pathfinder.gov.bc.ca",
              )

              def deployDBTemplate = openshift.process("-f",
                "openshift/postgresql.dc.json",
                "LABEL_APPVER=-${DEV_SUFFIX}-${PR_NUM}",
                "DATABASE_SERVICE_NAME=gwells-pgsql-${DEV_SUFFIX}-${PR_NUM}",
                "IMAGE_STREAM_NAMESPACE=''",
                "IMAGE_STREAM_NAME=gwells-postgresql-${DEV_SUFFIX}-${PR_NUM}",
                "IMAGE_STREAM_VERSION=${DEV_SUFFIX}",
                "POSTGRESQL_DATABASE=gwells",
                "VOLUME_CAPACITY=1Gi"
              )

              // some objects need to be copied from a base secret or configmap
              // these objects have an annotation "as-copy-of" in their object spec (e.g. an object in backend.dc.json)
              echo "Creating configmaps and secrets objects"
              List newObjectCopies = []

              for (o in (deployTemplate + deployDBTemplate)) {

                // only perform this operation on objects with 'as-copy-of'
                def sourceName = o.metadata && o.metadata.annotations && o.metadata.annotations['as-copy-of']
                if (sourceName && sourceName.length() > 0) {
                  def selector = openshift.selector("${o.kind}/${sourceName}")
                  if (selector.count() == 1) {

                    // create a copy of the object and add it to the new list of objects to be applied
                    Map copiedModel = selector.object(exportable:true)
                    copiedModel.metadata.name = o.metadata.name
                    echo "Copying ${o.kind} ${o.metadata.name}"
                    newObjectCopies.add(copiedModel)
                  }
                }
              }


              echo "Applying deployment config for pull request ${PR_NUM} on ${DEV_PROJECT}"

              // apply the templates, which will create new objects or modify existing ones as necessary.
              // the copies of base objects (secrets, configmaps) are also applied.
              openshift.apply(deployTemplate).label(['app':"gwells-${DEV_SUFFIX}-${PR_NUM}", 'app-name':"${APP_NAME}", 'env-name':"${DEV_SUFFIX}"], "--overwrite")
              openshift.apply(deployDBTemplate).label(['app':"gwells-${DEV_SUFFIX}-${PR_NUM}", 'app-name':"${APP_NAME}", 'env-name':"${DEV_SUFFIX}"], "--overwrite")
              openshift.apply(newObjectCopies).label(['app':"gwells-${DEV_SUFFIX}-${PR_NUM}", 'app-name':"${APP_NAME}", 'env-name':"${DEV_SUFFIX}"], "--overwrite")
              echo "Successfully applied deployment configs for ${PR_NUM}"

            }
            openshift.withProject(TOOLS_PROJECT) {
              def appBuild = openshift.selector("bc", "${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}")
              // temporarily set ENABLE_DATA_ENTRY=True during testing because False currently leads to a failing unit test
              appBuild.startBuild("--wait", "--env=ENABLE_DATA_ENTRY=True").logs("-f")
            }
          }
        }
      }
    }
  }
}
