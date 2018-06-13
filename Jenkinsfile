// Jenkinsfile (Scripted Pipeline)

/* Gotchas

- PodTemplate name/label has to be unique.
    otherwise,there is some configuration caching that won't actually take the latest configuration
    e.g.: Changing image, envvars, so on.
    maybe only when overwriting global templates?

References:
- https://gist.github.com/matthiasbalke/3c9ecccbea1d460ee4c3fbc5843ede4a

*/

import hudson.model.Result;
import jenkins.model.CauseOfInterruption.UserInterruption;
import org.kohsuke.github.*
import bcgov.OpenShiftHelper
import bcgov.GitHubHelper

@NonCPS
private static String stackTraceAsString(Throwable t) {
    StringWriter sw = new StringWriter();
    t.printStackTrace(new PrintWriter(sw));
    return sw.toString()
}

String stageStatusContext(String stageName){
    return "stages/${stageName.toLowerCase()}"
}

void setStageStatus(Map context, String name, String status) {
     GitHubHelper.createCommitStatus(this, context.pullRequest.head, status, "${env.BUILD_URL}", "Stage '${name}'", stageStatusContext(name))
}

void notifyStageStatus(Map context, String name, String status) {
    setStageStatus(context, name, status)
}

def _stage(String name, Map context, boolean retry=0, boolean withCommitStatus=true, Closure body) {
    def stageOpt =(context?.stages?:[:])[name]
    boolean isEnabled=(stageOpt == null || stageOpt == true)
    //echo "Stage - ${stage}"
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
                        parameters: [choice(name: 'action', choices: 'Re-run\nIgnore', description: 'What would you like to do?')]
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

Map context = [
  'name': 'gwells',
  'uuid' : "${env.JOB_BASE_NAME}-${env.BUILD_NUMBER}-${env.CHANGE_ID}",
  'env': [
      'dev':[:],
      'test':['params':['host':'gwells-test.pathfinder.gov.bc.ca']],
      'prod':['params':['host':'gwells-prod.pathfinder.gov.bc.ca', 'DB_PVC_SIZE':'5Gi']]
  ],
  'templates': [
      'build':[
          ['file':'openshift/postgresql.bc.json'],
          ['file':'openshift/backend.bc.json']
      ],
      'deployment':[
          ['file':'openshift/postgresql.dc.json',
              'params':[
                  'DATABASE_SERVICE_NAME':'gwells-pgsql${deploy.dcSuffix}',
                  'IMAGE_STREAM_NAMESPACE':'',
                  'IMAGE_STREAM_NAME':'gwells-postgresql${deploy.dcSuffix}',
                  'IMAGE_STREAM_VERSION':'${deploy.envName}',
                  'POSTGRESQL_DATABASE':'gwells',
                  'VOLUME_CAPACITY':'${env[DEPLOY_ENV_NAME]?.params?.DB_PVC_SIZE?:"1Gi"}'
              ]
          ],
          ['file':'openshift/backend.dc.json', 'params':['HOST':'${env[DEPLOY_ENV_NAME]?.params?.host?:("gwells" + deployments[DEPLOY_ENV_NAME].dcSuffix + "-" + deployments[DEPLOY_ENV_NAME].projectName + ".pathfinder.gov.bc.ca")}']]
      ]
  ],
  stages:[
    'Build': true,
    'Unit Test': true,
    'Code Quality': true,
    'Readiness - DEV': true,
    'Deploy - DEV': true,
    'Load Fixtures - DEV': true,
    'API Test': true,
    'Full Test - DEV': true
  ],
  pullRequest:[
    'id': env.CHANGE_ID,
    'head': GitHubHelper.getPullRequestLastCommitId(this)
  ]
]

def isCI = !"master".equalsIgnoreCase(env.CHANGE_TARGET)
def isCD = "master".equalsIgnoreCase(env.CHANGE_TARGET)


properties([
        buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '5')),
        durabilityHint('PERFORMANCE_OPTIMIZED') /*, parameters([string(defaultValue: '', description: '', name: 'run_stages')]) */
])

stage('Prepare') {
    abortAllPreviousBuildInProgress(currentBuild)
    echo "BRANCH_NAME=${env.BRANCH_NAME}\nCHANGE_ID=${env.CHANGE_ID}\nCHANGE_TARGET=${env.CHANGE_TARGET}\nBUILD_URL=${env.BUILD_URL}"
}

