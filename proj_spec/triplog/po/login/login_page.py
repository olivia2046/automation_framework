# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/5 9:13
# @Author : Olivia
# Desc:
# **************************************
from selenium import webdriver
from selenium.webdriver.common.by import By
from base.get_config import get_capabilities
import base.globalvars as glo
from proj_spec.triplog.po.dashboard.overview_page import OverviewPage
from proj_spec.triplog.po.triplog_base_page import TriplogBasePage


class TriplogLoginPage(TriplogBasePage):

    _email_locator = (By.ID, "account_email")
    _password_locator = (By.CSS_SELECTOR, "#passwordTxt > input[type=password]")
    _login_btn_locator = (By.CSS_SELECTOR,"#loginForm > div.n_login-row.n_login-row-border.n_login-btn-box > button")

    def __init__(self):
        caps = get_capabilities()
        browser_name = caps['browserName']
        if browser_name=='Chrome':
            self.driver = webdriver.Chrome()
            self.driver.get(glo.get_value("url1"))

    def login(self, email, password):

        self.find_element_and_input(self._email_locator, email)
        self.find_element_and_input(self._password_locator, password)
        self.find_element_and_click(self._login_btn_locator)

        return OverviewPage(self.driver)

