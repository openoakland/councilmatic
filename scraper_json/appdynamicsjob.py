# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.default_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("https://oakland.legistar.com/Calendar.aspx")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='City Home'])[1]/following::span[3]").click()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnSwitch").click()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstMax_Input").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Sign In'])[1]/preceding::li[1]").click()
        #driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstMax_Input").clear()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstMax_Input").send_keys("All")
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYearsAdvanced_Input").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Last Year'])[1]/preceding::li[20]").click()
        #driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYearsAdvanced_Input").clear()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYearsAdvanced_Input").send_keys("All Years")
        driver.find_element_by_id("visibleSearchButton").click()
        driver.find_element_by_id("ctl00_ButtonRSS").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | win_ser_1 | ]]
        # perhaps instead use driver.switch_to_window("win_ser_1")
        print(driver.page_source)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()