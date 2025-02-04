# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/2/3 9:29
# @Author : Olivia
# Desc:
# **************************************

import base.globalvars as glo
from playwright.sync_api import Page

class TriplogPWLoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator("#account_email")
        self.password_input = page.locator("#passwordTxt > input[type=password]")
        self.login_button = page.locator('//button[@type="submit" and @class="n_login-button"]')
        #self.error_message = page.locator(".error-message")


    # def navigate_to_login(self):
    #     self.page.goto(glo.get_value("url1"))
    #
    # def enter_username(self, username: str):
    #     self.email_input.fill(username)
    #
    # def enter_password(self, password: str):
    #     self.password_input.fill(password)
    #
    # def click_login(self):
    #     self.login_button.click()
    #
    # def get_error_message(self):
    #     return self.error_message.inner_text()

    def login(self, email, password):
        self.page.goto(glo.get_value("url1"))
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

        return self.page
