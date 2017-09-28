/*
	This is the Geb configuration file.

	See: http://www.gebish.org/manual/current/#configuration
*/
import org.openqa.selenium.Dimension
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.ie.InternetExplorerDriver
import org.openqa.selenium.firefox.FirefoxDriver
import org.openqa.selenium.phantomjs.PhantomJSDriver
import org.openqa.selenium.remote.DesiredCapabilities

waiting {
	timeout = 15
	retryInterval = 1
}

atCheckWaiting = [15, 1]

environments {

	// run via “./gradlew chromeTest”
	// See: http://code.google.com/p/selenium/wiki/ChromeDriver
	chrome {
		driver = { new ChromeDriver() }
/*	chrome {
		driver = { def d = new ChromeDriver(new DesiredCapabilities());
			//d.manage().window().size = new Dimension(1920, 1080);
			d.manage().window().maximize();
			return d
		}*/
	}
	// run via “./gradlew ieTest”
	ie {
		
		def d = new DesiredCapabilities();
		//d.internetExplorer().setCapability(InternetExplorerDriver.BROWSER_ATTACH_TIMEOUT,1500);
		d.internetExplorer().setCapability(InternetExplorerDriver.FORCE_CREATE_PROCESS,true);
		d.internetExplorer().setCapability(InternetExplorerDriver.INITIAL_BROWSER_URL,"https://gwells-dev.pathfinder.gov.bc.ca/");
		d.internetExplorer().setCapability(InternetExplorerDriver.INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS,true);
		d.internetExplorer().setCapability(InternetExplorerDriver.NATIVE_EVENTS,false);
		//d.internetExplorer().setCapability(InternetExplorerDriver.REQUIRE_WINDOW_FOCUS,true);
		driver = ie
		driver = { new InternetExplorerDriver(d) }

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
//baseUrl = "http://localhost:8000"
baseUrl = "http://gwells-dev.pathfinder.gov.bc.ca"

baseNavigatorWaiting = true

/*println sourceSets.smokeTest.output.classesDir*/
println "BaseURL: ${baseUrl}"
println "--------------------------"
reportsDir = "gebReports"
quitCachedDriverOnShutdown = true
