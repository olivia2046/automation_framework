# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/22 22:09
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage


class WorkSchedulePage(LeftNavBasePage):

    _title_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@text="Working Hours"]')
    _back_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/img_back"]')

    # def go_back(self):
    #
    #     pass

    # def get_title(self):
    #     pass