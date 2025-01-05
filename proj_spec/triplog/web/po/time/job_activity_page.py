# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2025/1/4 19:40
desc: 
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import base.globalvars as glo
from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage


class JobActivityPage(TriplogNavigablePage):
    url = glo.get_value("url1")+"/time/categoryList"
    _add_btn_loc = (By.XPATH, '//a[@class="create"]')
    _name_input_loc = (By.XPATH, '//input[@type="text" and @id="name" and @placeholder="required"]') # there're 2 elements with id=name
    _hourly_rate_input_loc = (By.ID, "hourlyRate")
    #_dept_office_select_loc = (By.XPATH, '//input[contains(@id, "easyui_textbox_input") and  @class="textbox-text validatebox-text textbox-prompt"]')
    _dept_office_dropdown_loc = (By.XPATH, '//a[@class="textbox-icon combo-arrow"]')

    _create_btn_loc = (By.XPATH, '//input[@type="submit" and @value="Create"]')
    _save_btn_loc = (By.XPATH, '//input[@type="submit" and @value="Save"]')



    def _input_job_activity_fields(self, **kwargs):
        name_input = self.find_element(self._name_input_loc)
        if name_input is not None:
            self.find_element_and_input(self._name_input_loc, kwargs['name'])
        if 'hourly_rate' in kwargs.keys():
            self.find_element_and_input(self._hourly_rate_input_loc, kwargs['hourly_rate'])
        if 'dept_office' in kwargs.keys():
            self.find_element_and_click(self._dept_office_dropdown_loc)
            _dept_office_option_loc = (By.XPATH, '//div[contains(@id, "user_dept_category_row") and text()="%s"]'%kwargs['dept_office'])
            self.find_element_and_click(_dept_office_option_loc)




    def add_job_activity(self, **kwargs):
        self.driver.get(self.url)
        assert 'name' in kwargs.keys()
        self.find_element_and_click(self._add_btn_loc)
        self._input_job_activity_fields(**kwargs)
        self.find_element_and_click(self._create_btn_loc)



