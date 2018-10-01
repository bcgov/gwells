This example demonstrates how to analyze a simple Java project with Gradle.

Prerequisites
=============
* [SonarQube](http://www.sonarqube.org/downloads/) 6.7+
* [Gradle](http://www.gradle.org/) 2.1 or higher

Usage
=====
* Analyze the project with SonarQube using Gradle:

        ./gradlew sonarqube [-Dsonar.host.url=... -Dsonar.jdbc.url=... -Dsonar.jdbc.username=... -Dsonar.jdbc.password=...]
        
Local Install
=============
To install SonarQube locally do the following:
* Download the version for your OS from [SonarQube](http://www.sonarqube.org/downloads/)
* Install locally following the directions
* Run server: http://localhost:9000
* Review your build.gradle, you need to add the following property: ```property "sonar.host.url", "http://localhost:9000"```
* run ./gradlew sonarqube from this directory
* Go to web browser and review result

[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/gate?key=org.sonarqube:bcgov-gwells&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)

[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=lines&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)

[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=ncloc&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)

[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=comment_lines_density&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=public_documented_api_density&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=function_complexity&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=test_errors&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=test_failures&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=skipped_tests&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=test_success_density&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=coverage&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_coverage&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=it_coverage&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_it_coverage&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=overall_coverage&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_overall_coverage&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=duplicated_lines_density&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_duplicated_lines_density&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=blocker_violations&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=critical_violations&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_blocker_violations&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_critical_violations&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=code_smells&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_code_smells&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=bugs&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_bugs&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=vulnerabilities&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_vulnerabilities&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=sqale_debt_ratio&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_sqale_debt_ratio&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_maintainability_rating&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_reliability_rating&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
[![Quality Gate](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/api/badges/measure?key=org.sonarqube:bcgov-gwells&metric=new_security_rating&template=FLAT)](https://sonarqube-moe-gwells-tools.pathfinder.gov.bc.ca/dashboard/index/org.sonarqube:bcgov-gwells)
