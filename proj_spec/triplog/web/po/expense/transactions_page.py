# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/19 8:52
# @Author : Olivia
# Desc:
# **************************************
from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage
import base.globalvars as glo

class TransactionPage(TriplogNavigablePage):
    url = glo.get_value("url1") + "/expense"

    def __init__(self, driver):
        """inistialize the transactions page


        :param driver:

        """
        super().__init__(driver)
        self.driver.get(self.url)
        # time.sleep(2)
        # try:
        #
        #     # self.find_element(self._trip_row_masked_loc,skip_error_handle=True)
        #     self.find_element(self._ytd_mileage_loc, skip_error_handle=True)
        #     self.find_element_and_click(self._ytd_save_btn_loc)
        #
        # except Exception as e:
        #     # logging.info("tips not prompted, continue with script")
        #     logging.info("Year to Date Mileage window not present")