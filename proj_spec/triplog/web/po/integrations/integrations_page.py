# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/6 20:01
# @Author : Olivia
# Desc:
# **************************************

from selenium.webdriver.common.by import By
import base.globalvars as glo
from proj_spec.triplog.web.po.triplog_base_page import TriplogWebBasePage


class IntegrationsPage(TriplogWebBasePage):
    _integrations_dialog_loc = (By.XPATH, '//div[@class="integrations-dialog-box integrations-dialog-box-show"]')
    _integrations_menu_loc = (By.XPATH,'//span[@class="n_nav-main-menu-text" and text()="Integrations"]')
    _close_btn_loc = (By.XPATH, '//a[@class="integrations-dialog-close-btn"]')


    def __init__(self, driver):
        super().__init__(driver)
        # self.driver = driver
        # self.find_element_and_click(self._integrations_menu_loc)
        from proj_spec.triplog.web.po.triplog_navigation_bar import TriplogNavigationBar
        navigator = TriplogNavigationBar(self.driver)
        navigator.navigate("Integrations")


    def is_integration_item_accessible(self, integration_name):
        # self.driver.get(glo.get_value("url1")+"/dashboard/overview")
        self.find_element_and_click(self._integrations_menu_loc)
        # cannot get the integration_item element when locating directly, need to locate the dialog first and locate the item in it
        dialog_box = self.find_element(self._integrations_dialog_loc)
        #integration_item = self.find_element(By.XPATH, '//div[@class="integrations-dialog"]//span[@class="integrations-dialog-item-name" and contains(text(),"%s")]'%integration_name)
        integration_item = dialog_box.find_element(by=By.XPATH, value='//span[@class="integrations-dialog-item-name" and contains(text(),"%s")]'%integration_name)
        accessibility = integration_item.is_enabled()
        self.find_element_and_click(self._close_btn_loc)
        # todo: if close button is not visible, click area outside of dialog(on laptop)
        return accessibility
