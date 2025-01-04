# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2025/1/4 11:42
desc: 
'''
from selenium.webdriver.common.by import By

import base.globalvars as glo
from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage


class TimeClockListPage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/time/list"
    _add_time_entry_loc = (By.ID, 'add_button')

    _save_btn_loc = (By.XPATH, '//input[@type="button" and @value="Delete"]/../input[1]')
    _delete_btn_loc = (By.XPATH, '//input[@type="button" and @value="Delete"]')


    def _get_nth_time_entry_locator(self, row_index):
        return (By.XPATH, '//tr[contains(@id, "timeentry_row")][%s]'%(row_index+1))

    def add_time_entry(self, **kwargs):
        self.find_element_and_click(self._add_time_entry_loc)
        self.find_element_and_click(self._save_btn_loc)


    def edit_time_enty(self, **kwargs):
        self.driver.get(self.url)
        self.find_element_and_click(self._get_nth_time_entry_locator(kwargs['row_index']))
        self.find_element_and_click(self._save_btn_loc)

    def delete_one_time_entry(self, row_index):
        self.driver.get(self.url)
        self.find_element_and_click(self._get_nth_time_entry_locator(row_index))
        self.find_element_and_click(self._delete_btn_loc)
        alert = self.driver.switch_to.alert
        alert.accept()




