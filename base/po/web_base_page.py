# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/6 12:36
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.remote.webdriver import WebDriver
from base.po.base_page import BasePage


class WebBasePage(BasePage):
    def __init__(self, driver: WebDriver):
        """
        Note: Must add this construction. If not, seem the one in BasePage isn't used either

        :param driver:
        """
        self.driver = driver