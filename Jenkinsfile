pipeline {
  environment {
    // PR_NUM is the pull request number e.g. 'pr-4'
    PR_NUM = "${env.JOB_BASE_NAME}".toLowerCase()
    APP_NAME = "gwells"
    DEV_PROJECT = "moe-gwells-dev"
    TOOLS_PROJECT = "moe-gwells-tools"
    SERVER_ENV = "dev"
    REPOSITORY = 'https://www.github.com/bcgov/gwells.git'
  }
  agent any
  stages {
    stage('Start pipeline') {
      steps {
        script {
          abortAllPreviousBuildInProgress(currentBuild)
        }
      }
    }

    // create a new dev environment for this pull request
    // e.g. gwells-dev-pr-999
    stage('Initialize new DEV environment') {
      steps {
        script {
          openshift.withCluster() {
            openshift.withProject(TOOLS_PROJECT) {
              checkout scm

              // create a new build config if one does not already exist
              echo "Applying build config for pull request ${PR_NUM}"
              def buildtemplate = openshift.process("-f",
                "openshift/backend.bc.json",
                "NAME_SUFFIX=-${SERVER_ENV}-${PR_NUM}",
                "ENV_NAME=${SERVER_ENV}",
                "APP_IMAGE_TAG=${PR_NUM}",
                "SOURCE_REPOSITORY_URL=${REPOSITORY}",
                "SOURCE_REPOSITORY_REF=pull/${CHANGE_ID}/head"
              )

              def dbtemplate = openshift.process("-f",
                "openshift/postgresql.bc.json",
                "NAME_SUFFIX=-${SERVER_ENV}-${PR_NUM}",
                "ENV_NAME=${SERVER_ENV}"
              )

              // apply the template objects to create and/or modify objects in the dev environment
              openshift.apply(buildtemplate)
              openshift.apply(dbtemplate)
              
            }
          }
        }
      }
    }

    // run unit tests & build files
    // see /app/.s2i/assemble for image build script
    stage('Build (with tests)') {
      steps {
        script {
          openshift.withCluster() {
            openshift.withProject(TOOLS_PROJECT) {
              echo "Running unit tests and building images..."
              echo "This may take several minutes. Logs are not forwarded to Jenkins by default (at this time)."
              echo "Additional logs can be found by monitoring builds in ${TOOLS_PROJECT}"

              def appBuild = openshift.selector("bc", "${APP_NAME}-${SERVER_ENV}-${PR_NUM}")
              // ENABLE_DATA_ENTRY=True is temporarily set during testing because False currently leads to a failing unit test
              appBuild.startBuild("--wait", "--env=ENABLE_DATA_ENTRY=True")  
            }
          }
        }
      }
    }

    // Deployment to dev happens automatically when a new image is tagged `dev`.
    // This stage monitors the newest deployment for pods/containers to report back as ready.
    stage('Deploy to dev') {
      steps {
        script {
          openshift.withCluster() {
            openshift.withProject(DEV_PROJECT) {     

              // process templates. deployTemplate and deployDBTemplate will contain sets of model specs
              echo "Creating a new deployment config for pull request ${PR_NUM}"
              def deployTemplate = openshift.process("-f",
                "openshift/backend.dc.json",
                "NAME_SUFFIX=-${SERVER_ENV}-${PR_NUM}",
                "BUILD_ENV_NAME=${SERVER_ENV}",
                "ENV_NAME=${SERVER_ENV}",
                "HOST=${APP_NAME}-${SERVER_ENV}-${PR_NUM}.pathfinder.gov.bc.ca",
              )

              def deployDBTemplate = openshift.process("-f",
                "openshift/postgresql.dc.json",
                "LABEL_APPVER=-${SERVER_ENV}-${PR_NUM}",
                "DATABASE_SERVICE_NAME=gwells-pgsql-${SERVER_ENV}-${PR_NUM}",
                "IMAGE_STREAM_NAMESPACE=''",
                "IMAGE_STREAM_NAME=gwells-postgresql-${SERVER_ENV}-${PR_NUM}",
                "IMAGE_STREAM_VERSION=${SERVER_ENV}",
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

              // apply the templates, which will create new objects or modify existing ones as necessary.
              // the copies of base objects (secrets, configmaps) are also applied.
              openshift.apply(deployTemplate).label(['app':"gwells-${SERVER_ENV}-${PR_NUM}", 'app-name':"${APP_NAME}", 'env-name':"${SERVER_ENV}"], "--overwrite")
              openshift.apply(deployDBTemplate).label(['app':"gwells-${SERVER_ENV}-${PR_NUM}", 'app-name':"${APP_NAME}", 'env-name':"${SERVER_ENV}"], "--overwrite")
              openshift.apply(newObjectCopies).label(['app':"gwells-${SERVER_ENV}-${PR_NUM}", 'app-name':"${APP_NAME}", 'env-name':"${SERVER_ENV}"], "--overwrite")
              echo "Successfully applied deployment configs for ${PR_NUM}"

              // promote the newly built image to DEV
              echo "Tagging new image to DEV imagestream."
              openshift.tag("${TOOLS_PROJECT}/gwells-application:${PR_NUM}", "${DEV_PROJECT}/gwells-${SERVER_ENV}-${PR_NUM}:dev")  // todo: clean up labels/tags
          
              // monitor the deployment status and wait until deployment is successful
              echo "Waiting for deployment to dev..."
              def newVersion = openshift.selector("dc", "${APP_NAME}-${SERVER_ENV}-${PR_NUM}").object().status.latestVersion
              def pods = openshift.selector('pod', [deployment: "${APP_NAME}-${SERVER_ENV}-${PR_NUM}-${newVersion}"])

              // wait until each container in this deployment's pod reports as ready
              pods.untilEach(1) {
                return it.object().status.containerStatuses.every {
                  it.ready
                }
              }
              echo "Deployment successful!"
            }
          }
        }
      }
    }

    stage('API Tests') {
      steps {
        script {
          podTemplate(
                label: "nodejs-${context.uuid}",
                name: "nodejs-${context.uuid}",
                serviceAccount: 'jenkins',
                cloud: 'openshift',
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
                node("nodejs-${context.uuid}") {
                    checkout scm
                    dir('api-tests') {
                        sh 'npm install -g newman'
                        String BASEURL = "${APP_NAME}-${SERVER_ENV}-${PR_NUM}.pathfinder.gov.bc.ca/gwells"
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
  }
}
