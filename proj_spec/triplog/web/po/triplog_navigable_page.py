# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:30
# @Author : Olivia
# Desc:
# **************************************
import logging

from selenium.webdriver.common.by import By

from proj_spec.triplog.web.po.triplog_base_page import TriplogBasePage
from proj_spec.triplog.web.po.triplog_navigation_bar import TriplogNavigationBar


class TriplogNavigablePage(TriplogBasePage):
    """
    page that has the navigation sidebar
    """
    _layer_popup_loc =(By.CSS_SELECTOR,"div#layui-layer1")
    def __init__(self, driver):
        self.driver = driver
        self.navigation_bar = TriplogNavigationBar(driver)


    def is_layer_popup_visible(self, expected=False):
        """check whether there're trial end/7 day pass pop up

        :param expected: if user should have access to page, expected=False, otherwise expected=True
        :return:
        """
        try:
            if expected:
                self.find_element(self._layer_popup_loc)
            else:
                self.find_element(self._layer_popup_loc,skip_error_handle=True)
            return True
        except Exception as e:
            logging.info("pop up not found")
            return False