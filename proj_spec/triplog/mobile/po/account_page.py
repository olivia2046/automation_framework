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
    _data_backup_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_action')

    def goto_data(self):
        """go to Data Backup Page

        :return:
        """
        self.find_element_and_click(self.get_locator_by_os("_data_backup_loc"))
        return DataPage(self.driver)
