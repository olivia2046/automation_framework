# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/6 17:28
# @Author : Olivia
# Desc:
# **************************************
import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import base.globalvars as glo
from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage


class TripsPage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/trip"
    _add_trip_locator = (By.CSS_SELECTOR,"#add_button")

    _confirm_delete_multiple_loc = (By.XPATH, "//div[@id='delete_multiple_dialog']//input[@type='submit' and "
                                              "@class='red_border_button' and @value='Delete']")


    _from_location_loc = (By.CSS_SELECTOR, "#fromLocation\.id")
    _to_location_loc = (By.CSS_SELECTOR, "#toLocation\.id")
    _create_button_loc = (By.XPATH, "//input[@type='submit' and @value='Create' and not(@class='blue_button')]")
    # save button when edit trip
    _save_button_loc = (By.XPATH, "//input[@type='button' and @ value='Create Return Trip']/preceding-sibling::input")
    _tips_locator = (By.CSS_SELECTOR, "mask#b + g > path:nth-child(2)")
    _ytd_mileage_loc = (By.XPATH, "//span[@class='ui-dialog-title' and text()='Year to Date Mileage Required']")
    _ytd_save_btn_loc = (By.XPATH,"//div[@id='year_to_date_dialog']//input[@type='submit' and @value='Save']")
    #_title_locator = (By.CSS_SELECTOR, "span.n_menu-selected-menuname")
    _trip_row_loc = (By.XPATH, "//div[contains(@id,'trip_row_')]")

    #_trips_loc = (By.XPATH, "//tr[contains(@id,'trip_row_')]")
    _trips_xpath = "//tr[contains(@id,'trip_row_')]"
    _trip_checkboxs_xpath = "(//input[@class='selected_id'])"
    _trip_row_masked_loc = (By.XPATH, "//div[contains(@id,'trip_row_') and contains(@id,'_mask_outer')]")
    _query_distance_loc = (By.CSS_SELECTOR,"input[type='button'][class='green_button'][value='Query Driving Distance']")

    def __init__(self,driver,accessible=True):
        """inistialize the trips page
        if user is expected to have access to this page(by default), process the possible tips pop up at the end;
        otherwise don't process the tips pop ups.

        :param driver:
        :param accessible:
        """
        super().__init__(driver)
        self.driver.get(self.url)
        time.sleep(2)
        try:

            #self.find_element(self._trip_row_masked_loc,skip_error_handle=True)
            self.find_element(self._ytd_mileage_loc,skip_error_handle=True)
            self.find_element_and_click(self._ytd_save_btn_loc)

        except Exception as e:
            #logging.info("tips not prompted, continue with script")
            logging.info("Year to Date Mileage window not present")

        if accessible:
            self.find_element_and_click(self._trip_row_loc)


    def choose_button(self, first_level_text, second_level_text):
        """

        :param first_level:
        :param second_level:
        :return:
        """
        _triangle_down_loc = (By.XPATH, "//div[@class='triangle_down' and text()='%s']"%first_level_text)
        link_loc = (By.XPATH, "//a[text()='%s']"%second_level_text)

        self.hover_over_element(_triangle_down_loc)
        self.find_element_and_click(link_loc)



    def add_trip(self, from_location, to_location, query_distance=False ):
        self.find_element_and_click(self._add_trip_locator)
        # self.select_dropdown_option(self._from_location_loc, from_location)
        # self.select_dropdown_option(self._to_location_loc, to_location)

        from_select = Select(self.find_element(self._from_location_loc))
        from_select.select_by_visible_text(from_location)
        to_select = Select(self.find_element(self._to_location_loc))
        to_select.select_by_visible_text(to_location)

        if query_distance:
            self.find_element_and_click(self._query_distance_loc)
            time.sleep(3)
            confirm_popup = self.driver.switch_to.alert
            confirm_popup.accept()

        self.find_element_and_click(self._create_button_loc)


    #def edit_trip(self, row_index, **kwargs):
    def edit_trip(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        #self.driver.get(self.url)
        time.sleep(2)
        row_index=kwargs['row_index']
        nth_trip_loc = (By.XPATH,"(%s)[%s]"%(self._trips_xpath,row_index+1)) #xpath index starts from 1
        self.find_element_and_click(nth_trip_loc)
        # trip_row_element = self.find_element(nth_trip_loc)
        # trip_row_element.click()

        #nth_trip.screenshot("nth_trip")

        #nth_trip.click()

        if "from_location" in kwargs:
            from_select = Select(self.find_element(self._from_location_loc))
            from_select.select_by_visible_text(kwargs['from_location'])
        if "to_location" in kwargs:
            to_select = Select(self.find_element(self._to_location_loc))
            to_select.select_by_visible_text(kwargs['to_location'])

        if "query_distance" in kwargs and kwargs["query_distance"] is True:
            self.find_element_and_click(self._query_distance_loc)
            time.sleep(3)
            confirm_popup = self.driver.switch_to.alert
            confirm_popup.accept()

        self.find_element_and_click(self._save_button_loc)


    def delete_trip_from_menu(self, index=0):
        """

        :return:
        """
        #self.driver.get(self.url)

        nth_trip_checkbox_loc = (By.XPATH, "%s[%s]"%(self._trip_checkboxs_xpath,index+1)) #xpath starts from 1
        self.find_element_and_click(nth_trip_checkbox_loc)

        self.choose_button("Delete","Delete Selected")

        self.find_element_and_click(self._confirm_delete_multiple_loc)


