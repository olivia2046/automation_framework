# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:42
# @Author : Olivia
# Desc: test trips functions using team account(and country of Canada)
# **************************************
import pytest
from abc import ABC, abstractmethod
from base.getdata import GetData
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.po.login.login_page import TriplogLoginPage


class TestTrips(TestTriplogWebBase,ABC):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        email, password = GetData.get_user_credential(cls.user_type)
        login_page = TriplogLoginPage()
        cls.driver = login_page.driver
        overview_page = login_page.login(email, password)
        cls.trips_page = overview_page.navigation_bar.goto_trips()



    @property
    @abstractmethod
    def user_type(cls):
        """
        sub-class only need to provide value of user_type
        there's no need to overwrite setup_class
        by heritating ABC and decorator @abstractmethod，ensure that sub-class must implement user_type
        otherwise TypeError will be thrown
        :return:
        """
        pass

    """
    If do not what to use abstract method to force sub-class to provide user_type, we can get sub-class's class name in parent class
    @classmethod
    def setup_class(cls):
        super().setup_class()
        user_type = getattr(cls, 'user_type', cls.__name__.lower())
        email, password = GetData.get_user_credential(cls.user_type)
        login_page = TriplogLoginPage()
        overview_page = login_page.login(email, password)
        cls.trips_page = overview_page.navigation_bar.goto_trips()
       
    """

    # @pytest.fixture(scope="class", autouse=True)
    # def setup_class(request):
    #     #super().setup_class()
    #     cls = request.node.cls
    #     user_type = getattr(cls, 'user_type', cls.__name__.lower())
    #     email, password = GetData.get_user_credential(user_type)
    #     login_page = TriplogLoginPage()
    #     overview_page = login_page.login(email, password)
    #     cls.trips_page = overview_page.navigation_bar.goto_trips()


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

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

