# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:30
# @Author : Olivia
# Desc: @todo: make initialize method abstract?
# **************************************
import logging

from selenium.webdriver.common.by import By

from proj_spec.triplog.web.po.triplog_base_page import TriplogWebBasePage
from proj_spec.triplog.web.po.triplog_navigation_bar import TriplogNavigationBar


class TriplogNavigablePage(TriplogWebBasePage):
    """
    page that has the navigation sidebar
    """
    url = None #to be provides by concrete sub-class
    _title_loc = (By.XPATH, '//span[@class="n_menu-selected-menuname"]')
    _layer_popup_loc =(By.CSS_SELECTOR,"div#layui-layer1")
    def __init__(self, driver):
        #super().__init__(driver)
        self.driver = driver
        self.navigation_bar = TriplogNavigationBar(driver)
        if self.url is not None:
            self.driver.get(self.url)


    def is_layer_popup_visible(self):
        """check whether there're trial end/7 day pass pop up

        :param expected: if user should have access to page, expected=False, otherwise expected=True
        :return:
        """

        popup = self.find_element(self._layer_popup_loc)
        if popup is None:
            logging.info("popup layer not found")
            return False
        else:
            logging.info("popup layer found")
            return True



    def jumped_to_billing(self):
        """whether page jumps to the Billing page

        :return:
        """
        return self.get_title()=='Billing'


    def get_title(self):
        title_element =  self.find_element(self._title_loc)
        if title_element is not None:
            return title_element.text
        else:
            return ""
