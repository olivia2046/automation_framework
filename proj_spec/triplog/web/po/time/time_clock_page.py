# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/20 15:41
# @Author : Olivia
# Desc:
# **************************************

from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage
import base.globalvars as glo

class TimeClockPage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/time/clock"

    def __init__(self, driver):
        """inistialize the time clock caclendar page


        :param driver:

        """
        super().__init__(driver)
        self.driver.get(self.url)
