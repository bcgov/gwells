# BDDStack setup and sample tests

## Description

This is an example of incorporating Geb into a Gradle build. It shows the use of Spock and JUnit 4 tests.

The build is setup to work with a variety of browsers and we aim to add as many as possible.
A JenkinsSlave image has been created that can run Chrome/Firefox Headless tests. This offers a viable option for replacing phantomJs. Please see the [JenkinsSlave Dockerfile][dockerfile] setup.
This repository also holds a Dockerfile for a CentOS based image that will run headless tests as well.

## Usage

The following commands will launch the tests with the individual browsers:

    ./gradlew chromeTest
    ./gradlew chromeHeadlessTest //Will run in pipeline as well
    ./gradlew firefoxTest
    ./gradlew firefoxHeadlessTest //Will run in pipeline as well
    ./gradlew edgeTest
    ./gradlew ieTest
    
To run with all, you can run:

    ./gradlew test

Replace `./gradlew` with `gradlew.bat` in the above examples if you're on Windows.

## Questions and issues

Please ask questions on our [Slack Channel][slack_channel] and raise issues in [BDDStack issue tracker][issue_tracker].

[dockerfile]: https://github.com/agehlers/openshift-tools/blob/master/provisioning/jenkins-slaves/chrome/Dockerfile
[issue_tracker]: https://github.com/rstens/BDDStack/issues
[slack_channel]: https://devopspathfinder.slack.com/messages/C7J72K1MG
