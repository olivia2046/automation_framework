# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 18:16
# @Author : Olivia
# Desc: todo: batteray
# **************************************
import os
import time

from appium.webdriver.common.appiumby import AppiumBy
from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class AppLoginPage(TriplogMobileBasePage):
    # permission
    _agree_btn_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_agree"]')

    _email_input_loc_android = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.bizlog.triplog:id/et_email"]')
    _email_input_loc_ios = (AppiumBy.XPATH, '//XCUIElementTypeTextField[@value="Email"]')
    _pwd_input_loc_android = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.bizlog.triplog:id/et_pwd"]')
    _pwd_input_loc_ios = (AppiumBy.XPATH, '//XCUIElementTypeSecureTextField[@value="Password"]')
    _login_btn_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/rtv_login"]')
    _login_btn_loc_ios = (AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="Sign in"]')

    _turn_on_time_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_time_tracking_ok"]')
    _save_time_mode_loc_android = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_set_time_mode_save"]')

    _loading_data_loc_android = (AppiumBy.XPATH,'//android.view.ViewGroup[@resource-id="com.bizlog.triplog:id/rcl_all"]')
    _loading_data_loc_ios = (AppiumBy.XPATH, '//XCUIElementTypeOther[@name="Please wait..."]')



    # def agree_permission(self):
    #     self.find_element_and_click(self._agree_btn_loc)

    def login(self, email, password):
        if self.os=='android': # phone os
            # cancel battery optimization, to prevent pop up
            import os
            from base.get_config import GetConfig
            # 要取消电池优化的包名
            package_name = self.driver.capabilities['appPackage']
            if os.name=='nt': # computer os
                find_str_cmd = "findstr"
            else:
                find_str_cmd = "grep"

            # 检查应用的电池优化状态
            os.system(f"adb shell dumpsys deviceidle whitelist | %s %s"%(find_str_cmd, package_name))

            # 添加到电池优化白名单
            os.system(f"adb shell dumpsys deviceidle whitelist +%s"%package_name)

            # 确认操作成功
            os.system(f"adb shell dumpsys deviceidle whitelist | %s %s"%(find_str_cmd, package_name))

        if self.os=='android': # todo: ios上没有Permission页？ 还是因为noreset=True?
            self.find_element_and_click(self.get_locator_by_os("_agree_btn_loc"))
        self.find_element_and_input(self.get_locator_by_os("_email_input_loc"), email)
        self.find_element_and_input(self.get_locator_by_os("_pwd_input_loc"), password)
        self.find_element_and_click(self.get_locator_by_os("_login_btn_loc"))

        time.sleep(3)
        self.find_element(self.get_locator_by_os("_loading_data_loc"),condition="invisibility_of_element")

        try:
            self.find_element_and_click(self.get_locator_by_os("_turn_on_time_loc"),skip_error_handle=True)
            self.find_element_and_click(self.get_locator_by_os("_save_time_mode_loc"), skip_error_handle=True)
        except Exception as e:
            pass


        # if self.get_default_page()=="Trips":
        #     return TripsTabPage(self.driver)
        # elif self.get_default_page()=="Transactions":
        #     return TransactionsTabPage(self.driver)
        # elif self.get_default_page()=="Reports":
        #     return ReportsTabPage(self.driver)
        # elif self.get_default_page()=="Submission":
        #     return SubmissionTabPage(self.driver)
        # # elif self.get_default_page()=="Time":
        # #     return MobileTimePage()
        # else:
        #     return TripsTabPage(self.driver)
        from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage
        tab_page = TabsBasePage(self.driver)

        return tab_page



    def get_default_page(self):
        title_loc_android = (AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_main_title"]')

        title=self.find_element(eval("title_loc_"+self.os)).text
        return title


