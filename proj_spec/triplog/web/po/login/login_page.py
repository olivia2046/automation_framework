# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/5 9:13
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By
#from base.get_config import get_capabilities

import base.globalvars as glo

from proj_spec.triplog.web.po.triplog_base_page import TriplogWebBasePage


class TriplogLoginPage(TriplogWebBasePage):

    _email_locator = (By.ID, "account_email")
    _password_locator = (By.CSS_SELECTOR, "#passwordTxt > input[type=password]")
    _login_btn_locator = (By.CSS_SELECTOR,"#loginForm > div.n_login-row.n_login-row-border.n_login-btn-box > button")

    def __init__(self,driver):
        #caps = get_capabilities()
        # from base.get_config import GetConfig
        # caps = GetConfig.get_capabilities()
        # browser_name = caps['browserName']
        # if browser_name=='Chrome':
        #     self.driver = webdriver.Chrome()
        # elif browser_name=='Firefox':
        #     self.driver = webdriver.Firefox()
        # elif browser_name=='Edge':
        #     self.driver = webdriver.Edge()
        self.driver=driver
        self.driver.get(glo.get_value("url1"))

    def login(self, email, password):
        from proj_spec.triplog.web.po.dashboard.overview_page import OverviewPage

        self.driver.maximize_window()

        self.find_element_and_input(self._email_locator, email)
        self.find_element_and_input(self._password_locator, password)
        self.find_element_and_click(self._login_btn_locator)
        #todo: wait for page to load completely
        return OverviewPage(self.driver)

