# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:42
# @Author : Olivia
# Desc: test trips functions using team account(and country of Canada)
# **************************************
import pytest
from base.getdata import GetData
from case.triplog.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.po.login.login_page import TriplogLoginPage


class TestTeamsTrips(TestTriplogWebBase):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        email, password = GetData.get_user_credential("teams_paid")
        login_page = TriplogLoginPage()
        overview_page = login_page.login(email, password)
        cls.trips_page = overview_page.navigation_bar.goto_trips()

    @pytest.mark.skip("debug")
    @pytest.mark.parametrize('from_location, to_location, query_distance',[('Golden Gate Bridge','South Lake Tahoe', True)])
    def test_add_trip(self,from_location, to_location, query_distance):
        self.trips_page.add_trip(from_location, to_location, query_distance)


    @pytest.mark.parametrize('kwargs',[{"row_index":0,"from_location":"South Lake Tahoe","to_location":"Golden Gate Bridge","query_distance":True}])
    def test_edit_trip(self, kwargs):
        """

        :param kwargs:
        :return:
        """

        #self.trips_page.edit_trip(0,kwargs)
        self.trips_page.edit_trip(**kwargs)





