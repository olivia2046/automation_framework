# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:54
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.tabs.bottom_navigator import BottomNavigator
from proj_spec.triplog.mobile.po.tabs.left_panel import LeftPanel
from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class TabsBasePage(TriplogMobileBasePage):
    #_bottom_trips_loc_android =(AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_item_customize_btn_name" and @text="Trips"]')
    _left_panel_loc_android = (AppiumBy.ID,'com.bizlog.triplog:id/img_main_icon')
    _title_loc_android = (AppiumBy.ID,'com.bizlog.triplog:id/tv_main_title')
    _battery_popup_loc_android = (AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="com.bizlog.triplog:id/rcl_all"]')
    _battery_popup_confirm_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_ok"]')

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

    def get_title(self):
        return self.find_element(self.get_locator_by_os("_title_loc")).text

