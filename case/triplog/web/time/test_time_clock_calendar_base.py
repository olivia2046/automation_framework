# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2025/1/5 10:36
desc: 
'''
import pytest
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase



class TestTimeClockCalendarBase(TestTriplogWebBase):
    user_identifier = None

    @classmethod
    def setup_class(cls):
        super().setup_class()
        from proj_spec.triplog.web.po.time.time_calendar_page import TimeClockCalendarPage
        cls.time_calendar_page = TimeClockCalendarPage(cls.driver)

    #@pytest.mark.skip("debug")
    @pytest.mark.parametrize('kwargs', [{}])
    def test_clock_in(self, kwargs):
        self.time_calendar_page.clock_in(**kwargs)

    @pytest.mark.skip("debug")
    @pytest.mark.parametrize('kwargs', [{}])
    def test_clock_out(self, kwargs):
        self.time_calendar_page.clock_out(**kwargs)