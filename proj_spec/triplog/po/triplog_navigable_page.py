# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:30
# @Author : Olivia
# Desc:
# **************************************
from proj_spec.triplog.po.triplog_base_page import TriplogBasePage
from proj_spec.triplog.po.triplog_navigation_bar import TriplogNavigationBar


class TriplogNavigablePage(TriplogBasePage):
    """
    page that has the navigation sidebar
    """
    def __init__(self, driver):
        self.driver = driver
        self.navigation_bar = TriplogNavigationBar(driver)


