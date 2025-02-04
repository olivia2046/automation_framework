# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/2/3 10:03
# @Author : Olivia
# Desc:
# **************************************

from proj_spec.triplog.playwright.triplog_pw_base_page import TriplogPWBasePage
from playwright.sync_api import Page
import time
import base.globalvars as glo

class TripsPage(TriplogPWBasePage):
    def __init__(self, page: Page):
        self.page = page
        self.page.goto(glo.get_value("url1")+"/trip")
        self.add_trip_button = page.locator("#add_button")
        self.from_select = page.locator("#fromLocation\.id")
        self.to_select = page.locator("#toLocation\.id")
        self.query_distance_button = page.locator("input[type='button'][class='green_button'][value='Query Driving Distance']")
        self.create_button = page.locator("//input[@type='submit' and @value='Create' and not(@class='blue_button')]")


    def add_trip(self, from_location, to_location, query_distance=False ):
        def handle_alert(dialog):
            print(f"弹窗消息: {dialog.message}")
            dialog.accept()  # 点击“确定”按钮

        self.add_trip_button.click()
        self.page.select_option("#fromLocation\.id", label=from_location)
        self.page.select_option("#toLocation\.id", label=to_location)


        if query_distance:
            # 监听弹窗事件
            #self.page.on("dialog", handle_alert) # alert will be automatically triggered without clicking query distance
            #self.page.on("dialog", lambda dialog: dialog.accept())
            self.query_distance_button.click()
            dialog = self.page.wait_for_event("dialog")
            dialog.accept()

            #time.sleep(3)


        self.create_button.click()


