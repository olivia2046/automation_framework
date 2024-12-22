# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/21 11:23
# @Author : Olivia
# Desc:
# **************************************
import logging
from appium.webdriver.common.appiumby import AppiumBy


from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class BottomNavigator(TriplogMobileBasePage):
    _more_or_less_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_main_bottom_more"]')
    _more_or_less_parent_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_main_bottom_more"]/..')
    def get_tab_locator(self, tab_text):
        if self.os=='android':
            return (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_item_customize_btn_name" '
                                    'and @text="%s"]/..'%tab_text)  # only parent of parent element clickable

    def expand_more_or_less(self):
        element = self.find_element(self.get_locator_by_os("_more_or_less_loc"),condition="element_to_be_clickable")
        text = element.text
        if text=='More':
            # only parent element clickable
            self.find_element_and_click(self.get_locator_by_os("_more_or_less_parent_loc"),condition="element_to_be_clickable")


    def is_submission_accessible(self):
        from proj_spec.triplog.mobile.po.tabs.submission_page import SubmissionPage
        try:
            self.expand_more_or_less() #menus may have been reordered, so need to expand first
            self.find_element_and_click(self.get_tab_locator('Submission'))
            page = SubmissionPage(self.driver)

            return page.get_title()=='Submission'
        except Exception as e:
            logging.info("Exception accessing mobile bottom tab Submission")
            return False


    def is_reports_accessible(self):
        from proj_spec.triplog.mobile.po.tabs.reports_page import ReportsTabPage
        try:
            self.expand_more_or_less() #menus may have been reordered, so need to expand first
            self.find_element_and_click(self.get_tab_locator('Reports'))
            page = ReportsTabPage(self.driver)

            return page.get_title()=='Reports'
        except Exception as e:
            logging.info("Exception accessing mobile bottom tab Submission")
            return False
