# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2024/12/31 08:32
desc:
'''
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage


class LastKnowParkingPage(LeftNavBasePage):
    _precondition_popup_title_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_title') #text: Enable a GPS Tracking Method to Access Last Known Parking
    _precondition_popup_ok_android = (AppiumBy.ID, 'com.bizlog.triplog:id/rtv_ok') # text: OK

    _last_parked_title_ios = (AppiumBy.IOS_CLASS_CHAIN,'**/XCUIElementTypeStaticText[`name == "Last Parked"`]')
    _show_on_maps_ios = (AppiumBy.ACCESSIBILITY_ID, 'Show on Maps')
    _cancel_btn_ios = (AppiumBy.ACCESSIBILITY_ID, 'Cancel')
    