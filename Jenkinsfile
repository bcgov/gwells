node('maven') {
    stage('Build') {
        echo "Building..."
        openshiftBuild bldCfg: 'gwells', showBuildLogs: 'true', waitTime: 1800000
        openshiftTag destStream: 'gwells', verbose: 'true', destTag: '$BUILD_ID', srcStream: 'gwells', srcTag: 'latest'
    }

    podTemplate(label: 'pythonnodejs', name: 'pythonnodejs', serviceAccount: 'jenkins', cloud: 'openshift', containers: [
    containerTemplate(
        name: 'jnlp',
        image: '172.50.0.2:5000/openshift/jenkins-slave-python3nodejs',
        resourceRequestCpu: '500m',
        resourceLimitCpu: '1000m',
        resourceRequestMemory: '1Gi',
        resourceLimitMemory: '4Gi',
        workingDir: '/tmp',
        command: '',
        args: '${computer.jnlpmac} ${computer.name}'
    )
    ])       
    {
        stage('Unit Test') {
            node('pythonnodejs') {
                checkout scm
                try {
                    sh 'pip install --upgrade pip && pip install -r requirements.txt'
                    sh 'cd frontend && npm install && npm run build && cd ..'
                    sh 'python manage.py collectstatic && python manage.py migrate'
                    sh 'export ENABLE_DATA_ENTRY="True" && python manage.py test -c nose.cfg'
                    sh 'cd frontend && npm test && cd ..'
                } 
                finally {
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
    }  

    stage('Deploy on Test') {
        echo "Deploying to Test..."
        openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'test', srcStream: 'gwells', srcTag: '$BUILD_ID'
        sleep 5
        openshiftVerifyDeployment depCfg: 'gwells', namespace: 'moe-gwells-test', replicaCount: 1, verbose: 'false', verifyReplicaCount: 'false', waitTime: 600000
	    echo ">>>> Test Deployment Complete"
    }
}

podTemplate(label: 'nodejs', name: 'nodejs', serviceAccount: 'jenkins', cloud: 'openshift', containers: [
  containerTemplate(
    name: 'jnlp',
    image: 'registry.access.redhat.com/openshift3/jenkins-slave-nodejs-rhel7',
    resourceRequestCpu: '500m',
    resourceLimitCpu: '1000m',
    resourceRequestMemory: '1Gi',
    resourceLimitMemory: '4Gi',
    workingDir: '/tmp',
    command: '',
    args: '${computer.jnlpmac} ${computer.name}',
    envVars: [
        secretEnvVar(key: 'GWELLS_API_TEST_USER', secretName: 'apitest-secrets', secretKey: 'username'),
        secretEnvVar(key: 'GWELLS_API_TEST_PASSWORD', secretName: 'apitest-secrets', secretKey: 'password'),
        envVar(key:'BASEURL', value: 'https://testapps.nrs.gov.bc.ca/gwells/registries')
       ]
  )
])       
{
    stage('API Test') {
        input "Ready to start Tests?"
        node('nodejs') {
        //the checkout is mandatory, otherwise functional test would fail
            echo "checking out source"
            echo "Build: ${BUILD_ID}"
            checkout scm
            dir('api-tests') {
            sh 'npm install -g newman'
            try {
                sh 'newman run registries_api_tests.json --global-var base_url=$BASEURL --global-var test_user=$GWELLS_API_TEST_USER --global-var test_password=$GWELLS_API_TEST_PASSWORD -r cli,junit,html;'
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
            }
        }
    }
}

podTemplate(label: 'bddstack', name: 'bddstack', serviceAccount: 'jenkins', cloud: 'openshift', containers: [
  containerTemplate(
    name: 'jnlp',
    image: '172.50.0.2:5000/openshift/jenkins-slave-bddstack',
    resourceRequestCpu: '500m',
    resourceLimitCpu: '1000m',
    resourceRequestMemory: '1Gi',
    resourceLimitMemory: '4Gi',
    workingDir: '/home/jenkins',
    command: '',
    args: '${computer.jnlpmac} ${computer.name}',
    envVars: [
        envVar(key:'BASEURL', value: 'https://testapps.nrs.gov.bc.ca/')
       ]
  )
])       
{
    stage('Smoke Test on Test') {
        node('bddstack') {
            //the checkout is mandatory, otherwise functional test would fail
            echo "checking out source"
            echo "Build: ${BUILD_ID}"
            checkout scm
            dir('functional-tests/build/test-results') {
                unstash 'coverage'
                sh 'rm coverage.xml'
                unstash 'api-tests'
                unstash 'nodejunit'
                }
            dir('functional-tests') {
                try {
                        sh './gradlew -DchromeHeadlessTest.single=WellDetails chromeHeadlessTest'
                } finally {
                        archiveArtifacts allowEmptyArchive: true, artifacts: 'build/reports/geb/**/*'
                        junit 'build/test-results/**/*.xml'
                        publishHTML (target: [
                                    allowMissing: false,
                                    alwaysLinkToLastBuild: false,
                                    keepAll: true,
                                    reportDir: 'build/reports/spock',
                                    reportFiles: 'index.html',
                                    reportName: "BDD Spock Report"
                                ])
                        publishHTML (target: [
                                    allowMissing: false,
                                    alwaysLinkToLastBuild: false,
                                    keepAll: true,
                                    reportDir: 'build/reports/tests/chromeHeadlessTest',
                                    reportFiles: 'index.html',
                                    reportName: "Full Test Report"
                                ])
                    perfReport compareBuildPrevious: true, excludeResponseTime: true, ignoreFailedBuilds: true, ignoreUnstableBuilds: true, modeEvaluation: true, modePerformancePerTestCase: true, percentiles: '0,50,90,100', relativeFailedThresholdNegative: 80.0, relativeFailedThresholdPositive: 20.0, relativeUnstableThresholdNegative: 50.0, relativeUnstableThresholdPositive: 50.0, sourceDataFiles: 'build/test-results/**/*.xml'
                }
            }
        }
    }
}    

stage('Deploy on Prod') {
    input "Deploy to Prod?"
    node('maven') {
        openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'prod', srcStream: 'gwells', srcTag: '$BUILD_ID'
	sh 'sleep 3m'
    }
}

podTemplate(label: 'bddstack', name: 'bddstack', serviceAccount: 'jenkins', cloud: 'openshift', containers: [
  containerTemplate(
    name: 'jnlp',
    image: '172.50.0.2:5000/openshift/jenkins-slave-bddstack',
    resourceRequestCpu: '500m',
    resourceLimitCpu: '1000m',
    resourceRequestMemory: '1Gi',
    resourceLimitMemory: '4Gi',
    workingDir: '/home/jenkins',
    command: '',
    args: '${computer.jnlpmac} ${computer.name}',
    envVars: [
        envVar(key:'BASEURL', value: 'https://apps.nrs.gov.bc.ca/')
       ]
  )
])       
{
    stage('Smoke Test on Prod') {
        input "Ready to smoke test Prod?"
        node('bddstack') {
            //the checkout is mandatory, otherwise functional test would fail
            echo "checking out source"
            echo "Build: ${BUILD_ID}"
            checkout scm
            dir('functional-tests/build/test-results') {
                unstash 'coverage'
                sh 'rm coverage.xml'
                unstash 'api-tests'
                unstash 'nodejunit'
                }
            dir('functional-tests') {
                try {
                        sh './gradlew -DchromeHeadlessTest.single=WellDetails chromeHeadlessTest'
                } finally {
                        archiveArtifacts allowEmptyArchive: true, artifacts: 'build/reports/geb/**/*'
                        junit 'build/test-results/**/*.xml'
                        publishHTML (target: [
                                    allowMissing: false,
                                    alwaysLinkToLastBuild: false,
                                    keepAll: true,
                                    reportDir: 'build/reports/spock',
                                    reportFiles: 'index.html',
                                    reportName: "BDD Spock Report"
                                ])
                        publishHTML (target: [
                                    allowMissing: false,
                                    alwaysLinkToLastBuild: false,
                                    keepAll: true,
                                    reportDir: 'build/reports/tests/chromeHeadlessTest',
                                    reportFiles: 'index.html',
                                    reportName: "Full Test Report"
                                ])
                    perfReport compareBuildPrevious: true, excludeResponseTime: true, ignoreFailedBuilds: true, ignoreUnstableBuilds: true, modeEvaluation: true, modePerformancePerTestCase: true, percentiles: '0,50,90,100', relativeFailedThresholdNegative: 80.0, relativeFailedThresholdPositive: 20.0, relativeUnstableThresholdNegative: 50.0, relativeUnstableThresholdPositive: 50.0, sourceDataFiles: 'build/test-results/**/*.xml'
                }
            }
        }
    }
} 