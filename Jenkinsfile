// Jenkinsfile (Scripted Pipeline)

/* Gotchas:
    - PodTemplate name/label has to be unique to ensure proper caching/validation
    - https://gist.github.com/matthiasbalke/3c9ecccbea1d460ee4c3fbc5843ede4a

   Libraries:
    - https://github.com/BCDevOps/jenkins-pipeline-shared-lib
    - http://github-api.kohsuke.org/apidocs/index.html
*/
import hudson.model.Result;
import jenkins.model.CauseOfInterruption.UserInterruption;
import org.kohsuke.github.*
import bcgov.OpenShiftHelper
import bcgov.GitHubHelper


// Print stack trace of error
@NonCPS
private static String stackTraceAsString(Throwable t) {
    StringWriter sw = new StringWriter();
    t.printStackTrace(new PrintWriter(sw));
    return sw.toString()
}


// Notify stage status and pass to Jenkins-GitHub library
void notifyStageStatus (Map context, String name, String status) {
    GitHubHelper.createCommitStatus(
        this,
        context.pullRequest.head,
        status,
        "${env.BUILD_URL}",
        "Stage '${name}'",
        "stages/${name.toLowerCase()}"
    )
}


/* _Stage wrapper:
    - runs stages against true|false in map context
    - receives stages defined separately in closures (body)
    - catches errors and provides output
*/
def _stage(String name, Map context, boolean retry=0, boolean withCommitStatus=true, Closure body) {
    timestamps {
        def stageOpt =(context?.stages?:[:])[name]
        boolean isEnabled=(stageOpt == null || stageOpt == true)
        echo "Running Stage '${name}' - enabled:${isEnabled}"

        if (isEnabled){
            stage(name) {
                waitUntil {
                    notifyStageStatus(context, name, 'PENDING')
                    boolean isDone=false
                    try{
                        body()
                        isDone=true
                        notifyStageStatus(context, name, 'SUCCESS')
                    }catch (ex){
                        notifyStageStatus(context, name, 'FAILURE')
                        echo "${stackTraceAsString(ex)}"
                        def inputAction = input(
                            message: "This step (${name}) has failed. See error above.",
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
                } //end waitUntil
            } //end Stage
        }else{
            stage(name) {
                echo 'Skipping'
            }
        }
    }
}


/* Project and build settings
   Includes:
    - build (*.bc) and config templates (*.dc)
    - stage names and enabled status (true|false)
*/
Map context = [
    'name': 'gwells',
    'uuid' : "${env.JOB_BASE_NAME}-${env.BUILD_NUMBER}-${env.CHANGE_ID}",
    'env': [
        'dev':[:],
        'test':[
            'params':[
                'host':'gwells-test.pathfinder.gov.bc.ca',
                'DB_PVC_SIZE':'5Gi'
            ]
        ],
        'prod':[
            'params':[
                'host':'gwells-prod.pathfinder.gov.bc.ca',
                'DB_PVC_SIZE':'5Gi'
            ]
        ]
    ],
    'templates': [
        'build':[
            ['file':'openshift/postgresql.bc.json'],
            ['file':'openshift/backend.bc.json']
        ],
        'deployment':[
            [
                'file':'openshift/postgresql.dc.json',
                'params':[
                    'DATABASE_SERVICE_NAME':'gwells-pgsql${deploy.dcSuffix}',
                    'IMAGE_STREAM_NAMESPACE':'',
                    'IMAGE_STREAM_NAME':'gwells-postgresql${deploy.dcSuffix}',
                    'IMAGE_STREAM_VERSION':'${deploy.envName}',
                    'POSTGRESQL_DATABASE':'gwells',
                    'VOLUME_CAPACITY':'${env[DEPLOY_ENV_NAME]?.params?.DB_PVC_SIZE?:"1Gi"}'
                ]
            ],
            [
                'file':'openshift/backend.dc.json',
                'params':[
                    'HOST':'${env[DEPLOY_ENV_NAME]?.params?.host?:("gwells" + deployments[DEPLOY_ENV_NAME].dcSuffix + "-" + deployments[DEPLOY_ENV_NAME].projectName + ".pathfinder.gov.bc.ca")}'
                ]
            ]
        ]
    ],
    stages:[
        'Build': true,
        'Unit Test': true,
        'Code Quality': false,
        'Deploy - DEV': true,
        'Load Fixtures': true,
        'ZAP Security Scan': false,
        'API Test': true,
        'Functional Tests': false
    ],
    pullRequest:[
        'id': env.CHANGE_ID,
        'head': GitHubHelper.getPullRequestLastCommitId(this)
    ]
]


/* Jenkins properties can be set on a pipeline-by-pipeline basis
    See Jenkins' Pipeline Systax for generation
    Globally equivalent to Jenkins > Manage Jenkins > Configure System
    https://jenkins.io/doc/pipeline/steps/workflow-multibranch/#properties-set-job-properties
*/
properties([
    buildDiscarder(
        logRotator(
            artifactDaysToKeepStr: '',
            artifactNumToKeepStr: '',
            daysToKeepStr: '',
            numToKeepStr: '5'
        )
    ),
    durabilityHint(
        'PERFORMANCE_OPTIMIZED'
    ),
    disableResume()
])


/* Prepare stage
    - abort any existing builds
    - echo pull request number
*/
stage('Prepare') {
    abortAllPreviousBuildInProgress(currentBuild)
}


/* Build stage
    - applying OpenShift build configs
    - creating OpenShift imagestreams, annotations and builds
    - build time optimizations (e.g. image reuse, build scheduling/readiness)
*/
_stage('Build', context) {
    node('master') {
        checkout scm
        new OpenShiftHelper().build(this, context)
        if ("master".equalsIgnoreCase(env.CHANGE_TARGET)) {
            new OpenShiftHelper().prepareForCD(this, context)
            new OpenShiftHelper().waitUntilEnvironmentIsReady(this, context, 'dev')
        }
        deleteDir()
    }
} //end stage


/* Continuous integration (CI)
   For feature branches merging into a release branch
    || Deployment, Fixtures and Fixture-Using Tests:
       - Deploy
       - Load fixtures
        -> || API tests
           || Functional tests
    || Unit tests and Code Quality
       - Unit tests
       - Code quality
    || ZAP Security Scan
       - ZAP security scan
*/
parallel (
    "Deployment, Fixtures and API/Functional Tests" : {
        _stage('Deploy - DEV', context) {
            node('master') {
                new OpenShiftHelper().deploy(this, context, 'dev')
            }
        }
        _stage('Load Fixtures - DEV', context) {
            node('master'){
                String projectName=context.deployments['dev'].projectName

                String podName = openshift.withProject(projectName){
                    String deploymentConfigName="gwells${context.deployments['dev'].dcSuffix}"
                    return openshift.selector('pod', ['deploymentconfig':deploymentConfigName]).objects()[0].metadata.name
                }

                sh "oc exec '${podName}' -n '${projectName}' -- bash -c '\
                    cd /opt/app-root/src/backend; \
                    python manage.py migrate; \
                    python manage.py loaddata gwells-codetables.json; \
                    python manage.py loaddata wellsearch-codetables.json registries-codetables.json; \
                    python manage.py loaddata wellsearch.json.gz registries.json; \
                    python manage.py createinitialrevisions \
                '"
            }
        } //end stage

        parallel (
            "API Test": {
                _stage('API Test', context) {
                    String baseURL = context.deployments['dev'].environmentUrl.substring(0, context.deployments['dev'].environmentUrl.indexOf('/', 8) + 1)
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
                                    envVar(
                                        key:'BASEURL',
                                        value: "${baseURL}gwells"
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
                    ],
                    envVars: [
                        envVar(
                            key:'BASEURL',
                            value: "${baseURL}gwells"
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
                ) {
                        node("nodejs-${context.uuid}") {
                            checkout scm
                            dir('api-tests') {
                                sh 'npm install -g newman'

                                try {
                                    sh '''
                                        newman run ./registries_api_tests.json \
                                            --global-var test_user=$GWELLS_API_TEST_USER \
                                            --global-var test_password=$GWELLS_API_TEST_PASSWORD \
                                            --global-var base_url="${BASEURL}" \
                                            --global-var auth_server=$GWELLS_API_TEST_AUTH_SERVER \
                                            --global-var client_id=$GWELLS_API_TEST_CLIENT_ID \
                                            --global-var client_secret=$GWELLS_API_TEST_CLIENT_SECRET \
                                            -r cli,junit,html
                                        newman run ./wells_api_tests.json \
                                            --global-var test_user=$GWELLS_API_TEST_USER \
                                            --global-var test_password=$GWELLS_API_TEST_PASSWORD \
                                            --global-var base_url="${BASEURL}" \
                                            --global-var auth_server=$GWELLS_API_TEST_AUTH_SERVER \
                                            --global-var client_id=$GWELLS_API_TEST_CLIENT_ID \
                                            --global-var client_secret=$GWELLS_API_TEST_CLIENT_SECRET \
                                            -r cli,junit,html
                                        newman run ./submissions_api_tests.json \
                                            --global-var test_user=$GWELLS_API_TEST_USER \
                                            --global-var test_password=$GWELLS_API_TEST_PASSWORD \
                                            --global-var base_url="${BASEURL}" \
                                            --global-var auth_server=$GWELLS_API_TEST_AUTH_SERVER \
                                            --global-var client_id=$GWELLS_API_TEST_CLIENT_ID \
                                            --global-var client_secret=$GWELLS_API_TEST_CLIENT_SECRET \
                                            -r cli,junit,html
                                    '''
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
                            } // end dir
                        } //end node
                    } //end podTemplate
                } //end stage
            },
            "Functional Tests":{
                _stage('Functional Tests', context){
                    String baseURL = context.deployments['dev'].environmentUrl.substring(
                        0,
                        context.deployments['dev'].environmentUrl.indexOf('/', 8) + 1
                    )
                    podTemplate(
                        label: "bddstack-${context.uuid}",
                        name: "bddstack-${context.uuid}",
                        serviceAccount: 'jenkins',
                        cloud: 'openshift',
                        containers: [
                          containerTemplate(
                             name: 'jnlp',
                             image: 'docker-registry.default.svc:5000/openshift/jenkins-slave-bddstack',
                             resourceRequestCpu: '800m',
                             resourceLimitCpu: '800m',
                             resourceRequestMemory: '3Gi',
                             resourceLimitMemory: '3Gi',
                             workingDir: '/home/jenkins',
                             command: '',
                             args: '${computer.jnlpmac} ${computer.name}',
                             envVars: [
                                 envVar(key:'BASEURL', value: baseURL),
                                 envVar(key:'GRADLE_USER_HOME', value: '/var/cache/artifacts/gradle')
                             ]
                          )
                        ],
                        volumes: [
                            persistentVolumeClaim(
                                mountPath: '/var/cache/artifacts',
                                claimName: 'cache',
                                readOnly: false
                            )
                        ]
                    ){
                        node("bddstack-${context.uuid}") {
                            echo "Build: ${BUILD_ID}"
                            echo "baseURL: ${baseURL}"
                            checkout scm
                            dir('functional-tests') {
                                try {
                                    sh './gradlew chromeHeadlessTest'
                                } finally {
                                        archiveArtifacts allowEmptyArchive: true, artifacts: 'build/reports/geb/**/*'
                                        junit testResults:'build/test-results/**/*.xml', allowEmptyResults:true
                                        publishHTML (
                                            target: [
                                                allowMissing: true,
                                                alwaysLinkToLastBuild: false,
                                                keepAll: true,
                                                reportDir: 'build/reports/spock',
                                                reportFiles: 'index.html',
                                                reportName: "Test: BDD Spock Report"
                                            ]
                                        )
                                        publishHTML (
                                            target: [
                                                allowMissing: true,
                                                alwaysLinkToLastBuild: false,
                                                keepAll: true,
                                                reportDir: 'build/reports/tests/chromeHeadlessTest',
                                                reportFiles: 'index.html',
                                                reportName: "Test: Full Test Report"
                                            ]
                                        )
                                }
                            } //end dir
                        } //end node
                    } //end podTemplate
                } //end stage
            }
        )
    },
    "Unit Tests and Code Quality" : {
        /* Unit test stage
            - use Django's manage.py to run python unit tests (w/ nose.cfg)
            - use 'npm run unit' to run JavaScript unit tests
            - stash test results for code quality stage
        */
        _stage('Unit Tests', context) {
            podTemplate(
                label: "node-${context.uuid}",
                name:"node-${context.uuid}",
                serviceAccount: 'jenkins',
                cloud: 'openshift',
                containers: [
                    containerTemplate(
                        name: 'jnlp',
                        image: 'jenkins/jnlp-slave:3.10-1-alpine',
                        args: '${computer.jnlpmac} ${computer.name}',
                        resourceRequestCpu: '100m',
                        resourceLimitCpu: '100m'
                    ),
                    containerTemplate(
                        name: 'app',
                        image: "docker-registry.default.svc:5000/moe-gwells-tools/gwells${context.buildNameSuffix}:${context.buildEnvName}",
                        ttyEnabled: true,
                        command: 'cat',
                        resourceRequestCpu: '1.5',
                        resourceLimitCpu: '1.5',
                        resourceRequestMemory: '2.5Gi',
                        resourceLimitMemory: '2.5Gi'
                    )
                ]
            ) {
                node("node-${context.uuid}") {
                    container('app') {
                        sh script: '''#!/usr/bin/container-entrypoint /bin/sh
                            printf "Python version: "&& python --version
                            printf "Pip version:    "&& pip --version
                            printf "Node version:   "&& node --version
                            printf "NPM version:    "&& npm --version
                        '''

                        parallel (
                            "Unit Test: Python": {
                                try {
                                    sh script: '''#!/usr/bin/container-entrypoint /bin/sh
                                        cd /opt/app-root/src/backend
                                        DATABASE_ENGINE=sqlite DEBUG=False TEMPLATE_DEBUG=False python manage.py test -c nose.cfg
                                    '''
                                    sh script: '''#!/usr/bin/container-entrypoint /bin/sh
                                        cp /opt/app-root/src/backend/nosetests.xml ./
                                        cp /opt/app-root/src/backend/coverage.xml ./
                                    '''
                                } finally {
                                    stash includes: 'nosetests.xml,coverage.xml', name: 'coverage'
                                    junit 'nosetests.xml'
                                }
                            },
                            "Unit Test: Node": {
                                try {
                                    sh script: '''#!/usr/bin/container-entrypoint /bin/sh
                                        cd /opt/app-root/src/frontend
                                        npm test
                                    '''
                                    sh script: '''#!/usr/bin/container-entrypoint /bin/sh
                                        mkdir -p frontend/test/
                                        cp -R /opt/app-root/src/frontend/test/unit ./frontend/test/
                                        cp /opt/app-root/src/frontend/junit.xml ./frontend/
                                    '''
                                } finally {
                                    archiveArtifacts allowEmptyArchive: true, artifacts: 'frontend/test/unit/**/*'
                                    stash includes: 'frontend/test/unit/coverage/clover.xml', name: 'nodecoverage'
                                    stash includes: 'frontend/junit.xml', name: 'nodejunit'
                                    junit 'frontend/junit.xml'
                                    publishHTML (
                                        target: [
                                            allowMissing: false,
                                            alwaysLinkToLastBuild: false,
                                            keepAll: true,
                                            reportDir: 'frontend/test/unit/coverage/lcov-report/',
                                            reportFiles: 'index.html',
                                            reportName: "Node Coverage Report"
                                        ]
                                    )
                                }
                            } //end branch
                        ) //end parallel
                    } //end container
                } //end node
            } //end podTemplate
        } //end stage


        /* Code quality stage - pipeline step/closure
            - unstash unit test results (previous stage)
            - use SonarQube to consume results (*.xml)
        */
        _stage('Code Quality', context) {
            podTemplate(
                name: "sonar-runner${context.uuid}",
                label: "sonar-runner${context.uuid}",
                serviceAccount: 'jenkins',
                cloud: 'openshift',
                containers:[
                    containerTemplate(
                        name: 'jnlp',
                        resourceRequestMemory: '1Gi',
                        resourceLimitMemory: '4Gi',
                        resourceRequestCpu: '500m',
                        resourceLimitCpu: '4000m',
                        image: 'registry.access.redhat.com/openshift3/jenkins-slave-maven-rhel7:v3.7',
                        workingDir: '/tmp',
                        args: '${computer.jnlpmac} ${computer.name}',
                        envVars: [
                            envVar(key:'GRADLE_USER_HOME', value: '/var/cache/artifacts/gradle')
                        ]
                    )
                ],
                volumes: [
                    persistentVolumeClaim(
                        mountPath: '/var/cache/artifacts',
                        claimName: 'cache',
                        readOnly: false
                    )
                ]
            ){
                node("sonar-runner${context.uuid}") {
                    //the checkout is mandatory, otherwise code quality check would fail
                    echo "checking out source"
                    echo "Build: ${BUILD_ID}"
                    checkout scm

                    String SONARQUBE_URL = 'https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca'
                    echo "SONARQUBE_URL: ${SONARQUBE_URL}"
                    dir('app') {
                        unstash 'nodejunit'
                        unstash 'nodecoverage'
                    }
                    dir('sonar-runner') {
                        unstash 'coverage'
                        sh script:
                            """
                                ./gradlew -q dependencies
                                ./gradlew sonarqube -Dsonar.host.url=${SONARQUBE_URL} -Dsonar.verbose=true \
                                    --stacktrace --info  -Dsonar.sources=..
                            """,
                            returnStdout: true
                    }
                } //end node
            } //end podTemplate
        } //end stage
    }, //end branch
    "ZAP Security Scan": {
        _stage('ZAP Security Scan', context) {
            podTemplate(
                label: "zap-${context.uuid}",
                name: "zap-${context.uuid}",
                serviceAccount: "jenkins",
                cloud: "openshift",
                containers: [
                    containerTemplate(
                        name: 'jnlp',
                        image: 'docker-registry.default.svc:5000/moe-gwells-dev/owasp-zap-openshift',
                        resourceRequestCpu: '500m',
                        resourceLimitCpu: '1000m',
                        resourceRequestMemory: '3Gi',
                        resourceLimitMemory: '4Gi',
                        workingDir: '/home/jenkins',
                        command: '',
                        args: '${computer.jnlpmac} ${computer.name}'
                    )
                ]
            ) {
                node("zap-${context.uuid}") {
                    //the checkout is mandatory
                    echo "checking out source"
                    echo "Build: ${BUILD_ID}"
                    checkout scm
                    dir('zap') {
                        def retVal = sh (
                            script: """
                                set -eux
                                ./runzap.sh
                            """
                        )
                        publishHTML(
                            target: [
                                allowMissing: false,
                                alwaysLinkToLastBuild: false,
                                keepAll: true,
                                reportDir: '/zap/wrk',
                                reportFiles: 'index.html',
                                reportName: 'ZAP Full Scan',
                                reportTitles: 'ZAP Full Scan'
                            ]
                        )
                        echo "Return value is: ${retVal}"
                    }
                } //end node
            } //end podTemplate
        } //end stage
    } //end branch
) //end parallel


/* Continuous integration (CI)
   For feature branches merging into a release branch
    || Deployment, Fixtures and Fixture-Using Tests:
       - Deploy
       - Load fixtures
        -> || API tests
           || Functional tests
    || Unit tests and Code Quality
       - Unit tests
       - Code quality
    || ZAP Security Scan
       - ZAP security scan
*/


/* Continuous deployment (CD)
   For PRs to the master branch, reserved for release branches and hotfixes
   Iterates through DEV (skipped), TEST and PROD environments
    - [prompt/stop]
      - deployment to persistent test environment
      - smoke tests
      - deployment
    - [prompt/stop]
      - deployment to persistent production environment
    - [prompt/stop]
      - merge sprint release or hotfix branch into master
      - close PR
      - delete branch
*/
for(String envKeyName: context.env.keySet() as String[]){
    String stageDeployName=envKeyName.toUpperCase()

    if ("master".equalsIgnoreCase(env.CHANGE_TARGET)) {
        _stage("Readiness - ${stageDeployName}", context) {
            node('master') {
                new OpenShiftHelper().waitUntilEnvironmentIsReady(this, context, envKeyName)
            }
        }

        _stage("Approve - ${stageDeployName}", context) {
            def inputResponse = null;
            try{
                inputResponse = input(
                    id: "deploy_${stageDeployName.toLowerCase()}",
                    message: "Deploy to ${stageDeployName}?",
                    ok: 'Approve',
                    submitterParameter: 'approved_by'
                )
            }catch(ex){
                error "Pipeline has been aborted. - ${ex}"
            }
            GitHubHelper.getPullRequest(this).comment(
                "User '${inputResponse}' has approved deployment to '${stageDeployName}'"
            )
        }

        _stage("Deploy - ${stageDeployName}", context) {
            node('master') {
                new OpenShiftHelper().deploy(this, context, envKeyName)
            }
        }

        _stage("Smoke Test - ${stageDeployName}", context){
            String baseURL = context.deployments[envKeyName].environmentUrl.substring(
                0,
                context.deployments[envKeyName].environmentUrl.indexOf('/', 8) + 1
            )
            podTemplate(
                label: "bddstack-${context.uuid}",
                name: "bddstack-${context.uuid}",
                serviceAccount: 'jenkins',
                cloud: 'openshift',
                containers: [
                  containerTemplate(
                     name: 'jnlp',
                     image: 'docker-registry.default.svc:5000/openshift/jenkins-slave-bddstack',
                     resourceRequestCpu: '800m',
                     resourceLimitCpu: '800m',
                     resourceRequestMemory: '3Gi',
                     resourceLimitMemory: '3Gi',
                     workingDir: '/home/jenkins',
                     command: '',
                     args: '${computer.jnlpmac} ${computer.name}',
                     envVars: [
                         envVar(key:'BASEURL', value: baseURL),
                         envVar(key:'GRADLE_USER_HOME', value: '/var/cache/artifacts/gradle')
                     ]
                  )
                ],
                volumes: [
                    persistentVolumeClaim(
                        mountPath: '/var/cache/artifacts',
                        claimName: 'cache',
                        readOnly: false
                    )
                ]
            ){
                node("bddstack-${context.uuid}") {
                    echo "Build: ${BUILD_ID}"
                    echo "baseURL: ${baseURL}"

                    //the checkout is mandatory, otherwise functional test would fail
                    echo "checking out source"
                    checkout scm
                    dir('functional-tests') {
                        Integer attempts = 0
                        Integer attemptsMax = 2
                        try {
                            waitUntil {
                                boolean isDone=false
                                attempts++
                                try{
                                    sh './gradlew -DchromeHeadlessTest.single=WellDetails chromeHeadlessTest'
                                    isDone=true
                                } catch (ex) {
                                    echo "${stackTraceAsString(ex)}"
                                    if ( attempts < attemptsMax ){
                                        echo "DEV - Functional Tests Failed - Wait one minute and retry once"
                                        sleep 60
                                    } else {
                                        echo "DEV - Functional Tests Failed - Retry Failed"
                                        throw ex
                                    }
                                }
                                return isDone
                            }
                        } finally {
                                archiveArtifacts allowEmptyArchive: true, artifacts: 'build/reports/geb/**/*'
                                junit testResults:'build/test-results/**/*.xml', allowEmptyResults:true
                                publishHTML (
                                    target: [
                                        allowMissing: true,
                                        alwaysLinkToLastBuild: false,
                                        keepAll: true,
                                        reportDir: 'build/reports/spock',
                                        reportFiles: 'index.html',
                                        reportName: "Test: BDD Spock Report"
                                    ]
                                )
                                publishHTML (
                                    target: [
                                        allowMissing: true,
                                        alwaysLinkToLastBuild: false,
                                        keepAll: true,
                                        reportDir: 'build/reports/tests/chromeHeadlessTest',
                                        reportFiles: 'index.html',
                                        reportName: "Test: Full Test Report"
                                    ]
                                )
                        }
                    } //end dir
                } //end node
            } //end podTemplate
        } //end stage
    } //end if
} // end for


/* Cleanup stage - pipeline step/closure
    - Prompt user to continue
    - Remove temporary OpenShift resources (moe-gwells-dev)
    - Merge and delete branches
*/
stage('Cleanup') {

    def inputResponse = null
    String mergeMethod='merge'

    waitUntil {
        boolean isDone=false
        try{
            inputResponse=input(
                id: 'close_pr',
                message: "Ready to Accept/Merge (using '${mergeMethod}' method), and Close pull-request #${env.CHANGE_ID}?",
                ok: 'Yes',
                submitter: 'authenticated',
                submitterParameter: 'approver'
            )
            echo "inputResponse:${inputResponse}"

            echo "Merging and Closing PR"
            GitHubHelper.mergeAndClosePullRequest(this, mergeMethod)

            echo "Clearing OpenShift resources"
            new OpenShiftHelper().cleanup(this, context)

            // TODO: broadcast status/result to Slack channel
            isDone=true
        }catch (ex){
            echo "${stackTraceAsString(ex)}"
            def inputAction = input(
                message: "This 'Cleanup' stage has failed. See error above.",
                ok: 'Confirm',
                submitter: 'authenticated',
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
    } //end waitUntil
}
