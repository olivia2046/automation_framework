# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/2/3 10:03
# @Author : Olivia
# Desc:
# **************************************

import logging
from proj_spec.triplog.playwright.triplog_pw_base_page import TriplogPWBasePage
from playwright.sync_api import Page
import time
import base.globalvars as glo

class TripsPage(TriplogPWBasePage):

    def __init__(self, page: Page):
        self.page = page
        self.url = glo.get_value("url1") + "/trip"
        self.page.goto(self.url)
        self.add_trip_button = page.locator("#add_button")
        self.from_select = page.locator("#fromLocation\.id")
        self.to_select = page.locator("#toLocation\.id")
        self.query_distance_button = page.locator("input[type='button'][class='green_button'][value='Query Driving Distance']")
        self.create_button = page.locator("//input[@type='submit' and @value='Create' and not(@class='blue_button')]")
        self.count_container = page.locator('(//div[@class="small"])[1]')
        self.save_button = page.locator("//input[@type='button' and @ value='Create Return Trip']/preceding-sibling::input")
        self.confirm_delete_multiple = page.locator("//div[@id='delete_multiple_dialog']//input[@type='submit' and "
                                              "@class='red_border_button' and @value='Delete']")


    def choose_button(self, first_level_text, second_level_text):
        """

        :param first_level:
        :param second_level:
        :return:
        """
        triangle_down = self.page.locator("//div[@class='triangle_down' and text()='%s']"%first_level_text)
        button_link = self.page.locator("//a[text()='%s']"%second_level_text)

        triangle_down.hover()
        button_link.click()


    def get_number_of_trips_filtered(self):
        """

        :return:
        """
        self.page.goto(self.url)# page doesn't get refreshed after operations, so need to manually refresh to get latest count
        try:
            text = self.count_container.inner_text()
            count = int(text.split('\n /')[-1].strip().replace("nbsp;", ""))
            return count
        except Exception as e:
            logging.error("error getting count of filtered trips: %s" % e)
            return -1



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

    def get_nth_trip(self,n):
        """

        :param n:
        :return:
        """
        return self.page.locator("(//tr[contains(@id,'trip_row_')])[%s]"%(n+1))


    def get_nth_trip_checkbox(self, n):
        """

        :param n:
        :return:
        """
        return self.page.locator( "(//input[@class='selected_id'])[%s]"%(n+1))


    def edit_trip(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        # self.driver.get(self.url)
        # time.sleep(2)
        row_index=kwargs['row_index']
        # nth_trip_loc = (By.XPATH,"(%s)[%s]"%(self._trips_xpath,row_index+1)) #xpath index starts from 1
        # self.find_element_and_click(nth_trip_loc)
        self.get_nth_trip(row_index).click()

        if "from_location" in kwargs:
            self.page.select_option("#fromLocation\.id", label=kwargs['from_location'])
        if "to_location" in kwargs:
            self.page.select_option("#toLocation\.id", label=kwargs['to_location'])

        if "query_distance" in kwargs and kwargs["query_distance"] is True:
            self.query_distance_button.click()
            dialog = self.page.wait_for_event("dialog")
            dialog.accept()

        self.save_button.click()


    def delete_trip(self, index=0):
        """Delete trip from menu bar

        :return:
        """
        #self.driver.get(self.url)
        self.get_nth_trip_checkbox(index).click()
        # nth_trip_checkbox_loc = (By.XPATH, "%s[%s]"%(self._trip_checkboxs_xpath,index+1)) #xpath starts from 1
        # self.find_element_and_click(nth_trip_checkbox_loc)
        self.choose_button("Delete","Delete Selected")
        self.confirm_delete_multiple.click()