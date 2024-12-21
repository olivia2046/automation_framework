# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/20 16:22
# @Author : Olivia
# Desc:
# **************************************
import base.globalvars as glo
from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage


class MileageReportsPage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/report/list"

    # def __init__(self, driver):
    #     """inistialize the mileage report page
    #
    #
    #     :param driver:
    #
    #     """
    #     super().__init__(driver)
    #     self.driver.get(self.url)
