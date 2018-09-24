/*
  This is the Geb configuration file.

  See: http://www.gebish.org/manual/current/#configuration
*/

import org.openqa.selenium.Dimension
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions
import org.openqa.selenium.firefox.FirefoxDriver
import org.openqa.selenium.firefox.FirefoxOptions
import org.openqa.selenium.ie.InternetExplorerDriver
import org.openqa.selenium.edge.EdgeDriver
import org.openqa.selenium.safari.SafariDriver
import org.openqa.selenium.remote.DesiredCapabilities

waiting {
  timeout = 20
  retryInterval = 1
}

//Using default waiting configuration
atCheckWaiting = true

environments {

  // run via “./gradlew chromeTest”
  // See: https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver
  chrome {
    driver = {
      ChromeOptions o = new ChromeOptions()
      o.addArguments("window-size=1600,900")
      new ChromeDriver(o)
      }
  }

  // run via “./gradlew chromeHeadlessTest”
  // See: https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver
  chromeHeadless {
    driver = {
      ChromeOptions o = new ChromeOptions()
      o.addArguments('headless')
      o.addArguments('disable-gpu')
      o.addArguments('no-sandbox')
      o.addArguments("window-size=1600,900")
      new ChromeDriver(o)
    }
  }

  // run via “./gradlew firefoxTest”
  // See: https://github.com/SeleniumHQ/selenium/wiki/FirefoxDriver
  firefox {
    driver = {
      FirefoxOptions o = new FirefoxOptions()
      o.addArguments("-window-size=1600,900")
      new FirefoxDriver(o)
    }
  }

  firefoxHeadless {
    driver = {
      FirefoxOptions o = new FirefoxOptions()
      o.addArguments("-headless")
      o.addArguments("-window-size=1600,900")
      new FirefoxDriver(o)
    }
  }

  // run via “./gradlew ieTest”
  // See: https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver
  ie {
    def d = new DesiredCapabilities();
    d.setCapability(InternetExplorerDriver.INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS,true);
    d.setCapability(InternetExplorerDriver.IGNORE_ZOOM_SETTING,true);
    d.setCapability(InternetExplorerDriver.NATIVE_EVENTS,false);
    d.setCapability(InternetExplorerDriver.REQUIRE_WINDOW_FOCUS,true);

    driver = { new InternetExplorerDriver(d) }
  }

  // run via “./gradlew edgeTest”
  // See: https://github.com/SeleniumHQ/selenium/wiki
  edge {
    driver = { new EdgeDriver() }
  }

  // run via “./gradlew safariTest”
  // See: https://github.com/SeleniumHQ/selenium/wiki
  safari {
    driver = { new SafariDriver() }
  }
}

// To run the tests with all browsers just run “./gradlew test”

baseNavigatorWaiting = true

// Allows for setting you baseurl in an environment variable.
// This is particularly handy for development and the pipeline
Map env = System.getenv()
baseUrl = env['BASE_URL']
if (!baseUrl) {
  baseUrl = "http://127.0.0.1:8000/gwells/"
}

println "--------------------------------------"
println "BaseURL: ${baseUrl}"
println "--------------------------------------"

autoClearCookies = true
autoClearWebStorage = true
cacheDriverPerThread = true
quitCachedDriverOnShutdown = true
