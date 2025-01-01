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
    _title_loc_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "Work Schedule"`][1]')
    _back_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/img_back')
    _back_loc_ios = (AppiumBy.IOS_PREDICATE, 'name == "Back" AND label == "Back" AND type == "XCUIElementTypeButton"')

    # def go_back(self):
    #
    #     pass

    # def get_title(self):
    #     pass