# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 22:14
# @Author : Olivia
# Desc:
# **************************************
import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class LeftPanel(TriplogMobileBasePage):
    menu_title_mapping = {"Auto Start on":"Auto Start Settings","Work Schedule":"Working Hours",
                          "Navigate/Route Planning":"Route Planning","Adjust Odometer":"Adjust Vehicle Odometer"}

    _adv_feature_switch_android = (AppiumBy.XPATH,'//android.widget.Switch[@resource-id="com.bizlog.triplog:id/switch_btn"]')
    _left_panel_loc_android = (AppiumBy.XPATH,'//android.widget.LinearLayout[@resource-id="com.bizlog.triplog:id/ll_drawer"]')


    def switch_advanced_features(self):
        self.find_element_and_click(self.get_locator_by_os("_adv_feature_switch"))

    def get_menu_locator(self,menu_text):
        """

        :param menu_text:
        :param os_type:
        :return:
        """
        if self.os=='android':
            return (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_title" and @text="%s"]/../..'
                    %menu_text) # only parent of parent element clickable


    def collapse_left_panel(self):
        """

        :return:
        """



#     def scroll_up_panel(self):
#         """
#         from selenium.webdriver import ActionChains
# from selenium.webdriver.common.actions import interaction
# from selenium.webdriver.common.actions.action_builder import ActionBuilder
# from selenium.webdriver.common.actions.pointer_input import PointerInput
#
# actions = ActionChains(driver)
# # override as 'touch' pointer action
# actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
# actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
# actions.w3c_actions.pointer_action.pointer_down()
# actions.w3c_actions.pointer_action.pause(2)
# actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
# actions.w3c_actions.pointer_action.release()
# actions.perform()
#         :return:
#         """
#
#         pass
#         # # 定位菜单 panel
#         # panel = driver.find_element(By.ID, "panel_id")
#         #
#         # # 初始化 TouchAction
#         # action = TouchAction(driver)
#         #
#         # # 滑动 panel，直到目标菜单项可见
#         # while True:
#         #     try:
#         #         # 尝试查找目标菜单项
#         #         target_item = panel.find_element(By.XPATH, "//android.widget.TextView[@text='Target Menu']")
#         #         if target_item.is_displayed():
#         #             print("目标菜单项已可见")
#         #             break
#         #     except:
#         #         pass
#         #
#         #     # 滑动 panel
#         #     action.press(panel).move_to(x=0, y=-200).release().perform()


    def is_left_menu_accessible(self,menu_name):


        advanced_switch = self.find_element(self.get_locator_by_os("_adv_feature_switch"))
        if (menu_name in ('Navigate/Route Planning','Frequent Trip Rules','Adjust Odometer','Business Activities',
                          'Last Known Parking','Banks & Credit Cards','Invite Accoutant')
                and advanced_switch.get_attribute("checked")=='false'):
            self.switch_advanced_features()
            # scroll up the left pane
            self.swipe_up(self.get_locator_by_os("_left_panel_loc"),0.5)

        try:
            if menu_name=='Last Known Parking':
                # do not click
                self.find_element(self.get_menu_locator("%s" % menu_name))
                # todo: click menu and handle pop up
                self.swipe_left(self.get_locator_by_os("_left_panel_loc"), horizontal_rate=1)
                return True
            self.find_element_and_click(self.get_menu_locator("%s"%menu_name))


            if menu_name=='Work Schedule':
                from proj_spec.triplog.mobile.po.left_nav.work_schedule_page import WorkSchedulePage
                page = WorkSchedulePage(self.driver)
            elif menu_name=='Approval Management':
                from proj_spec.triplog.mobile.po.left_nav.approval_mgmt_page import ApprovalMgmtPage
                page = ApprovalMgmtPage(self.driver)
                while 'loading' in page.get_title():
                    time.sleep(3)
            else:
                from proj_spec.triplog.mobile.po.left_nav.left_nav_base_page import LeftNavBasePage
                page = LeftNavBasePage(self.driver)
            title = page.get_title()
            if menu_name in self.menu_title_mapping.keys():
                expected_title = self.menu_title_mapping[menu_name]
            else:
                expected_title = menu_name
            # go back
            page.go_back()

            return title=='%s'%expected_title
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


