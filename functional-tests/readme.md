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


To run a single class of tests, you can run:

    ./gradlew chromeTest --tests <ClassName>

NOTE: To find the class name, navigate to the &ast;.groovy files under [./src/test/groovy](./src/test/groovy).  or example, the `Registry/SearchRegistrySpecs.groovy` file has:
```
class SearchRegistrySpecs extends GebReportingSpec {
```

To run just this sets of Functional tests:
```
        ./gradlew chromeTest -tests SearchRegistrySpecs
```



## Questions and issues

Please ask questions on our [Slack Channel][slack_channel] and raise issues in [BDDStack issue tracker][issue_tracker].

[dockerfile]: https://github.com/agehlers/openshift-tools/blob/master/provisioning/jenkins-slaves/chrome/Dockerfile
[issue_tracker]: https://github.com/rstens/BDDStack/issues
[slack_channel]: https://devopspathfinder.slack.com/messages/C7J72K1MG

## Performance Testing with BDDStack and JMeter

include the following in your build.gradle (Optional - if this section is not declared, default configuration is used):

	jmeter {
	  jmTestFiles = [file("src/test/jmeter/test2.jmx")] //if jmx file is not in the default location
	  jmSystemPropertiesFiles= [file("src/test/jmeter/jmeter.properties")] //to add additional system properties
	  enableExtendedReports = true //produce Graphical and CSV reports
	}

**Changing default path**

In order to use a custom directory for jmx files (default is `src/test/jmeter`) you can set the property *testFileDir*.
* E.g. testFileDir = file("src/main/resources/jmeter")

**Include and exclude files**

When working with the default or custom path to scan for jmx files, you can include or exclude specific files with the *ïncludes* and *excludes* properties.
* E.g. excludes = ["excludeThisTest.jmx"]

(Note that you should provide a list of patterns, not just a String)

### Edit JMeter files

By default the plugin will search for *.jmx files in `src/test/jmeter`. You can launch the UI end edit your files by running:

`gradle jmGui`

### Run the tests

You can run the tests by executing

`gradle jmRun`

### Create Reports

You can run the tests by executing

`gradle jmReport`

By default, extended reports are turned on and HTML reports are turned off

The results of the tests will can be found in(default location, can be overridden) `build/jmeter-report`

## License

Code released under the [Apache License, Version 2.0](https://github.com/bcgov/gwells/blob/master/LICENSE).
