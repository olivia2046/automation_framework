# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 18:11
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from base.po.mobile_base_page import MobileBasePage
from proj_spec.triplog.mobile.start.login_page import AppLoginPage


class AppStartPage(MobileBasePage):
    _login_btn_loc = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_login"]')

    def goto_login_page(self):
        self.find_element_and_click(self._login_btn_loc)
        return AppLoginPage(self.driver)