"""Module Summary:

Purpose:
This module demonstrates a basic proficiency in using Python to automate
website / web-based application testing using Selenium Webdriver & Chrome.

Requirements: 
    Python Packages:
        1. selenium
        2. webdriver-manager

Parameters: Defined as variables for simplicity's sake.
    Variables:
        base_webpage = str, URL
        tc_1_script = str, inline JS
        tc_1_headerText_CssSelector = str, CSS Selector
        tc_1_headerText_Value = str, text that's expected to be onscreen.
        tc_1_searchBar_CssSelector = str, CSS Selector
        tc_1_searchBar_Text = str, text to be added in the search bar.
        tc_1_searchBar_KeyStroke = str, matching value for "RETURN"
        tc_1_firstResult_CssSelector = str, CSS Selector
        tc_1_finalHeaderText_CssSelector = str, CSS Selector
        tc_1_finalHeaderText_Value = str, text that's expected to be onscreen.

Returns: 
    1. Assertion Exceptions (if a step in the test case fails)
    2. Test Case Completion Status (if test case has no errors)
    
"""

#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#Classes
class EventListener(AbstractEventListener):
    """Purpose: This class enables event-listening for selenium."""
    clicked = False
    def before_click(self, element, driver):
        print ("Event : before element click()")
        
    def after_click(self, element, driver):
        print ("Event : after element click()")
        
class TestDriverChrome():
    """This class creates a testing-ready browser."""
    def __init__(self, base_webpage):
        """This constructor/method builds the initial testable browser."""
        self.base_webpage = base_webpage
        options = webdriver.ChromeOptions()  #Mute Selenium DevTools.
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        d = DesiredCapabilities.CHROME  #Enable Browser Logging.
        d['goog:loggingPrefs'] = { 'browser':'ALL' }
        self.sel_service = Service(ChromeDriverManager().install())
        #self.sel_service = ("Chrome 95.048 Webdriver/chromedriver.exe")  
        self.driver = webdriver.Chrome(
            service=self.sel_service, 
            options=options, 
            desired_capabilities=d)
        #Add events wrapper for driver to handle event listening.
        self.e_driver = EventFiringWebDriver(self.driver, EventListener())
        self.e_driver.get(self.base_webpage)
        #Remove other windows that open.
        if len(self.e_driver.window_handles) > 1:
            for handle in self.e_driver.window_handles:
                self.e_driver.switch_to.window(handle)
                if self.e_driver.current_url != base_webpage:
                    self.e_driver.close()
                else:
                    pass
    def run_custom_script(self, script):
        """This method allows a custom JS script to run in the browser."""
        self.e_driver.execute_script(script)
        print("Script Completed")
    def run_assert(self, cssSelector, value):
        """This method checks if the browser's element matches the given value."""
        foundValue = self.e_driver.find_element(By.CSS_SELECTOR, cssSelector).get_attribute('innerText')
        assert(value == foundValue), "The value found on the website was different than what was expected."
        print("Assert Completed")
    def run_click(self, cssSelector):
        """This method clicks on an element in the browser."""
        editor = WebDriverWait(self.e_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector)))
        editor.click()
        print("Click Completed")
    def run_type(self, cssSelector, text):
        """This method clears an input field and types in text."""
        editor = WebDriverWait(self.e_driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, cssSelector)))
        #editor.click()
        editor.send_keys(Keys.CONTROL, 'a')
        editor.send_keys(Keys.BACKSPACE)
        editor.send_keys(text)
        print("Typing Completed")
    def run_keystroke(self, cssSelector, stroke):
        """This method sends a keystroke to an element in the browser."""
        editor = WebDriverWait(self.e_driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, cssSelector)))
        editor.send_keys(Keys.__getattribute__(Keys, stroke))
        print("Keystroke Completed")
    def end_test_driver(self):
        """This method kills the browser and all tabs."""
        self.e_driver.quit()   

#Variables
base_webpage = "https://en.wikipedia.org/wiki/Machine_learning"
tc_1_script = "console.log('Hello World!')"
tc_1_headerText_CssSelector = "#firstHeading"
tc_1_headerText_Value = "Machine learning"
tc_1_searchBar_CssSelector = "#searchInput"
tc_1_searchBar_Text = "software testing automation"
tc_1_searchBar_KeyStroke = "RETURN"
tc_1_firstResult_CssSelector = (
    "#mw-content-text > div.searchresults.mw-searchresults-has-iw "
    "> ul > li:nth-child(1) > div.mw-search-result-heading > a"
    )
tc_1_finalHeaderText_CssSelector = "#firstHeading"
tc_1_finalHeaderText_Value = "Test automation"

#Functions 
print("START: test_wikipedia_post" + '\n')
tc_1 = TestDriverChrome(base_webpage)
tc_1.run_custom_script(tc_1_script)
tc_1.run_assert(tc_1_headerText_CssSelector, tc_1_headerText_Value)
tc_1.run_click(tc_1_searchBar_CssSelector)
tc_1.run_type(tc_1_searchBar_CssSelector, tc_1_searchBar_Text)
tc_1.run_keystroke(tc_1_searchBar_CssSelector, tc_1_searchBar_KeyStroke)
tc_1.run_click(tc_1_firstResult_CssSelector)
tc_1.run_assert(tc_1_finalHeaderText_CssSelector, tc_1_finalHeaderText_Value)
print("Test Case 1 Completed", '\n')
input("Hit \"Enter\" to Quit.")
tc_1.end_test_driver()
