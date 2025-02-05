# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/2/5 13:47
# @Author : Olivia
# Desc:
# **************************************
import logging

from proj_spec.triplog.playwright.triplog_pw_base_page import TriplogPWBasePage


class NavigationBar(TriplogPWBasePage):

    def navigate(self, first_level_menu_text, second_level_menu_text=""):
        """

        :return:
        """
        try:
            first_level_menu_loc = '//span[@class="n_nav-main-menu-text" and text()="%s"]'%first_level_menu_text
            second_level_menu_loc = "//li[contains(@class,'n_submenu-item')]/a[contains(text(),'%s')]"%second_level_menu_text
            #second_level_menu = self.page.locator("//li[contains(@class,'n_submenu-item')]/a[contains(text(),'%s')]"%second_level_menu_text)
            first_level_menu = self.page.locator(first_level_menu_loc)

            if second_level_menu_text!="":
                # #self.page.locator(first_level_menu_loc).scroll_into_view_if_needed()
                # #self.page.wait_for_selector(first_level_menu_loc)
                # first_level_menu = self.page.query_selector(first_level_menu_loc)
                # first_level_menu.hover()
                # #self.page.wait_for_selector(second_level_menu_loc, state='visible')
                # self.page.query_selector(second_level_menu_loc).click()
                self.page.hover(first_level_menu_loc)
                self.page.locator(second_level_menu_loc).click()
            else:
                self.page.locator(first_level_menu_loc).click()

            from proj_spec.triplog.playwright.triplog_navigable_page import TriplogNavigablePage
            return TriplogNavigablePage(self.page)

        except Exception as e:
            logging.error(e)
            return None


