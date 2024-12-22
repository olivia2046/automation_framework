# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 18:16
# @Author : Olivia
# Desc:
# **************************************
import os
import time

from appium.webdriver.common.appiumby import AppiumBy

from base.po.mobile_base_page import MobileBasePage
from proj_spec.triplog.mobile.po.tabs.trips_tab_page import TripsTabPage


class AppLoginPage(MobileBasePage):
    # permission
    _agree_btn_loc = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_agree"]')

    _email_input_loc = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.bizlog.triplog:id/et_email"]')
    _pwd_input_loc = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.bizlog.triplog:id/et_pwd"]')
    _login_btn_loc = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_login"]')

    # def agree_permission(self):
    #     self.find_element_and_click(self._agree_btn_loc)

    def login(self, email, password):
        self.find_element_and_click(self._agree_btn_loc)
        self.find_element_and_input(self._email_input_loc, email)
        self.find_element_and_input(self._pwd_input_loc, password)
        self.find_element_and_click(self._login_btn_loc)

        time.sleep(3)
        if self.get_default_page()=="Trips":
            return TripsTabPage(self.driver)
        # elif self.get_default_page()=="Reports":
        #     return MobileReportsPage()
        # elif self.get_default_page()=="Submission":
        #     return MobileSubmissionPage()
        # elif self.get_default_page()=="Time":
        #     return MobileTimePage()
        pass


    def get_default_page(self):
        title_loc_android = (AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_main_title"]')

        title=self.find_element(eval("title_loc_"+self.os)).text
        return title


