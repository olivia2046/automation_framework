# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/17 20:25
# @Author : Olivia
# Desc: test access of paid users, including premium, teams and enterprise
# **************************************
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.web.po.mileage.trips_page import TripsPage


class TestPaidAccess(TestTriplogWebBase):
    user_identifier = "single_paid"
    def test_mileage_access(self):
        """test access to Mileage functions

        :return:
        """
        trips_page = TripsPage(self.driver)

        assert not trips_page.is_layer_popup_visible()

