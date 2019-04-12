from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from .scraper import Scraper
from ..controller.action_details import ActionDetails
from ..model.meeting_details import MeetingDetails as MeetingDetailsModel
from ..model.meeting_item import MeetingItem as MeetingItemModel

class MeetingDetails(Scraper):
    def __init__(self, url, wait=5, driver=None):
        super().__init__(default_url = url, wait=5, driver=driver)
        self.url = url

    def go_to_meeting_details_page(self):
        self.get(self.url)

    def get_action_details_url(self, elt, base_url=None):
        if base_url is None:
            base_url = self.base_url

        try:
            link_elt = elt.find_element(By.TAG_NAME, 'a')
            on_click_str = link_elt.get_attribute('onclick')
            pattern = "radopen\('(.*?)'"

            matches = re.match(pattern, on_click_str)
            if matches:
                url = matches[1]
                if url.startswith("http"):
                    return url
                else:
                    return "%s%s" % (base_url, url)
            else:
                return None
        except Exception as e:
            return None       

    def get_action_details(self, elt, base_url=None, wait=5):
        url = self.get_action_details_url(elt, base_url)

        if url is not None:
            adc = ActionDetails(url, wait)
            adc.go_to_action_details_page()
            action_details = adc.scrape_page()

            adc.close()

            return action_details
        else:
            return None

    def scrape_meeting_items(self):
        meeting_item_list = []

        rows = self.driver.find_elements(By.XPATH, 
                    "//div[@id='ctl00_ContentPlaceHolder1_gridMain']//table[@class='rgMasterTable']/tbody/tr")

        for row in rows:
            #get each column of the row
            cols = row.find_elements(By.XPATH, 'td')

            if cols is not None and len(cols) > 0:
                if cols[0].text == "No records to display.":
                    break
                    
                file_num = cols[0].text
                file_url = self.elt_get_href(cols[0])

                version = cols[1].text
                agenda_num = cols[2].text
                meeting_item_name = cols[3].text
                meeting_type = cols[4].text
                title = cols[5].text
                action = cols[6].text
                result = cols[7].text

                action_details = self.get_action_details(cols[8])

                video = self.elt_get_href(cols[9])

                meeting_item = MeetingItemModel(
                    file_num, file_url, version, agenda_num,
                    meeting_item_name, meeting_type, title,
                    action, result, action_details, video)

                meeting_item_list.append(meeting_item)

        return meeting_item_list
                
    def _scrape_page(self):
        meeting_name = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_hypName").text
        meeting_datetime = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblDate").text 
        meeting_location = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblLocation").text  

        published_agenda_elt = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_tdAgenda")
        published_agenda = self.elt_get_href(published_agenda_elt)

        agenda_packet = None
        try:
            self.wait_for("ctl00_ContentPlaceHolder1_tdAgendaPacket", wait_time=1)
            agenda_packet_elt = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_tdAgendaPacket")
            if agenda_packet_elt is not None:
                agenda_packet = self.elt_get_href(agenda_packet_elt)
        except:
            agenda_packet = None

        
        meeting_video_elt = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_trVideoX")
        meeting_video = self.get_video_link(meeting_video_elt)

        agenda_status = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblAgendaStatus").text

        minutes_status = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblMinutesStatus").text

        published_minutes_elt = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_tdMinutes")
        published_minutes = self.elt_get_href(published_minutes_elt)

        eComment_elt = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_tdeComment2")
        eComment = self.elt_get_href(eComment_elt)

        additional_notes = None
        try:
            self.wait_for("ctl00_ContentPlaceHolder1_lblMessage", wait_time=1)
            additional_notes_elt = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblMessage")
            if additional_notes_elt is not None:
                additional_notes = additional_notes_elt.text
        except:
            additional_notes = None

        meeting_items = self.scrape_meeting_items()

        return MeetingDetailsModel(
            meeting_name=meeting_name, 
            meeting_datetime=meeting_datetime, 
            meeting_location=meeting_location, 
            published_agenda=published_agenda, 
            agenda_packet=agenda_packet, 
            meeting_video=meeting_video,
            agenda_status=agenda_status,
            minutes_status=minutes_status,
            published_minutes=published_minutes,
            eComment=eComment,
            additional_notes=additional_notes,
            meeting_items=meeting_items
        )

    def run(self):
        self.go_to_meeting_details_page()

        meeting_details = self.scrape_page()
        md_json = meeting_details.to_json()

        print(md_json)

        

