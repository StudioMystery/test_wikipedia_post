"""Module Summary:

Requirements: Selenium Webdriver for Python

Parameters: No parameters necessary

Returns: List of test cases and their completion status
    
"""
#Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Classes
class e_listener(AbstractEventListener):
    clicked = False
    def before_click(self, element, driver):
        print ("Event : before element click()")
        
    def after_click(self, element, driver):
        print ("Event : after element click()")

#Variables
base_webpage = "https://en.wikipedia.org/wiki/Machine_learning"
options = webdriver.ChromeOptions()  #Mute Selenium DevTools listening:
options.add_experimental_option('excludeSwitches', ['enable-logging'])
d = DesiredCapabilities.CHROME  #Enable Browser Logging
d['goog:loggingPrefs'] = { 'browser':'ALL' }
sel_service = Service("Chrome 95.048 Webdriver/chromedriver.exe")  #Define Selenium Driver to ignore constant log
driver = webdriver.Chrome(service=sel_service, options=options, desired_capabilities=d)
#Add events wrapper for driver
e_driver = EventFiringWebDriver(driver, e_listener())
e_driver.get(base_webpage)
#Remove other windows that open
if len(e_driver.window_handles) > 1:
    for handle in e_driver.window_handles:
        e_driver.switch_to.window(handle)
        if e_driver.current_url != base_webpage:
            e_driver.close()
        else:
            pass
#Add event listener that adds the element a user clicks to the chrome Console.
#
e_driver.execute_script()
#Functions
print("START: test_wikipedia_post")
print("")
