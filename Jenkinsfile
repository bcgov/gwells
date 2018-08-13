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
    - primary means of running stages
    - reads which stages are to be run
    - handles stages defined separately in closures (body)
    - catches errors and provides output
*/
def _stage(String name, Map context, boolean retry=0, boolean withCommitStatus=true, Closure body) {
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


/* Project and pipeline-specific settings
   Includes:
    - project name
    - uuid
    - web path (dev|test|prod)
    - build config templates (*.bc)
    - deployment config templates (*.dc) and parameters
    - stage names and enabled status (true|false)
    - git pull request details
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
        'Readiness - DEV': true,
        'Deploy - DEV': true,
        'Load Fixtures - DEV': true,
        'ZAP Security Scan': false,
        'API Test': true,
        'Functional Tests': false
    ],
    pullRequest:[
        'id': env.CHANGE_ID,
        'head': GitHubHelper.getPullRequestLastCommitId(this)
    ]
]


/* Continuous integration (CI)
   Triggers when a PR targets a sprint release branch
    - prepare OpenShift environment
    - build (build configs, imagestreams)
    - unit tests
    - deployment to transient dev environment
    - load fixtures
    - API tests
    - functional tests
    - merge PR into sprint release branch

   Continuous deployment (CD)
   Triggers when a PR targets the master branch, reserved for release branches and hotfixes
    - All CI steps
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
def isCI = !"master".equalsIgnoreCase(env.CHANGE_TARGET)
def isCD = "master".equalsIgnoreCase(env.CHANGE_TARGET)


/* Jenkins properties can be set on a pipeline-by-pipeline basis
   Includes:
    - build discarder
    - build concurrency
    - master node failure handling
    - throttling
    - parameters
    - build triggers
    See Jenkins' Pipeline Systax for generation
    Globally equivalent to Jenkins > Manage Jenkins > Configure System
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
    echo "BRANCH_NAME=${env.BRANCH_NAME}"
    echo "CHANGE_ID=${env.CHANGE_ID}"
    echo "CHANGE_TARGET=${env.CHANGE_TARGET}"
    echo "BUILD_URL=${env.BUILD_URL}"
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
        }
        deleteDir()
    }
} //end stage


/* Unit test stage - pipeline step/closure
    - use Django's manage.py to run python unit tests (w/ nose.cfg)
    - use 'npm run unit' to run JavaScript unit tests
*/
_stage('DEV: Unit Tests and Deployment', context) {
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
            ),
            containerTemplate(
                name: 'app',
                image: "docker-registry.default.svc:5000/moe-gwells-tools/gwells${context.buildNameSuffix}:${context.buildEnvName}",
                ttyEnabled: true,
                command: 'cat',
                resourceRequestCpu: '2.5',
                resourceRequestMemory: '2.5Gi'
            )
        ]
    ) {
        parallel (
            "Deployment": {
                node('master') {
                    new OpenShiftHelper().waitUntilEnvironmentIsReady(this, context, 'dev')
                    new OpenShiftHelper().deploy(this, context, 'dev')

                    String projectName=context.deployments['dev'].projectName
                    String deploymentConfigName="gwells${context.deployments['dev'].dcSuffix}"
                    def podList = openshift.withProject(projectName){
                        return openshift.selector('pod', ['deploymentconfig':deploymentConfigName]).objects()
                    }
                    String pod0 = podList[0].metadata.name
                    String pod1 = podList[0].metadata.name
                    parallel (
                        "Load Fixtures": {
                            sh "oc exec '${pod0}' -n '${projectName}' -- bash -c '\
                                cd /opt/app-root/src/backend; \
                                python manage.py loaddata gwells-codetables.json; \
                                python manage.py loaddata wellsearch-codetables.json registries-codetables.json; \
                                python manage.py loaddata wellsearch.json.gz registries.json; \
                                python manage.py createinitialrevisions \
                            '"
                        },
                        "Unit Tests": {
                            sh "oc exec '${pod1}' -n '${projectName}' -- bash -c '\
                                cd /opt/app-root/src/frontend; \
                                npm install --save-dev jest@23; \
                                npm test --detectLeaks --runInBand -- --logHeapUsage --maxWorkers=1 \
                            '"
                            sh "oc exec '${pod1}' -n '${projectName}' -- bash -c '\
                                cd /opt/app-root/src/backend; \
                                DATABASE_ENGINE=sqlite DEBUG=False TEMPLATE_DEBUG=False python manage.py test -c nose.cfg \
                            '"
                        },
                        "API Tests": {
                            def stageOpt =(context?.stages?:[:])['API Test']
                            if (stageOpt == null || stageOpt == true) {
                                String baseURL = context.deployments['dev'].environmentUrl.substring(
                                    0,
                                    context.deployments['dev'].environmentUrl.indexOf('/', 8) + 1
                                )
                                podTemplate(
                                    label: "nodejs-${context.uuid}",
                                    name: "nodejs-${context.uuid}",
                                    serviceAccount: 'jenkins',
                                    cloud: 'openshift',
                                    containers: [
                                        containerTemplate(
                                            name: 'jnlp',
                                            image: 'registry.access.redhat.com/openshift3/jenkins-agent-nodejs-8-rhel7',
                                            resourceRequestCpu: '1Gi',
                                            resourceRequestMemory: '1Gi',
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
                                    ]
                                ) {
                                    node("nodejs-${context.uuid}") {
                                        //the checkout is mandatory, otherwise functional test would fail
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
                            }
                        },
                        "Functional Tests": {
                            def stageOpt =(context?.stages?:[:])['Functional Tests']
                            if (stageOpt == null || stageOpt == true) {
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
                                         resourceRequestMemory: '3Gi',
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
                                        //the checkout is mandatory, otherwise functional test would fail
                                        checkout scm
                                        dir('functional-tests') {
                                            try {
                                                sh './gradlew chromeHeadlessTest'
                                            } catch (ex) {
                                                echo "${stackTraceAsString(ex)}"
                                                throw ex
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
                            }
                        },
                        "ZAP Security Scan": {
                            def stageOpt =(context?.stages?:[:])['ZAP Security Scan']
                            if (stageOpt == null || stageOpt == true) {
                                podTemplate(
                                    label: "zap-${context.uuid}",
                                    name: "zap-${context.uuid}",
                                    serviceAccount: "jenkins",
                                    cloud: "openshift",
                                    containers: [
                                        containerTemplate(
                                            name: 'jnlp',
                                            image: 'docker-registry.default.svc:5000/moe-gwells-dev/owasp-zap-openshift',
                                            resourceRequestCpu: '1Gi',
                                            resourceRequestMemory: '4Gi',
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
                                                script: "./runzap.sh",
                                                returnStdout: true
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
                            } //end if
                        } //end branch
                    ) //end parallel
                } //end node
            } //end node
        ) //end parallel
    } //end podTemplate
} //end stage


/* Primary stage execution block
   - iterates through stages, set in context (Map)
   - _stage wrapper adds functionality, stability
*/
for(String envKeyName: context.env.keySet() as String[]){
    String stageDeployName=envKeyName.toUpperCase()

    if (!"DEV".equalsIgnoreCase(stageDeployName) && isCD){
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

        String testStageName="DEV".equalsIgnoreCase(stageDeployName)?"Functional Tests":"Smoke Test - ${stageDeployName}"
        _stage(testStageName, context){
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
                     resourceRequestMemory: '3Gi',
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
                                    if ("DEV".equalsIgnoreCase(stageDeployName)) {
                                        sh './gradlew chromeHeadlessTest'
                                    } else {
                                        sh './gradlew -DchromeHeadlessTest.single=WellDetails chromeHeadlessTest'
                                    }
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
