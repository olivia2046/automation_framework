# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/2/3 9:27
# @Author : Olivia
# Desc:
# **************************************
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="class",autouse=True)
def page(request,get_login_info):
    from base.get_config import GetConfig
    caps = GetConfig.get_capabilities()
    browser_name = caps['browserName']

    with sync_playwright() as p:
        if browser_name=='Chrome':
            browser = p.chromium.launch(channel="chrome", headless=False, args=["--start-maximized"])
        # elif browser_name=='Firefox':
        #     driver = webdriver.Firefox()
        # elif browser_name=='Edge':
        #     driver = webdriver.Edge()
        # elif browser_name=='Safari':
        #     driver = webdriver.Safari()

        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        # screen_width = page.evaluate("window.screen.width")
        # screen_height = page.evaluate("window.screen.height")
        # page.set_viewport_size({"width": screen_width, "height": screen_height})
        #request.cls.driver = driver
        from proj_spec.triplog.playwright.login.login import TriplogPWLoginPage
        login_page = TriplogPWLoginPage(page)
        if request.cls.user_identifier is not None:
            #email, password = GetData.get_user_credential(request.cls.user_identifier)
            email, password = get_login_info
            request.cls.default_page = login_page.login(email, password)
        yield
        browser.close()


def pytest_collection_modifyitems(config, items):
    # skip parent test class
    items[:] = [item for item in items if "Base" not in item.nodeid]


