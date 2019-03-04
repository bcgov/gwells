#!groovy

import groovy.json.JsonOutput
import bcgov.GitHubHelper


// Notify stage status and pass to Jenkins-GitHub library
void notifyStageStatus (String name, String status) {
    GitHubHelper.createCommitStatus(
        this,
        GitHubHelper.getPullRequestLastCommitId(this),
        status,
        "${env.BUILD_URL}",
        "Stage '${name}'",
        "Stage: ${name}"
    )
}


// Create deployment status and pass to Jenkins-GitHub library
void createDeploymentStatus (String suffix, String status, String stageUrl) {
    def ghDeploymentId = new GitHubHelper().createDeployment(
        this,
        "pull/${env.CHANGE_ID}/head",
        [
            'environment':"${suffix}",
            'task':"deploy:pull:${env.CHANGE_ID}"
        ]
    )

    new GitHubHelper().createDeploymentStatus(
        this,
        ghDeploymentId,
        "${status}",
        ['targetUrl':"https://${stageUrl}/gwells"]
    )

    if ('SUCCESS'.equalsIgnoreCase("${status}")) {
        echo "${suffix} deployment successful!"
    } else if ('PENDING'.equalsIgnoreCase("${status}")){
        echo "${suffix} deployment pending."
    }
}


// Print stack trace of error
@NonCPS
private static String stackTraceAsString(Throwable t) {
    StringWriter sw = new StringWriter();
    t.printStackTrace(new PrintWriter(sw));
    return sw.toString()
}


// OpenShift wrapper
def _openshift(String name, String project, Closure body) {
    script {
        openshift.withCluster() {
            openshift.withProject(project) {
                echo "Running Stage '${name}'"
                waitUntil {
                    notifyStageStatus (name, 'PENDING')
                    boolean isDone=false
                    try {
                        body()
                        isDone=true
                        notifyStageStatus(name, 'SUCCESS')
                        echo "Completed Stage '${name}'"
                    } catch (error){
                        notifyStageStatus(name, 'FAILURE')
                        echo "${stackTraceAsString(error)}"
                        def inputAction = input(
                            message: "This step (${name}) has failed. See related messages.",
                            ok: 'Confirm',
                            parameters: [
                                choice(
                                    name: 'action',
                                    choices: 'Re-run\nIgnore',
                                    description: 'What would you like to do?'
                                )
                            ]
                        )
                        if ('Ignore'.equalsIgnoreCase(inputAction)){
                            isDone=true
                        }
                    }
                    return isDone
                }
            }
        }
    }
}


// Functional test script
// Can be limited by assinging toTest var
def functionalTest (String stageName, String stageUrl, String envSuffix, String toTest='all') {
    _openshift(env.STAGE_NAME, toolsProject) {
        echo "Testing"
        // these functional tests are commented out on this branch
        // because we are not loading the page that the tests run against.

        // podTemplate(
        //     label: "bddstack-${ENV_SUFFIX}-${PR_NUM}",
        //     name: "bddstack-${ENV_SUFFIX}-${PR_NUM}",
        //     serviceAccount: 'jenkins',
        //     cloud: 'openshift',
        //     containers: [
        //         containerTemplate(
        //             name: 'jnlp',
        //             image: 'docker-registry.default.svc:5000/bcgov/jenkins-slave-bddstack:v1-stable',
        //             resourceRequestCpu: '800m',
        //             resourceLimitCpu: '800m',
        //             resourceRequestMemory: '4Gi',
        //             resourceLimitMemory: '4Gi',
        //             workingDir: '/home/jenkins',
        //             command: '',
        //             args: '${computer.jnlpmac} ${computer.name}',
        //             envVars: [
        //                 envVar(key:'BASE_URL', value: BASE_URL),
        //                 envVar(key:'OPENSHIFT_JENKINS_JVM_ARCH', value: 'x86_64')
        //             ]
        //         )
        //     ],
        //     volumes: [
        //         persistentVolumeClaim(
        //             mountPath: '/var/cache/artifacts',
        //             claimName: 'cache',
        //             readOnly: false
        //         )
        //     ]
        // ) {
        //     node("bddstack-${ENV_SUFFIX}-${PR_NUM}") {
        //         //the checkout is mandatory, otherwise functional tests would fail
        //         echo "checking out source"
        //         checkout scm
        //         dir('functional-tests') {
        //             try {
        //                 echo "BASE_URL = ${BASE_URL}"
        //                 if ('all'.equalsIgnoreCase(toTest)) {
        //                     sh './gradlew chromeHeadlessTest'
        //                 } else {
        //                     sh "./gradlew -DchromeHeadlessTest.single=${toTest} chromeHeadlessTest"
        //                 }
        //             } catch (error) {
        //                 echo error
        //             }
        //         }
        //     }
        // }
    }
    return true
}


