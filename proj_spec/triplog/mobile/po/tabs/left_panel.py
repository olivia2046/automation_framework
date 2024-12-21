# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 22:14
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy


from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class LeftPanel(TriplogMobileBasePage):

    _locations_loc_android = (AppiumBy, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_title" and @text="Locations"]')
    _submission_loc_android = (AppiumBy, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_title" and @text="Submission"]')

    def get_menu_locator(self,menu_text):
        """

        :param menu_text:
        :param os_type:
        :return:
        """
        if self.os=='android':
            return (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_title" and @text="%s"]/../..'%menu_text)


    def is_submission_accessible(self):

        from proj_spec.triplog.mobile.po.tabs.submission_page import SubmissionPage

        self.find_element_and_click(self.get_menu_locator("Submission"))
        page = SubmissionPage(self.driver)
        return page.get_title()=='Submission'



    # def is_locations_accessible(self):
    #     self.find_element_and_click(self.get_locator("_locations_loc"))
    #     locations_page =


