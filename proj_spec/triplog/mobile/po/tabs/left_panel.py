# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 22:14
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy


from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class LeftPanel(TriplogMobileBasePage):


    _adv_feature_switch_android = (AppiumBy.XPATH,'//android.widget.Switch[@resource-id="com.bizlog.triplog:id/switch_btn"]')


    def switch_advanced_features(self):
        self.find_element_and_click(self.get_locator_by_os("adv_feature_switch"))

    def get_menu_locator(self,menu_text):
        """

        :param menu_text:
        :param os_type:
        :return:
        """
        if self.os=='android':
            return (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_title" and @text="%s"]/../..'
                    %menu_text) # only parent of parent element clickable


    def is_left_menu_accessible(self,menu_name):

        from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage

        self.find_element_and_click(self.get_menu_locator("%s"%menu_name))
        page = TabsBasePage(self.driver)
        return page.get_title()=='menu_name'


    def is_submission_accessible(self):

        from proj_spec.triplog.mobile.po.tabs.submission_tab_page import SubmissionTabPage

        self.find_element_and_click(self.get_menu_locator("Submission"))
        page = SubmissionTabPage(self.driver)
        return page.get_title()=='Submission'



    # def is_locations_accessible(self):
    #     self.find_element_and_click(self.get_locator("_locations_loc"))
    #     locations_page =


