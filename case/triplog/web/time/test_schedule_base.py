# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/5 21:24
# @Author : Olivia
# Desc:
# **************************************
import pytest
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase


class TestScheduleBase(TestTriplogWebBase):
    user_identifier = None

    @classmethod
    def setup_class(cls):
        super().setup_class()

        from proj_spec.triplog.web.po.time.schedule_page import SchedulePage
        cls.schedule_page = SchedulePage(cls.driver)

    # @pytest.mark.skip("debug")
    @pytest.mark.parametrize('kwargs', [{"user": "enterprisepaid@qa.com"},{"user": "enterprise_user1@qa.com"}])
    def test_add_time_entry(self, kwargs):
        self.schedule_page.add_schedule(**kwargs)