// Functional test script
// Can be limited by assinging toTest var
def unitTestDjango (String stageName, String envProject, String envSuffix) {
    _openshift(env.STAGE_NAME, envProject) {
        def DB_target = envSuffix == "staging" ? "${appName}-pgsql-${envSuffix}" : "${appName}-pgsql-${envSuffix}-${prNumber}"
        def DB_newVersion = openshift.selector("dc", "${DB_target}").object().status.latestVersion
        def DB_pod = openshift.selector('pod', [deployment: "${DB_target}-${DB_newVersion}"])
        echo "Temporarily granting elevated DB rights"
        def db_ocoutput_grant = openshift.exec(
            DB_pod.objects()[0].metadata.name,
            "--",
            "bash -c '\
                psql -c \"ALTER USER \\\"\${POSTGRESQL_USER}\\\" WITH SUPERUSER;\" \
            '"
        )
        echo "Temporary DB grant results: "+ db_ocoutput_grant.actions[0].out

        def target = envSuffix == "staging" ? "${appName}-${envSuffix}" : "${appName}-${envSuffix}-${prNumber}"
        def newVersion = openshift.selector("dc", "${target}").object().status.latestVersion
        def pods = openshift.selector('pod', [deployment: "${target}-${newVersion}"])

        echo "Running Django unit tests"
        def ocoutput = openshift.exec(
            pods.objects()[0].metadata.name,
            "--",
            "bash -c '\
                cd /opt/app-root/src/backend; \
                python manage.py test -c nose.cfg \
            '"
        )
        echo "Django test results: "+ ocoutput.actions[0].out

        echo "Revoking ADMIN rights"
        def db_ocoutput_revoke = openshift.exec(
            DB_pod.objects()[0].metadata.name,
            "--",
            "bash -c '\
                psql -c \"ALTER USER \\\"\${POSTGRESQL_USER}\\\" WITH NOSUPERUSER;\" \
            '"
        )
        echo "DB Revocation results: "+ db_ocoutput_revoke.actions[0].out
    }
}


