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



class AppLoginPage(MobileBasePage):
    # permission
    _agree_btn_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_agree"]')

    _email_input_loc_android = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.bizlog.triplog:id/et_email"]')
    _pwd_input_loc_android = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.bizlog.triplog:id/et_pwd"]')
    _login_btn_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_login"]')
    _turn_on_time_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_time_tracking_ok"]')
    _save_time_mode_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_set_time_mode_save"]')
    _loading_data_loc_android = (AppiumBy.XPATH,'//android.view.ViewGroup[@resource-id="com.bizlog.triplog:id/rcl_all"]')

    # def agree_permission(self):
    #     self.find_element_and_click(self._agree_btn_loc)

    def login(self, email, password):
        from proj_spec.triplog.mobile.po.tabs.trips_tab_page import TripsTabPage
        from proj_spec.triplog.mobile.po.tabs.reports_tab_page import ReportsTabPage
        from proj_spec.triplog.mobile.po.tabs.submission_tab_page import SubmissionTabPage
        from proj_spec.triplog.mobile.po.tabs.transactions_tab_page import TransactionsTabPage

        self.find_element_and_click(self.get_locator_by_os("_agree_btn_loc"))
        self.find_element_and_input(self.get_locator_by_os("_email_input_loc"), email)
        self.find_element_and_input(self.get_locator_by_os("_pwd_input_loc"), password)
        self.find_element_and_click(self.get_locator_by_os("_login_btn_loc"))

        time.sleep(3)
        self.find_element(self.get_locator_by_os("_loading_data_loc"),condition="invisibility_of_element")

        try:
            self.find_element_and_click(self.get_locator_by_os("_turn_on_time_loc"),skip_error_handle=True)
            self.find_element_and_click(self.get_locator_by_os("_save_time_mode_loc"), skip_error_handle=True)
        except Exception as e:
            pass


        # if self.get_default_page()=="Trips":
        #     return TripsTabPage(self.driver)
        # elif self.get_default_page()=="Transactions":
        #     return TransactionsTabPage(self.driver)
        # elif self.get_default_page()=="Reports":
        #     return ReportsTabPage(self.driver)
        # elif self.get_default_page()=="Submission":
        #     return SubmissionTabPage(self.driver)
        # # elif self.get_default_page()=="Time":
        # #     return MobileTimePage()
        # else:
        #     return TripsTabPage(self.driver)
        from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage
        return TabsBasePage(self.driver)



    def get_default_page(self):
        title_loc_android = (AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_main_title"]')

        title=self.find_element(eval("title_loc_"+self.os)).text
        return title


