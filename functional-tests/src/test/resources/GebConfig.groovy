/*
	This is the Geb configuration file.

	See: http://www.gebish.org/manual/current/#configuration
*/


import org.openqa.selenium.Dimension
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.firefox.FirefoxDriver
import org.openqa.selenium.phantomjs.PhantomJSDriver
import org.openqa.selenium.remote.DesiredCapabilities

waiting {
	timeout = 30
	retryInterval = 0.25
}

atCheckWaiting = [30, 025]

environments {

	// run via “./gradlew chromeTest”
	// See: http://code.google.com/p/selenium/wiki/ChromeDriver
	chrome {
		driver = { new ChromeDriver() }
	}

	// run via “./gradlew firefoxTest”
	// See: http://code.google.com/p/selenium/wiki/FirefoxDriver
	firefox {
		driver = { new FirefoxDriver() }
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
baseUrl = "http://tfrs-mem-tfrs-dev.pathfinder.gov.bc.ca/"


println """
            .  .       .
            |  |     o |
;-. ,-: . , |  | ;-. . |-
| | | | |/  |  | | | | |
' ' `-` '   `--` ' ' ' `-'
--------------------------
"""
println "BaseURL: ${baseUrl}"
println "--------------------------"
reportsDir = "gebReports"
quitCachedDriverOnShutdown = true
