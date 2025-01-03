# -*- coding: utf-8 -*-
# **************************************
# @Time : 2025/1/2 19:37
# @Author : Olivia
# Desc:
# **************************************
import pytest

from case.triplog.web.test_triplog_web_base import TestTriplogWebBase
from proj_spec.triplog.web.po.expense.transactions_page import TransactionsPage


class TestExpenseTransactions(TestTriplogWebBase):
    user_identifier = None
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.transactions_page = TransactionsPage(cls.driver)

    @pytest.mark.skip("debug")
    @pytest.mark.parametrize('kwargs', [{"amount": 12, "category": "Income"},{"amount": 20, "category": "Telephone"}])
    def test_create_transaction(self,kwargs):

        self.transactions_page.create_transaction(**kwargs)


    @pytest.mark.parametrize('kwargs', [{"row_index":0,"amount": 50, "category": "Income"}])
    def test_edit_transaction(self,kwargs):

        self.transactions_page.edit_transaction(**kwargs)