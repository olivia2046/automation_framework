# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/20 15:41
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By

from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage
import base.globalvars as glo

class TimeClockCalendarPage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/time/clock"

    _clock_in_menu_loc = (By.ID, "clock_in")
    _clock_in_btn_loc = (By.ID, "tt_clock_in")
    _clock_out_menu_loc = (By.ID, "clock_out")
    _clock_out_btn_loc = (By.ID, "tt_clock_out")

    # def __init__(self, driver):
    #     """inistialize the time clock caclendar page
    #
    #
    #     :param driver:
    #
    #     """
    #     super().__init__(driver)
    #     self.driver.get(self.url)

    def clock_in(self, **kwargs):
        clock_out_menu = self.find_element(self._clock_out_menu_loc)
        if clock_out_menu is not None:
            clock_out_menu.click()
            self.find_element_and_click(self._clock_out_btn_loc)
        self.driver.get(self.url)
        self.find_element_and_click(self._clock_in_menu_loc)
        self.find_element_and_click(self._clock_in_btn_loc)

        clock_out_menu = self.find_element(self._clock_out_menu_loc)
        assert clock_out_menu is not None

    def clock_out(self, **kwargs):
        clock_in_menu = self.find_element(self._clock_in_menu_loc)
        if clock_in_menu is not None:
            clock_in_menu.click()
            self.find_element_and_click(self._clock_in_btn_loc)
        self.driver.get(self.url)
        # clock_out_menu = self.find_element(self._clock_out_menu_loc,condition="element_to_be_clickable")
        # if clock_out_menu is not None:
        #     clock_out_menu.click()
        # clock_out_btn = self.find_element(self._clock_out_btn_loc,condition="element_to_be_clickable")
        # if clock_out_btn is not None:
        #     clock_out_btn.click()
        self.find_element_and_click(self._clock_out_menu_loc)
        self.find_element_and_click(self._clock_out_btn_loc)

        clock_in_menu = self.find_element(self._clock_in_menu_loc)
        assert clock_in_menu is not None
