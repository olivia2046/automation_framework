# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/7 20:31
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By

from proj_spec.triplog.web.po.triplog_base_page import TriplogWebBasePage


class DetailSettingBasePage(TriplogWebBasePage):
    _title_loc = (By.XPATH, '//section[@id="c1"]//h1')


    def get_title(self):
        title_element = self.find_element(self._title_loc)
        if title_element is not None:
            return title_element.text
        else:
            return ""

