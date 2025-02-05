# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/6 12:21
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By
from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage
import base.globalvars as glo


class OverviewPage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/dashboard/overview"
    #_title_loc = (By.XPATH,"//span[@class='n_menu-selected-menuname']")

    # def __init__(self, driver):
    #     """inistialize the time clock page
    #
    #
    #     :param driver:
    #
    #     """
    #     super().__init__(driver)
    #     self.driver.get(self.url)
    

    # def get_title(self):
    #     """
    #
    #     :return:
    #     """
    #     title_ele = self.find_element(self._title_loc)
    #     return title_ele.text


