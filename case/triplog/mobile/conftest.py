# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 17:43
# @Author : Olivia
# Desc:
# **************************************

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from proj_spec.triplog.mobile.po.start.start_page import AppStartPage


@pytest.fixture(scope="class",autouse=True)
def driver_init(request,get_login_info):
    from base.getdata import GetData
    from base.get_config import GetConfig
    caps = GetConfig.get_capabilities()
    from base.get_config import GetConfig
    caps = GetConfig.get_capabilities()

    if 'platformName' in caps and caps['platformName'].lower() == 'android':
        options = UiAutomator2Options().load_capabilities(caps)
    else:
        options = XCUITestOptions().load_capabilities(caps)
    request.cls.driver = webdriver.Remote(GetConfig.get_cmd_executor(), options=options)

    app_start_page = AppStartPage(request.cls.driver)
    login_page = app_start_page.goto_login_page()

    if request.cls.user_identifier is not None:
        #email, password = GetData.get_user_credential(request.cls.user_identifier)
        email, password = get_login_info
        request.cls.page = login_page.login(email, password)
    yield
    request.cls.driver.quit()


