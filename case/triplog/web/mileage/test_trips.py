# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:42
# @Author : Olivia
# Desc:
# **************************************
import pytest
from base.getdata import GetData
from case.triplog.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.po.login.login_page import TriplogLoginPage


class TestTrips(TestTriplogWebBase):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        email, password = GetData.get_user_credential("enterprise_paid")
        login_page = TriplogLoginPage()
        overview_page = login_page.login(email, password)
        cls.trips_page = overview_page.navigation_bar.goto_trips()

    @pytest.mark.parametrize('from_location, to_location',[('Golden Gate Bridge','South Lake Tahoe')])
    def test_add_trips(self,from_location, to_location):
        self.trips_page.add_trip(from_location, to_location)





