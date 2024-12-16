# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:42
# @Author : Olivia
# Desc: test trips functions using team account(and country of Canada)
# **************************************
import pytest

from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.po.mileage.trips_page import TripsPage


@pytest.mark.abstract
class TestTrips(TestTriplogWebBase):
    #__test__ = False
    user_identifier = None

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.trips_page = TripsPage(cls.driver)



    #@pytest.mark.skip("")
    @pytest.mark.parametrize('from_location, to_location, query_distance',
                             [('Golden Gate Bridge', 'South Lake Tahoe', True)])
    def test_add_trip(self, from_location, to_location, query_distance):
        """first line
        second line

        :param from_location:
        :param to_location:
        :param query_distance:
        :return:
        """
        self.trips_page.add_trip(from_location, to_location, query_distance)
        assert 1 == 1

    @pytest.mark.parametrize('kwargs', [
        {"row_index": 0, "from_location": "South Lake Tahoe", "to_location": "Golden Gate Bridge",
         "query_distance": True}])
    def test_edit_trip(self, kwargs):
        """

        :param kwargs:
        :return:
        """

        # self.trips_page.edit_trip(0,kwargs)
        self.trips_page.edit_trip(**kwargs)


