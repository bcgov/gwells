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
//baseUrl = "http://localhost:8000"
baseUrl = "http://gwells-dev.pathfinder.gov.bc.ca/"
//baseUrl = "https://dlvrapps.nrs.gov.bc.ca/" //Dev
//baseUrl = "https://testapps.nrs.gov.bc.ca/" //Test
//baseUrl = "https://apps.nrs.gov.bc.ca/" //Prod

baseNavigatorWaiting = true

/*println sourceSets.smokeTest.output.classesDir*/
println "BaseURL: ${baseUrl}"
println "--------------------------"
reportsDir = "gebReports"

cacheDriverPerThread = true
quitCachedDriverOnShutdown = true
