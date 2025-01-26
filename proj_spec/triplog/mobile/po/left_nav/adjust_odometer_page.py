# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2024/12/28 14:28
desc: 
'''
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage


class AdjustOdometerPage(LeftNavBasePage):
    _odometer_title_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_title')
    _odometer_title_ios = (AppiumBy.XPATH, '//XCUIElementTypeNavigationBar/XCUIElementTypeStaticText[1]')
    _number_picker_android = (AppiumBy.ID, 'com.bizlog.triplog:id/txt_widget_numberpicker')
    _number_picker_ios = (AppiumBy.XPATH, '//XCUIElementTypeAlert//XCUIElementTypeCell//XCUIElementTypeTextField')
    _confirm_btn_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rtv_ok')
    _confirm_btn_ios = (AppiumBy.ACCESSIBILITY_ID, 'OK')

    def __init__(self, driver, reading=999999):
        super().__init__(driver)
        if self.is_odometer_reading_popup():
            self.set_odometer(reading)

    def is_odometer_reading_popup(self):
        """check if the Current Odomeer Reading from Dashboard windows pops up

        :return:
        """
        popup = self.find_element(self.get_locator_by_os("_odometer_title"))
        if popup is not None and "Current Odometer Reading" in popup.text:
            return True
        else:
            return False

    def set_odometer(self, number):
        self.find_element_and_input(self.get_locator_by_os("_number_picker"), str(number))
        self.find_element_and_click(self.get_locator_by_os("_confirm_btn"))