/**
This function wrapper allows stages to be optional/skipped.
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

_stage('Unit Test', context) {
    podTemplate(label: "node-${context.uuid}", name:"node-${context.uuid}", serviceAccount: 'jenkins', cloud: 'openshift', containers: [
        containerTemplate(name: 'jnlp', image: 'jenkins/jnlp-slave:3.10-1-alpine', args: '${computer.jnlpmac} ${computer.name}', resourceRequestCpu: '100m',resourceLimitCpu: '100m'),
        containerTemplate(name: 'app', image: "docker-registry.default.svc:5000/moe-gwells-tools/gwells${context.buildNameSuffix}:${context.buildEnvName}", ttyEnabled: true, command: 'cat',
            resourceRequestCpu: '2000m',
            resourceLimitCpu: '2000m',
            resourceRequestMemory: '2Gi',
            resourceLimitMemory: '2Gi')
      ]
    ) {
        node("node-${context.uuid}") {
            try {
                container('app') {
                    sh script: '''#!/usr/bin/container-entrypoint /bin/sh
                        set -x
                        python --version
                        pip --version
                        node --version
                        npm --version

                        (cd /opt/app-root/src && python manage.py migrate)
                        (cd /opt/app-root/src && export ENABLE_DATA_ENTRY="True" && export NOSE_PROCESSES=4 && python manage.py test -c nose.cfg)
                        (cd /opt/app-root/src/frontend && npm test)
                        mkdir -p frontend/test/
                        cp -R /opt/app-root/src/frontend/test/unit ./frontend/test/
                        cp /opt/app-root/src/nosetests.xml ./
                        cp /opt/app-root/src/coverage.xml ./
                        cp /opt/app-root/src/frontend/junit.xml ./frontend/
                    '''
                }
            } finally {
                archiveArtifacts allowEmptyArchive: true, artifacts: 'frontend/test/unit/**/*'
                stash includes: 'nosetests.xml,coverage.xml', name: 'coverage'
                stash includes: 'frontend/test/unit/coverage/clover.xml', name: 'nodecoverage'
                stash includes: 'frontend/junit.xml', name: 'nodejunit'
                junit 'nosetests.xml,frontend/junit.xml'
                publishHTML (target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: 'frontend/test/unit/coverage/lcov-report/',
                    reportFiles: 'index.html',
                    reportName: "Node Coverage Report"
                ])
            }
        }
    }
} //end stage



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
            persistentVolumeClaim(mountPath: '/var/cache/artifacts', claimName: 'cache', readOnly: false)
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
                sh './gradlew -q dependencies'
                sh returnStdout: true, script: "./gradlew sonarqube -Dsonar.host.url=${SONARQUBE_URL} -Dsonar.verbose=true --stacktrace --info  -Dsonar.sources=.."
            }
        }
    }

} //end stage


