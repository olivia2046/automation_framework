# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2025/1/25 18:04
desc:
'''
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.alert.alert_base_page import AlertBasePage


class LastParkedAlertPage(AlertBasePage):
    _show_on_maps_loc_ios = (AppiumBy.ACCESSIBILITY_ID,'Show on Maps')


    def is_displayed(self):
        alert_box = self.find_element(self.get_locator_by_os("_alert_loc"))
        if alert_box is not None and 'Last Parked' in self.get_title():
            return True
        else:
            return False


    def show_on_maps(self):
        self.find_element_and_click(self.get_locator_by_os("_show_on_maps_loc"))



