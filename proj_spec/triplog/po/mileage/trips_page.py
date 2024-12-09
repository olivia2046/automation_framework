# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/6 17:28
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from proj_spec.triplog.po.triplog_navigable_page import TriplogNavigablePage


class TripsPage(TriplogNavigablePage):

    _add_trip_locator = (By.CSS_SELECTOR,"#add_button")
    _from_location_loc = (By.CSS_SELECTOR, "#fromLocation\.id")
    _to_location_loc = (By.CSS_SELECTOR, "#toLocation\.id")
    _create_button_loc = (By.XPATH, "//input[@type='submit' and @value='Create' and not(@class='blue_button')]")



    def add_trip(self, from_location, to_location ):
        self.find_element_and_click(self._add_trip_locator)
        # self.select_dropdown_option(self._from_location_loc, from_location)
        # self.select_dropdown_option(self._to_location_loc, to_location)

        from_select = Select(self.find_element(self._from_location_loc))
        from_select.select_by_visible_text(from_location)
        to_select = Select(self.find_element(self._to_location_loc))
        to_select.select_by_visible_text(to_location)
        self.find_element_and_click(self._create_button_loc)