# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 21:58
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from base.po.mobile_base_page import MobileBasePage


class TriplogMobileBasePage(MobileBasePage):

    _msg_box_loc_android = (AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="com.bizlog.triplog:id/rcl_all"]')
    _msg_box_title_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_title"]')
    _msg_box_ok_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_ok"]')
    _msg_box_continue_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_continue"]')
    _msg_box_cancel_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_cancel"]')

    def get_title(self):
        title_elemenet = self.find_element(self.get_locator_by_os("_msg_box_title"))
        if title_elemenet is not None:
            return title_elemenet.text
        else:
            return ""


    def confirm_msg_box(self):
        """

        :return:
        """

        self.find_element_and_click(self.get_locator_by_os("_msg_box_ok"))


    def continue_msg_box(self):
        """

        :return:
        """

        self.find_element_and_click(self.get_locator_by_os("_msg_box_continue"))


    def cancel_msg_box(self):
        """

        :return:
        """

        self.find_element_and_click(self.get_locator_by_os("_msg_box_cancel"))


    def is_msgbox_poped_up(self):
        """whether there is a message box poped up

        :return:
        """
        msgbox_element = self.find_element(self.get_locator_by_os("_msg_box_loc"))
        return msgbox_element is not None
