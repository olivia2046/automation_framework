# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/13 20:25
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By

from proj_spec.triplog.web.po.triplog_base_page import TriplogWebBasePage


class TrialEndPage(TriplogWebBasePage):
    _subscribe_btn_loc = (By.XPATH, "//div[@id='layui-layer1']//button[@class='blue_button']")


    def click_subscribe(self):
        self.find_element_and_click(self._subscribe_btn_loc)
