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
        String PROJECT = 'moe-gwells-test'

        // Names, routes and ports
        String DB_NAME  = 'gwells-pgsql-staging'
        String APP_NAME = 'gwells-staging'
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
                            def dcDbV  = dcDb.object().status.latestVersion
                            def dbPods = openshift.selector('pod', [deployment: "${DB_NAME}-${dcDbV}"])
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
                expression {DB_STAT == 'online'}
            }
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(PROJECT) {
                            // Scale app down
                            def dcApp = openshift.selector("dc", "${APP_NAME}")
                            dcApp.scale("--replicas=0","--timeout=5s")

                            // Point route to maintenance screen (temporarily using minio)
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
                            def dcDbV  = dcDb.object().status.latestVersion
                            def dbPods = openshift.selector('pod', [deployment: "${DB_NAME}-${dcDbV}"])
                            def dbPod0 = dbPods.objects()[0].metadata.name
                            openshift.exec(
                                dbPod0,
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
                            def dcDbV  = dcDb.object().status.latestVersion
                            def dbPods = openshift.selector('pod', [deployment: "${DB_NAME}-${dcDbV}"])
                            def dbPod0 = dbPods.objects()[0].metadata.name
                            openshift.exec(
                                dbPod0,
                                "--",
                                "bash -c '\
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
                            def dcDbV  = dcDb.object().status.latestVersion
                            def dbPods = openshift.selector('pod', [deployment: "${DB_NAME}-${dcDbV}"])
                            def dbPod0 = dbPods.objects()[0].metadata.name
                            openshift.exec(
                                dbPod0,
                                "--",
                                "bash -c '\
                                    psql -t -d gwells -U \${POSTGRESQL_USER} -c \
                                        \"SELECT db_replicate_step2();\" \
                                '"
                            )

                            // Get a count of wells, ensure >= WELL_CHECK
                            WELL_COUNT = openshift.exec(
                                dbPod0,
                                "--",
                                "bash -c '\
                                    psql -t -d gwells -U \${POSTGRESQL_USER} -c \
                                        \"SELECT count(*) from well;\" \
                                            | grep -Eo \"[[:digit:]]*\" \
                                '"
                            ).out.trim()
                            WELL_RESULT = sh(
                                script: """
                                    if [ ${WELL_COUNT} -gt ${WELL_CHECK} ]
                                    then
                                        echo "true"
                                    else
                                        echo "false"
                                    fi
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
                            def newVersion = dcApp.object().status.latestVersion
                            def pods = openshift.selector('pod', [deployment: "${APP_NAME}-${newVersion}"])
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
                        echo "Database not accessible, replication skipped"
                    } else if (WELL_RESULT != 'true'){
                        echo "Well count below ${WELL_CHECK}"
                    } else {
                        echo "Replication complete!  Well check: ${WELL_CHECK}"
                    }
                }
            }
        }
    }
}
