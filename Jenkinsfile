pipeline {
  environment {
    // PR_NUM is the pull request number e.g. 'pr-4'
    PR_NUM = "${env.JOB_BASE_NAME}".toLowerCase()
    APP_NAME = "gwells"
    PROJECT = "moe-gwells-dev"
    TOOLS_PROJECT = "moe-gwells-tools"
    SERVER_ENV = "dev"
    REPOSITORY = 'https://www.github.com/bcgov/gwells'
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
              if ( !openshift.selector("bc", "${APP_NAME}-${SERVER_ENV}-${PR_NUM}").exists() ) {
                echo "Creating a new build config for pull request ${PR_NUM}"
                def buildtemplate = openshift.process("-f",
                  "openshift/backend.bc.json",
                  "NAME_SUFFIX=${SERVER_ENV}-${PR_NUM}",
                  "ENV_NAME=${SERVER_ENV}",
                  "SOURCE_REPOSITORY_URL=${REPOSITORY}/pull/${CHANGE_ID}"
                )
                openshift.create(buildtemplate)

                def dbtemplate = openshift.process("-f",
                  "openshift/postgresql.bc.json",
                  "NAME_SUFFIX=${SERVER_ENV}-${PR_NUM}",
                  "ENV_NAME=${SERVER_ENV}"
                )
                openshift.create(dbtemplate)
              }
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
              if ( !openshift.selector("dc", "${APP_NAME}-${SERVER_ENV}-${PR_NUM}").exists() ) {
                echo "Creating a new deployment config for pull request ${PR_NUM}"
                def deployTemplate = openshift.process("-f",
                  "openshift/backend.dc.json",
                  "NAME_SUFFIX=${SERVER_ENV}-${PR_NUM}",
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
                openshift.create(deployTemplate)
                openshift.create(deployDBTemplate)
              }


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
