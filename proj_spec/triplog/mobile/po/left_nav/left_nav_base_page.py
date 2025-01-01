# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/21 11:37
# @Author : Olivia
# Desc: base page of pages accessed from left navigation bar
# **************************************
from appium.webdriver.common.appiumby import AppiumBy
from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage
from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class LeftNavBasePage(TriplogMobileBasePage):
    _title_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_main_title')
    _back_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/img_main_icon')
    def go_back(self):
        self.find_element_and_click(self.get_locator_by_os("_back_loc"))
        return TabsBasePage


    def get_title(self):
        return self.find_element(self.get_locator_by_os("_title_loc")).text


    def goto_logout(self):
        tab_base_page = self.go_back()
        tab_base_page.show_left_panel()
        pass