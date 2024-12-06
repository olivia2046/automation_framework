# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/6 12:21
# @Author : Olivia
# Desc:
# **************************************
from selenium.webdriver.common.by import By

from proj_spec.triplog.po.triplog_base_page import TriplogBasePage


class OverviewPage(TriplogBasePage):
    _title_loc = (By.XPATH,'//*[@id="triplog-body"]/div[1]/div[2]/div[2]/span[1]')

    def get_title(self):
        """

        :return:
        """
        title_ele = self.find_element(self._title_loc)
        return title_ele.text
