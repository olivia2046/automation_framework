# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/5 20:29
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By

import base.globalvars as glo
from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage


class SchedulePage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/time/schedule"
    _add_btn_loc = (By.ID, "add_button")
    _assign_user_loc = (By.XPATH,'//div[@class="head_add"]')
    _save_draft_loc = (By.ID, 'tt_save')

    def add_schedule(self,**kwargs):
        self.driver.get(self.url)
        assert "user" in kwargs.keys()
        self.find_element_and_click(self._add_btn_loc)
        save_draft_btn = self.find_element(self._save_draft_loc)
        #if save_draft_btn is not None:
        self.find_element_and_click(self._assign_user_loc)
        user_loc = (By.XPATH, '//span[text()="%s"]'%kwargs['user'])
        self.find_element_and_click(user_loc)
        save_draft_btn.click()

