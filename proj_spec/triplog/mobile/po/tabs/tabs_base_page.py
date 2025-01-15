# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:54
# @Author : Olivia
# Desc:
# **************************************
import time

from appium.webdriver.common.appiumby import AppiumBy
import base.globalvars as glo
from proj_spec.triplog.mobile.po.tabs.bottom_navigator import BottomNavigator
from proj_spec.triplog.mobile.po.tabs.left_panel import LeftPanel
from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class TabsBasePage(TriplogMobileBasePage):
    #_bottom_trips_loc_android =(AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_item_customize_btn_name" and @text="Trips"]')
    _left_panel_loc_android = (AppiumBy.ID,'com.bizlog.triplog:id/img_main_icon')
    _title_loc_android = (AppiumBy.ID,'com.bizlog.triplog:id/tv_main_title')
    _battery_popup_loc_android = (AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="com.bizlog.triplog:id/rcl_all"]')
    _battery_popup_confirm_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_ok"]')

    _track_method_popup_loc_android = (AppiumBy.ANDROID_UIAUTOMATOR, """new UiSelector().text("Choose how to track 
 your hours")""")  # there's CRLF among the text
    _opt_clock_inout_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rb_set_time_mode_1')
    _opt_duration_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rb_set_time_mode_2')
    _confirm_popup_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_set_time_mode_save')

    _schedule_popup_loc_android = (AppiumBy.ANDROID_UIAUTOMATOR, """new UiSelector().text("Shift Scheduling,
Job Dispatching")""")
    _close_popup_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_schedule_close')
    _remind_later_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_schedule_dismiss')





    def __init__(self,driver):
        super().__init__(driver)
        self.left_panel = LeftPanel(self.driver)
        self.bottom_nav = BottomNavigator(self.driver)




    # def cancel_battery_optimization(self):
    #
    #     # turn off battery optimization pop up
    #     battery_popup_confirm_btn = self.find_element(self.get_locator_by_os("_battery_popup_confirm"))
    #     if battery_popup_confirm_btn is not None:
    #         battery_popup_confirm_btn.click()




    def show_left_panel(self):
        self.find_element_and_click(self.get_locator_by_os("_left_panel_loc"))
        return LeftPanel(self.driver)

    def get_title(self):
        title_element = self.find_element(self.get_locator_by_os("_title_loc"))
        if title_element is not None:
            return title_element.text
        else:
            return ""


    def is_time_track_method_popup_displayed(self):
        """

        :return:
        """

        if self.find_element(self.get_locator_by_os("_track_method_popup_loc")) is not None:
            return True
        else:
            return False

    def choose_time_track_method(self, method="clock_in_out"):
        if method=="clock_in_out":
            self.find_element_and_click(self.get_locator_by_os("_opt_clock_inout_loc"))
        else:
            self.find_element_and_click(self.get_locator_by_os("_opt_duration_loc"))
        glo.set_value("time_track_method",method)
        self.find_element_and_click(self.get_locator_by_os('_confirm_popup_loc'))
        #time.sleep(5)
        self.wait_for_loading_finish()

    def is_schedule_popup_visible(self):
        return self.find_element(self.get_locator_by_os("_schedule_popup_loc")) is not None

    def close_schedule_popup(self):
        self.find_element_and_click(self.get_locator_by_os("_close_popup_loc"))
        # loading_dialog = self.find_element(self.get_locator_by_os("_loading_dialog_loc"))
        # if loading_dialog is not None:
        #     self.find_element(self.get_locator_by_os("_loading_dialog_loc"), condition="invisibility_of_element")
        self.wait_for_loading_finish()


    def logout(self):
        left_panel = self.show_left_panel()
        account_page = left_panel.goto_account_page()
        account_page.sign_out()
