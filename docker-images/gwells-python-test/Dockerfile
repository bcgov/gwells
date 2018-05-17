FROM openshift/python:3.5
USER 0

RUN yum -y --setopt=tsflags=nodocs install wget nano Xvfb  xorg-x11-xauth java-1.8.0-openjdk-devel git firefox unzip lsof rsync tar which zip bzip2 && \
wget -q -O /tmp/google-chrome.rpm https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
yum -y localinstall /tmp/google-chrome.rpm && rm -f /tmp/google-chrome.rpm &&  yum clean all -y && rm -rf /var/cache/yum && \
java -version && git version && google-chrome --product-version

RUN wget -q -O /tmp/gradle.zip https://services.gradle.org/distributions/gradle-4.2-bin.zip && \
mkdir /opt/gradle && \
unzip -q -d /opt/gradle /tmp/gradle.zip && rm -f /tmp/gradle.zip && \
/opt/gradle/gradle-4.2/bin/gradle -v


RUN curl -sL "https://gist.githubusercontent.com/cvarjao/45d7ef35515353acb54563a1be1ddf6d/raw/60d010ee3c6d8606dfa70d80e50a4ee0324ea148/jenkins-slave-base.rhel7.sh" |  bash -s

USER 1001

RUN mkdir -p /tmp/sonar-runner/src/main/java && \
echo '' > /tmp/sonar-runner/src/main/java/HelloWorld.java && \
echo 'public class HelloWorld {' >> /tmp/sonar-runner/src/main/java/HelloWorld.java && \
echo '  public static void main(String[] args) {' >> /tmp/sonar-runner/src/main/java/HelloWorld.java && \
echo '      System.out.println("Hello, World");' >> /tmp/sonar-runner/src/main/java/HelloWorld.java && \
echo '  }' >> /tmp/sonar-runner/src/main/java/HelloWorld.java && \
echo '}' >> /tmp/sonar-runner/src/main/java/HelloWorld.java && \
echo '' > /tmp/sonar-runner/build.gradle && \
echo 'plugins { ' >> /tmp/sonar-runner/build.gradle && \
echo '  id "java" ' >> /tmp/sonar-runner/build.gradle && \
echo '  id "jacoco" ' >> /tmp/sonar-runner/build.gradle && \
echo '  id "org.sonarqube" version "2.6.1" ' >> /tmp/sonar-runner/build.gradle && \
echo '  id "groovy"' >> /tmp/sonar-runner/build.gradle && \
echo '  id "com.energizedwork.webdriver-binaries" version "1.0"' >> /tmp/sonar-runner/build.gradle && \
echo '  id "net.foragerr.jmeter" version "1.0.10-3.3"' >> /tmp/sonar-runner/build.gradle && \
echo '} ' >> /tmp/sonar-runner/build.gradle && \
echo '' >> /tmp/sonar-runner/build.gradle && \
echo 'ext {' >> /tmp/sonar-runner/build.gradle && \
echo '    // The drivers we want to use' >> /tmp/sonar-runner/build.gradle && \
echo '    drivers = ["firefox", "firefoxHeadless", "chrome", "chromeHeadless","ie","edge","safari"]' >> /tmp/sonar-runner/build.gradle && \
echo '' >> /tmp/sonar-runner/build.gradle && \
echo '    ext {' >> /tmp/sonar-runner/build.gradle && \
echo '        groovyVersion = "2.4.12"' >> /tmp/sonar-runner/build.gradle && \
echo '        gebVersion = "2.1"' >> /tmp/sonar-runner/build.gradle && \
echo '        seleniumVersion = "3.6.0"' >> /tmp/sonar-runner/build.gradle && \
echo '        chromeDriverVersion = "2.36"' >> /tmp/sonar-runner/build.gradle && \
echo '        geckoDriverVersion = "0.18.0"' >> /tmp/sonar-runner/build.gradle && \
echo '        ieDriverVersion = "3.6"' >> /tmp/sonar-runner/build.gradle && \
echo '        edgeDriverVersion = seleniumVersion' >> /tmp/sonar-runner/build.gradle && \
echo '        safariDriverVersion = seleniumVersion' >> /tmp/sonar-runner/build.gradle && \
echo '    }' >> /tmp/sonar-runner/build.gradle && \
echo '}' >> /tmp/sonar-runner/build.gradle && \
echo '' >> /tmp/sonar-runner/build.gradle && \
echo 'dependencies { ' >> /tmp/sonar-runner/build.gradle && \
echo '    compile "junit:junit:4.12" ' >> /tmp/sonar-runner/build.gradle && \
echo '    // If using Spock, need to depend on geb-spock' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.gebish:geb-spock:$gebVersion"' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile("org.spockframework:spock-core:1.1-groovy-2.4") {' >> /tmp/sonar-runner/build.gradle && \
echo '        exclude group: "org.codehaus.groovy"' >> /tmp/sonar-runner/build.gradle && \
echo '    }' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.codehaus.groovy:groovy-all:$groovyVersion"' >> /tmp/sonar-runner/build.gradle && \
echo '' >> /tmp/sonar-runner/build.gradle && \
echo '    // If using JUnit, need to depend on geb-junit (3 or 4)' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.gebish:geb-junit4:$gebVersion"' >> /tmp/sonar-runner/build.gradle && \
echo '' >> /tmp/sonar-runner/build.gradle && \
echo '    //Support' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.seleniumhq.selenium:selenium-support:$seleniumVersion"' >> /tmp/sonar-runner/build.gradle && \
echo '' >> /tmp/sonar-runner/build.gradle && \
echo '    // Drivers' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.seleniumhq.selenium:selenium-safari-driver:$seleniumVersion"' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.seleniumhq.selenium:selenium-chrome-driver:$seleniumVersion"' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.seleniumhq.selenium:selenium-firefox-driver:$seleniumVersion"' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.seleniumhq.selenium:selenium-ie-driver:$seleniumVersion"' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.seleniumhq.selenium:selenium-edge-driver:$seleniumVersion"' >> /tmp/sonar-runner/build.gradle && \
echo '' >> /tmp/sonar-runner/build.gradle && \
echo '    // Spock reports' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile( "com.athaydes:spock-reports:1.4.0" ) {' >> /tmp/sonar-runner/build.gradle && \
echo '        transitive = false // this avoids affecting your version of Groovy/Spock' >> /tmp/sonar-runner/build.gradle && \
echo '    }' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.slf4j:slf4j-api:1.7.13"' >> /tmp/sonar-runner/build.gradle && \
echo '    testCompile "org.slf4j:slf4j-simple:1.7.13"' >> /tmp/sonar-runner/build.gradle && \
echo '} ' >> /tmp/sonar-runner/build.gradle && \
echo ' ' >> /tmp/sonar-runner/build.gradle && \
echo 'repositories { ' >> /tmp/sonar-runner/build.gradle && \
echo '  repositories { ' >> /tmp/sonar-runner/build.gradle && \
echo '    maven { ' >> /tmp/sonar-runner/build.gradle && \
echo '      url "http://repo1.maven.org/maven2/" ' >> /tmp/sonar-runner/build.gradle && \
echo '    } ' >> /tmp/sonar-runner/build.gradle && \
echo '    maven { ' >> /tmp/sonar-runner/build.gradle && \
echo '      url "https://plugins.gradle.org/m2/" ' >> /tmp/sonar-runner/build.gradle && \
echo '    } ' >> /tmp/sonar-runner/build.gradle && \
echo '  } ' >> /tmp/sonar-runner/build.gradle && \
echo '} ' >> /tmp/sonar-runner/build.gradle && \
echo ' ' >> /tmp/sonar-runner/build.gradle && \
echo 'task hello {' >> /tmp/sonar-runner/build.gradle && \
echo '  doLast {' >> /tmp/sonar-runner/build.gradle && \
echo '    println "Hello world!"' >> /tmp/sonar-runner/build.gradle && \
echo '  }' >> /tmp/sonar-runner/build.gradle && \
echo '} ' >> /tmp/sonar-runner/build.gradle && \
(cd /tmp/sonar-runner && /opt/gradle/gradle-4.2/bin/gradle --no-daemon --info -S -g ${APP_ROOT}/.gradle dependencies) && \
rm -rf /tmp/sonar-runner

USER 1001