# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/2/3 10:04
# @Author : Olivia
# Desc:
# **************************************
from playwright.sync_api import Page
class TriplogPWBasePage():
    def __init__(self, page: Page):
        self.page = page