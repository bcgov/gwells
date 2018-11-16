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


// String APP_DC = 'gwells-dev-pr-1022'
pipeline {
    environment {
        // Project name (moe-gwells-test|moe-gwells-prod)
        String PROJECT = 'moe-gwells-dev'

        // Deployment configs
        String APP_DC = 'gwells-dev-pr-1022'
        String DB_DC  = 'gwells-pgsql-dev-pr-1022'

        // Routes and ports
        String APP_NAME = 'gwells-dev-pr-1022'
        String APP_PORT = 'web'
        String MNT_NAME = 'gwells-minio'
        String MNT_PORT = '9000-tcp'

        // Minimum well count for success
        int WELL_CHECK = 100000

        // Checks
        String DB_STAT = ""
    }
    agent none
    stages {
        stage('Prep') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            echo "Saving vars and checking db"
                            def dcDb   = openshift.selector("dc", "${DB_DC}")
                            def dcDbV  = dcDb.object().status.latestVersion
                            def dbPods = openshift.selector('pod', [deployment: "${DB_DC}-${dcDbV}"])
                            def dbPod0 = dbPods.objects()[0].metadata.name
                            DB_STAT = openshift.exec(
                                dbPod0,
                                "--",
                                "bash -c '\
                                    psql -d gwells -c \"SELECT 1 AS online FROM WELLS.WELLS_WELLS LIMIT 1;\" \
                                        | grep -o online \
                                '"
                            ).out.trim()
                        }
                    }
                }
            }
        }
        stage('App Down') {
            when {
                expression { DB_STAT == 'online' }
            }
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            // Scale app down
                            def dcApp = openshift.selector("dc", "${APP_DC}")
                            dcApp.scale("--replicas=0","--timeout=5s")

                            // Point route to maintenance screen (temporarily using minio)
                            def route = openshift.selector("route", "${APP_DC}")
                            def patch = '\'{"spec": { \
                                "to": {"name": "' + "${MNT_NAME}"+ '"}, \
                                "port": {"targetPort": "' + "${MNT_PORT}" + '"} \
                            }}\''
                            route.patch( patch )
                        }
                    }
                }
            }
        }
        stage('Do Stuff') {
            when {
                expression { DB_STAT == 'online' }
            }
            steps {
                script {
                    echo "This is where the exciting stuff happens"
                    sleep 30
                }
            }
        }
        stage('App Up') {
            when {
                expression { DB_STAT == 'online' }
            }
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            // Scale app up
                            def dcApp = openshift.selector("dc", "${APP_DC}")
                            dcApp.scale("--replicas=2","--timeout=10m")

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
                            def patch = '\'{"spec": { \
                                "to": {"name": "' + "${APP_NAME}"+ '"}, \
                                "port": {"targetPort": "' + "${APP_PORT}" + '" } \
                            }}\''
                            route.patch( patch )
                        }
                    }
                }
            }
        }
        stage('Notify') {
            when {
                expression { DB_STAT != 'online' }
            }
            steps {
                script {
                    echo "Database is offline, no action taken"
                }
            }
        }
    }
}
