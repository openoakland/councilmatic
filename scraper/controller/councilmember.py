from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from datetime import datetime

from .scraper import Scraper
from ..model.councilmember import CouncilMember as CouncilMemberModel
from ..model.department import Department as DepartmentModel

class CouncilMember(Scraper):
    def __init__(self, default_url='https://oakland.legistar.com/Calendar.aspx', wait=30, driver=None):
        #Started selenium on legistar calendar webpage. Since the city council page generates an ID for the url
        #and I am not sure that the ID is persistent or changing.
        super().__init__(default_url, wait, driver)   

    def get_depts(self):
        input_id = "ctl00_ContentPlaceHolder1_lstName_Input"
        select_li_xpath_str = "//div[@id='ctl00_ContentPlaceHolder1_lstName_DropDown']//ul[@class='rcbList']/li[@class='rcbItem']"

        return self.get_select_text(input_id, select_li_xpath_str)   

    def set_dept_name(self, dept_name, sleep_time=1):
        input_id = "ctl00_ContentPlaceHolder1_lstName_Input"
        select_xpath_str = "//div[@id='ctl00_ContentPlaceHolder1_lstName_DropDown']//ul[@class='rcbList']/li[@class='rcbItem'][text() = '%s']" % dept_name
        self.set_select_elt(input_id, select_xpath_str, dept_name, sleep_time)

    def go_to_councilmember_page(self):
        #do a GET request to base url.
        self.get(self.default_url)
        #go to city council page
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Calendar'])[1]/following::span[3]").click()

        #click on "people" button
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Calendar (0)'])[1]/following::span[3]").click()

    def to_date(self, date_str):
        try:
            format_str = '%d/%m/%Y'
            dt = datetime.strptime(date_str, format_str)
            return dt
        except:
            return None

    def _scrape_page(self):
        councilmember_dict = {}
        
        #find div that holds table with council members info and extract the rows of the table.
        rows = self.driver.find_elements(By.XPATH, 
                    "//div[@id='ctl00_ContentPlaceHolder1_gridPeople']/table/tbody/tr")

        last_member_start_date = None
        for i, row in enumerate(rows):
            #print(i, str(row))
            #get each column of the row.
            cols = row.find_elements(By.TAG_NAME, 'td')

            #extract data
            department_name = cols[0].text
            name = cols[1].text
  
            title = cols[2].text
            
            start_date = self.to_date(cols[3].text)

            end_date = self.to_date(cols[4].text)

            email = cols[5].text
            website = cols[6].text
            appointed_by = cols[7].text

            """
            print("department name", department_name)
            print("name: ", name)
            print("title: ", title)
            print("start_date: ", start_date)
            print("end_date: ", end_date) 
            print("email: ", email)
            print("website: ", website)
            print("appointed_by ", appointed_by)
            """

            department = DepartmentModel(department_name, title,
                                            start_date, end_date, appointed_by)

            if name not in councilmember_dict or councilmember_dict.get(name) is None:
                councilmember = CouncilMemberModel(name, email, website, {
                    department_name: department
                })
                councilmember_dict[name] = councilmember
            else:
                if department_name not in councilmember_dict[name].departments:
                    councilmember_dict[name].departments[department_name] = department
            
            if (last_member_start_date is None or start_date is None 
                or start_date > last_member_start_date):
                last_member_start_date = start_date
                councilmember_dict[name].last_member_start_date = last_member_start_date

        return councilmember_dict

    def scrape_pages(self, num_of_retries=3, sleep_time=5):
        data = self.scrape_page(num_of_retries)

        pagination_link_dict = self.get_pagination_link_dict(
            num_of_retries=num_of_retries,
            sleep_time=sleep_time)
        if len(pagination_link_dict.keys()) > 0:
            page_num = 2
            page_num_str = str(page_num)
            while page_num_str in pagination_link_dict.keys():
                curr_page_link = pagination_link_dict[page_num_str]
                curr_page_link.click()
                self.sleep(sleep_time)
                data.update(self.scrape_page(num_of_retries, sleep_time=sleep_time))

                pagination_link_dict = self.get_pagination_link_dict(
                    num_of_retries=num_of_retries,
                    sleep_time=sleep_time)

                page_num += 1

                page_num_str = str(page_num)

        return data

    def query(self, dept_name="All Departments", sleep_time=5, wait_time=5):
        if dept_name is not None and dept_name != "":
            self.set_dept_name(dept_name)
            self.sleep(sleep_time)  
            self.wait_for_login_link(wait_time) 

        return self.scrape_pages(sleep_time=sleep_time)

    def run(self):
        self.go_to_councilmember_page();
        
        councilmember_dict = self.query("All Departments")

        councilmember_list = [councilmember_dict[x] for x in sorted(councilmember_dict.keys())]

        #turn to json
        cm_json = CouncilMemberModel.to_map_list_json(councilmember_list)

        print(cm_json)

        self.close()

if __name__ == "__main__":
    main()