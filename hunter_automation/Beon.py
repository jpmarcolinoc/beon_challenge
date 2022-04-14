import re
from collections import namedtuple
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select


FilterValue = namedtuple('FilterValue', ['tech', 'offers',  'business', 'role'])


class Beon(object):

    URL = 'https://beon.studio/'

    bt_join_us = ".join-us"

    def __init__(self, chrome_driver: webdriver.Chrome):
        self.driver = chrome_driver

    def __navigate(self):
        if self.driver.current_url != self.URL:
            self.driver.get(self.URL)

    def join_us(self):
        self.__navigate()
        self.driver.find_element(By.CSS_SELECTOR, self.bt_join_us).click()


class JobOfferCard(object):
    txt_offer_title = '.job-offer__title'
    txt_pill_tech = '.badge-tech'

    # First job-offer-detail-subtitle is the business value
    txt_business = '//*/div[contains(@class, "job-offer__details")]/*/span[contains(@class, "job-offer-detail-subtitle")][1]'

    def __init__(self, ele: WebElement):
        self.ele = ele

    @property
    def title(self):
        return self.ele.find_element_by_css_selector(self.txt_offer_title).text

    @property
    def tech(self):
        return self.ele.find_element_by_css_selector(self.txt_pill_tech).text

    @property
    def business(self):
        return self.ele.find_element(By.XPATH, self.txt_business).text

    def __repr__(self):
        return f'{self.title} - {self.tech} - {self.business}'

class Careers(object):
    st_tech = '//*[@id="section-job-offers-container"]/div[1]/div[1]/select'
    st_business = '//*[@id="section-job-offers-container"]/div[1]/div[2]/select'
    st_role = '//*[@id="section-job-offers-container"]/div[1]/div[3]/select'
    card_job_offer = '.job-offer'  # CSS selector

    txt_no_results = '//*[@id="section-job-offers-container"]/div[3]/div[3]'

    def __init__(self, chrome_driver: webdriver.Chrome):
        self.driver = chrome_driver

    def has_results(self):
        try:
            no_results = self.driver.find_element(By.XPATH, self.txt_no_results)
            if 'no results' in no_results.text:
                return False
        except:
            return True

    def search_for(self, tech=None, business=None, role=None):
        tech_select = Select(self.driver.find_element(By.XPATH, self.st_tech))
        bsn_select = Select(self.driver.find_element(By.XPATH, self.st_business))
        rle_select = Select(self.driver.find_element(By.XPATH, self.st_role))

        for select, value in zip([tech_select, bsn_select, rle_select], [tech, business, role]):
            if value:
                select.select_by_value(value)
            else:
                select.select_by_index(1)
        # No need to click submit

    def get_search_results(self) -> List[JobOfferCard]:
        if not self.has_results():
            return []

        job_offer_cards = self.driver.find_elements(By.CSS_SELECTOR, self.card_job_offer)
        return [JobOfferCard(ele) for ele in job_offer_cards]

    def get_filter_values(self) -> FilterValue:
        tech_select = Select(self.driver.find_element(By.XPATH, self.st_tech))
        bsn_select = Select(self.driver.find_element(By.XPATH, self.st_business))
        rle_select = Select(self.driver.find_element(By.XPATH, self.st_role))
        tech_text = tech_select.first_selected_option.text

        tech, count = re.match(r'(.*)\((\d+)\)', tech_text).groups()

        return FilterValue(tech=tech,
                           offers=int(count),
                           business=bsn_select.first_selected_option.text,
                           role=rle_select.first_selected_option.text)

