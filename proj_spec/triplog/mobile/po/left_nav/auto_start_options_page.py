# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2025/1/23 08:50
desc:
'''
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage


class AutoStartOptionsPage(LeftNavBasePage):
    _learn_more_title_loc_ios = (AppiumBy.IOS_CLASS_CHAIN,'**/XCUIElementTypeStaticText[`name == "Learn more about auto start options"`]')
    _learn_more_title_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_title" and'
                                                     'contains(@text,"Learn more about auto start options")]')
    _learn_more_ok_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rtv_ok')
    _learn_more_ok_loc_ios = (AppiumBy.ACCESSIBILITY_ID,'OK')
    _back_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_action')
    _back_loc_ios = (AppiumBy.ACCESSIBILITY_ID,'Cancel')

    # def __init__(self):
    #     super().__init__()
    #     if self.is_learn_more_displayed():
    #         auto_start_options_displayed = True
    #         self.confirm_learn_more()


    def confirm_learn_more(self):
        self.find_element_and_click(self.get_locator_by_os("_learn_more_ok_loc"))

    def is_learn_more_displayed(self):
        learn_more_title = self.find_element(self.get_locator_by_os("_learn_more_title_loc"))
        if learn_more_title is not None:
            return True
        else:
            return False




