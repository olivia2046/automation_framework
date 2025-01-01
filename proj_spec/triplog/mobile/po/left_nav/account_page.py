# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/25 12:51
# @Author : Olivia
# Desc:
# **************************************
from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.data_page import DataPage
from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class AccountPage(TriplogMobileBasePage):
    _sign_out_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_switch_account')
    # Sign Out
    # Continue: com.bizlog.triplog:id/rtv_ok
    # Cancel: com.bizlog.triplog:id/rtv_continue
    # Sync current account data: com.bizlog.triplog:id/rcl_all
    _data_backup_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_action')

    def goto_data(self):
        """go to Data Backup Page

        :return:
        """
        self.find_element_and_click(self.get_locator_by_os("_data_backup_loc"))
        return DataPage(self.driver)


    def sign_out(self):
        """

        :return:
        """
        from proj_spec.triplog.mobile.po.start.start_page import AppStartPage

        self.find_element_and_click(self.get_locator_by_os("_sign_out_loc"))
        popup_msgbox = self.find_element(self.get_locator_by_os("_msg_box_loc"))
        if popup_msgbox is not None:
            self.find_element_and_click(self.get_locator_by_os("_msg_box_ok"))
            return AppStartPage(self.driver)
        else:
            return self