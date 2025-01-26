# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 17:43
# @Author : Olivia
# Desc:
# **************************************
import logging

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from proj_spec.triplog.mobile.po.start.start_page import AppStartPage


# @pytest.fixture(scope="class",autouse=True)
# def driver_init(request,get_login_info):
#     from base.getdata import GetData
#     from base.get_config import GetConfig
#     caps = GetConfig.get_capabilities()
#
#     if 'platformName' in caps and caps['platformName'].lower() == 'android':
#         options = UiAutomator2Options().load_capabilities(caps)
#     else:
#         options = XCUITestOptions().load_capabilities(caps)
#     request.cls.driver = webdriver.Remote(GetConfig.get_cmd_executor(), options=options)
#     #request.cls.driver = webdriver
#
#     app_start_page = AppStartPage(request.cls.driver)
#     login_page = app_start_page.goto_login_page()
#
#     if request.cls.user_identifier is not None:
#         #email, password = GetData.get_user_credential(request.cls.user_identifier)
#         email, password = get_login_info
#         request.cls.page = login_page.login(email, password)
#     yield
#     request.cls.driver.quit()

def _init_driver():
    from base.get_config import GetConfig
    caps = GetConfig.get_capabilities()

    if 'platformName' in caps and caps['platformName'].lower() == 'android':
        options = UiAutomator2Options().load_capabilities(caps)
    else:
        options = XCUITestOptions().load_capabilities(caps)

    driver = webdriver.Remote(GetConfig.get_cmd_executor(), options=options)
    return driver

# Fixture: 初始化 WebDriver（session scope）
@pytest.fixture(scope="class", autouse=True)
def init_driver():

    from base.get_config import GetConfig
    caps = GetConfig.get_capabilities()

    if 'platformName' in caps and caps['platformName'].lower() == 'android':
        options = UiAutomator2Options().load_capabilities(caps)
    else:
        options = XCUITestOptions().load_capabilities(caps)

    # 初始化 WebDriver
    driver = webdriver.Remote(GetConfig.get_cmd_executor(), options=options)

    yield driver

    #logging.info("app state:%s"%driver.query_app_state(caps['appium:appPackage']))
    try:
        # 退出 WebDriver
        driver.quit()
    except Exception as e:
        logging.error(e)


# Fixture: 每个测试类的登录操作（class scope）
@pytest.fixture(scope="class", autouse=True)
def class_setup(request, init_driver, get_login_info):
    """fixture of class level, used for login and inistialize test class properties

    :param request:
    :param init_driver:
    :param get_login_info:
    :return:
    """

    try:

        request.cls.driver  = init_driver  # 从 session 级别的 fixture 获取共享的 WebDriver


        # 进入登录页并登录
        app_start_page = AppStartPage(request.cls.driver)
        # IOS上若已登录需手动登出
        if request.cls.driver.capabilities['platformName']=='ios' and not app_start_page.is_login_btn_displayed():
            from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage
            current_page = TabsBasePage(request.cls.driver)
            current_page.handle_current_pages()
            current_page.logout()

            request.cls.driver = _init_driver()
            app_start_page = AppStartPage(request.cls.driver)
            init_driver=request.cls.driver

        login_page = app_start_page.goto_login_page()

        # get login information and login
        if request.cls.user_identifier is not None:
            email, password = get_login_info
            login_result = login_page.login(email, password)
            if login_result is not None:
                request.cls.page = login_result
            else:

                raise Exception("Login failed")


    except Exception as e:
        logging.error(f"Login failed for {request.cls.__name__}: {e}")

        # 跳过当前测试类并重启应用
        pytest.fail(f"Skipping {request.cls.__name__} due to login failure")
        #request.cls.reset()  # 重启APP，确保下一测试类从干净的状态开始
        request.cls.driver.quit()

    # from base.get_config import GetConfig
    # caps = GetConfig.get_capabilities()
    # logging.info("app state:%s" % request.cls.driver.query_app_state(caps['appium:appPackage'])) #only applies to android
    yield request.cls.driver  # execute test case


    # logout logic
    if hasattr(request.cls.page, "logout"):
        request.cls.page.logout()

    #logging.info("app state:%s" % request.cls.driver.query_app_state(caps['appium:appPackage']))