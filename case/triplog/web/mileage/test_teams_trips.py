# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:42
# @Author : Olivia
# Desc: test trips functions using team account(and country of Canada)
# **************************************
import logging

import pytest,time
from case.triplog.web.mileage.test_trips import TestTrips
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.po.mileage.trips_page import TripsPage


class TestTeamsTrips(TestTriplogWebBase):
    user_identifier="teams_paid"

    # @classmethod
    # def setup_class(cls):
    #     super().setup_class()
    #     email, password = GetData.get_user_credential("teams_paid")
    #     login_page = TriplogLoginPage()
    #     overview_page = login_page.login(email, password)
    #     cls.trips_page = overview_page.navigation_bar.goto_trips()

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.trips_page = TripsPage(cls.driver)


    # def setup_method(self):
    #     self.driver.get(self.trips_page.url)
        # time.sleep(2)
        # try:
        #
        #     #self.find_element(self._trip_row_masked_loc,skip_error_handle=True)
        #     self.find_element(self._ytd_mileage_loc,skip_error_handle=True)
        #     self.find_element_and_click(self._ytd_save_btn_loc)
        #
        # except Exception as e:
        #     #logging.info("tips not prompted, continue with script")
        #     logging.info("Year to Date Mileage window not present")
        #
        # self.find_element_and_click(self._trip_row_loc)


    @pytest.mark.parametrize('from_location, to_location, query_distance',[('Golden Gate Bridge','South Lake Tahoe', True)])
    def test_add_trip(self,from_location, to_location, query_distance):
        """first line
        second line

        :param from_location:
        :param to_location:
        :param query_distance:
        :return:
        """
        self.trips_page.add_trip(from_location, to_location, query_distance)
        assert 1 == 1


    @pytest.mark.parametrize('kwargs',[{"row_index":0,"from_location":"South Lake Tahoe","to_location":"Golden Gate Bridge","query_distance":True}])
    def test_edit_trip(self, kwargs):
        """

        :param kwargs:
        :return:
        """

        #self.trips_page.edit_trip(0,kwargs)
        self.trips_page.edit_trip(**kwargs)





