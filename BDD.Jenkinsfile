environment {
        JAVA_HOME = '/usr'
    }

node('master') {
    
    stage('checkout for static code analysis') {
        echo "checking out source"
        echo "Build: ${BUILD_ID}"
        checkout scm
    }
	
	stage('validation') {
        dir('navunit') {
            sh './gradlew --debug --stacktrace phantomJsTest'
        }
    }
}
