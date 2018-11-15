#!groovy

// Cron job for postgres vacuum and replication
//
//  Setup in Jenkins:
//  > Folder > New Item > Pipeline
//  > Pipeline > Definition > Pipeline script from SCM
//    SCM: Git
//      Repository URL: https://github.com/bcgov/gwells
//      Branches to build: */master
//      Script path: scripts/Jenkinsfiles/pg_replicate


// Cronjob time (in UTC)
properties(
    [
        pipelineTriggers(
            [
                cron( 'H 11 * * 1-6' )
            ]
        )
    ]
)


// String APP_DC = 'gwells-dev-pr-1012'
pipeline {
    environment {
        // Project name (moe-gwells-test|moe-gwells-prod)
        String PROJECT = 'moe-gwells-dev'

        // Deployment configs
        String APP_DC = 'gwells-dev-pr-1012'
        String DB_DC  = 'gwells-pgsql-dev-pr-1012'

        // Routes and ports
        String APP_NAME = 'gwells-dev-pr-1012'
        String APP_PORT = 'web'
        String MNT_NAME = 'gwells-minio'
        String MNT_PORT = '9000-tcp'

        // Minimum well count for success
        int WELL_CHECK = 100000
    }
    agent none
    stages {
        stage('Prep') {
            steps {
                script {
                    echo "Saving vars and checking db"
                }
            }
        }
        stage('App Down') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            // Scale app down
                            def dcApp = openshift.selector("dc", "${APP_DC}")
                            dcApp.scale("--replicas=0","--timeout=5s")

                            // Point route to maintenance screen (temporarily using minio)
                            def route = openshift.selector("route", "${APP_DC}")
                            def patch = '\'{"spec": {"to": {"name": "' + "${MNT_NAME}"+ '"}, "port": {"targetPort": "' + "${MNT_PORT}" + '" }}}\''
                            route.patch( patch )
                        }
                    }
                }
            }
        }
        stage('App Up'){
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            // Scale app up
                            def dcApp = openshift.selector("dc", "${APP_DC}")
                            dcApp.scale("--replicas=2","--timeout=5m")

                            // Wait until pods are ready
                            def newVersion = dcApp.object().status.latestVersion
                            def pods = openshift.selector('pod', [deployment: "${APP_DC}-${newVersion}"])
                            timeout(5) {
                                pods.untilEach(2) {
                                    return it.object().status.containerStatuses.every {
                                        it.ready
                                    }
                                }
                            }

                            // Point route to app
                            def route = openshift.selector("route", "${APP_DC}")
                            def patch = '\'{"spec": {"to": {"name": "' + "${APP_NAME}"+ '"}, "port": {"targetPort": "' + "${APP_PORT}" + '" }}}\''
                            route.patch( patch )
                        }
                    }
                }
            }
        }
    }
}
