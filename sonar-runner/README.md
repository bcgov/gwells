This example demonstrates how to analyze a simple Java project with Gradle.

Prerequisites
=============
* [SonarQube](http://www.sonarqube.org/downloads/) 4.5+
* [Gradle](http://www.gradle.org/) 2.1 or higher

Usage
=====
* Analyze the project with SonarQube using Gradle:

        gradle sonarqube [-Dsonar.host.url=... -Dsonar.jdbc.url=... -Dsonar.jdbc.username=... -Dsonar.jdbc.password=...]
        
Local Install
=============
To install SonarQube locally do the following:
* Download the version for your OS from [SonarQube](http://www.sonarqube.org/downloads/)
* Install locally following the directions
* Run server: http://localhost
* Review your build.gradle, you need to add the following property: ```property "sonar.host.url", "http://localhost:9000"```
* run ./gradlew sonarqube from this directory
* Go to web browser and review result

Caveat
======
If you want to run this on windows on your developer stations you need to set the version in build.gradle to:
id "org.sonarqube" version "2.6.1".
Version 1.2 actually causes issues in Windows but not in Linux.       