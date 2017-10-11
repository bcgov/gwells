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
