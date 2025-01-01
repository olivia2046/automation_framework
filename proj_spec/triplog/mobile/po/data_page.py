# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/25 12:51
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage

def DataPage(TriplogMobileBasePage):

    _sync_with_cloud_android = (AppiumBy.ID, 'com.bizlog.triplog:id/pn_data_sync') # only parent of parent clickable
