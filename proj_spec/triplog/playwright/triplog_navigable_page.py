# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/2/5 14:15
# @Author : Olivia
# Desc:
# **************************************
import logging


from proj_spec.triplog.playwright.triplog_pw_base_page import TriplogPWBasePage


class TriplogNavigablePage(TriplogPWBasePage):
    """
    page that has the navigation sidebar
    """
    url = None #to be provides by concrete sub-class
    _layer_popup_loc = "div#layui-layer1"
    _title_loc = '//span[@class="n_menu-selected-menuname"]'

    def __init__(self, page):
        super().__init__(page)
        from proj_spec.triplog.playwright.navigation_bar import NavigationBar
        self.navigation_bar = NavigationBar(page)
        if self.url is not None:
            self.page.goto(self.url)



    def is_layer_popup_visible(self):
        """check whether there're trial end/7 day pass pop up

        :param expected: if user should have access to page, expected=False, otherwise expected=True
        :return:
        """
        if self.page.locator(self._layer_popup_loc) is None:
            logging.info("popup layer not found")
            return False
        else:
            logging.info("popup layer found")
            return True


    def jumped_to_billing(self):
        """whether page jumps to the Billing page

        :return:
        """
        return self.get_title()=='Billing'


    def get_title(self):
        title_element =  self.page.locator(self._title_loc)
        if title_element is not None:
            return title_element.inner_text()
        else:
            return ""