# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/23 13:17
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage


class BankAccountsPage(LeftNavBasePage):
    _title_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@text="Bank Accounts"]')
    _back_loc_android = (AppiumBy.ACCESSIBILITY_ID, 'updateSideBarCollapsed')

    pass