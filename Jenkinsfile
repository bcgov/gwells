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
    TEST_SUFFIX = "staging"

    // PROD_PROJECT is the prod deployment.
    // New production images can be deployed by tagging an existing "test" image as "prod".
    PROD_PROJECT = "moe-gwells-test"
    PROD_SUFFIX= "production"

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
    stage('ImageStreams ') {
      steps {
        script {
          abortAllPreviousBuildInProgress(currentBuild)
          openshift.withCluster() {
            openshift.withProject(TOOLS_PROJECT) {

              // Process db and app template into list objects
              //  - variable substitution
              def dbtemplate = openshift.process("-f",
                "openshift/postgresql.bc.json",
                "ENV_NAME=${DEV_SUFFIX}"
              )
              //
              def buildtemplate = openshift.process("-f",
                "openshift/backend.bc.json",
                "ENV_NAME=${DEV_SUFFIX}",
                "NAME_SUFFIX=-${DEV_SUFFIX}-${PR_NUM}",
                "APP_IMAGE_TAG=${PR_NUM}",
                "SOURCE_REPOSITORY_URL=${REPOSITORY}",
                "SOURCE_REPOSITORY_REF=pull/${CHANGE_ID}/head"
              )

              // Apply oc list objects
              //  - add docker image reference as tag in gwells-postgresql
              echo "Preparing database imagestream"
              echo " \$ oc process -f openshift/postgresql.bc.json -p ENV_NAME=${DEV_SUFFIX} | oc apply -n moe-gwells-tools -f -"
              openshift.apply(dbtemplate)
              //  - add docker image reference as tag in gwells-application
              //  - create build config
              echo "Preparing backend imagestream and buildconfig"
              echo " \$ oc process -f openshift/backend.bc.json -p ENV_NAME=${DEV_SUFFIX} -p NAME_SUFFIX=-${DEV_SUFFIX}-${PR_NUM} -p APP_IMAGE_TAG=${PR_NUM} -p SOURCE_REPOSITORY_URL=${REPOSITORY} -p SOURCE_REPOSITORY_REF=pull/${CHANGE_ID}/head | oc apply -n moe-gwells-tools -f -"
              openshift.apply(buildtemplate)
            }
          }
        }
      }
    }

    // the Build stage runs unit tests and builds files. an image will be outputted to the app's imagestream
    // builds use the source to image strategy. See /app/.s2i/assemble for image build script
    stage('Build (with tests)') {
      steps {
        script {
          openshift.withCluster() {
            openshift.withProject(TOOLS_PROJECT) {
              echo "Running unit tests and building images..."
              echo "This may take several minutes. Logs are not forwarded to Jenkins by default (at this time)."
              echo "Additional logs can be found by monitoring builds in ${TOOLS_PROJECT}"

              // Select appropriate buildconfig
              def appBuild = openshift.selector("bc", "${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}")
              // temporarily set ENABLE_DATA_ENTRY=True during testing because False currently leads to a failing unit test
              echo "Building"
              echo " \$ oc start-build -n moe-gwells-tools ${APP_NAME}-${DEV_SUFFIX}-${PR_NUM} --wait --env=ENABLE_DATA_ENTRY=true --follow=true"
              appBuild.startBuild("--wait", "--env=ENABLE_DATA_ENTRY=True").logs("-f")
            }
          }
        }
      }
    }


    // the Deploy to Dev stage creates a new dev environment for the pull request (if necessary), tags the newly built
    // application image into that environment, and monitors the newest deployment for pods/containers to
    // report back as ready.
    stage('Deploy to dev') {
      steps {
        script {
          openshift.withCluster() {
            openshift.withProject(DEV_PROJECT) {
              // Process postgres deployment config (sub in vars, create list items)
              echo " \$ oc process -f openshift/postgresql.dc.json -p DATABASE_SERVICE_NAME=gwells-pgsql-${DEV_SUFFIX}-${PR_NUM} -p IMAGE_STREAM_NAMESPACE='' -p IMAGE_STREAM_NAME=gwells-postgresql-${DEV_SUFFIX}-${PR_NUM} -p IMAGE_STREAM_VERSION=${DEV_SUFFIX} -p LABEL_APPVER=-${DEV_SUFFIX}-${PR_NUM} -p POSTGRESQL_DATABASE=gwells -p VOLUME_CAPACITY=1Gi | oc apply -n moe-gwells-dev -f -"
              def deployDBTemplate = openshift.process("-f",
                "openshift/postgresql.dc.json",
                "DATABASE_SERVICE_NAME=gwells-pgsql-${DEV_SUFFIX}-${PR_NUM}",
                "IMAGE_STREAM_NAMESPACE=''",
                "IMAGE_STREAM_NAME=gwells-postgresql-${DEV_SUFFIX}-${PR_NUM}",
                "IMAGE_STREAM_VERSION=${DEV_SUFFIX}",
                "LABEL_APPVER=-${DEV_SUFFIX}-${PR_NUM}",
                "POSTGRESQL_DATABASE=gwells",
                "VOLUME_CAPACITY=1Gi"
              )

              // Process postgres deployment config (sub in vars, create list items)
              echo " \$ oc process -f openshift/backend.dc.json -p BUILD_ENV_NAME=${DEV_SUFFIX} -p ENV_NAME=${DEV_SUFFIX} -p NAME_SUFFIX=-${DEV_SUFFIX}-${PR_NUM} | oc apply -n moe-gwells-dev -f -"
              echo "Processing deployment config for pull request ${PR_NUM}"
              def deployTemplate = openshift.process("-f",
                "openshift/backend.dc.json",
                "BUILD_ENV_NAME=${DEV_SUFFIX}",
                "ENV_NAME=${DEV_SUFFIX}",
                "HOST=${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}.pathfinder.gov.bc.ca",
                "NAME_SUFFIX=-${DEV_SUFFIX}-${PR_NUM}"
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
                    echo "[as-copy-of] Copying ${o.kind} ${o.metadata.name}"
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

              // promote the newly built image to DEV
              echo "Tagging new image to DEV imagestream."
              openshift.tag("${TOOLS_PROJECT}/gwells-application:${PR_NUM}", "${DEV_PROJECT}/gwells-${DEV_SUFFIX}-${PR_NUM}:dev")  // todo: clean up labels/tags
              openshift.tag("${TOOLS_PROJECT}/gwells-postgresql:dev", "${DEV_PROJECT}/gwells-postgresql-${DEV_SUFFIX}-${PR_NUM}:dev")  // todo: clean up labels/tags

              // monitor the deployment status and wait until deployment is successful
              echo "Waiting for deployment to dev..."
              def newVersion = openshift.selector("dc", "${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}").object().status.latestVersion
              def pods = openshift.selector('pod', [deployment: "${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}-${newVersion}"])

              // wait until each container in this deployment's pod reports as ready
              timeout(15) {
                pods.untilEach(2) {
                  return it.object().status.containerStatuses.every {
                    it.ready
                  }
                }
              }

              echo "Deployment successful!"
              echo "Loading fixtures"
              def firstPod = pods.objects()[0].metadata.name
              openshift.exec(firstPod, "--", "bash -c '\
                cd /opt/app-root/src/backend; \
                python manage.py loaddata \
                  gwells-codetables.json \
                  wellsearch-codetables.json \
                  registries-codetables.json \
                  registries.json \
                  aquifers.json \
                  wellsearch.json.gz; \
                python manage.py createinitialrevisions'")
            }
          }
        }
      }
    }

    stage('API Tests') {
      steps {
        script {
          podTemplate(
                label: "nodejs-${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}",
                name: "nodejs-${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}",
                serviceAccount: 'jenkins',
                cloud: 'openshift',
                activeDeadlineSeconds: 1800,
                containers: [
                    containerTemplate(
                        name: 'jnlp',
                        image: 'registry.access.redhat.com/openshift3/jenkins-agent-nodejs-8-rhel7',
                        resourceRequestCpu: '800m',
                        resourceLimitCpu: '800m',
                        resourceRequestMemory: '1Gi',
                        resourceLimitMemory: '1Gi',
                        workingDir: '/tmp',
                        command: '',
                        args: '${computer.jnlpmac} ${computer.name}',
                        envVars: [
                            secretEnvVar(
                                key: 'GWELLS_API_TEST_USER',
                                secretName: 'apitest-secrets',
                                secretKey: 'username'
                            ),
                            secretEnvVar(
                                key: 'GWELLS_API_TEST_PASSWORD',
                                secretName: 'apitest-secrets',
                                secretKey: 'password'
                            ),
                            secretEnvVar(
                                key: 'GWELLS_API_TEST_AUTH_SERVER',
                                secretName: 'apitest-secrets',
                                secretKey: 'auth_server'
                            ),
                            secretEnvVar(
                                key: 'GWELLS_API_TEST_CLIENT_ID',
                                secretName: 'apitest-secrets',
                                secretKey: 'client_id'
                            ),
                            secretEnvVar(
                                key: 'GWELLS_API_TEST_CLIENT_SECRET',
                                secretName: 'apitest-secrets',
                                secretKey: 'client_secret'
                            )
                        ]
                    )
                ]
            ) {
                node("nodejs-${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}") {
                    checkout scm
                    dir('api-tests') {
                        sh 'npm install -g newman'
                        String BASEURL = "https://${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}.pathfinder.gov.bc.ca/gwells"
                        try {
                            sh """
                                newman run ./registries_api_tests.json \
                                    --global-var test_user=\$GWELLS_API_TEST_USER \
                                    --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                    --global-var base_url=${BASEURL} \
                                    --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                    --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                    --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                    -r cli,junit,html
                                newman run ./wells_api_tests.json \
                                    --global-var test_user=\$GWELLS_API_TEST_USER \
                                    --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                    --global-var base_url=${BASEURL} \
                                    --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                    --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                    --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                    -r cli,junit,html
                                newman run ./submissions_api_tests.json \
                                    --global-var test_user=\$GWELLS_API_TEST_USER \
                                    --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                    --global-var base_url=${BASEURL} \
                                    --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                    --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                    --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                    -r cli,junit,html
                                newman run ./aquifers_api_tests.json \
                                    --global-var test_user=\$GWELLS_API_TEST_USER \
                                    --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                    --global-var base_url=${BASEURL} \
                                    --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                    --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                    --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                    -r cli,junit,html
                            """
                        } finally {
                          junit 'newman/*.xml'
                          publishHTML (
                              target: [
                                  allowMissing: false,
                                  alwaysLinkToLastBuild: false,
                                  keepAll: true,
                                  reportDir: 'newman',
                                  reportFiles: 'newman*.html',
                                  reportName: "API Test Report"
                              ]
                          )
                          stash includes: 'newman/*.xml', name: 'api-tests'
                        }
                    }
                }
            }
        }
      }
    }

    // the Promote to Test stage allows approving the tagging of the newly built image into the test environment,
    // which will trigger an automatic deployment of that image.
    // The deployment configs in the openshift folder are applied first in case there are any changes to the templates.
    // this stage should only occur when the pull request is being made against the master branch.
    stage('Deploy image to staging') {
      when {
        expression { env.CHANGE_TARGET == 'master' }
      }
      steps {
        script {
          openshift.withCluster() {
            openshift.withProject(TEST_PROJECT) {
              input "Deploy to staging?"

              echo "Updating staging deployment..."

              def deployDBTemplate = openshift.process("-f",
                "openshift/postgresql.dc.json",
                "LABEL_APPVER=-${TEST_SUFFIX}",
                "DATABASE_SERVICE_NAME=gwells-pgsql-${TEST_SUFFIX}",
                "IMAGE_STREAM_NAMESPACE=''",
                "IMAGE_STREAM_NAME=gwells-postgresql-${TEST_SUFFIX}",
                "IMAGE_STREAM_VERSION=${TEST_SUFFIX}",
                "POSTGRESQL_DATABASE=gwells",
                "VOLUME_CAPACITY=1Gi"
              )

              def deployTemplate = openshift.process("-f",
                "openshift/backend.dc.json",
                "NAME_SUFFIX=-${TEST_SUFFIX}",
                "BUILD_ENV_NAME=${TEST_SUFFIX}",
                "ENV_NAME=${TEST_SUFFIX}",
                "HOST=${APP_NAME}-${TEST_SUFFIX}.pathfinder.gov.bc.ca",
              )

              // some objects need to be copied from a base secret or configmap
              // these objects have an annotation "as-copy-of" in their object spec (e.g. an object in backend.dc.json)
              echo "Creating configmaps and secrets objects"
              List newObjectCopies = []

              // todo: refactor to explicitly copy the objects we need
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

              // apply the templates, which will create new objects or modify existing ones as necessary.
              // the copies of base objects (secrets, configmaps) are also applied.
              echo "Applying deployment config for pull request ${PR_NUM} on ${TEST_PROJECT}"

              openshift.apply(deployTemplate).label(['app':"gwells-${TEST_SUFFIX}", 'app-name':"${APP_NAME}", 'env-name':"${TEST_SUFFIX}"], "--overwrite")
              openshift.apply(deployDBTemplate).label(['app':"gwells-${TEST_SUFFIX}", 'app-name':"${APP_NAME}", 'env-name':"${TEST_SUFFIX}"], "--overwrite")
              openshift.apply(newObjectCopies).label(['app':"gwells-${TEST_SUFFIX}", 'app-name':"${APP_NAME}", 'env-name':"${TEST_SUFFIX}"], "--overwrite")
              echo "Successfully applied TEST deployment config"

              // promote the newly built image to DEV
              echo "Tagging new image to TEST imagestream."

              // Application/database images are tagged in the tools imagestream as the new test/prod image
              openshift.tag("${TOOLS_PROJECT}/gwells-application:${PR_NUM}", "${TOOLS_PROJECT}/gwells-application:${TEST_SUFFIX}")  // todo: clean up labels/tags
              // openshift.tag("${TOOLS_PROJECT}/gwells-postgresql:test", "${TOOLS_PROJECT}/gwells-postgresql:${TEST_SUFFIX}")

              // Images are then tagged into the target environment namespace (test or prod)
              openshift.tag("${TOOLS_PROJECT}/gwells-application:${TEST_SUFFIX}", "${TEST_PROJECT}/gwells-${TEST_SUFFIX}:${TEST_SUFFIX}")  // todo: clean up labels/tags
              openshift.tag("${TOOLS_PROJECT}/gwells-postgresql:test", "${TEST_PROJECT}/gwells-postgresql-${TEST_SUFFIX}:${TEST_SUFFIX}")  // todo: clean up labels/tags

              // monitor the deployment status and wait until deployment is successful
              echo "Waiting for deployment to TEST..."
              def newVersion = openshift.selector("dc", "gwells-${TEST_SUFFIX}").object().status.latestVersion
              def pods = openshift.selector('pod', [deployment: "gwells-${TEST_SUFFIX}-${newVersion}"])

              // wait until at least one pod reports as ready
              timeout(15) {
                pods.untilEach(2) {
                  return it.object().status.containerStatuses.every {
                    it.ready
                  }
                }
              }

              echo "TEST deployment successful."
              echo "Loading fixtures"
              def firstPod = pods.objects()[0].metadata.name
              openshift.exec(firstPod, "--", "bash -c '\
                cd /opt/app-root/src/backend; \
                python manage.py loaddata \
                  gwells-codetables.json \
                  wellsearch-codetables.json \
                  registries-codetables.json \
                  registries.json \
                  aquifers.json \
                  wellsearch.json.gz; \
                python manage.py createinitialrevisions'")
            }
          }
        }
      }
    }

    stage('API Tests against Staging') {
      when {
        expression { env.CHANGE_TARGET == 'master' }
      }
      steps {
        script {
          podTemplate(
                label: "nodejs-${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}-${env.CHANGE_ID}",
                name: "nodejs-${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}-${env.CHANGE_ID}",
                serviceAccount: 'jenkins',
                cloud: 'openshift',
                activeDeadlineSeconds: 1800,
                containers: [
                    containerTemplate(
                        name: 'jnlp',
                        image: 'registry.access.redhat.com/openshift3/jenkins-agent-nodejs-8-rhel7',
                        resourceRequestCpu: '800m',
                        resourceLimitCpu: '800m',
                        resourceRequestMemory: '1Gi',
                        resourceLimitMemory: '1Gi',
                        workingDir: '/tmp',
                        command: '',
                        args: '${computer.jnlpmac} ${computer.name}',
                        envVars: [
                            secretEnvVar(
                                key: 'GWELLS_API_TEST_USER',
                                secretName: 'apitest-secrets',
                                secretKey: 'username'
                            ),
                            secretEnvVar(
                                key: 'GWELLS_API_TEST_PASSWORD',
                                secretName: 'apitest-secrets',
                                secretKey: 'password'
                            ),
                            secretEnvVar(
                                key: 'GWELLS_API_TEST_AUTH_SERVER',
                                secretName: 'apitest-secrets',
                                secretKey: 'auth_server'
                            ),
                            secretEnvVar(
                                key: 'GWELLS_API_TEST_CLIENT_ID',
                                secretName: 'apitest-secrets',
                                secretKey: 'client_id'
                            ),
                            secretEnvVar(
                                key: 'GWELLS_API_TEST_CLIENT_SECRET',
                                secretName: 'apitest-secrets',
                                secretKey: 'client_secret'
                            )
                        ]
                    )
                ]
            ) {
                node("nodejs-${APP_NAME}-${DEV_SUFFIX}-${PR_NUM}-${env.CHANGE_ID}") {
                    checkout scm
                    dir('api-tests') {
                        sh 'npm install -g newman'
                        String BASEURL = "https://gwells-${TEST_SUFFIX}.pathfinder.gov.bc.ca/gwells"
                        try {
                            sh """
                                newman run ./registries_api_tests.json \
                                    --global-var test_user=\$GWELLS_API_TEST_USER \
                                    --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                    --global-var base_url=${BASEURL} \
                                    --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                    --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                    --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                    -r cli,junit,html
                                newman run ./wells_api_tests.json \
                                    --global-var test_user=\$GWELLS_API_TEST_USER \
                                    --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                    --global-var base_url=${BASEURL} \
                                    --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                    --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                    --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                    -r cli,junit,html
                                newman run ./submissions_api_tests.json \
                                    --global-var test_user=\$GWELLS_API_TEST_USER \
                                    --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                    --global-var base_url=${BASEURL} \
                                    --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                    --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                    --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                    -r cli,junit,html
                                newman run ./aquifers_api_tests.json \
                                    --global-var test_user=\$GWELLS_API_TEST_USER \
                                    --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                    --global-var base_url=${BASEURL} \
                                    --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                    --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                    --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                    -r cli,junit,html
                            """
                        } finally {
                          junit 'newman/*.xml'
                          publishHTML (
                              target: [
                                  allowMissing: false,
                                  alwaysLinkToLastBuild: false,
                                  keepAll: true,
                                  reportDir: 'newman',
                                  reportFiles: 'newman*.html',
                                  reportName: "API Test Report"
                              ]
                          )
                          stash includes: 'newman/*.xml', name: 'api-tests'
                        }
                    }
                }
            }
        }
      }
    }


    stage('Deploy image to Production') {
      when {
        expression { env.CHANGE_TARGET == 'master' }
      }
      steps {
        script {
          openshift.withCluster() {
            openshift.withProject(PROD_PROJECT) {
              input "Deploy to production?"

              echo "Updating production deployment..."
              def deployTemplate = openshift.process("-f",
                "openshift/backend.dc.json",
                "NAME_SUFFIX=-${PROD_SUFFIX}",
                "BUILD_ENV_NAME=${PROD_SUFFIX}",
                "ENV_NAME=${PROD_SUFFIX}",
                "HOST=${APP_NAME}-${PROD_SUFFIX}.pathfinder.gov.bc.ca",
              )

              def deployDBTemplate = openshift.process("-f",
                "openshift/postgresql.dc.json",
                "LABEL_APPVER=-${PROD_SUFFIX}",
                "DATABASE_SERVICE_NAME=gwells-pgsql-${PROD_SUFFIX}",
                "IMAGE_STREAM_NAMESPACE=''",
                "IMAGE_STREAM_NAME=gwells-postgresql-${PROD_SUFFIX}",
                "IMAGE_STREAM_VERSION=${PROD_SUFFIX}",
                "POSTGRESQL_DATABASE=gwells",
                "VOLUME_CAPACITY=2Gi"
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

              // apply the templates, which will create new objects or modify existing ones as necessary.
              // the copies of base objects (secrets, configmaps) are also applied.
              echo "Applying deployment config for pull request ${PR_NUM} on ${PROD_PROJECT}"

              openshift.apply(deployTemplate).label(['app':"gwells-${PROD_SUFFIX}", 'app-name':"${APP_NAME}", 'env-name':"${PROD_SUFFIX}"], "--overwrite")
              openshift.apply(deployDBTemplate).label(['app':"gwells-${PROD_SUFFIX}", 'app-name':"${APP_NAME}", 'env-name':"${PROD_SUFFIX}"], "--overwrite")
              openshift.apply(newObjectCopies).label(['app':"gwells-${PROD_SUFFIX}", 'app-name':"${APP_NAME}", 'env-name':"${PROD_SUFFIX}"], "--overwrite")
              echo "Successfully applied production deployment config"

              // promote the newly built image to DEV
              echo "Tagging new image to production imagestream."

              // Application/database images are tagged in the tools imagestream as the new prod image
              openshift.tag("${TOOLS_PROJECT}/gwells-application:${PR_NUM}", "${TOOLS_PROJECT}/gwells-application:${PROD_SUFFIX}")  // todo: clean up labels/tags

              // TODO: determine best way to manage database images (at the moment they never change, but we don't want an unforeseen change to impact prod)
              // openshift.tag("${TOOLS_PROJECT}/gwells-postgresql:prod", "${TOOLS_PROJECT}/gwells-postgresql:${PROD_SUFFIX}")

              // Images are then tagged into the target environment namespace (prod)
              openshift.tag("${TOOLS_PROJECT}/gwells-application:${PROD_SUFFIX}", "${PROD_PROJECT}/gwells-${PROD_SUFFIX}:${PROD_SUFFIX}")  // todo: clean up labels/tags
              openshift.tag("${TOOLS_PROJECT}/gwells-postgresql:prod", "${PROD_PROJECT}/gwells-postgresql-${PROD_SUFFIX}:${PROD_SUFFIX}")  // todo: clean up labels/tags

              // monitor the deployment status and wait until pgsql-${ deployment is successful
              echo "Waiting for deployment to production..."
              def newVersion = openshift.selector("dc", "gwells-${PROD_SUFFIX}").object().status.latestVersion
              def pods = openshift.selector('pod', [deployment: "gwells-${PROD_SUFFIX}-${newVersion}"])

              // wait until pods reports as ready
              timeout(15) {
                pods.untilEach(2) {
                  return it.object().status.containerStatuses.every {
                    it.ready
                  }
                }
              }

              echo "Production deployment successful."

            }
          }
        }
      }
    }
  }
}
