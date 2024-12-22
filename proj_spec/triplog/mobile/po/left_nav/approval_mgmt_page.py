# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/22 22:17
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage


class ApprovalMgmtPage(LeftNavBasePage):
    _back_loc_android = (AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.bizlog.triplog:id/img_web_back"]')
    _title_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_web_title"]')
