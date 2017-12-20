node('maven') {
    stage('Build') {
        echo "Building..."
        openshiftBuild bldCfg: 'gwells', showBuildLogs: 'true'
        openshiftTag destStream: 'gwells', verbose: 'true', destTag: '$BUILD_ID', srcStream: 'gwells', srcTag: 'latest'
    }
	
}


stage('Deploy on Test') {
    input "Deploy to Test?"
    node('maven') {
        openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'test', srcStream: 'gwells', srcTag: '$BUILD_ID'
    }
}

node('bddstack') {
	
	stage('FT on Test (TBD)') {
		//the checkout is mandatory, otherwise functional test would fail
//        echo "checking out source"
//        echo "Build: ${BUILD_ID}"
//        checkout scm
//        dir('functional-tests') {
//			try {
//                sh './gradlew --debug --stacktrace chromeHeadlessTest'
//			} finally { 
//				archiveArtifacts allowEmptyArchive: true, artifacts: 'build/reports/**/*'
//                archiveArtifacts allowEmptyArchive: true, artifacts: 'build/test-results/**/*'
//                junit 'build/test-results/**/*.xml'
//			}
//        }
	  sh 'sleep 5s'
    }

}

stage('Deploy on Prod') {
    input "Deploy to Prod?"
    node('maven') {
        openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'prod', srcStream: 'gwells', srcTag: '$BUILD_ID'
	sh 'sleep 3m'
    }
}

node('bddstack') {
    stage('ST on Prod (TBD)') {
        sh 'sleep 5s'
    }
}
