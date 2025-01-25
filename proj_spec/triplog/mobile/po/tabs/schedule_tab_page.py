# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2024/12/22 9:52
desc: 
'''
from appium.webdriver.common.appiumby import AppiumBy
from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage

class ScheduleTabPage(TabsBasePage):
    _progress_dialog_loc_ios = (AppiumBy.ACCESSIBILITY_ID, 'Loading work schedule. Please wait...')

