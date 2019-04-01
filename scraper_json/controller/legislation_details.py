from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from .scraper import Scraper
from ..model.legislation_details import LegislationDetails as LegislationDetailsModel

class LegislationDetails(Scraper):
    def __init__(self, url, wait=5, driver=None):
        super().__init__(default_url = url, wait=5, driver=driver)
        self.url = url

    def go_to_legislation_details_page(self):
        self.get(self.url)

    def _scrape_page(self):
        file_num = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblFile2").text
        version = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblVersion2").text
        legislation_details_name = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblName2").text

        legislation_detail_type = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblType2").text
        status = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblStatus2").text
        file_created = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblIntroduced2").text
        in_control = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_hypInControlOf2").text
        on_agenda = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblOnAgenda2").text
        final_action = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblPassed2").text
        title = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblTitle2").text

        # TODO: handle attachments later
        attachments = None

        # TODO: handle legislation details_history later
        legislation_items = None

        return LegislationDetailsModel(
            file_num, version, legislation_details_name,
            legislation_details_type, status, file_created,
            in_control, on_agenda, final_action,
            title, attachments, legislation_items
        )

    def run(self):
        self.go_to_legislation_details_page()

        legislation_details = self.scrape_page()
        ld_json = legislation_details.to_json()

        print(ld_json)

        

