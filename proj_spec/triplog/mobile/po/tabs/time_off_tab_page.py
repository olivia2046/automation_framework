# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2024/12/22 9:52
desc: 
'''
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage

class TimeOffTabPage(TabsBasePage):
    _title_loc_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "Time off"`][1]')
