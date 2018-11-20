#!groovy

// Cron job for postgres vacuum and replication of Wells data
//
//  Setup in Jenkins:
//  > Folder > New Item > Pipeline
//  > Pipeline > Definition > Pipeline script from SCM
//    SCM: Git
//      Repository URL: https://github.com/bcgov/gwells
//      Branches to build: */master
//      Script path: scripts/Jenkinsfiles/wells_replication


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


pipeline {
    environment {
        // Project name (moe-gwells-test|moe-gwells-prod)
        String PROJECT = 'moe-gwells-prod'

        // Names, routes and ports
        String DB_NAME  = 'gwells-pgsql-production'
        String APP_NAME = 'gwells-production'
        String APP_PORT = 'web'
        String MNT_NAME = 'proxy-caddy'
        String MNT_PORT = '2015-tcp'

        // Checks
        String DB_STAT = ""
        String WELL_RESULT = ""
        Integer WELL_COUNT = 0
        Integer WELL_CHECK = 100000
    }
    agent none
    stages {
        stage('Prep') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            echo "Saving vars and checking db"
                            def dcDb   = openshift.selector("dc", "${DB_NAME}")
                            def latest = dcDb.object().status.latestVersion
                            def dbPods = openshift.selector('pod', [deployment: "${DB_NAME}-${latest}"])
                            DB_STAT = openshift.exec(
                                dbPods.objects()[0].metadata.name,
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
                expression {DB_STAT == 'online'}
            }
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            // Scale app down
                            def dcApp = openshift.selector("dc", "${APP_NAME}")
                            dcApp.scale("--replicas=0","--timeout=5s")

                            // Point route to maintenance screen
                            def route = openshift.selector("route", "${APP_NAME}")
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
        stage('Vacuum Db') {
            when {
                expression {DB_STAT == 'online'}
            }
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            def dcDb   = openshift.selector("dc", "${DB_NAME}")
                            def latest = dcDb.object().status.latestVersion
                            def dbPods = openshift.selector('pod', [deployment: "${DB_NAME}-${latest}"])
                            openshift.exec(
                                dbPods.objects()[0].metadata.name,
                                "--",
                                "bash -c '\
                                    psql -t -d gwells -c \"VACUUM FULL;\" \
                                '"
                            )
                        }
                    }
                }
            }
        }
        stage('Replicate 1/2') {
            when {
                expression {DB_STAT == 'online'}
            }
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            def dcDb   = openshift.selector("dc", "${DB_NAME}")
                            def latest = dcDb.object().status.latestVersion
                            def dbPods = openshift.selector('pod', [deployment: "${DB_NAME}-${latest}"])
                            openshift.exec(
                                dbPods.objects()[0].metadata.name,
                                "--",
                                "echo bash -c '\
                                    psql -t -d gwells -U \${POSTGRESQL_USER} -c \
                                        \"SELECT db_replicate_step1(_subset_ind=>false);\" \
                                '"
                            )
                        }
                    }
                }
            }
        }
        stage('Replicate 2/2') {
            when {
                expression {DB_STAT == 'online'}
            }
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            def dcDb   = openshift.selector("dc", "${DB_NAME}")
                            def latest = dcDb.object().status.latestVersion
                            def dbPods = openshift.selector('pod', [deployment: "${DB_NAME}-${latest}"])
                            openshift.exec(
                                dbPods.objects()[0].metadata.name,
                                "--",
                                "echo bash -c '\
                                    psql -t -d gwells -U \${POSTGRESQL_USER} -c \
                                        \"SELECT db_replicate_step2();\" \
                                '"
                            )

                            // Get a count of wells, ensure >= WELL_CHECK
                            WELL_COUNT = openshift.exec(
                                dbPods.objects()[0].metadata.name,
                                "--",
                                "bash -c '\
                                    psql -t -d gwells -U \${POSTGRESQL_USER} -c \
                                        \"SELECT count(*) from well;\" \
                                            | grep -Eo \"[[:digit:]]*\" \
                                '"
                            ).out.trim()

                            // Make sure there are enough well results
                            WELL_RESULT = sh(
                                script: """
                                    [ ${WELL_COUNT} -lt ${WELL_CHECK} ] || echo "true"
                                """,
                                returnStdout: true
                            ).trim()
                        }
                    }
                }
            }
        }
        stage('App Up') {
            when {
                expression {DB_STAT == 'online' && WELL_RESULT == 'true'}
            }
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            // Scale app up
                            def dcApp = openshift.selector("dc", "${APP_NAME}")
                            dcApp.scale("--replicas=2","--timeout=10m")

                            // Wait until pods are ready
                            def latest = dcApp.object().status.latestVersion
                            def pods = openshift.selector('pod', [deployment: "${APP_NAME}-${latest}"])
                            timeout(5) {
                                pods.untilEach(2) {
                                    return it.object().status.containerStatuses.every {
                                        it.ready
                                    }
                                }
                            }

                            // Point route to app
                            def route = openshift.selector("route", "${APP_NAME}")
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
            steps {
                script {
                    if (DB_STAT != 'online'){
                        echo "Replication skipped.  Database not accessible."
                    } else if (WELL_RESULT != 'true'){
                        echo "Application offline.  Well count: ${WELL_COUNT}, min: ${WELL_CHECK}."
                    } else {
                        echo "Replication complete!  Well count: ${WELL_COUNT}."
                    }
                }
            }
        }
    }
}
