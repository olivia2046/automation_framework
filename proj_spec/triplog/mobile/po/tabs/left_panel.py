# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 22:14
# @Author : Olivia
# Desc:
# **************************************
import time

from appium.webdriver.common.appiumby import AppiumBy

from proj_spec.triplog.mobile.po.alert.last_parked_alert_page import LastParkedAlertPage
from proj_spec.triplog.mobile.po.left_nav.account_page import AccountPage
from proj_spec.triplog.mobile.po.left_nav.auto_start_settings_page import AutoStartSettingsPage
from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class LeftPanel(TriplogMobileBasePage):
    menu_title_mapping_android = {"Auto Start on":"Auto Start Settings","Auto Start On":"Auto Start Settings","Work Schedule":"Working Hours",
                          "Navigate/Route Planning":"Route Planning","Adjust Odometer":"Adjust Vehicle Odometer"}
    menu_title_mapping_ios = {"Auto Start On": "Auto Start Settings", "Navigate/Route Planning": "Route Planning",
                                  "Adjust Vehicle Odometer": "Choose Vehicle to Adjust Odometer","Business Activities":"Activities"}

    _adv_feature_switch_android = (AppiumBy.ID,'com.bizlog.triplog:id/switch_btn')
    _adv_feature_switch_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeOther[`name == "Show advanced features"`]/XCUIElementTypeSwitch')
    _left_panel_loc_android = (AppiumBy.ID,'com.bizlog.triplog:id/nsv_drawer')
    _left_panel_loc_ios= (AppiumBy.ACCESSIBILITY_ID, 'Toolbar')
    _account_status_loc_android= (AppiumBy.ID, 'com.bizlog.triplog:id/tv_account_status_info')
    _account_status_loc_ios = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_account_status_info')
    _account_email_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_account_email')
    # ios locate by accessiblity id of account's email

    _chevron_loc_ios = (AppiumBy.ACCESSIBILITY_ID, 'chevron')
    # todo: replace the loc on android
    _account_bar_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/cl_account_msg')
    _account_bar_loc_ios = (AppiumBy.XPATH,'//XCUIElementTypeButton[@name="chevron"]/..')

    def switch_advanced_features(self):
        #self.find_element_and_click(self.get_locator_by_os("_adv_feature_switch"))
        switch_element = self.find_element(self.get_locator_by_os("_adv_feature_switch"), condition="element_to_be_clickable")
        #switch_element.screenshot("switch.png")
        if switch_element is not None:
            switch_element.click()

    def get_menu_locator(self,menu_text):
        """

        :param menu_text:
        :param os_type:
        :return:
        """
        if self.os=='android':
            return (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_title" and @text="%s"]/../..'
                    %menu_text) # only parent of parent element clickable
        else:
            return (AppiumBy.ACCESSIBILITY_ID, menu_text)


    def goto_account_page(self):
        self.find_element_and_click(self.get_locator_by_os("_account_email_loc"))
        return AccountPage(self.driver)


    def is_advanced_switch_checked(self):
        advanced_switch = self.find_element(self.get_locator_by_os("_adv_feature_switch"))
        if advanced_switch is None:
            return False
        else:
            if self.os=='android':
                """Only the following attributes are supported: [checkable, checked, {class,className}, clickable, 
                {content-desc,contentDescription}, enabled, focusable, focused, {long-clickable,longClickable}, package, 
                password, {resource-id,resourceId}, scrollable, selection-start, selection-end, selected, {text,name}, hint, 
                extras, bounds, displayed, contentSize]"""
                return advanced_switch.get_attribute("checked")=='true'
            else:
                return advanced_switch.get_attribute("value")=='1'


    def is_left_menu_accessible(self,menu_name):
        """
        Todo: handle page loading of Approval Management. Currrent workaround: put Approval Manangement to the last case
        :param menu_name:
        :return:
        """


        if (menu_name in ('Navigate/Route Planning','Frequent Trip Rules','Adjust Odometer','Business Activities',
                          'Last Known Parking','Banks & Credit Cards','Invite Accountant')):
            advanced_switch = self.find_element(self.get_locator_by_os("_adv_feature_switch"))
            # if advanced_switch is None:
            #     return False

            # todo: is_selected() on android?
            if advanced_switch is not None and not self.is_advanced_switch_checked():
                self.switch_advanced_features()
                # scroll up the left pane
                self.swipe_up(self.get_locator_by_os("_left_panel_loc"), 0.5)

        # todo: if expected to have menu but actually not, need to handle exception to swipe the left panel off
        try:
            if menu_name in ('Last Known Parking','Banks & Credit Cards'):
                # do not click
                if self.find_element(self.get_menu_locator("%s" % menu_name)) is None:
                    accessibility = False
                else:
                    accessibility = True

                # todo: click menu and handle pop up/long loading page
                self.swipe_left(self.get_locator_by_os("_left_panel_loc"), horizontal_rate=1)
                return accessibility
            #todo: uniform ios/android menu name?
            if menu_name=='Auto Start on' and self.os=='ios':
                menu_name='Auto Start On'
            elif menu_name=='Adjust Odometer' and self.os=='ios':
                menu_name='Adjust Vehicle Odometer'
            menu_element = self.find_element(self.get_menu_locator("%s"%menu_name),condition="element_to_be_clickable")
            if menu_element is None:
                return False
            else:
                menu_element.click()

            auto_start_options_displayed = False
            if menu_name in ('Auto Start on','Auto Start On'):
                from proj_spec.triplog.mobile.po.left_nav.auto_start_options_page import AutoStartOptionsPage
                page = AutoStartOptionsPage(self.driver)
                if page.is_learn_more_displayed():
                    auto_start_options_displayed = True
                    page.confirm_learn_more()
                else:
                    page = AutoStartSettingsPage(self.driver)
                #     #auto_start_options_page.go_back()
            elif menu_name=='Work Schedule':
                from proj_spec.triplog.mobile.po.left_nav.work_schedule_page import WorkSchedulePage
                page = WorkSchedulePage(self.driver)
            elif menu_name=='Approval Management':
                from proj_spec.triplog.mobile.po.left_nav.approval_mgmt_page import ApprovalMgmtPage
                page = ApprovalMgmtPage(self.driver)
                while 'loading' in page.get_title():
                    time.sleep(3)
            elif menu_name=='Navigate/Route Planning':
                from proj_spec.triplog.mobile.po.left_nav.route_planning_page import RoutePlanningPage
                page = RoutePlanningPage(self.driver)
            elif menu_name in ('Adjust Odometer','Adjust Vehicle Odometer'):
                from proj_spec.triplog.mobile.po.left_nav.adjust_odometer_page import AdjustOdometerPage
                page = AdjustOdometerPage(self.driver)
                # if page.is_odometer_reading_popup():
                #     page.set_odometer(999999)
            else:
                from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage
                page = LeftNavBasePage(self.driver)

            if auto_start_options_displayed:
                expected_title = "Auto Start Options"
            elif menu_name in eval("self.menu_title_mapping_"+self.os).keys():
                expected_title = eval("self.menu_title_mapping_"+self.os)[menu_name]
            # elif menu_name == "Business Activities" and self.os=='ios':
            #     expected_title = 'Activities'
            elif menu_name == "Last Know Parking":
                alert_displayed = page.alert.is_displayed()
                if alert_displayed and 'Enable a GPS Tracking Method' in page.alert.get_title():
                    page.alert.confirm()
                elif alert_displayed and 'Last Parked' in page.alert.get_title():
                    page.alert.cancel()
                return True
            else:
                expected_title = menu_name
            if self.os=='android':
                title = page.get_title()
                accessibility =  (title=='%s'%expected_title)
            else: # todo: ios need to add accessibility id to title element
                accessibility = self.find_element((AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "%s"`]'%expected_title)) is not None
            page.go_back()

            return accessibility
        except Exception as e:
            # collapse the left panel
            self.swipe_left(self.get_locator_by_os("_left_panel_loc"),horizontal_rate=1)
            return False



    def is_submission_accessible(self):

        from proj_spec.triplog.mobile.po.tabs.submission_tab_page import SubmissionTabPage

        self.find_element_and_click(self.get_menu_locator("Submission"))
        page = SubmissionTabPage(self.driver)
        return page.get_title()=='Submission'



    # def is_locations_accessible(self):
    #     self.find_element_and_click(self.get_locator("_locations_loc"))
    #     locations_page =


    def goto_account_page(self):
        self.find_element_and_click(self.get_locator_by_os("_account_bar_loc"))
        return AccountPage(self.driver)