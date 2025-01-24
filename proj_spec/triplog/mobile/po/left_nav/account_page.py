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
    _sign_out_loc_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "Sign out"`]')
    # Sign Out
    # Continue: com.bizlog.triplog:id/rtv_ok
    # Cancel: com.bizlog.triplog:id/rtv_continue
    # Sync current account data: com.bizlog.triplog:id/rcl_all
    _data_backup_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_action')
    _data_backup_loc_ios = (AppiumBy.ACCESSIBILITY_ID, 'Data Backup')

    _msg_ok_loc_ios = (AppiumBy.ACCESSIBILITY_ID, 'Continue')
    _progress_dialog_loc_ios = (AppiumBy.XPATH, '//XCUIElementTypeOther[contains(@name,"Backing up data")]')


    # #_continue_signout_loc_android = super().get_locator_by_os("_msg_ok_loc")
    # _continue_signout_loc_ios = (AppiumBy.ACCESSIBILITY_ID, 'Continue')


    #
    # def __init__(self, driver):
    #     super().__init__(driver)
    #     if self.os=='android':
    #         self._continue_signout_loc_android = super().get_locator_by_os("_msg_ok_loc")


    def goto_data(self):
        """go to Data Backup Page

        :return:
        """
        self.find_element_and_click(self.get_locator_by_os("_data_backup_loc"))
        return DataPage(self.driver)


    def wait_for_loading_finish(self):
        """# override parent method, as on ios the locator is different

        :return:
        """
        if self.os=='android':
            super().wait_for_loading_finish()
        else:
            loading_dialog = self.find_element(self.get_locator_by_os("_progress_dialog_loc"))
            if loading_dialog is not None:
                self.find_element(self.get_locator_by_os("_progress_dialog_loc"), condition="invisibility_of_element",timeout=30)



    def sign_out(self):
        """

        :return:
        """
        from proj_spec.triplog.mobile.po.start.start_page import AppStartPage

        self.find_element_and_click(self.get_locator_by_os("_sign_out_loc"))
        popup_msgbox = self.find_element(self.get_locator_by_os("_msg_box_loc"))
        if popup_msgbox is not None:
            self.find_element_and_click(self.get_locator_by_os("_msg_ok_loc"))
            self.wait_for_loading_finish()
        app_page = AppStartPage(self.driver)
        if self.os=='ios':
            backup_complete_title = self.find_element(app_page.get_backup_complete_title_loc())
            if backup_complete_title is not None:
                app_page.confirm_backup_completion()
        return app_page