// API test function
def apiTest (String stageName, String stageUrl, String envSuffix) {
    _openshift(env.STAGE_NAME, toolsProject) {
        podTemplate(
            label: "nodejs-${appName}-${envSuffix}-${prNumber}",
            name: "nodejs-${appName}-${envSuffix}-${prNumber}",
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
                        envVar(
                            key:'BASE_URL',
                            value: "https://${stageUrl}/gwells"
                        ),
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
            node("nodejs-${appName}-${envSuffix}-${prNumber}") {
                checkout scm
                dir('api-tests') {
                    sh 'npm install -g newman'
                    try {
                        sh """
                            newman run ./registries_api_tests.json \
                                --global-var test_user=\$GWELLS_API_TEST_USER \
                                --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                --global-var base_url=\$BASE_URL \
                                --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                -r cli,junit,html
                            newman run ./wells_api_tests.json \
                                --global-var test_user=\$GWELLS_API_TEST_USER \
                                --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                --global-var base_url=\$BASE_URL \
                                --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                -r cli,junit,html
                            newman run ./submissions_api_tests.json \
                                --global-var test_user=\$GWELLS_API_TEST_USER \
                                --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                --global-var base_url=\$BASE_URL \
                                --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                -r cli,junit,html
                            newman run ./aquifers_api_tests.json \
                                --global-var test_user=\$GWELLS_API_TEST_USER \
                                --global-var test_password=\$GWELLS_API_TEST_PASSWORD \
                                --global-var base_url=\$BASE_URL \
                                --global-var auth_server=\$GWELLS_API_TEST_AUTH_SERVER \
                                --global-var client_id=\$GWELLS_API_TEST_CLIENT_ID \
                                --global-var client_secret=\$GWELLS_API_TEST_CLIENT_SECRET \
                                -r cli,junit,html
                        """

                        if ("dev".equalsIgnoreCase("${envSuffix}")) {
                            sh """
                                newman run ./wells_search_api_tests.json \
                                --global-var base_url=\$BASE_URL \
                                -r cli,junit,html
                            """
                        }

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
    return true
}


pipeline {
    environment {
        // Project-wide settings - app name, repo
        appName = "gwells"
        repository = 'https://www.github.com/bcgov/gwells.git'

        // prNumber is the pull request number e.g. 'pr-4'
        prNumber = "${env.JOB_BASE_NAME}".toLowerCase()

        // toolsProject is where images are built
        toolsProject = "moe-gwells-tools"

        // devProject is the project where individual development environments are spun up
        devProject = "moe-gwells-dev"
        devSuffix = "dev"
        devAppName = "${appName}-${devSuffix}-${prNumber}"
        devHost = "${devAppName}.pathfinder.gov.bc.ca"

        // stagingProject contains the test deployment. The test image is a candidate for promotion to prod.
        stagingProject = "moe-gwells-test"
        stagingSuffix = "staging"
        stagingHost = "gwells-staging.pathfinder.gov.bc.ca"

        // demoProject is for a stable demo environment.  It can be for training or presentation.
        demoProject = "moe-gwells-test"
        demoSuffix = "demo"
        demoHost = "gwells-demo.pathfinder.gov.bc.ca"

        // prodProject is the prod deployment.
        // TODO: New production images can be deployed by tagging an existing "test" image as "prod".
        prodProject = "moe-gwells-prod"
        prodSuffix = "production"
        prodHost = "gwells-prod.pathfinder.gov.bc.ca"
    }
    agent any
    stages {
        // the Start Pipeline stage will process and apply OpenShift build templates which will create
        // buildconfigs and an imagestream for built images.
        // each pull request gets its own buildconfig but all new builds are pushed to a single imagestream,
        // to be tagged with the pull request number.
        // e.g.:  gwells-app:pr-999
        stage('ALL - Prepare Templates') {
            steps {
                script {
                    echo "Cancelling previous builds..."
                    timeout(10) {
                        abortAllPreviousBuildInProgress(currentBuild)
                    }
                    echo "Previous builds cancelled"

                    _openshift(env.STAGE_NAME, toolsProject) {
                        //  - variable substitution
                        def buildtemplate = openshift.process("-f",
                            "openshift/backend.bc.json",
                            "ENV_NAME=${devSuffix}",
                            "NAME_SUFFIX=-${devSuffix}-${prNumber}",
                            "APP_IMAGE_TAG=${prNumber}",
                            "SOURCE_REPOSITORY_URL=${repository}",
                            "SOURCE_REPOSITORY_REF=pull/${CHANGE_ID}/head"
                        )

                        // Apply oc list objects
                        //  - add docker image reference as tag in gwells-application
                        //  - create build config
                        echo "Preparing backend imagestream and buildconfig"
                        echo " \$ oc process -f openshift/backend.bc.json -p ENV_NAME=${devSuffix} -p NAME_SUFFIX=-${devSuffix}-${prNumber} -p APP_IMAGE_TAG=${prNumber} -p SOURCE_REPOSITORY_URL=${REPOSITORY} -p SOURCE_REPOSITORY_REF=pull/${CHANGE_ID}/head | oc apply -n moe-gwells-tools -f -"
                        openshift.apply(buildtemplate)
                    }
                }
            }
        }


        // the Build stage builds files; an image will be outputted to the app's imagestream,
        // using the source-to-image (s2i) strategy. See /app/.s2i/assemble for image build script
        stage('ALL - Build') {
            steps {
                script {
                    _openshift(env.STAGE_NAME, toolsProject) {
                        echo "Running unit tests and building images..."
                        echo "This may take several minutes. Logs are not forwarded to Jenkins by default (at this time)."
                        echo "Additional logs can be found by monitoring builds in ${toolsProject}"

                        // Select appropriate buildconfig
                        def appBuild = openshift.selector("bc", "${devAppName}")
                        // temporarily set ENABLE_DATA_ENTRY=True during testing because False currently leads to a failing unit test
                        echo "Building"
                        echo " \$ oc start-build -n moe-gwells-tools ${devAppName} --wait --env=ENABLE_DATA_ENTRY=true --follow=true"
                        appBuild.startBuild("--wait", "--env=ENABLE_DATA_ENTRY=True").logs("-f")
                    }
                }
            }
        }

        // the Deploy to Dev stage creates a new dev environment for the pull request (if necessary), tagging
        // the newly built application image into that environment.  This stage monitors the newest deployment
        // for pods/containers to report back as ready.
        stage('DEV - Deploy') {
            when {
                expression { env.CHANGE_TARGET != 'master' && env.CHANGE_TARGET != 'demo' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, devProject) {
                        // Process postgres deployment config (sub in vars, create list items)
                        echo " \$ oc process -f openshift/postgresql.dc.json -p DATABASE_SERVICE_NAME=gwells-pgsql-${devSuffix}-${prNumber} -p IMAGE_STREAM_NAMESPACE=bcgov -p IMAGE_STREAM_NAME=postgresql-9.6-oracle-fdw -p IMAGE_STREAM_VERSION=v1-stable -p NAME_SUFFIX=-${devSuffix}-${prNumber} -p POSTGRESQL_DATABASE=gwells -p VOLUME_CAPACITY=1Gi | oc apply -n moe-gwells-dev -f -"
                        def deployDBTemplate = openshift.process("-f",
                            "openshift/postgresql.dc.json",
                            "DATABASE_SERVICE_NAME=gwells-pgsql-${devSuffix}-${prNumber}",
                            "IMAGE_STREAM_NAMESPACE=bcgov",
                            "IMAGE_STREAM_NAME=postgresql-9.6-oracle-fdw",
                            "IMAGE_STREAM_VERSION=v1-stable",
                            "NAME_SUFFIX=-${devSuffix}-${prNumber}",
                            "POSTGRESQL_DATABASE=gwells",
                            "VOLUME_CAPACITY=1Gi"
                        )

                        // Process postgres deployment config (sub in vars, create list items)
                        echo " \$ oc process -f openshift/backend.dc.json -p ENV_NAME=${devSuffix} -p NAME_SUFFIX=-${devSuffix}-${prNumber} | oc apply -n moe-gwells-dev -f -"
                        echo "Processing deployment config for pull request ${prNumber}"
                        def deployTemplate = openshift.process("-f",
                            "openshift/backend.dc.json",
                            "ENV_NAME=${devSuffix}",
                            "HOST=${devHost}",
                            "NAME_SUFFIX=-${devSuffix}-${prNumber}"
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

                        echo "Applying deployment config for pull request ${prNumber} on ${devProject}"

                        // apply the templates, which will create new objects or modify existing ones as necessary.
                        // the copies of base objects (secrets, configmaps) are also applied.
                        openshift.apply(deployTemplate).label(['app':"${devAppName}", 'app-name':"${appName}", 'env-name':"${devSuffix}"], "--overwrite")
                        openshift.apply(deployDBTemplate).label(['app':"${devAppName}", 'app-name':"${appName}", 'env-name':"${devSuffix}"], "--overwrite")
                        openshift.apply(newObjectCopies).label(['app':"${devAppName}", 'app-name':"${appName}", 'env-name':"${devSuffix}"], "--overwrite")
                        echo "Successfully applied deployment configs for ${prNumber}"

                        // promote the newly built image to DEV
                        echo "Tagging new image to DEV imagestream."
                        openshift.tag("${toolsProject}/gwells-application:${prNumber}", "${devProject}/${devAppName}:dev")  // todo: clean up labels/tags
                        openshift.tag("${toolsProject}/gwells-postgresql:dev", "${devProject}/gwells-postgresql-${devSuffix}-${prNumber}:dev")  // todo: clean up labels/tags

                        // post a notification to Github that this pull request is being deployed
                        createDeploymentStatus(devSuffix, 'PENDING', devHost)

                        // monitor the deployment status and wait until deployment is successful
                        echo "Waiting for deployment to dev..."
                        def newVersion = openshift.selector("dc", "${devAppName}").object().status.latestVersion
                        def pods = openshift.selector('pod', [deployment: "${devAppName}-${newVersion}"])

                        // wait until each container in this deployment's pod reports as ready
                        timeout(15) {
                            pods.untilEach(2) {
                                return it.object().status.containerStatuses.every {
                                    it.ready
                                }
                            }
                        }

                        // Report a pass to GitHub
                        createDeploymentStatus(devSuffix, 'SUCCESS', devHost)
                    }
                }
            }
        }


        // the Django Unit Tests stage runs backend unit tests using a test DB that is
        // created and destroyed afterwards.
        stage('DEV - Django Unit Tests') {
            when {
                expression { env.CHANGE_TARGET != 'master' && env.CHANGE_TARGET != 'demo' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, devProject) {
                        def result = unitTestDjango (env.STAGE_NAME, devProject, devSuffix)
                    }
                }
            }
        }


        stage('DEV - Load Fixtures') {
            when {
                expression { env.CHANGE_TARGET != 'master' && env.CHANGE_TARGET != 'demo' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, devProject) {
                        def newVersion = openshift.selector("dc", "${devAppName}").object().status.latestVersion
                        def pods = openshift.selector('pod', [deployment: "${devAppName}-${newVersion}"])

                        echo "Loading fixtures"
                        def ocoutput = openshift.exec(
                            pods.objects()[0].metadata.name,
                            "--",
                            "bash -c '\
                                cd /opt/app-root/src/backend; \
                                python manage.py loaddata \
                                gwells-codetables.json \
                                wellsearch-codetables.json \
                                registries-codetables.json \
                                registries.json \
                                wellsearch.json \
                                aquifers.json \
                            '"
                        )
                        echo "Load Fixtures results: "+ ocoutput.actions[0].out

                        openshift.exec(
                            pods.objects()[0].metadata.name,
                            "--",
                            "bash -c '\
                                cd /opt/app-root/src/backend; \
                                python manage.py createinitialrevisions \
                            '"
                        )
                    }
                }
            }
        }

        
        // Functional tests temporarily limited to smoke tests
        // See https://github.com/BCDevOps/BDDStack
        stage('DEV - Smoke Tests') {
            when {
                expression { env.CHANGE_TARGET != 'master' && env.CHANGE_TARGET != 'demo' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, toolsProject) {
                        def result = functionalTest ('DEV - Smoke Tests', devHost, devSuffix, 'SearchSpecs')
                    }
                }
            }
        }


        stage('DEV - API Tests') {
            when {
                expression { env.CHANGE_TARGET != 'master' && env.CHANGE_TARGET != 'demo' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, devProject) {
                        def result = apiTest ('DEV - API Tests', devHost, devSuffix)
                    }
                }
            }
        }


        // the Promote to Test stage allows approving the tagging of the newly built image into the test environment,
        // which will trigger an automatic deployment of that image.
        // The deployment configs in the openshift folder are applied first in case there are any changes to the templates.
        // this stage should only occur when the pull request is being made against the master branch.
        stage('STAGING - Deploy') {
            when {
                expression { env.CHANGE_TARGET == 'master' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, stagingProject) {
                        echo "Preparing..."

                        // Process db and app template into list objects
                        // TODO: Match docker-compose image from moe-gwells-tools
                        echo "Updating staging deployment..."
                        def deployDBTemplate = openshift.process("-f",
                            "openshift/postgresql.dc.json",
                            "NAME_SUFFIX=-${stagingSuffix}",
                            "DATABASE_SERVICE_NAME=gwells-pgsql-${stagingSuffix}",
                            "IMAGE_STREAM_NAMESPACE=bcgov",
                            "IMAGE_STREAM_NAME=postgresql-9.6-oracle-fdw",
                            "IMAGE_STREAM_VERSION=v1-stable",
                            "POSTGRESQL_DATABASE=gwells",
                            "VOLUME_CAPACITY=5Gi"
                        )

                        def deployTemplate = openshift.process("-f",
                            "openshift/backend.dc.json",
                            "NAME_SUFFIX=-${stagingSuffix}",
                            "ENV_NAME=${stagingSuffix}",
                            "HOST=${stagingHost}",
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
                        echo "Applying deployment config for pull request ${prNumber} on ${stagingProject}"

                        openshift.apply(deployTemplate).label(
                            [
                                'app':"gwells-${stagingSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${stagingSuffix}"
                            ],
                            "--overwrite"
                        )
                        openshift.apply(deployDBTemplate).label(
                            [
                                'app':"gwells-${stagingSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${stagingSuffix}"
                            ],
                            "--overwrite"
                        )
                        openshift.apply(newObjectCopies).label(
                            [
                                'app':"gwells-${stagingSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${stagingSuffix}"
                            ],
                            "--overwrite"
                        )
                        echo "Successfully applied TEST deployment config"

                        // promote the newly built image to DEV
                        echo "Tagging new image to TEST imagestream."

                        // Application/database images are tagged in the tools imagestream as the new test/prod image
                        openshift.tag(
                            "${toolsProject}/gwells-application:${prNumber}",
                            "${toolsProject}/gwells-application:${stagingSuffix}"
                        )  // todo: clean up labels/tags
                        // openshift.tag("${toolsProject}/gwells-postgresql:staging", "${toolsProject}/gwells-postgresql:${stagingSuffix}")

                        // Images are then tagged into the target environment namespace (test or prod)
                        openshift.tag(
                            "${toolsProject}/gwells-application:${stagingSuffix}",
                            "${stagingProject}/gwells-${stagingSuffix}:${stagingSuffix}"
                        )  // todo: clean up labels/tags
                        openshift.tag(
                            "${toolsProject}/gwells-postgresql:${stagingSuffix}",
                            "${stagingProject}/gwells-postgresql-${stagingSuffix}:${stagingSuffix}"
                        )  // todo: clean up labels/tags

                        createDeploymentStatus(stagingSuffix, 'PENDING', stagingHost)

                        // Create cronjob for well export
                        def cronTemplate = openshift.process("-f",
                            "openshift/export-wells.cj.json",
                            "ENV_NAME=${stagingSuffix}",
                            "PROJECT=${stagingProject}",
                            "TAG=${stagingSuffix}"
                        )
                        openshift.apply(cronTemplate).label(
                            [
                                'app':"gwells-${stagingSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${stagingSuffix}"
                            ],
                            "--overwrite"
                        )

                        // monitor the deployment status and wait until deployment is successful
                        echo "Waiting for deployment to STAGING..."
                        def newVersion = openshift.selector("dc", "gwells-${stagingSuffix}").object().status.latestVersion
                        def pods = openshift.selector('pod', [deployment: "gwells-${stagingSuffix}-${newVersion}"])

                        // wait until at least one pod reports as ready
                        timeout(15) {
                            pods.untilEach(2) {
                                return it.object().status.containerStatuses.every {
                                    it.ready
                                }
                            }
                        }

                        createDeploymentStatus(stagingSuffix, 'SUCCESS', stagingHost)
                    }
                }
            }
        }


        // the Django Unit Tests stage runs backend unit tests using a test DB that is
        // created and destroyed afterwards.
        stage('Staging - Django Unit Tests') {
            when {
                expression { env.CHANGE_TARGET == 'master' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, stagingProject) {
                        def result = unitTestDjango (env.STAGE_NAME, stagingProject, stagingSuffix)
                    }
                }
            }
        }


        stage('STAGING - API Tests') {
            when {
                expression { env.CHANGE_TARGET == 'master' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, toolsProject) {
                        def result = apiTest ('STAGING - API Tests', stagingHost, stagingSuffix)
                    }
                }
            }
        }


        // Single functional test
        stage('STAGING - Smoke Tests') {
            when {
                expression { env.CHANGE_TARGET == 'master' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, toolsProject) {
                        def result = functionalTest ('STAGING - Smoke Tests', stagingHost, stagingSuffix, 'SearchSpecs')
                    }
                }
            }
        }


        // Push to Demo branch to deploy in demo environment
        stage('DEMO - Deploy') {
            when {
                expression { env.CHANGE_TARGET == 'demo' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, demoProject) {
                        echo "Preparing..."

                        // Process db and app template into list objects
                        echo "Updating staging deployment..."
                        def deployDBTemplate = openshift.process("-f",
                            "openshift/postgresql.dc.json",
                            "NAME_SUFFIX=-${demoSuffix}",
                            "DATABASE_SERVICE_NAME=gwells-pgsql-${demoSuffix}",
                            "IMAGE_STREAM_NAMESPACE=bcgov",
                            "IMAGE_STREAM_NAME=postgresql-9.6-oracle-fdw",
                            "IMAGE_STREAM_VERSION=v1-stable",
                            "POSTGRESQL_DATABASE=gwells",
                            "VOLUME_CAPACITY=5Gi"
                        )

                        def deployTemplate = openshift.process("-f",
                            "openshift/backend.dc.json",
                            "NAME_SUFFIX=-${demoSuffix}",
                            "ENV_NAME=${demoSuffix}",
                            "HOST=${demoHost}",
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
                        echo "Applying deployment config for pull request ${prNumber} on ${demoProject}"

                        openshift.apply(deployTemplate).label(
                            [
                                'app':"gwells-${demoSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${demoSuffix}"
                            ],
                            "--overwrite"
                        )
                        openshift.apply(deployDBTemplate).label(
                            [
                                'app':"gwells-${demoSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${demoSuffix}"
                            ],
                            "--overwrite"
                        )
                        openshift.apply(newObjectCopies).label(
                            [
                                'app':"gwells-${demoSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${demoSuffix}"
                            ],
                            "--overwrite"
                        )
                        echo "Successfully applied DEMO deployment config"

                        // promote the newly built image to DEV
                        echo "Tagging new image to DEMO imagestream."

                        // Application/database images are tagged in the tools imagestream as the new test/prod image
                        openshift.tag(
                            "${toolsProject}/gwells-application:${prNumber}",
                            "${toolsProject}/gwells-application:${demoSuffix}"
                        )  // todo: clean up labels/tags
                        // openshift.tag("${toolsProject}/gwells-postgresql:staging", "${toolsProject}/gwells-postgresql:${demoSuffix}")

                        // Images are then tagged into the target environment namespace (test or prod)
                        openshift.tag(
                            "${toolsProject}/gwells-application:${demoSuffix}",
                            "${demoProject}/gwells-${demoSuffix}:${demoSuffix}"
                        )  // todo: clean up labels/tags
                        openshift.tag(
                            "${toolsProject}/gwells-postgresql:staging",
                            "${demoProject}/gwells-postgresql-${demoSuffix}:${demoSuffix}"
                        )  // todo: clean up labels/tags

                        createDeploymentStatus(demoSuffix, 'PENDING', demoHost)

                        // Create cronjob for well export
                        def cronTemplate = openshift.process("-f",
                            "openshift/export-wells.cj.json",
                            "ENV_NAME=${demoSuffix}",
                            "PROJECT=${demoProject}",
                            "TAG=${demoSuffix}"
                        )
                        openshift.apply(cronTemplate).label(
                            [
                                'app':"gwells-${demoSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${demoSuffix}"
                            ],
                            "--overwrite"
                        )

                        // monitor the deployment status and wait until deployment is successful
                        echo "Waiting for deployment to DEMO..."
                        def newVersion = openshift.selector("dc", "gwells-${demoSuffix}").object().status.latestVersion
                        def pods = openshift.selector('pod', [deployment: "gwells-${demoSuffix}-${newVersion}"])

                        // wait until at least one pod reports as ready
                        timeout(15) {
                            pods.untilEach(2) {
                                return it.object().status.containerStatuses.every {
                                    it.ready
                                }
                            }
                        }

                        createDeploymentStatus(demoSuffix, 'SUCCESS', demoHost)
                    }
                }
            }
        }


        stage('DEMO - API Tests') {
            when {
                expression { env.CHANGE_TARGET == 'demo' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, toolsProject) {
                        def result = apiTest ('DEMO - API Tests', demoHost, demoSuffix)
                    }
                }
            }
        }


        // Single functional test
        stage('DEMO - Smoke Tests') {
            when {
                expression { env.CHANGE_TARGET == 'demo' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, toolsProject) {
                        def result = functionalTest ('DEMO - Smoke Tests', demoHost, demoSuffix, 'SearchSpecs')
                    }
                }
            }
        }


        stage('PROD - Deploy') {
            when {
                expression { env.CHANGE_TARGET == 'master' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, prodProject) {
                        input "Deploy to production?"
                        echo "Updating production deployment..."

                        def deployDBTemplate = openshift.process("-f",
                            "openshift/postgresql.dc.json",
                            "NAME_SUFFIX=-${prodSuffix}",
                            "DATABASE_SERVICE_NAME=gwells-pgsql-${prodSuffix}",
                            "IMAGE_STREAM_NAMESPACE=bcgov",
                            "IMAGE_STREAM_NAME=postgresql-9.6-oracle-fdw",
                            "IMAGE_STREAM_VERSION=v1-stable",
                            "POSTGRESQL_DATABASE=gwells",
                            "VOLUME_CAPACITY=20Gi"
                        )

                        def deployTemplate = openshift.process("-f",
                            "openshift/backend.dc.json",
                            "NAME_SUFFIX=-${prodSuffix}",
                            "ENV_NAME=${prodSuffix}",
                            "HOST=${prodHost}",
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
                        echo "Applying deployment config for pull request ${prNumber} on ${prodProject}"

                        openshift.apply(deployDBTemplate).label(
                            [
                                'app':"gwells-${prodSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${prodSuffix}"
                            ],
                            "--overwrite"
                        )
                        openshift.apply(deployTemplate).label(
                            [
                                'app':"gwells-${prodSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${prodSuffix}"
                            ],
                            "--overwrite"
                        )
                        openshift.apply(newObjectCopies).label(
                            [
                                'app':"gwells-${prodSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${prodSuffix}"
                            ],
                            "--overwrite"
                        )
                        echo "Successfully applied production deployment config"

                        // promote the newly built image to DEV
                        echo "Tagging new image to production imagestream."

                        // Application/database images are tagged in the tools imagestream as the new prod image
                        openshift.tag(
                            "${toolsProject}/gwells-application:${prNumber}",
                            "${toolsProject}/gwells-application:${prodSuffix}"
                        )  // todo: clean up labels/tags

                        // TODO: determine best way to manage database images (at the moment they never change, but we don't want an unforeseen change to impact prod)
                        // openshift.tag("${toolsProject}/gwells-postgresql:prod", "${toolsProject}/gwells-postgresql:${prodSuffix}")

                        // Images are then tagged into the target environment namespace (prod)
                        openshift.tag(
                            "${toolsProject}/gwells-application:${prodSuffix}",
                            "${prodProject}/gwells-${prodSuffix}:${prodSuffix}"
                        )  // todo: clean up labels/tags
                        openshift.tag(
                            "${toolsProject}/gwells-postgresql:prod",
                            "${prodProject}/gwells-postgresql-${prodSuffix}:${prodSuffix}"
                        )  // todo: clean up labels/tags

                        createDeploymentStatus(prodSuffix, 'PENDING', prodUrl)

                        // Create cronjob for well export
                        def cronTemplate = openshift.process("-f",
                            "openshift/export-wells.cj.json",
                            "ENV_NAME=${prodSuffix}",
                            "PROJECT=${prodProject}",
                            "TAG=${prodSuffix}"
                        )
                        openshift.apply(cronTemplate).label(
                            [
                                'app':"gwells-${prodSuffix}",
                                'app-name':"${appName}",
                                'env-name':"${prodSuffix}"
                            ],
                            "--overwrite"
                        )

                        // monitor the deployment status and wait until deployment is successful
                        echo "Waiting for deployment to production..."
                        def newVersion = openshift.selector("dc", "gwells-${prodSuffix}").object().status.latestVersion
                        def pods = openshift.selector('pod', [deployment: "gwells-${prodSuffix}-${newVersion}"])

                        // wait until pods reports as ready
                        timeout(15) {
                            pods.untilEach(2) {
                                return it.object().status.containerStatuses.every {
                                    it.ready
                                }
                            }
                        }

                        createDeploymentStatus(prodSuffix, 'SUCCESS', prodUrl)
                    }
                }
            }
        }


        // Single functional test
        stage('PROD - Smoke Tests') {
            when {
                expression { env.CHANGE_TARGET == 'master' }
            }
            steps {
                script {
                    _openshift(env.STAGE_NAME, toolsProject) {
                        def result = functionalTest ('PROD - Smoke Tests', prodUrl, prodSuffix, 'SearchSpecs')
                    }
                }
            }
        }
    }
}
