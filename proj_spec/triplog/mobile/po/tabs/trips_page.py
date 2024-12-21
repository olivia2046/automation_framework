# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:53
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage


class MobileTripsPage(TabsBasePage):
    _title_loc_android = (AppiumBy,'//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_main_title"]')

    def get_title(self):
        return self.find_element(self.get_locator_by_os("_title_loc")).text


