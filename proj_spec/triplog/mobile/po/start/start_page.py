# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 18:11
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from base.po.mobile_base_page import MobileBasePage
from proj_spec.triplog.mobile.po.start.login_page import AppLoginPage
from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class AppStartPage(TriplogMobileBasePage):
    _login_btn_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_login"]')
    _login_btn_loc_ios = (AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="Log in"]')

    _backup_complete_title_loc_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "Backup Completed"`]')
    _backup_complete_ok_loc_ios = (AppiumBy.ACCESSIBILITY_ID, 'OK')


    def goto_login_page(self):
        self.find_element_and_click(self.get_locator_by_os("_login_btn_loc"))
        return AppLoginPage(self.driver)


    def is_login_btn_displayed(self):
        if self.find_element(self.get_locator_by_os("_login_btn_loc")) is not None:
            return True
        else:
            return False


    def get_backup_complete_title_loc(self):
        return self.get_locator_by_os("_backup_complete_title_loc")


    def confirm_backup_completion(self):
        self.find_element_and_click(self.get_locator_by_os("_backup_complete_ok_loc"))