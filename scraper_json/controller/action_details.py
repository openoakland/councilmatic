from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from .scraper import Scraper
from ..model.action_details import ActionDetails as ActionDetailsModel
from ..model.vote_item import VoteItem as VoteItemModel

class ActionDetails(Scraper):
    def __init__(self, url, wait=5, driver=None):
        super().__init__(default_url = url, wait=5, driver=driver)
        self.url = url

    def go_to_action_details_page(self):
        self.get(self.url)

    def get_vote_items(self):
        vote_items = []

        rows = self.driver.find_elements(By.XPATH, 
                    "//div[@id='ctl00_ContentPlaceHolder1_gridVote']//table[@class='rgMasterTable']/tbody/tr")

        for row in rows:
            #get each column of the row
            cols = row.find_elements(By.XPATH, 'td')

            if cols is not None and len(cols) > 0:
                if cols[0].text == "No records to display.":
                    break

                person_name = cols[0].text
                vote = cols[1].text

                vote_item = VoteItemModel(person_name, vote)
                vote_items.append(vote_item)

        return vote_items

    def _scrape_page(self):
        file_num_elt = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_hypFile")
        file_num = file_num_elt.text
        file_url = self.elt_get_href(file_num_elt.find_element_by_xpath('..'))

        version = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblVersion2").text
        action_type = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblType").text
        title = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblTitle").text
        mover = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_hypMover").text
        seconder = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_hypSeconder").text
        result = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblResult").text
        agenda_note = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblAgendaNote").text
        minute_note = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblMinutesNote").text
        action = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblAction").text
        action_text = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblActionText").text

        votes = self.get_vote_items()

        return ActionDetailsModel(
            file_num,
            file_url,
            version,
            action_type,
            title,
            mover,
            seconder,
            result,
            agenda_note,
            minute_note,
            action,
            action_text,
            votes
        )

    def run(self):
        self.go_to_action_details_page()

        action_details = self.scrape_page()
        ad_json = action_details.to_json()

        print(ad_json)

        

