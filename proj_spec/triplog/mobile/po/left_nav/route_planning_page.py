# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2025/12/31 08:22
desc:
'''
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage


class RoutePlanningPage(LeftNavBasePage):
    _popup_title_loc_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "Introducing Route Planning"`]')

    _popup_confirm_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "OK"`]')
