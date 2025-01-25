# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2025/1/25 16:49
desc:
'''
from appium.webdriver.common.appiumby import AppiumBy

from base.po.mobile_base_page import MobileBasePage


class AlertBasePage(MobileBasePage):
    _alert_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rcl_all')
    #_alert_loc_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeAlert')
    _alert_loc_ios = (AppiumBy.CLASS_NAME, 'XCUIElementTypeAlert')
    _ok_btn_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rtv_ok')
    _ok_btn_loc_ios = (AppiumBy.ACCESSIBILITY_ID,'OK')
    _cancel_btn_loc_ios = (AppiumBy.ACCESSIBILITY_ID, 'Cancel')
    _title_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_title')
    _title_loc_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[1]')

    def is_displayed(self):
        alert_box = self.find_element(self.get_locator_by_os("_alert_loc"))
        return alert_box is not None


    def get_title(self):
        title_element =  self.find_element(self.get_locator_by_os("_title_loc"))
        if title_element is not None:
            return title_element.text
        else:
            return ""


    def confirm(self):
        self.find_element_and_click(self.get_locator_by_os("_title_loc"))


    def cancel(self):
        self.find_element_and_click(self.get_locator_by_os("_cancel_btn_loc"))

