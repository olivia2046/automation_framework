# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2025/1/4 19:19
desc: 
'''
import pytest
from case.triplog.web.test_triplog_web_base import TestTriplogWebBase



class TestTimeClockList(TestTriplogWebBase):
    user_identifier = None

    @classmethod
    def setup_class(cls):
        super().setup_class()
        from proj_spec.triplog.web.po.time.time_list_page import TimeClockListPage
        cls.time_list_page = TimeClockListPage(cls.driver)

    #@pytest.mark.skip("debug")
    @pytest.mark.parametrize('kwargs', [{"amount": 12, "category": "Income"}, {"amount": 20, "category": "Telephone"}])
    def test_add_time_entry(self, kwargs):
        self.time_list_page.add_time_entry(**kwargs)

    #@pytest.mark.skip("debug")
    @pytest.mark.parametrize('kwargs', [{"row_index": 0, "amount": 50, "category": "Income"}])
    def test_edit_time_entry(self, kwargs):
        self.time_list_page.edit_time_enty(**kwargs)

    @pytest.mark.parametrize('row_index', [0])
    def test_delete_one_time_entry(self, row_index):
        self.time_list_page.delete_one_time_entry(row_index)