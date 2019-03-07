from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from scraper import Scraper
from model.legislation import Legislation as LegislationModel

class Legislation(Scraper):
    def __init__(self, base_url='https://oakland.legistar.com/Legislation.aspx', wait=5, driver=None):
        super().__init__(base_url, wait, driver)    

    def run(self):
        #do a GET request to base url.
        self.get(self.base_url)

        #empty most of the time. So try a different year for testing purposes
        #self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYears_Arrow").click()
        #self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='All Years'])[1]/following::li[1]").click()
        #end test commands.

        legislation_list = []
        
        #find div that holds table with council members info and extract the rows of the table.
        rows = self.driver.find_elements(By.XPATH, 
                    "//div[@id='ctl00_ContentPlaceHolder1_gridMain']/table/tbody/tr")

        for i, row in enumerate(rows):
            print(i, str(row))
            #get each column of the row.
            cols = row.find_elements(By.TAG_NAME, 'td')
            
            #extract data
            file_num = cols[0].text
            file_link = self.elt_get_href(cols[0])
  
            legislation_type = cols[1].text
            
            status = cols[2].text

            file_created = cols[3].text

            final_action = cols[4].text
            title = cols[5].text

            print("num: ", file_num)
            print("link: ", file_link)
            print("legislation_type: ", legislation_type)
            print("status ", status)
            print("file_created: ", file_created)
            print("final_action: ", final_action) 
            print("title: ", title)
            
           

            #create data storage object
            legislation = LegislationModel(file_num, file_link, legislation_type, 
                                        status, file_created, 
                                        final_action, title)

            legislation_list.append(legislation)

        #turn to json
        cl_json = LegislationModel.to_map_list_json(legislation_list)

        print(cl_json)

def main():
    cc = Legislation()
    cc.run()
    cc.close()

if __name__ == "__main__":
    main()