for(String envKeyName: context.env.keySet() as String[]){
    String stageDeployName=envKeyName.toUpperCase()

    if ("DEV".equalsIgnoreCase(stageDeployName) || isCD) {
        _stage("Readiness - ${stageDeployName}", context) {
            node('master') {
                new OpenShiftHelper().waitUntilEnvironmentIsReady(this, context, envKeyName)
            }
        }
    }

    if (!"DEV".equalsIgnoreCase(stageDeployName) && isCD){
        _stage("Approve - ${stageDeployName}", context) {
            def inputResponse = null;
            try{
                inputResponse = input(id: "deploy_${stageDeployName.toLowerCase()}", message: "Deploy to ${stageDeployName}?", ok: 'Approve', submitterParameter: 'approved_by')
            }catch(ex){
                error "Pipeline has been aborted. - ${ex}"
            }
            //echo "inputResponse:${inputResponse}"
            GitHubHelper.getPullRequest(this).comment("User '${inputResponse}' has approved deployment to '${stageDeployName}'")
        }
    }

    if ("DEV".equalsIgnoreCase(stageDeployName) || isCD){
        _stage("Deploy - ${stageDeployName}", context) {
            node('master') {
                new OpenShiftHelper().deploy(this, context, envKeyName)
            }
        }
    }

    if ("DEV".equalsIgnoreCase(stageDeployName)){
        _stage("Load Fixtures - ${stageDeployName}", context) {
            node('master'){
                String podName=null
                String projectName=context.deployments[envKeyName].projectName
                String deploymentConfigName="gwells${context.deployments[envKeyName].dcSuffix}"
                echo "env:${context.env[envKeyName]}"
                echo "deployment:${context.deployments[envKeyName]}"
                echo "projectName:${projectName}"
                echo "deploymentConfigName:${deploymentConfigName}"

                openshift.withProject(projectName){
                    podName=openshift.selector('pod', ['deploymentconfig':deploymentConfigName]).objects()[0].metadata.name
                }
                sh "oc exec '${podName}' -n '${projectName}' -- bash -c 'cd /opt/app-root/src && pwd && python manage.py flush --no-input'"
                // Lookup tables common to all system components (e.g. Django apps)
                sh "oc exec '${podName}' -n '${projectName}' -- bash -c 'cd /opt/app-root/src && pwd && python manage.py loaddata gwells-codetables.json'"
                // Lookup tables for the Wellsearch component (not yet a Django app) and Registries app
                sh "oc exec '${podName}' -n '${projectName}' -- bash -c 'cd /opt/app-root/src && pwd && python manage.py loaddata wellsearch-codetables.json registries-codetables.json'"
                // Test data for the Wellsearch component (not yet a Django app) and Registries app
                sh "oc exec '${podName}' -n '${projectName}' -- bash -c 'cd /opt/app-root/src && pwd && python manage.py loaddata wellsearch.json.gz registries.json'"
            }
        }
    }

    if ("DEV".equalsIgnoreCase(stageDeployName)){
        _stage('API Test', context) {
            String baseURL = context.deployments[envKeyName].environmentUrl.substring(0, context.deployments[envKeyName].environmentUrl.indexOf('/', 8) + 1)
            podTemplate(label: "nodejs-${context.uuid}", name: "nodejs-${context.uuid}", serviceAccount: 'jenkins', cloud: 'openshift', containers: [
              containerTemplate(
                name: 'jnlp',
                image: 'registry.access.redhat.com/openshift3/jenkins-slave-nodejs-rhel7',
                resourceRequestCpu: '800m',
                resourceLimitCpu: '800m',
                resourceRequestMemory: '1Gi',
                resourceLimitMemory: '1Gi',
                workingDir: '/tmp',
                command: '',
                args: '${computer.jnlpmac} ${computer.name}',
                envVars: [
                    envVar(key:'BASEURL', value: "${baseURL}gwells"),
                    secretEnvVar(key: 'GWELLS_API_TEST_USER', secretName: 'apitest-secrets', secretKey: 'username'),
                    secretEnvVar(key: 'GWELLS_API_TEST_PASSWORD', secretName: 'apitest-secrets', secretKey: 'password'),
                    secretEnvVar(key: 'GWELLS_API_TEST_AUTH_SERVER', secretName: 'apitest-secrets', secretKey: 'auth_server'),
                    secretEnvVar(key: 'GWELLS_API_TEST_CLIENT_ID', secretName: 'apitest-secrets', secretKey: 'client_id'),
                    secretEnvVar(key: 'GWELLS_API_TEST_CLIENT_SECRET', secretName: 'apitest-secrets', secretKey: 'client_secret')
                ]
              )
            ],envVars: [
                envVar(key:'BASEURL', value: "${baseURL}gwells"),
                secretEnvVar(key: 'GWELLS_API_TEST_USER', secretName: 'apitest-secrets', secretKey: 'username'),
                secretEnvVar(key: 'GWELLS_API_TEST_PASSWORD', secretName: 'apitest-secrets', secretKey: 'password'),
                secretEnvVar(key: 'GWELLS_API_TEST_AUTH_SERVER', secretName: 'apitest-secrets', secretKey: 'auth_server'),
                secretEnvVar(key: 'GWELLS_API_TEST_CLIENT_ID', secretName: 'apitest-secrets', secretKey: 'client_id'),
                secretEnvVar(key: 'GWELLS_API_TEST_CLIENT_SECRET', secretName: 'apitest-secrets', secretKey: 'client_secret')
            ])
            {
                node("nodejs-${context.uuid}") {
                //the checkout is mandatory, otherwise functional test would fail
                    echo "checking out source"
                    echo "Build: ${BUILD_ID}"
                    echo "baseURL: ${baseURL}"
                    sh '''#!/bin/bash
                        echo BASEURL=$BASEURL
                    '''

                    //input(message: "Verify Environment variables. Continue?")
                    checkout scm
                    dir('api-tests') {
                        sh 'npm install -g newman'

                        try {
                            sh 'newman run ./registries_api_tests.json --global-var test_user=$GWELLS_API_TEST_USER --global-var test_password=$GWELLS_API_TEST_PASSWORD --global-var base_url="${BASEURL}" --global-var auth_server=$GWELLS_API_TEST_AUTH_SERVER --global-var client_id=$GWELLS_API_TEST_CLIENT_ID --global-var client_secret=$GWELLS_API_TEST_CLIENT_SECRET -r cli,junit,html;'
                        } finally {
                                junit 'newman/*.xml'
                                publishHTML (target: [
                                            allowMissing: false,
                                            alwaysLinkToLastBuild: false,
                                            keepAll: true,
                                            reportDir: 'newman',
                                            reportFiles: 'newman*.html',
                                            reportName: "API Test Report"
                                        ])
                                stash includes: 'newman/*.xml', name: 'api-tests'
                        }
                    } // end dir
                } //end node
            } //end podTemplate
        } //end stage
    }

    if ("DEV".equalsIgnoreCase(stageDeployName) || isCD){
        String testStageName="DEV".equalsIgnoreCase(stageDeployName)?"Full Test - DEV":"Smoke Test - ${stageDeployName}"
        _stage(testStageName, context){
            String baseURL = context.deployments[envKeyName].environmentUrl.substring(0, context.deployments[envKeyName].environmentUrl.indexOf('/', 8) + 1)
            podTemplate(label: "bddstack-${context.uuid}", name: "bddstack-${context.uuid}", serviceAccount: 'jenkins', cloud: 'openshift',
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
                    persistentVolumeClaim(mountPath: '/var/cache/artifacts', claimName: 'cache', readOnly: false)
                ]
            ){
                node("bddstack-${context.uuid}") {
                    echo "Build: ${BUILD_ID}"
                    echo "baseURL: ${baseURL}"
                    sh 'echo "BASEURL=${BASEURL}"'
                    sh 'echo "GRADLE_USER_HOME=${GRADLE_USER_HOME}"'

                    //the checkout is mandatory, otherwise functional test would fail
                    echo "checking out source"
                    checkout scm
                    /*
                    dir('functional-tests/build/test-results') {
                        sh 'echo "BASEURL=${BASEURL}"'
                        unstash 'coverage'
                        sh 'rm coverage.xml'
                        unstash 'nodejunit'
                    }
                    */
                    //dir('app') {
                    //    sh 'python manage.py loaddata wells registries'
                    //}
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
                                publishHTML (target: [
                                            allowMissing: true,
                                            alwaysLinkToLastBuild: false,
                                            keepAll: true,
                                            reportDir: 'build/reports/spock',
                                            reportFiles: 'index.html',
                                            reportName: "Test: BDD Spock Report"
                                        ])
                                publishHTML (target: [
                                            allowMissing: true,
                                            alwaysLinkToLastBuild: false,
                                            keepAll: true,
                                            reportDir: 'build/reports/tests/chromeHeadlessTest',
                                            reportFiles: 'index.html',
                                            reportName: "Test: Full Test Report"
                                        ])
                            //todo: install perf report plugin.
                            //perfReport compareBuildPrevious: true, excludeResponseTime: true, ignoreFailedBuilds: true, ignoreUnstableBuilds: true, modeEvaluation: true, modePerformancePerTestCase: true, percentiles: '0,50,90,100', relativeFailedThresholdNegative: 80.0, relativeFailedThresholdPositive: 20.0, relativeUnstableThresholdNegative: 50.0, relativeUnstableThresholdPositive: 50.0, sourceDataFiles: 'build/test-results/**/*.xml'
                        }
                    } //end dir
                } //end node
            } //end podTemplate
        } //end stage
    } //end if
} // end for

