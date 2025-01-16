# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:58
# @Author : Olivia
# Desc:
# **************************************
import logging

from appium.webdriver.common.appiumby import AppiumBy

from base.po.mobile_base_page import MobileBasePage


class TriplogMobileBasePage(MobileBasePage):
    activity_page_mapping = {
        "com.esocialllc.triplog.module.setting.SettingTimeRuleActivity":"WorkSchedulePage",
        "com.esocialllc.triplog.module.connectbank.ConnectBankActivity":"BankAccountsPage",
        "com.esocialllc.triplog.tutorial.AutoStartSettingActivity":"Auto Start on"

    }

    _toolbar_loc_ios = (AppiumBy.IOS_PREDICATE,'name == "Toolbar"') # left panel, **/XCUIElementTypeToolbar[`name == "Toolbar"`]
    _navbar_loc_ios = (AppiumBy.IOS_CLASS_CHAIN,'**/XCUIElementTypeNavigationBar') # head bar of page, use for defining which page is current page
    _bottom_menu_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rl_main_bottom_menu')


    _msg_box_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rcl_all')
    _msg_box_title_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_title')
    _msg_box_ok_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rtv_ok')
    _msg_box_continue_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rtv_continue')
    _msg_box_cancel_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rtv_cancel')
    _progress_dialog_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rcl_all') # same as message box

    # send report window when error
    _send_report_file_loc_android = (AppiumBy.ID, 'android:id/content_preview_filename')

    def find_element(self, locator, timeout=5, condition='visibility_of_element_located', skip_error_handle=False):
        """

        :param locator:
        :param timeout:
        :param condition:
        :param skip_error_handle:
        :return:
        """
        return super().find_element(locator,timeout,condition)
        # todo: add error handling of report log window

    def get_title(self):
        title_elemenet = self.find_element(self.get_locator_by_os("_msg_box_title"))
        if title_elemenet is not None:
            return title_elemenet.text
        else:
            return ""


    def confirm_msg_box(self):
        """

        :return:
        """

        self.find_element_and_click(self.get_locator_by_os("_msg_box_ok"))


    def continue_msg_box(self):
        """

        :return:
        """

        self.find_element_and_click(self.get_locator_by_os("_msg_box_continue"))


    def cancel_msg_box(self):
        """

        :return:
        """

        self.find_element_and_click(self.get_locator_by_os("_msg_box_cancel"))


    def is_msgbox_poped_up(self):
        """whether there is a message box poped up

        :return:
        """
        msgbox_element = self.find_element(self.get_locator_by_os("_msg_box_loc"))
        return msgbox_element is not None


    def get_current_page(self):
        if self.os=='android': #use activity
            current_activity = self.driver.current_activity
            logging.info("current activity: %s"%current_activity)
            if current_activity in self.activity_page_mapping.keys():
                return eval("%s(self.driver)"%self.activity_page_mapping[current_activity])
            elif self.find_element(self.get_locator_by_os("_bottom_menu_loc")) is not None: # tab page
                from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage
                return TabsBasePage(self.driver)
            else:
                from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage
                return LeftNavBasePage(self.driver)

        else: #use hiarchy
            pass


    def wait_for_loading_finish(self):
        """wait for the progress dialog to finish loading

        :return:
        """
        loading_dialog = self.find_element(self.get_locator_by_os("_progress_dialog_loc"))
        if loading_dialog is not None:
            self.find_element(self.get_locator_by_os("_progress_dialog_loc"), condition="invisibility_of_element")


    def logout(self):
        # get current concrete page and use its logout method to sign out
        concrete_page = self.get_current_page()
        concrete_page.logout()