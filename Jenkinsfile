node('maven') {
    stage('Build') {
        echo "Building..."
        openshiftBuild bldCfg: 'gwells', showBuildLogs: 'true'
        openshiftTag destStream: 'gwells', verbose: 'true', destTag: '$BUILD_ID', srcStream: 'gwells', srcTag: 'latest'
    }

    stage('Deploy on Dev') {
        echo "Deploying to dev..."
        openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'dev', srcStream: 'gwells', srcTag: '$BUILD_ID'
		//Sleeping for a while to wait deployment completes
		sh 'sleep 3m'
	}
    
    stage('Code Quality Check') {
		//the checkout is mandatory, otherwise code quality check would fail
        echo "checking out source"
        echo "Build: ${BUILD_ID}"
        checkout scm
        SONARQUBE_PWD = sh (
            script: 'oc env dc/sonarqube --list | awk  -F  "=" \'/SONARQUBE_ADMINPW/{print $2}\'',
            returnStdout: true
        ).trim()
        echo "SONARQUBE_PWD: ${SONARQUBE_PWD}"

        SONARQUBE_URL = sh (
            script: 'oc get routes -o wide --no-headers | awk \'/sonarqube/{ print match($0,/edge/) ?  "https://"$2 : "http://"$2 }\'',
            returnStdout: true
        ).trim()
        echo "SONARQUBE_URL: ${SONARQUBE_URL}"

        dir('sonar-runner') {
            sh returnStdout: true, script: "./gradlew sonarqube -Dsonar.host.url=${SONARQUBE_URL} -Dsonar.verbose=true --stacktrace --info  -Dsonar.sources=.."
        }
    }

	
}

node('master') {
	
	stage('Functional Test') {
		//the checkout is mandatory, otherwise functional test would fail
        echo "checking out source"
        echo "Build: ${BUILD_ID}"
        checkout scm
        dir('navunit') {
			try {
				sh './gradlew --debug --stacktrace phantomjsTest'
			} finally { 
				archiveArtifacts allowEmptyArchive: true, artifacts: 'build/reports/**/*'
			}
        }
    }

}


stage('deploy-test') {
    input "Deploy to test?"
  
    node('maven') {
        openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'test', srcStream: 'gwells', srcTag: '$BUILD_ID'
    }
}

stage('deploy-prod') {
    input "Deploy to prod?"
    
    node('maven') {
        openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'prod', srcStream: 'gwells', srcTag: '$BUILD_ID'
    }
}
