node('maven') {
    stage('Build') {
        echo "Building..."
        openshiftBuild bldCfg: 'gwells', showBuildLogs: 'true'

        // Temporarily removed this next line as it's to be done in the Deployments...
        // openshiftTag destStream: 'gwells', verbose: 'true', destTag: '$BUILD_ID', srcStream: 'gwells', srcTag: 'latest'

        echo ">>> Get Image Hash"
        IMAGE_HASH = sh (
          script: 'oc get istag gwells:latest -o template --template="{{.image.dockerImageReference}}"|awk -F ":" \'{print $3}\'',
 	           returnStdout: true).trim()
        echo ">> IMAGE_HASH: $IMAGE_HASH"
    }
}


stage('Deploy on Test') {
    input "Deploy to Test?"
    node('maven') {
		// GW - following is to prepare for move to IMAGE_HASH 
		echo "Deploy on Test >> IMAGE_HASH: $IMAGE_HASH"
		openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'master-testblue', srcStream: 'gwells', srcTag: 'test'
		openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'master-test', srcStream: 'gwells', srcTag: "${IMAGE_HASH}"

		// GW Will remove this next line once prior 3 lines have been tested
        // openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'test', srcStream: 'gwells', srcTag: '$BUILD_ID'

		openshiftVerifyDeployment depCfg: 'gwells', namespace: 'moe-gwells-test', replicaCount: 1, verbose: 'false', verifyReplicaCount: 'false'			
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
		// GW - following is to prepare for move to IMAGE_HASH 
		echo "Deploy on Prod >> IMAGE_HASH: $IMAGE_HASH"
		openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'master-prodblue', srcStream: 'gwells', srcTag: 'prod'
		openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'master-prod', srcStream: 'gwells', srcTag: "${IMAGE_HASH}"

	    // GW Will remove this next line once prior 3 lines have been tested
        // openshiftTag destStream: 'gwells', verbose: 'true', destTag: 'prod', srcStream: 'gwells', srcTag: '$BUILD_ID'

		openshiftVerifyDeployment depCfg: 'gwells', namespace: 'moe-gwells-prod', replicaCount: 1, verbose: 'false', verifyReplicaCount: 'false'			

	// GW no longer needed as we have openshiftVerifyDeployment
	// sh 'sleep 3m'
    }
}

node('bddstack') {
    stage('ST on Prod (TBD)') {
        sh 'sleep 5s'
    }
}
