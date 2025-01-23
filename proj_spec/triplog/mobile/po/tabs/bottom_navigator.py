# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/21 11:23
# @Author : Olivia
# Desc:
# **************************************
import logging
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy


from proj_spec.triplog.mobile.po.triplog_mobile_base_page import TriplogMobileBasePage


class BottomNavigator(TriplogMobileBasePage):
    _more_or_less_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/tv_main_bottom_more')
    # todo: ios locator
    _more_or_less_loc_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "More"`]')
    _more_or_less_parent_loc_android = (AppiumBy.ID, 'com.bizlog.triplog:id/ll_main_bottom_menu_more') # on android, only parent clickable
    _more_or_less_parent_loc_ios = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "More"`]')

    def get_tab_locator(self, tab_text):
        if self.os=='android':
            return (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.bizlog.triplog:id/tv_item_customize_btn_name" '
                                    'and @text="%s"]/..'%tab_text)  # only parent of parent element clickable
        else:
            return (AppiumBy.ACCESSIBILITY_ID, tab_text)

    def expand_more_or_less(self):

        element = self.find_element(self.get_locator_by_os("_more_or_less_loc"),condition="element_to_be_clickable")
        #element.screenshot("more or less.png")

        if element is not None:
            text = element.text
            print("more or less text: %s"%text)

            if text=='More':
                # only parent element clickable
                self.find_element_and_click(self.get_locator_by_os("_more_or_less_parent_loc"),condition="element_to_be_clickable")
            # # 登录后为展开状态显示More
            # # workaround: click the button once, and record height(0 as top of screen) of element before and after clicking
            # height_before_click = self.find_element(self.get_locator_by_os("_more_or_less_loc")).rect['y']
            # height_before_click = element.rect['y']
            # self.find_element_and_click(self.get_locator_by_os("_more_or_less_parent_loc"),
            #                             condition="element_to_be_clickable")
            # height_after_click = self.find_element(self.get_locator_by_os("_more_or_less_loc")).rect['y']
            # if height_before_click < height_after_click: # needs to expand(click again)
            #     self.find_element_and_click(self.get_locator_by_os("_more_or_less_parent_loc"),
            #                                 condition="element_to_be_clickable")
        else: # no More/Less switcher as there're no enough buttons
            return

    def is_tab_page_accessible(self, tab_name, expected=True):
        """

        :param tab_name:
        :param expected:
        :return:
        """

        try:
            self.expand_more_or_less() #menus may have been reordered, so need to expand first

            from proj_spec.triplog.mobile.po.tabs.tabs_base_page import TabsBasePage
            page = TabsBasePage(self.driver)
            expected_title=tab_name

            # if expected:
            #     self.find_element_and_click(self.get_tab_locator('%s' % tab_name))
            # else:
            #     if expected:
            #         self.find_element_and_click(self.get_tab_locator('%s' % tab_name),skip_error_handle=True)
            if tab_name == 'Time':
                if self.os=="android":
                    time_tab = self.find_element(self.get_tab_locator('Time'), condition="element_to_be_clickable")
                else:
                    time_tab = self.find_element(self.get_tab_locator('Time Clock'), condition="element_to_be_clickable")
                if time_tab is not None:
                    time_tab.click()
                else:
                    self.find_element_and_click(self.get_tab_locator("Timesheet"))
                if page.is_time_track_method_popup_displayed():
                    page.choose_time_track_method("clock_in_out")
                return page.get_title() in ("Time Clock", "Timesheet") #todo:currently when choose clock in out from Timesheet tab, page title will not get refreshed
            else:
                self.find_element_and_click(self.get_tab_locator('%s' % tab_name))

                if tab_name=="Schedule":
                    if page.is_schedule_popup_visible():
                        page.close_schedule_popup()

                    expected_title="Work Schedule"
                elif tab_name=="Time off":
                    expected_title="Time Off"
                return page.get_title()=='%s'%expected_title
        except NoSuchElementException as nse:
            if expected:
                logging.error(nse)
        except Exception as e:
            logging.error(e)
            logging.info("Exception accessing mobile bottom tab %s" % tab_name)
            return False


    # def is_trips_accessible(self):
    #     from proj_spec.triplog.mobile.po.tabs.trips_tab_page import TripsTabPage
    #     try:
    #         self.expand_more_or_less() #menus may have been reordered, so need to expand first
    #         self.find_element_and_click(self.get_tab_locator('Trips'))
    #         page = TripsTabPage(self.driver)
    #
    #         return page.get_title()=='Trips'
    #     except Exception as e:
    #         logging.info("Exception accessing mobile bottom tab Trips")
    #         return False
    #
    #
    # def is_fuels_accessible(self):
    #     from proj_spec.triplog.mobile.po.tabs.fuels_tab_page import FuelsTabPage
    #     try:
    #         self.expand_more_or_less() #menus may have been reordered, so need to expand first
    #         self.find_element_and_click(self.get_tab_locator('Fuels'))
    #         page = FuelsTabPage(self.driver)
    #
    #         return page.get_title()=='Fuels'
    #     except Exception as e:
    #         logging.info("Exception accessing mobile bottom tab Fuels")
    #         return False
    #
    #
    # def is_submission_accessible(self):
    #     from proj_spec.triplog.mobile.po.tabs.submission_tab_page import SubmissionTabPage
    #     try:
    #         self.expand_more_or_less() #menus may have been reordered, so need to expand first
    #         self.find_element_and_click(self.get_tab_locator('Submission'))
    #         page = SubmissionTabPage(self.driver)
    #
    #         return page.get_title()=='Submission'
    #     except Exception as e:
    #         logging.info("Exception accessing mobile bottom tab Submission")
    #         return False
    #
    #
    # def is_reports_accessible(self):
    #     from proj_spec.triplog.mobile.po.tabs.reports_tab_page import ReportsTabPage
    #     try:
    #         self.expand_more_or_less() #menus may have been reordered, so need to expand first
    #         self.find_element_and_click(self.get_tab_locator('Reports'))
    #         page = ReportsTabPage(self.driver)
    #
    #         return page.get_title()=='Reports'
    #     except Exception as e:
    #         logging.info("Exception accessing mobile bottom tab Submission")
    #         return False
