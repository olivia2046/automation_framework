# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/25 12:51
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage

def DataPage(TriplogMobileBasePage):

    _sync_with_cloud_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_title" '
        'and @text="Sync Data between Device and Cloud"]') # only parent of parent clickable
