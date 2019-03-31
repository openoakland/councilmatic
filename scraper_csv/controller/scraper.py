from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import unittest, time, re
from urllib.parse import urlsplit

class Scraper(ABC):
    def __init__(self, default_url, wait=30, driver=None):
        self.default_url = default_url

        self.base_url = None
        if self.default_url is not None:
            self.base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(self.default_url))

        self.wait_time = wait
        if driver is None:
            # default to firefox
            self.driver = webdriver.Firefox()
        else:
            self.driver = driver
        
        self.driver.implicitly_wait(wait)

    def wait_for_login_link(self, wait_time=10):
        self.wait_for(id_str="ctl00_hypSignIn", wait_time=wait_time)

    def elt_get_href(self, elt):
        try:
            link_elt = elt.find_element(By.TAG_NAME, 'a')
            return link_elt.get_attribute('href')
        except:
            return None

    def get_web_element_attribute_names(self, web_element):
        """Get all attribute names of a web element"""
        # get element html
        html = web_element.get_attribute("outerHTML")
        # find all with regex
        pattern = """([a-z]+-?[a-z]+_?)='?"?"""
        return re.findall(pattern, html)

    def get_select_text(self, input_id, select_li_xpath_str):
        # click on the input element to get the select menu to appear
        self.driver.find_element_by_id(input_id).click()

        li_elts = self.driver.find_elements_by_xpath(select_li_xpath_str)

        return [x.text for x in li_elts]

    def set_select_elt(self, input_id, select_li_xpath_str, val, num_of_retries=3,
                        sleep_time=1):
        select_input = self.driver.find_element_by_id(input_id)

        if select_input.get_attribute('value') != val:
            # only click is the new select value is different from the current value
            select_input.click()

            def fn():
                return self.driver.find_element_by_xpath(select_li_xpath_str)

            new_selected_elt = self.retry(
                fn, num_of_retries=num_of_retries, 
                sleep_time=sleep_time, err_msg="Set select failed")

            new_selected_elt.click()

    def set_chbx(self, id_str, val):
        ckbx = self.driver.find_element_by_id(id_str)

        if (ckbx.get_attribute('checked') is None) == val:
            ckbx.click()

    """
    modified from https://gist.github.com/dariodiaz/3104601
    """
    def highlight(self, element, sleep_time=0.3):
        """Highlights (blinks) a Selenium Webdriver element"""
        parent = element._parent
        def apply_style(s):
            parent.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);",
                element, s)
        original_style = element.get_attribute('style')
        apply_style("background: yellow; border: 2px solid red;")
        self.sleep(sleep_time)
        apply_style(original_style)

    def sleep(self, sleep_time):
        if sleep_time is not None and sleep_time > 0:
            time.sleep(sleep_time)

    def get(self, url):
        self.curr_page_link = url
        self.driver.get(url)

    def retry(self, fnc, num_of_retries=3, sleep_time=1, err_msg="Exceeded maximum number of retries"):
        err = None
        for i in range(num_of_retries):
            try:
                return fnc()
            except Exception as e:
                err = e
                #print(e)
                self.sleep(sleep_time)

        err_msg = "%s - %s" % (err_msg, str(err))
        raise Exception(err_msg)

    def _get_pagination_link_dict(self):
        page_link_dict = {}

        xpath_str = "//table[@summary='Data pager which controls on which page is the RadGrid control.']/tbody/tr/td/div[@class='rgWrap rgNumPart']/a"

        page_links = self.driver.find_elements_by_xpath(xpath_str)

        if page_links is not None and len(page_links)>0:
            for page_link in page_links:
                if page_link.text != "...":
                    page_link_dict[page_link.text] = page_link
                elif page_link.get_attribute("title") != "Next Pages":
                    more_link = page_link

            try:
                more_link = self.driver.find_element_by_xpath("//table[@summary='Data pager which controls on which page is the RadGrid control.']/tbody/tr/td/div[@class='rgWrap rgNumPart']/a[@title='Next Pages']")

                last_page_num = max([int(x) for x in page_link_dict.keys()])
                page_link_dict[str(last_page_num+1)] = more_link
            except:
                # no more link
                pass

        return page_link_dict   

    def get_pagination_link_dict(self, num_of_retries=3, sleep_time=3):
        return self.retry(fnc=self._get_pagination_link_dict, 
                            num_of_retries=num_of_retries,
                            sleep_time=sleep_time,
                            err_msg="Error getting pagination links")


    @abstractmethod
    def _scrape_page(self, num_of_retries=3, sleep_time=3):
        pass

    def scrape_page(self, num_of_retries=3, sleep_time=3):
        return self.retry(
            fnc=self._scrape_page, 
            num_of_retries=num_of_retries,
            sleep_time=sleep_time,
            err_msg="Scraping page failed"
        )

    def scrape_pages(self, num_of_retries=3, sleep_time=5):
        data = self.scrape_page(num_of_retries)

        pagination_link_dict = self.get_pagination_link_dict(
            num_of_retries=num_of_retries,
            sleep_time=sleep_time)
        if len(pagination_link_dict.keys()) > 0:
            page_num = 2
            page_num_str = str(page_num)
            while page_num_str in pagination_link_dict.keys():
                self.curr_page_link = pagination_link_dict[page_num_str]
                self.curr_page_link.click()
                self.sleep(sleep_time)
                data += self.scrape_page(num_of_retries, sleep_time=sleep_time)

                pagination_link_dict = self.get_pagination_link_dict(
                    num_of_retries=num_of_retries,
                    sleep_time=sleep_time)

                page_num += 1

                page_num_str = str(page_num)

        return data
    
        



    def close(self):
        try:
            self.driver.quit()
        except:
            pass

    def wait_for(self, id_str, wait_time=10):
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.ID, id_str)))
        except:
            raise Exception("%s was not found" % id_str)



