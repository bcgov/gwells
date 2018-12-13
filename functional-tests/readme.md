# Description

This is an example of incorporating Geb into a Gradle build. It shows the use of Spock and JUnit 4 tests.

The build is setup to work with a variety of browsers and we aim to add as many as possible.
A JenkinsSlave image has been created that can run Chrome/Firefox Headless tests. This offers a viable option for replacing phantomJs. Please see the [JenkinsSlave Dockerfile][dockerfile] setup.
This repository also holds a Dockerfile for a CentOS based image that will run headless tests as well.

# Usage

The following commands will launch the tests with the individual browser:
```
./gradlew chromeTest
./gradlew chromeHeadlessTest // Will run in OpenShift

./gradlew firefoxTest
./gradlew firefoxHeadlessTest // Will run in OpenShift
```

The following are experimental and may need additional work/configuration to make work:
```
./gradlew edgeTest // Only on Windows
./gradlew ieTest // Only on Windows, read wiki for set up instructions
./gradlew safariTest // Only on MacOS, read wiki for set up instructions
```


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

# Geb - Key Concepts

  Geb Manual: http://www.gebish.org/manual/current
  Geb API Doc: http://www.gebish.org/manual/current/api/

  All of the documentation is useful and will need to be referenced eventually, however, certain key sections are listed below to jump start learning:

  Pages:
    - http://www.gebish.org/manual/current/#pages

    Notable sections:
      http://www.gebish.org/manual/current/#the-page-object-pattern-2
      http://www.gebish.org/manual/current/#template-options
      http://www.gebish.org/manual/current/#at-checker

  Modules:
    - http://www.gebish.org/manual/current/#modules
    Modules aren't ever strictly required, but are useful for modularizing pieces of a page definition that might span multiple pages.  IE: the common page header and footer.

  Navigators:
    - http://www.gebish.org/manual/current/#the-jquery-ish-navigator-api
    - http://www.gebish.org/manual/current/#navigator

    Notable sections:
      http://www.gebish.org/manual/current/#the-code-code-function
      http://www.gebish.org/manual/current/#finding-filtering
      http://www.gebish.org/manual/current/#interact-closures

  Waiting:
    - http://www.gebish.org/manual/current/#implicit-assertions-waiting

    Waitng Config:
    - http://www.gebish.org/manual/current/#waiting-configuration
    - http://www.gebish.org/manual/current/#at-check-waiting

  At Checking:
    - http://www.gebish.org/manual/current/#at-checking

  Debugging:
    - http://www.gebish.org/manual/current/#pausing-and-debugging


# Other Useful Links

Spock: <http://spockframework.org/>

Groovy: <http://groovy-lang.org/>

Selenium: <https://github.com/SeleniumHQ/selenium/wiki>

What is BDD: <https://inviqa.com/blog/bdd-guide>

SourceSets:
* <https://docs.gradle.org/current/userguide/java_plugin.html#sec:working_with_java_source_sets>
* <https://dzone.com/articles/integrating-gatling-into-a-gradle-build-understand>
```
sourceSets {
   test {
       groovy {
           srcDirs = [‘src/groovy’]
       }
       resources {
           srcDirs = [‘src/resources’]
       }
   }
}
```

# Troubleshooting Guide
## Groovy
### Getters and Setters

  > Groovy has built in getter/setter support.  Meaning if a class variable `String dog` exists, then `setDog()` and `getDog()` are automatically present by default.  The unexpected sid effect of this, is that if you create your own `setDog()` method, it will not be called, as groovy has already reserved that method itself.

#### Example

In the below code snippet, calling `setInputField()` from your spec will NOT call the `setInputField()` method in the snippet.  Instead, it will call the auto-magically created `setInputField()` setter created by Groovy by default.

```
class MyPage extends page {
  static content = {
    nameField { $('#inputField') }
  }

  setNameField(String someValue) {
    inputField.value(someValue)
  }
}
```

A simple solution is to ensure the method name is different, and not just the variable name prefixed with `set` or `get`.

```
class MyPage extends page {
  static content = {
    nameField { $('#inputField') }
  }

  setName(String someValue) {
    inputField.value(someValue)
  }
}
```

## Geb

## Spock

## Gradle

# Questions and issues

Please ask questions on our [Slack Channel][slack_channel] and raise issues in [BDDStack issue tracker][issue_tracker].

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
