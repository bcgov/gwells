pipeline {
  environment {
    // PR_NUM is the pull request number e.g. 'pr-4'
    PR_NUM = "${env.JOB_BASE_NAME}".toLowerCase()
    APP_NAME = "gwells"
    PROJECT = "moe-gwells-dev"
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

    // create a new environment for this pull request
    // e.g. gwells-dev-pr-999
    stage('Initialize new DEV environment') {
      steps {
        script {
          openshift.withCluster() {
            openshift.withProject(TOOLS_PROJECT) {
              checkout scm

              // create a new build config if one does not already exist
                echo "Creating a new build config for pull request ${PR_NUM}"
                def buildtemplate = openshift.process("-f",
                  "openshift/backend.bc.json",
                  "NAME_SUFFIX=-${SERVER_ENV}-${PR_NUM}",
                  "ENV_NAME=${SERVER_ENV}",
                  "SOURCE_REPOSITORY_URL=${REPOSITORY}",
                  "SOURCE_REPOSITORY_REF=pull/${CHANGE_ID}/head"
                )
                openshift.apply(buildtemplate)

                def dbtemplate = openshift.process("-f",
                  "openshift/postgresql.bc.json",
                  "NAME_SUFFIX=-${SERVER_ENV}-${PR_NUM}",
                  "ENV_NAME=${SERVER_ENV}"
                )
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

              // start building the base image. In the future, we should only have to do this once. (future improvement)
              def baseBuild = openshift.selector("bc", "gwells-python-runtime-${SERVER_ENV}-${PR_NUM}")
              baseBuild.startBuild("--wait")
              def appBuild = openshift.selector("bc", "${APP_NAME}-${SERVER_ENV}-${PR_NUM}")
              appBuild.startBuild("--wait")
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
            openshift.withProject(PROJECT) {     
              // if a deployment config does not exist for this pull request, create one
              
                echo "Creating a new deployment config for pull request ${PR_NUM}"
                def deployTemplate = openshift.process("-f",
                  "openshift/backend.dc.json",
                  "NAME_SUFFIX=-${SERVER_ENV}-${PR_NUM}",
                  "BUILD_ENV_NAME=",
                  "ENV_NAME=${SERVER_ENV}",
                  "HOST=${APP_NAME}-${SERVER_ENV}-${PR_NUM}.pathfinder.gov.bc.ca",
                )

                def deployDBTemplate = openshift.process("-f",
                  "openshift/postgresql.dc.json",
                  "DATABASE_SERVICE_NAME=gwells-pgsql${SERVER_ENV}-${PR_NUM}",
                  "IMAGE_STREAM_NAMESPACE=''",
                  "IMAGE_STREAM_NAME=gwells-postgresql${SERVER_ENV}-${PR_NUM}",
                  "IMAGE_STREAM_VERSION=${SERVER_ENV}",
                  "POSTGRESQL_DATABASE=gwells",
                  "VOLUME_CAPACITY=1Gi"
                )
                openshift.apply(deployTemplate)
                openshift.apply(deployDBTemplate)
              


              echo "Waiting for deployment to dev..."
              def newVersion = openshift.selector("dc", "${APP_NAME}-${PR_NUM}").object().status.latestVersion

              // find the pods for the newest deployment
              def pods = openshift.selector('pod', [deployment: "${APP_NAME}-${PR_NUM}-${newVersion}"])

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
  }
}

// ERROR: process returned an error;
// {reference={}, err=error: unable to process template
//   Required value: template.parameters[1]: parameter BUILD_ENV_NAME is required and must be specified, verb=process, cmd=oc --server=https://172.50.0.1:443 --certificate-authority=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt --namespace=moe-gwells-dev --token=XXXXX process -f openshift/backend.dc.json NAME_SUFFIX=-dev-pr-935 BUILD_ENV_NAME= ENV_NAME=dev HOST=gwells-dev-pr-935.pathfinder.gov.bc.ca -o=json , out=, status=1}

// Finished: FAILURE