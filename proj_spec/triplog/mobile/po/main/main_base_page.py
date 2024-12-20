# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:54
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class MobileMainBasePage(TriplogMobileBasePage):
    _bottom_trips_loc_android =(AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_item_customize_btn_name" and @text="Trips"]')

    pass