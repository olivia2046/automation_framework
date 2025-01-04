# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2025/1/4 19:40
desc: 
'''
import pytest
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase


class TestJobActivity(TestTriplogWebBase):
    user_identifier = None

    @classmethod
    def setup_class(cls):
        super().setup_class()

        from proj_spec.triplog.web.po.time.job_activity_page import JobActivityPage
        cls.job_activity_page = JobActivityPage(cls.driver)

    # @pytest.mark.skip("debug")
    @pytest.mark.parametrize('kwargs',
                             [{"name": "Painting","hourly_rate":"15.00", "dept_office":"Contracting" }])
    def test_add_job_activity(self, kwargs):
        self.job_activity_page.add_job_activity(**kwargs)