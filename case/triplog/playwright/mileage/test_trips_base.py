# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/2/3 9:54
# @Author : Olivia
# Desc:
# **************************************
from case.triplog.playwright.test_triplog_pw_base import TestTriplogPWBase
import pytest

from proj_spec.triplog.playwright.mileage.trips_page import TripsPage


@pytest.mark.usefixtures("page")
class TestTripsBase(TestTriplogPWBase):
    user_identifier = None

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.trips_page = TripsPage(cls.default_page)

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
        c_before = self.trips_page.get_number_of_trips_filtered()
        self.trips_page.add_trip(from_location, to_location, query_distance)
        c_after = self.trips_page.get_number_of_trips_filtered()
        assert c_after == c_before + 1, "trip not added successfully"