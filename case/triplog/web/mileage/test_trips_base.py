# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:42
# @Author : Olivia
# Desc: test trips functions using team account(and country of Canada)
# **************************************
import pytest

from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.web.po.mileage.trips_page import TripsPage


@pytest.mark.abstract
class TestTripsBase(TestTriplogWebBase):
    #__test__ = False
    user_identifier = None

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.trips_page = TripsPage(cls.driver)



    @pytest.mark.skip("")
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
        c_before = self.trips_page.get_number_of_trips_filtered()
        self.trips_page.add_trip(from_location, to_location, query_distance)
        c_after = self.trips_page.get_number_of_trips_filtered()
        assert c_after==c_before+1,"trip not added successfully"

    @pytest.mark.skip("")
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

    @pytest.mark.skip("")
    def test_delete_trip_from_menu(self):
        """


        :return:
        """
        c_before = self.trips_page.get_number_of_trips_filtered()
        self.trips_page.delete_trip(0)
        c_after = self.trips_page.get_number_of_trips_filtered()
        assert c_after==c_before-1,"trip not deleted successfully"


    def test_submit_trips(self, indexes=[0], comments=""):
        self.trips_page.submit_trips(indexes, comments)


