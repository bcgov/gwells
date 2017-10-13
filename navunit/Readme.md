# Functional Testing Framework - GWELLS Edition

### Introduction
The GWELLS Test framework is based on navUnit, which lets you navigate through your HTML based application by specifying a starting page, the link to click on, and finally assert that the page being navigated to is correct.

This framework has been designed to be extremely basic in design, simple to use and administer, and most of all easy to incorporate within any Web Based Application project.

A more detailed description of navUnit can be found here: https://github.com/bcgov/navUnit
 
GWELLS has adopted this framework in order to enable BDD. 

navUnit is based on:
 
1. Geb Browser Automation Framework (http://www.gebish.org/)

> It brings together the power of WebDriver, the elegance of jQuery content selection, the robustness of Page Object modelling and the expressiveness of the Groovy language.

> Page Object Model is a design pattern to create Object Repository for web UI elements.
  Under this model, for each web page in the application, there should be corresponding page class.
  This Page class will find the WebElements of that web page and also contains Page methods which perform operations on those WebElements.
 
2. Spock Framework
   Behaviour-Driven Development (http://spockframework.org/)

These frameworks allow us to expand the functional (BDD) tests to a large degree and increased sophistication.
The following section contain specific guidance with regards to the GWELLS usage of this toolstack.
----

## Usage

The following commands will launch the tests with the individual browsers:

    ./gradlew chromeTest
    ./gradlew firefoxTest (Make sure you install FireFox version 46 or older, newer version will not work.)
    ./gradlew phantomJsTest
    
NOTE: ***Use phantomjsTest when configuring the OpenShift Pipeline***
----   

## Getting Started



----
# Adding IExplorer testing to framework

The following steps need to be followed:

1. Change code/config to pull down the IE WebDriver 
2. Change IE Settings 
3. Change Registry 

## Change code/config to pull down the IE WebDriver

**Gebconfig.groovy:**
'''
/*
	This is the Geb configuration file.

	See: http://www.gebish.org/manual/current/#configuration
*/
import org.openqa.selenium.Dimension
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.firefox.FirefoxDriver
import org.openqa.selenium.ie.InternetExplorerDriver
import org.openqa.selenium.phantomjs.PhantomJSDriver
import org.openqa.selenium.remote.DesiredCapabilities

waiting {
	timeout = 15
	retryInterval = 1
}

atCheckWaiting = [20, 1]

environments {

	// run via “./gradlew chromeTest”
	// See: http://code.google.com/p/selenium/wiki/ChromeDriver
/*	chrome {
		driver = { new ChromeDriver() }*/
	chrome {
		driver = { def d = new ChromeDriver(new DesiredCapabilities());
			//d.manage().window().size = new Dimension(1920, 1080);
			d.manage().window().maximize();
			return d
	}
}

	// run via “./gradlew firefoxTest”
	// See: http://code.google.com/p/selenium/wiki/FirefoxDriver
	firefox {
		driver = { new FirefoxDriver() }
	}

	ie {
		//driver = { new InternetExplorerDriver() }
/*		driver = { def d = new InternetExplorerDriver(new DesiredCapabilities());
			//d.setCapability(InternetExplorerDriver.INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS,true);
			//d.setCapability(InternetExplorerDriver.IGNORE_ZOOM_SETTING,true);
			d.setCapability(InternetExplorerDriver.NATIVE_EVENTS,true);
			return d*/
			def d = new DesiredCapabilities();
			d.setCapability(InternetExplorerDriver.INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS,true);
			d.setCapability(InternetExplorerDriver.IGNORE_ZOOM_SETTING,true);
			d.setCapability(InternetExplorerDriver.NATIVE_EVENTS,false);
			d.setCapability(InternetExplorerDriver.REQUIRE_WINDOW_FOCUS,true);
		
		driver = { new InternetExplorerDriver(d) }	
	}

    phantomJs {
		driver = { def d = new PhantomJSDriver(new DesiredCapabilities());
			d.manage().window().size = new Dimension(1280, 1024);
    		return d
		}
    }
}

// To run the tests with all browsers just run:
//
// phantomJs --> “./gradlew phantomJsTest”   (headless)
// chrome    --> "./gradlew chromeTest"
baseUrl = "http://localhost:8000"
//baseUrl = "http://gwells-dev.pathfinder.gov.bc.ca"

baseNavigatorWaiting = true

/*println sourceSets.smokeTest.output.classesDir*/
println "BaseURL: ${baseUrl}"
println "--------------------------"
reportsDir = "gebReports"

cacheDriverPerThread = true
quitCachedDriverOnShutdown = true
''' 
----
**osSpecificDownloads.gradle:**
'''
import org.apache.tools.ant.taskdefs.condition.Os
import org.apache.commons.io.FileUtils

buildscript {
	repositories {
		jcenter()
	}
	dependencies {
		classpath "commons-io:commons-io:2.5"
	}
}

task downloadChromeDriver {
	def outputFile = file("$buildDir/webdriver/chromedriver.zip")
	inputs.property("chromeDriverVersion", chromeDriverVersion)
	outputs.file(outputFile)

	doLast {
		def driverOsFilenamePart
		if (Os.isFamily(Os.FAMILY_WINDOWS)) {
			driverOsFilenamePart = "win32"
		} else if (Os.isFamily(Os.FAMILY_MAC)) {
			driverOsFilenamePart = "mac64"
		} else if (Os.isFamily(Os.FAMILY_UNIX)) {
			driverOsFilenamePart = Os.isArch("amd64") ? "linux64" : "linux32"
		}
		FileUtils.copyURLToFile(new URL("http://chromedriver.storage.googleapis.com/${chromeDriverVersion}/chromedriver_${driverOsFilenamePart}.zip"), outputFile)
	}
}

task unzipChromeDriver(type: Copy) {
	def outputDir = file("$buildDir/webdriver/chromedriver")
	dependsOn downloadChromeDriver
	outputs.dir(outputDir)

	from(zipTree(downloadChromeDriver.outputs.files.singleFile))
	into(outputDir)
}

task downloadIeDriver {
	def outputFile = file("$buildDir/webdriver/IEDriverServer_Win32_2.53.0.zip")
	inputs.property("IeDriverVersion", chromeDriverVersion)
	outputs.file(outputFile)

	doLast {
		FileUtils.copyURLToFile(new URL("http://selenium-release.storage.googleapis.com/2.53/IEDriverServer_Win32_2.53.0.zip"), outputFile)
	}
}

task unzipIeDriver(type: Copy) {
	def outputDir = file("$buildDir/webdriver/iedriver")
	dependsOn downloadIeDriver
	outputs.dir(outputDir)

	from(zipTree(downloadIeDriver.outputs.files.singleFile))
	into(outputDir)
}

task downloadPhantomJs {
	def osFilenamePart
	if (Os.isFamily(Os.FAMILY_WINDOWS)) {
		osFilenamePart = "windows.zip"
	} else if (Os.isFamily(Os.FAMILY_MAC)) {
		osFilenamePart = "macosx.zip"
	} else if (Os.isFamily(Os.FAMILY_UNIX)) {
		osFilenamePart = Os.isArch("amd64") ? "linux-x86_64.tar.bz2" : "linux-i686.tar.bz2"
	}

	def filename = "phantomjs-$phantomJsVersion-$osFilenamePart"
	def outputFile = file("$buildDir/webdriver/$filename")
	inputs.property("phantomJsVersion", phantomJsVersion)
	outputs.file(outputFile)

	doLast {
		FileUtils.copyURLToFile(new URL("https://bitbucket.org/ariya/phantomjs/downloads/$filename"), outputFile)
	}
}

task unzipPhantomJs(type: Copy) {
	def outputDir = file("$buildDir/webdriver/phantomjs")
	dependsOn downloadPhantomJs
	outputs.dir(outputDir)

	def archive = downloadPhantomJs.outputs.files.singleFile

	from(Os.isFamily(Os.FAMILY_MAC) || Os.isFamily(Os.FAMILY_WINDOWS) ? zipTree(archive) : tarTree(archive))
	into(outputDir)
	eachFile { FileCopyDetails fcp ->
		fcp.relativePath = new RelativePath(!fcp.directory, *fcp.relativePath.segments[1..-1])
	}
}
'''
----

**build.gradle:**
'''
import org.apache.tools.ant.taskdefs.condition.Os

ext {
    // The drivers we want to use
    drivers = ["firefox","chrome", "phantomJs", "ie"]

    ext {
        groovyVersion = '2.4.12'
        gebVersion = '1.1.1'
        seleniumVersion = '2.53.0'
        chromeDriverVersion = '2.30'
        phantomJsVersion = '2.1.1'
    }
}

apply plugin: "groovy"
apply from: "gradle/idea.gradle"
apply from: "gradle/osSpecificDownloads.gradle"

repositories {
    mavenCentral()
}

dependencies {
    // If using Spock, need to depend on geb-spock
    testCompile "org.gebish:geb-spock:$gebVersion"
    testCompile("org.spockframework:spock-core:1.0-groovy-2.4") {
        exclude group: "org.codehaus.groovy"
    }
    testCompile "org.codehaus.groovy:groovy-all:$groovyVersion"

    // If using JUnit, need to depend on geb-junit (3 or 4)
    testCompile "org.gebish:geb-junit4:$gebVersion"

    testCompile "org.seleniumhq.selenium:selenium-support:$seleniumVersion"

    // Drivers
    testCompile "org.seleniumhq.selenium:selenium-chrome-driver:$seleniumVersion"
    
    testCompile "org.seleniumhq.selenium:selenium-firefox-driver:$seleniumVersion"

    testCompile "org.seleniumhq.selenium:selenium-ie-driver:$seleniumVersion"
    
    // using a custom version of phantomjs driver for now as the original one does not support WebDriver > 2.43.1
    testCompile("com.codeborne:phantomjsdriver:1.3.0") {
        // phantomjs driver pulls in a different selenium version
        transitive = false
    }
/*    testCompile( 'com.athaydes:spock-reports:1.3.2' ) {
        transitive = false // this avoids affecting your version of Groovy/Spock
    }
    // if you don't already have slf4j-api and an implementation of it in the classpath, add this!
    testCompile 'org.slf4j:slf4j-api:1.7.13'
    testCompile 'org.slf4j:slf4j-simple:1.7.13'*/
}

drivers.each { driver ->
    task "${driver}Test"(type: Test) {
        reports {
            html.destination = reporting.file("$name/tests")
            junitXml.destination = file("$buildDir/test-results/$name")
        }

        outputs.upToDateWhen { false }  // Always run tests

        systemProperty "geb.build.reportsDir", reporting.file("$name/geb")
        systemProperty "geb.env", driver

        // If you wanted to set the baseUrl in your build…
        // systemProperty "geb.build.baseUrl", "http://myapp.com"
    }
}

chromeTest {
    dependsOn unzipChromeDriver

    def chromedriverFilename = Os.isFamily(Os.FAMILY_WINDOWS) ? "chromedriver.exe" : "chromedriver"
    systemProperty "webdriver.chrome.driver", new File(unzipChromeDriver.outputs.files.singleFile, chromedriverFilename).absolutePath
}

phantomJsTest {
    dependsOn unzipPhantomJs

    def phantomJsFilename = Os.isFamily(Os.FAMILY_WINDOWS) ? "phantomjs.exe" : "phantomjs"
    systemProperty "phantomjs.binary.path", new File(unzipPhantomJs.outputs.files.singleFile, phantomJsFilename).absolutePath
}

ieTest {
    dependsOn unzipIeDriver

    def iedriverFilename = Os.isFamily(Os.FAMILY_WINDOWS) ? "IEDriverServer.exe" : "IEDriverServer"
    systemProperty "webdriver.ie.driver", new File(unzipIeDriver.outputs.files.singleFile, iedriverFilename).absolutePath
}

test {
    dependsOn drivers.collect { tasks["${it}Test"] }
    enabled = false
}

apply from: "gradle/ci.gradle"

'''
----

### Change IE Settings

The IEDriverServer exectuable must be downloaded and placed in your PATH.  


On IE 7 or higher on Windows Vista or Windows 7, you must set the Protected Mode settings for each zone to be the same value. The value can be on or off, as long as it is the same for every zone. To set the Protected Mode settings, choose "Internet Options..." from the Tools menu, and click on the Security tab. For each zone, there will be a check box at the bottom of the tab labeled "Enable Protected Mode".  


Additionally, "Enhanced Protected Mode" must be disabled for IE 10 and higher. This option is found in the Advanced tab of the Internet Options dialog.


The browser zoom level must be set to 100% so that the native mouse events can be set to the correct coordinates.

It is also suggested to add your web site under to test to trusted domains \(only for https\) local website runs do not need that.

## Change Registry

For IE 11 only, you will need to set a registry entry on the target computer so that the driver can maintain a connection to the instance of Internet Explorer it creates. 

For 32-bit Windows installations, the key you must examine in the registry editor is **HKEY\_LOCAL\_MACHINE\\SOFTWARE\\Microsoft\\Internet Explorer\\Main\\FeatureControl\\FEATURE\_BFCACHE**. 

For 64-bit Windows installations, the key is **HKEY\_LOCAL\_MACHINE\\SOFTWARE\\Wow6432Node\\Microsoft\\Internet Explorer\\Main\\FeatureControl\\FEATURE\_BFCACHE**. 

Please note that the FEATURE\_BFCACHE subkey may or may not be present, and should be created if it is not present. Important: Inside this key, **create a DWORD value named iexplore.exe with the value of 0.**

## Used Links:

https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver

https://github.com/SeleniumHQ/selenium/wiki/DesiredCapabilities

https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/6511

https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/5116

https://seleniumhq.github.io/selenium/docs/api/java/org/openqa/selenium/ie/InternetExplorerDriver.html

## Issues

+ Slow\! 
+ You might want to try to work with IE Explore 32-bits. 
+ It works with 64 bit browser but apparently with the 32 bit browser everything is better 
+ When you start the test, it could take up to several minutes until the actual test starts. Patience\! 
+ There are many suggestion with regards to the desired webdriver capabilities settings, I have tried many, but the current set seems to be working to a degree. I do suggest not to change the method for setting these as other methods gave me interest, unwanted, results like the browser instantiating 10s of times. 
