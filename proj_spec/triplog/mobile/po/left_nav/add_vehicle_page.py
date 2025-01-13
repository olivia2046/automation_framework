# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/13 20:44
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage


class AddVehiclePage(LeftNavBasePage):
    _model_input_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/txt_vehicle_model')
    _save_btn_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_action')


    def add_vehicle(self, **kwargs):
        if 'model' in kwargs.keys():
            self.find_element_and_input(self.get_locator_by_os("_model_input_loc"), kwargs['model'])

        self.find_element_and_click(self.get_locator_by_os("_save_btn_loc"))