stage('Cleanup') {

    def inputResponse = null
    String mergeMethod=isCI?'squash':'merge'

    waitUntil {
        boolean isDone=false
        try{
            inputResponse=input(id: 'close_pr', message: "Ready to Accept/Merge (using '${mergeMethod}' method), and Close pull-request #${env.CHANGE_ID}?", ok: 'Yes', submitter: 'authenticated', submitterParameter: 'approver')
            echo "inputResponse:${inputResponse}"

            echo "Merging and Closing PR"
            GitHubHelper.mergeAndClosePullRequest(this, mergeMethod)

            echo "Clearing OpenShift resources"
            new OpenShiftHelper().cleanup(this, context)

            //echo "Clearing OpenShift resources"
            //setStageStatus(context, 'Cleanup', 'SUCCESS')
            isDone=true
        }catch (ex){
            echo "${stackTraceAsString(ex)}"
            def inputAction = input(
                message: "This 'Cleanup' stage has failed. See error above.",
                ok: 'Confirm',
                submitter: 'authenticated',
                parameters: [choice(name: 'action', choices: 'Re-run\nIgnore', description: 'What would you like to do?')]
            )
            if ('Ignore'.equalsIgnoreCase(inputAction)){
                isDone=true
            }
        }
        return isDone
    }
}
