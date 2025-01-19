# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:53
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy
from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage



class TripsTabPage(TabsBasePage):

    _next_tip_loc_ios = (AppiumBy.IOS_CLASS_CHAIN,'**/XCUIElementTypeButton[`name == "Next"`]')
    _done_tip_loc_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "Done"`]')

    def get_title(self):
        return self.find_element(self.get_locator_by_os("_title_loc")).text


    def handle_change_activities_tips(self):
        self.find_element_and_click(self.get_locator_by_os("_change_activity_loc"))
        self.find_element_and_click(self.get_locator_by_os("_next_tip_loc"))
        self.find_element_and_click(self.get_locator_by_os("_next_tip_loc"))
        self.find_element_and_click(self.get_locator_by_os("_done_tip_loc"))


