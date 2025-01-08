# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/7 20:31
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By

from proj_spec.triplog.web.po.triplog_base_page import TriplogWebBasePage


class DetailSettingBasePage(TriplogWebBasePage):
    _title_loc = (By.XPATH, '//section[@class="tab-content"]//h1')
    _upgrade_btn_loc = (By.XPATH, '//a[@class="blue_button" and contains(text(),"Upgrade Now")]')


    def get_title(self):
        title_elements = self.find_elements(self._title_loc)
        if title_elements is not None:
            for element in title_elements:
                if element.is_displayed():
                    title_element = element
                    return title_element.text
            return ""
        else:
            return ""


    def is_upgrade_visible(self):
        # upgrade_btn = self.find_element(self._upgrade_btn_loc, condition = "presence_of_element_located")
        # return upgrade_btn.is_displayed()
        #upgrade_btn = self.find_element(self._upgrade_btn_loc,condition="element_to_be_clickable")
        upgrade_btns = self.find_elements(self._upgrade_btn_loc)
        for btn in upgrade_btns:
            if btn.is_displayed():
                return True
        return False
