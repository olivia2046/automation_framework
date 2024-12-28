# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2024/12/28 14:28
desc: 
'''
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage


class AdjustOdometerPage(LeftNavBasePage):
    _odometer_title_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_title"]')
    _confirm_btn_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_ok"]')

    def is_odometer_reading_popup(self):
        """check if the Current Odomeer Reading from Dashboard windows pops up

        :return:
        """
        popup = self.find_element(self.get_locator_by_os("_odometer_title"))
        if popup is not None and "Current Odometer Reading" in popup.text:
            return True
        else:
            return False

    def confirm_odometer_setting(self):
        self.find_element_and_click(self.get_locator_by_os("_confirm_btn"))
